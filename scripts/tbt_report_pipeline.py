#!/usr/bin/env python3
"""
TBT Report Pipeline — Level 3 Sandbox
---------------------------------------
실제 업무 재현: WTO TBT 공개 통보문 → 번역 + 구조 추출 → KTL 심층분석보고서 초안 생성
공개 데이터만 사용 (내부 데이터, PII 없음)

필요 환경변수:
  ANTHROPIC_API_KEY   Claude API 키 (없으면 구조 템플릿만 생성)
  NOTIFICATION_ID     특정 통보문 ID (없으면 최신 1건 자동 선택)
"""

import urllib.request
import json
import os
import sys
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# 설정
# ---------------------------------------------------------------------------
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
NOTIFICATION_ID   = os.environ.get('NOTIFICATION_ID', '')

HIGH_IMPACT_COUNTRIES = [
    'china', 'eu', 'european union', 'united states', 'vietnam',
    'indonesia', 'malaysia', 'saudi arabia', 'japan', 'india',
]
HIGH_IMPACT_SECTORS = [
    'battery', 'electric vehicle', 'display', 'semiconductor', 'electronics',
    'chemical', 'pfas', 'reach', 'rohs', 'ecodesign', 'energy efficiency',
    'cybersecurity', 'medical', 'food', 'wireless', 'telecom', 'automotive',
]

# ---------------------------------------------------------------------------
# Step 1: WTO TBT 통보문 수집 (ePing 공개 API)
# ---------------------------------------------------------------------------
def fetch_notification(days_back=7):
    since = (datetime.utcnow() - timedelta(days=days_back)).strftime('%Y-%m-%d')
    url = (
        'https://eping.wto.org/api/v1/notifications/search'
        f'?domain=TBT&dateFrom={since}&pageSize=20&page=1'
    )
    req = urllib.request.Request(url, headers={
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (KTL TBT Monitor)',
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode('utf-8'))
    except Exception as e:
        print(f"  ePing API 실패: {e}")
        return None

    items = []
    raw = data if isinstance(data, list) else (
        data.get('notifications') or data.get('items') or
        data.get('results') or data.get('data') or []
    )
    for item in raw:
        title  = item.get('title') or item.get('subject') or ''
        symbol = item.get('symbol') or item.get('id') or ''
        member = item.get('member') or item.get('country') or ''
        date   = item.get('distributionDate') or item.get('date') or ''
        text   = item.get('description') or item.get('content') or ''
        if title:
            items.append({'title': title, 'symbol': symbol, 'member': member,
                          'date': date, 'text': text})
    return items

def pick_target(items):
    if not items:
        return None
    if NOTIFICATION_ID:
        for it in items:
            if NOTIFICATION_ID in str(it.get('symbol', '')):
                return it
    # 한국 수출 관련성 높은 건 우선 선택
    def score(it):
        t = (it['title'] + ' ' + it['member']).lower()
        s = sum(3 for c in HIGH_IMPACT_COUNTRIES if c in t)
        s += sum(2 for sec in HIGH_IMPACT_SECTORS if sec in t)
        return s
    return max(items, key=score)

# ---------------------------------------------------------------------------
# Step 2: Claude API 번역 + 구조 추출
# ---------------------------------------------------------------------------
def call_claude(prompt: str, system: str = '') -> str:
    if not ANTHROPIC_API_KEY:
        return ''
    payload = json.dumps({
        'model': 'claude-sonnet-4-6',
        'max_tokens': 4096,
        'system': system,
        'messages': [{'role': 'user', 'content': prompt}],
    }).encode('utf-8')
    req = urllib.request.Request(
        'https://api.anthropic.com/v1/messages',
        data=payload,
        headers={
            'x-api-key': ANTHROPIC_API_KEY,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json',
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            resp = json.loads(r.read().decode('utf-8'))
            return resp['content'][0]['text']
    except Exception as e:
        print(f"  Claude API 실패: {e}")
        return ''

SYSTEM_REPORT = """당신은 KTL(한국산업기술시험원) 수출지원센터의 TBT 규제 분석 전문가입니다.
WTO TBT 통보문을 바탕으로 한국 수출기업 대상 심층분석보고서 초안을 작성합니다.
규정 준수, 사실 기반, 원문 근거 중심으로 작성하며 원문에 없는 내용은 임의 생성하지 않습니다."""

def translate_and_extract(item: dict) -> dict:
    title  = item['title']
    member = item['member']
    date   = item['date']
    text   = item.get('text', '') or '(원문 전문 미제공 — 제목 및 메타데이터 기반 분석)'

    if not ANTHROPIC_API_KEY:
        print("  ANTHROPIC_API_KEY 없음 → 템플릿 구조만 생성")
        return _template_fill(item)

    print("  Claude API로 번역 + 구조 추출 중...")
    prompt = f"""아래 WTO TBT 통보문을 분석하여 JSON으로 구조화하세요.

통보국: {member}
통보문 번호/ID: {item.get('symbol', '미확인')}
제목: {title}
배포일: {date}
원문 내용: {text[:3000]}

다음 JSON 구조로 출력하세요 (한국어):
{{
  "규제명_영문": "",
  "규제명_국문": "",
  "통보번호": "",
  "통보국": "",
  "채택일": "",
  "시행일": "",
  "의견수렴마감일": "",
  "HS_code": "",
  "규제요지": "",
  "적용범위": "",
  "주요내용": "",
  "인증정보": "",
  "도입배경": "",
  "세부내용_요약": "",
  "기업애로_예상": "",
  "대응방안_중소기업": "",
  "대응방안_중견기업": "",
  "대응방안_대기업": "",
  "TBT통보여부": "통보",
  "참고URL": ""
}}

확인되지 않는 항목은 "원문상 확인되지 않음"으로 표시하세요."""

    raw = call_claude(prompt, SYSTEM_REPORT)
    try:
        start = raw.find('{')
        end   = raw.rfind('}') + 1
        return json.loads(raw[start:end])
    except Exception:
        print("  JSON 파싱 실패 → 템플릿 구조로 대체")
        return _template_fill(item)

def _template_fill(item: dict) -> dict:
    return {
        '규제명_영문': item['title'],
        '규제명_국문': f"[번역 필요] {item['title']}",
        '통보번호': item.get('symbol', '미확인'),
        '통보국': item['member'],
        '채택일': item['date'],
        '시행일': '원문상 확인되지 않음',
        '의견수렴마감일': '원문상 확인되지 않음',
        'HS_code': '작성없음',
        '규제요지': '원문 전문 제공 시 작성 가능',
        '적용범위': '원문 전문 제공 시 작성 가능',
        '주요내용': '원문 전문 제공 시 작성 가능',
        '인증정보': '공식자료 확인 필요',
        '도입배경': '원문 전문 제공 시 작성 가능',
        '세부내용_요약': '원문 전문 제공 시 작성 가능',
        '기업애로_예상': '원문 분석 후 작성',
        '대응방안_중소기업': '원문 분석 후 작성',
        '대응방안_중견기업': '원문 분석 후 작성',
        '대응방안_대기업': '원문 분석 후 작성',
        'TBT통보여부': '통보',
        '참고URL': '',
    }

# ---------------------------------------------------------------------------
# Step 3: 주요국 규제동향 생성 (Claude API)
# ---------------------------------------------------------------------------
def generate_country_comparison(info: dict) -> str:
    if not ANTHROPIC_API_KEY:
        return _country_template(info['통보국'])

    print("  주요국 규제동향 생성 중...")
    prompt = f"""
규제명: {info['규제명_국문']}
통보국: {info['통보국']}
규제요지: {info['규제요지']}
적용범위: {info['적용범위']}

위 규제와 유사한 주요국(미국, EU, 일본, 중국) 기술규제 동향을 아래 형식으로 작성하세요.
각 국가당 현행규정, 도입동향, 유사품목 제도 3줄 이내로 압축합니다.
공식자료 근거가 없는 내용은 "공식자료 확인 필요"로 표시하세요.

출력 형식 (마크다운):
### 미국
- (현행 규정) ...
- (도입동향) ...
- (유사품목 제도 도입동향) ...

### EU
...
### 일본
...
### 중국
...
"""
    result = call_claude(prompt, SYSTEM_REPORT)
    return result if result else _country_template(info['통보국'])

def _country_template(notifying_member: str) -> str:
    return """### 미국
- (현행 규정) 공식자료 확인 필요
- (도입동향) 공식자료 확인 필요
- (유사품목 제도 도입동향) 공식자료 확인 필요

### EU
- (현행 규정) 공식자료 확인 필요
- (도입동향) 공식자료 확인 필요
- (유사품목 제도 도입동향) 공식자료 확인 필요

### 일본
- (현행 규정) 공식자료 확인 필요
- (도입동향) 공식자료 확인 필요
- (유사품목 제도 도입동향) 공식자료 확인 필요

### 중국
- (현행 규정) 공식자료 확인 필요
- (도입동향) 공식자료 확인 필요
- (유사품목 제도 도입동향) 공식자료 확인 필요"""

# ---------------------------------------------------------------------------
# Step 4: 보고서 마크다운 생성 (KTL master template 서식)
# ---------------------------------------------------------------------------
def generate_report(info: dict, country_comp: str, today: str) -> str:
    sym = info.get('통보번호', '미확인')
    report_id = f"SANDBOX-{today.replace('-','')}"

    lines = [
        f"# 무역기술장벽(TBT) 심층분석보고서 {report_id}",
        f"# 『{info['통보국']}, {info['규제명_국문']}』",
        f"> ⚠️ 본 보고서는 WTO TBT 공개 데이터 기반 **자동 생성 샌드박스 초안**입니다.",
        f"> 실제 보고서 발행 전 담당자 검토 필수. 생성일: {today}",
        "",
        "---",
        "",
        "| 항목 | 내용 |",
        "|------|------|",
        f"| TBT 통보여부 | {info.get('TBT통보여부','통보')} |",
        f"| HS Code | {info.get('HS_code','작성없음')} |",
        f"| 통보국 | {info.get('통보국','')} |",
        f"| 전년도 수출액 | 작성없음 |",
        f"| 작성기관 | 한국산업기술시험원 |",
        f"| 문의처 | tbt@kotica.or.kr |",
        "",
        "---",
        "",
        "# 규제 요약서",
        "",
        "## □ 규제 개요",
        f" ㅇ (규제요지) {info.get('규제요지','원문 전문 제공 시 작성 가능')}",
        "",
        f" ㅇ (적용범위) {info.get('적용범위','원문 전문 제공 시 작성 가능')}",
        "",
        "## □ 주요 내용",
        f" ㅇ (주요 내용) {info.get('주요내용','원문 전문 제공 시 작성 가능')}",
        "",
        f" ㅇ (인증정보) {info.get('인증정보','공식자료 확인 필요')}",
        "",
        "## □ 기술규제 영향분석",
        f" ㅇ (규제 영향 분석 결과) {info.get('기업애로_예상','원문 분석 후 작성')}",
        "",
        "---",
        "",
        "# 요약문",
        "",
        "| 구분 | 항목 | 내용 |",
        "|------|------|------|",
        f"| 규제명 | 영문 | {info.get('규제명_영문','')} |",
        f"| 규제명 | 국문 | {info.get('규제명_국문','')} |",
        f"| WTO/TBT 통보문 번호 | | {sym} |",
        f"| 통보국 | | {info.get('통보국','')} |",
        f"| 채택(예정)일 | | {info.get('채택일','')} |",
        f"| 시행현황 | | {info.get('시행일','원문상 확인되지 않음')} |",
        f"| HS Code | | {info.get('HS_code','작성없음')} |",
        f"| 의견수렴 마감일 | | {info.get('의견수렴마감일','원문상 확인되지 않음')} |",
        "",
        "---",
        "",
        "# Ⅰ. 규제 개요",
        "",
        "## □ 도입배경",
        f" ㅇ {info.get('도입배경','원문 전문 제공 시 작성 가능')}",
        "",
        "## □ 규제 요지",
        f" ㅇ {info.get('규제요지','원문 전문 제공 시 작성 가능')}",
        "",
        "## □ 적용대상",
        f" ㅇ {info.get('적용범위','원문 전문 제공 시 작성 가능')}",
        "",
        "## □ 시행일",
        f" ㅇ {info.get('시행일','원문상 확인되지 않음')}",
        "",
        "---",
        "",
        "# Ⅱ. 규제 세부 내용",
        "",
        "## □ 세부내용",
        f" ㅇ {info.get('세부내용_요약','원문 전문 제공 시 작성 가능')}",
        "",
        "---",
        "",
        "# Ⅲ. 관련 인증 정보",
        "",
        "## □ 인증 절차",
        f" ㅇ (인증 개요) {info.get('인증정보','공식자료 확인 필요')}",
        "",
        "## □ 신청 시 유의사항",
        " ㅇ (인증 유효기간) 공식자료 확인 필요",
        " ㅇ (인증비용) 공식자료 확인 필요",
        " ㅇ (위반 시 제재) 공식자료 확인 필요",
        "",
        "---",
        "",
        "# Ⅳ. 주요국 규제동향 및 규제수준 비교",
        "",
        "## 1. 주요국 기술규제 동향",
        "",
        country_comp,
        "",
        "---",
        "",
        "# Ⅴ. 예상 애로사항 및 파급효과",
        "",
        "## 1. 기술규제 영향 평가 검토",
        "",
        "### ㅇ 규제 개요",
        f" - {info.get('규제요지','원문 분석 후 작성')}",
        "",
        "### ㅇ 평가 항목별 영향 분석",
        "",
        "| 평가항목 | 평가결과 |",
        "|----------|----------|",
        "| 허가·인증 대응 부담 | 원문 분석 후 작성 |",
        "| 시험·문서 영향 | 원문 분석 후 작성 |",
        "| 표시·라벨 영향 | 원문 분석 후 작성 |",
        "| 사후관리 부담 | 원문 분석 후 작성 |",
        "",
        "## 2. TBT 협정문 위배 여부 판단",
        "",
        "| 연번 | 무역기술장벽 유형 | 위반사항 |",
        "|------|------------------|----------|",
        "| 1 | 국제표준과 일치화 되지 않은 표준 | 원문 분석 후 작성 |",
        "| 2 | 자국 제품과 수입제품의 차별적 대우 | 원문 분석 후 작성 |",
        "| 3 | 불필요한 무역방해 초래 | 원문 분석 후 작성 |",
        "| 4 | 적용되는 법률 및 기술규정의 투명성 부재 | 원문 분석 후 작성 |",
        "",
        "---",
        "",
        "# Ⅵ. 대응 방안",
        "",
        "## □ 대응 방안",
        "",
        "| 구분 | 대응 핵심 | 대응 방안 |",
        "|------|-----------|-----------|",
        f"| 중소기업 | 적용 여부 확인 | {info.get('대응방안_중소기업','원문 분석 후 작성')} |",
        f"| 중견기업 | 허가자료 준비 | {info.get('대응방안_중견기업','원문 분석 후 작성')} |",
        f"| 대기업 | 포트폴리오 관리 | {info.get('대응방안_대기업','원문 분석 후 작성')} |",
        "",
        " ㅇ 본 보고서는 우리 수출기업의 무역기술장벽 대응을 위한 해외 기술규제 정보를 분석 및 제공하기 위해 작성되었습니다.",
        " ㅇ 위 규제와 관련된 정보는 해외인증기술규제정보포털(knowtbt.kr)에서 열람 가능합니다.",
        "",
        "---",
        "",
        "# 참고 1 참고자료",
        "",
        f" ㅇ WTO ePing TBT 통보문 플랫폼: https://eping.wto.org",
        f" ㅇ 통보문 번호: {sym}",
        info.get('참고URL', ''),
        "",
        "---",
        "",
        "# 참고 2 규제원문(전문) 번역본",
        "",
        "> ※ 본 샌드박스 버전은 원문 전문 번역본 미포함.",
        "> 실제 운영 시: 규제기관 공식 관보 URL → 전문 번역 → 첨부",
        "",
    ]
    return '\n'.join(lines)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"=== TBT 보고서 파이프라인 샌드박스 ({today}) ===")
    print(f"    API 모드: {'Claude API 활성' if ANTHROPIC_API_KEY else '템플릿 모드 (API key 없음)'}")

    # Step 1: 통보문 수집
    print("\n[1/4] WTO TBT 통보문 수집...")
    items = fetch_notification(days_back=30)
    if not items:
        print("  → API 응답 없음 (샌드박스 환경 네트워크 제한)")
        print("  → 데모용 더미 데이터로 진행")
        items = [{
            'title': 'Regulation on energy efficiency requirements for household appliances',
            'symbol': 'G/TBT/N/EU/999',
            'member': 'European Union',
            'date': today,
            'text': 'This regulation establishes minimum energy efficiency requirements for household electrical appliances including refrigerators, washing machines, and dishwashers.',
        }]

    target = pick_target(items)
    print(f"  → 선택: [{target['member']}] {target['title']}")

    # Step 2: 번역 + 구조 추출
    print("\n[2/4] 번역 및 구조 추출...")
    info = translate_and_extract(target)

    # Step 3: 주요국 비교
    print("\n[3/4] 주요국 규제동향 생성...")
    country_comp = generate_country_comparison(info)

    # Step 4: 보고서 생성
    print("\n[4/4] 보고서 초안 생성...")
    report_md = generate_report(info, country_comp, today)

    # 저장
    out_dir  = os.path.join(os.path.dirname(__file__), '..', 'output', 'sandbox-reports')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f'{today}-tbt-report-sandbox.md')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(report_md)

    print(f"\n✅ 보고서 초안 생성: {out_path}")
    print(f"   통보국: {info.get('통보국','')}")
    print(f"   규제명: {info.get('규제명_국문','')}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
