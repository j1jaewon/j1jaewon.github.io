#!/usr/bin/env python3
"""
TBT Report Pipeline — Level 3 Sandbox
---------------------------------------
실제 업무 재현: 각국 규제 원문 PDF → 번역 + 구조 추출 → KTL 심층분석보고서 초안 생성

사용법:
  python3 scripts/tbt_report_pipeline.py <규제원문.pdf>

필요 환경변수:
  ANTHROPIC_API_KEY   Claude API 키 (없으면 구조 템플릿만 생성)
"""

import sys
import os
import json
import base64
import urllib.request
import urllib.error
from datetime import datetime

ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')

# ---------------------------------------------------------------------------
# Step 1: PDF 읽기
# ---------------------------------------------------------------------------
def read_pdf(path: str) -> bytes:
    with open(path, 'rb') as f:
        return f.read()

# ---------------------------------------------------------------------------
# Step 2: Claude API 호출 (PDF 직접 전달)
# ---------------------------------------------------------------------------
def call_claude_with_pdf(pdf_bytes: bytes, prompt: str, system: str = '') -> str:
    """PDF를 base64로 인코딩하여 Claude API에 직접 전달"""
    if not ANTHROPIC_API_KEY:
        return ''

    pdf_b64 = base64.standard_b64encode(pdf_bytes).decode('utf-8')

    payload = json.dumps({
        'model': 'claude-sonnet-4-6',
        'max_tokens': 4096,
        'system': system,
        'messages': [{
            'role': 'user',
            'content': [
                {
                    'type': 'document',
                    'source': {
                        'type': 'base64',
                        'media_type': 'application/pdf',
                        'data': pdf_b64,
                    },
                },
                {
                    'type': 'text',
                    'text': prompt,
                }
            ],
        }],
    }).encode('utf-8')

    req = urllib.request.Request(
        'https://api.anthropic.com/v1/messages',
        data=payload,
        headers={
            'x-api-key': ANTHROPIC_API_KEY,
            'anthropic-version': '2023-06-01',
            'anthropic-beta': 'pdfs-2024-09-25',
            'content-type': 'application/json',
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            resp = json.loads(r.read().decode('utf-8'))
            return resp['content'][0]['text']
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='ignore')
        print(f"  Claude API 오류 ({e.code}): {body[:300]}")
        return ''
    except Exception as e:
        print(f"  Claude API 실패: {e}")
        return ''

SYSTEM_REPORT = """당신은 KTL(한국산업기술시험원) 수출지원센터의 TBT 규제 분석 전문가입니다.
각국 규제 원문 PDF를 분석하여 한국 수출기업 대상 심층분석보고서 초안을 작성합니다.
원문에 없는 내용은 임의 생성하지 않고 반드시 "원문상 확인되지 않음" 또는 "공식자료 확인 필요"로 표시합니다."""

# ---------------------------------------------------------------------------
# Step 3: 구조화된 정보 추출
# ---------------------------------------------------------------------------
def extract_info(pdf_bytes: bytes) -> dict:
    if not ANTHROPIC_API_KEY:
        print("  ANTHROPIC_API_KEY 없음 → 템플릿 구조만 생성")
        return _empty_template()

    print("  PDF → Claude API: 번역 + 구조 추출 중...")
    prompt = """이 PDF 규제 원문을 분석하여 아래 JSON 형식으로 출력하세요.
원문에서 확인되지 않는 항목은 반드시 "원문상 확인되지 않음"으로 표시하세요.

{
  "규제명_원문": "",
  "규제명_국문": "",
  "통보국": "",
  "통보번호_또는_문서번호": "",
  "발행기관": "",
  "채택일": "",
  "시행일": "",
  "의견수렴마감일": "",
  "HS_code": "",
  "TBT통보여부": "",
  "도입배경": "",
  "규제요지": "",
  "적용대상": "",
  "세부내용_요약": "",
  "인증_신고_절차": "",
  "인증_유효기간": "",
  "위반시_제재": "",
  "경과조치": "",
  "기업애로_예상": "",
  "대응방안_중소기업": "",
  "대응방안_중견기업": "",
  "대응방안_대기업": "",
  "참고URL": ""
}

JSON만 출력하세요. 다른 설명 불필요."""

    raw = call_claude_with_pdf(pdf_bytes, prompt, SYSTEM_REPORT)
    if not raw:
        return _empty_template()

    try:
        start = raw.find('{')
        end   = raw.rfind('}') + 1
        return json.loads(raw[start:end])
    except Exception as e:
        print(f"  JSON 파싱 실패 ({e}) → 템플릿 구조로 대체")
        return _empty_template()

def _empty_template() -> dict:
    return {k: '원문상 확인되지 않음' for k in [
        '규제명_원문', '규제명_국문', '통보국', '통보번호_또는_문서번호',
        '발행기관', '채택일', '시행일', '의견수렴마감일', 'HS_code',
        'TBT통보여부', '도입배경', '규제요지', '적용대상', '세부내용_요약',
        '인증_신고_절차', '인증_유효기간', '위반시_제재', '경과조치',
        '기업애로_예상', '대응방안_중소기업', '대응방안_중견기업',
        '대응방안_대기업', '참고URL',
    ]}

# ---------------------------------------------------------------------------
# Step 4: 주요국 규제동향 생성
# ---------------------------------------------------------------------------
def generate_country_comparison(pdf_bytes: bytes, info: dict) -> str:
    if not ANTHROPIC_API_KEY:
        return _country_template()

    print("  주요국 규제동향 생성 중...")
    prompt = f"""이 규제 원문과 아래 분석 정보를 바탕으로,
유사한 규제를 운영하는 주요국(미국, EU, 일본, 중국)의 기술규제 동향을 작성하세요.

규제요지: {info.get('규제요지', '')}
적용대상: {info.get('적용대상', '')}

각 국가별로 (현행 규정), (도입동향), (유사품목 제도 도입동향) 3줄 이내로 작성하세요.
공식자료 근거가 없는 내용은 "공식자료 확인 필요"로 표시하세요.

출력 형식:
### 미국
- (현행 규정) ...
- (도입동향) ...
- (유사품목 제도 도입동향) ...

### EU
...
### 일본
...
### 중국
..."""

    result = call_claude_with_pdf(pdf_bytes, prompt, SYSTEM_REPORT)
    return result if result else _country_template()

def _country_template() -> str:
    return "\n".join([
        "### 미국\n- (현행 규정) 공식자료 확인 필요\n- (도입동향) 공식자료 확인 필요\n- (유사품목 제도 도입동향) 공식자료 확인 필요",
        "\n### EU\n- (현행 규정) 공식자료 확인 필요\n- (도입동향) 공식자료 확인 필요\n- (유사품목 제도 도입동향) 공식자료 확인 필요",
        "\n### 일본\n- (현행 규정) 공식자료 확인 필요\n- (도입동향) 공식자료 확인 필요\n- (유사품목 제도 도입동향) 공식자료 확인 필요",
        "\n### 중국\n- (현행 규정) 공식자료 확인 필요\n- (도입동향) 공식자료 확인 필요\n- (유사품목 제도 도입동향) 공식자료 확인 필요",
    ])

# ---------------------------------------------------------------------------
# Step 5: KTL master template 서식으로 보고서 생성
# ---------------------------------------------------------------------------
def generate_report(info: dict, country_comp: str, today: str, source_file: str) -> str:
    sym = info.get('통보번호_또는_문서번호', '미확인')
    report_id = f"SANDBOX-{today.replace('-','')}"

    lines = [
        f"# 무역기술장벽(TBT) 심층분석보고서 {report_id}",
        f"# 『{info.get('통보국','')}, {info.get('규제명_국문','')}』",
        "",
        f"> ⚠️ 본 보고서는 규제 원문 PDF 기반 **자동 생성 샌드박스 초안**입니다.",
        f"> 담당자 검토·검증 후 최종 게시. 생성일: {today} | 원문: {os.path.basename(source_file)}",
        "",
        "---",
        "",
        "| 항목 | 내용 |",
        "|------|------|",
        f"| TBT 통보여부 | {info.get('TBT통보여부','원문상 확인되지 않음')} |",
        f"| HS Code | {info.get('HS_code','작성없음')} |",
        f"| 통보국 | {info.get('통보국','')} |",
        f"| 발행기관 | {info.get('발행기관','')} |",
        f"| 전년도 수출액 | 작성없음 |",
        f"| 작성기관 | 한국산업기술시험원 |",
        f"| 문의처 | tbt@kotica.or.kr |",
        "",
        "---",
        "",
        "# 규제 요약서",
        "",
        "## □ 규제 개요",
        f" ㅇ (규제요지) {info.get('규제요지','')}",
        "",
        f" ㅇ (적용범위) {info.get('적용대상','')}",
        "",
        "## □ 주요 내용",
        f" ㅇ (주요 내용) {info.get('세부내용_요약','')}",
        "",
        f" ㅇ (인증정보) {info.get('인증_신고_절차','')}",
        f"  - (유효기간) {info.get('인증_유효기간','')}",
        f"  - (위반 시 제재) {info.get('위반시_제재','')}",
        "",
        "## □ 기술규제 영향분석",
        f" ㅇ (규제 영향 분석 결과) {info.get('기업애로_예상','')}",
        f" ㅇ (권고사항) 원문 분석 및 공식자료 확인 후 작성",
        "",
        "## □ 예상되는 기업애로 요인 분석 및 파급효과",
        f" ㅇ {info.get('기업애로_예상','')}",
        "",
        "## □ 대응 방안",
        f" ㅇ 기업 규모별 전략",
        f"  - (중소기업) {info.get('대응방안_중소기업','')}",
        f"  - (중견기업) {info.get('대응방안_중견기업','')}",
        f"  - (대기업) {info.get('대응방안_대기업','')}",
        "",
        "---",
        "",
        "# 요약문",
        "",
        "| 구분 | 항목 | 내용 |",
        "|------|------|------|",
        f"| 규제명 | 원문 | {info.get('규제명_원문','')} |",
        f"| 규제명 | 국문 | {info.get('규제명_국문','')} |",
        f"| WTO/TBT 통보문 번호 | | {sym} |",
        f"| 통보국 | | {info.get('통보국','')} |",
        f"| 채택(예정)일 | | {info.get('채택일','')} |",
        f"| 시행(예정)일 | | {info.get('시행일','')} |",
        f"| HS Code | | {info.get('HS_code','작성없음')} |",
        f"| 의견수렴 마감일 | | {info.get('의견수렴마감일','')} |",
        f"| 규제 주요 내용 | 해당부처 | {info.get('발행기관','')} |",
        f"| 규제 주요 내용 | 규제목적 | {info.get('도입배경','')} |",
        f"| 규제 주요 내용 | 주요내용 | {info.get('규제요지','')} |",
        "",
        "---",
        "",
        "# Ⅰ. 규제 개요",
        "",
        "## □ 도입배경",
        f" ㅇ {info.get('도입배경','')}",
        "",
        "## □ 규제 요지",
        f" ㅇ {info.get('규제요지','')}",
        "",
        "## □ 적용대상",
        f" ㅇ {info.get('적용대상','')}",
        "",
        "## □ 시행일",
        f" ㅇ {info.get('시행일','')}",
        f"  - 채택일: {info.get('채택일','')}",
        f"  - 경과조치: {info.get('경과조치','')}",
        "",
        "---",
        "",
        "# Ⅱ. 규제 세부 내용",
        "",
        "## □ 세부내용",
        f" ㅇ {info.get('세부내용_요약','')}",
        "",
        "> ※ 원문 조항별 세부 내용은 참고 2 규제원문(전문) 번역본 참조",
        "",
        "---",
        "",
        "# Ⅲ. 관련 인증 정보",
        "",
        "## □ 인증 절차",
        f" ㅇ (인증 개요) {info.get('인증_신고_절차','')}",
        "",
        "## □ 신청 시 유의사항",
        f" ㅇ (인증 유효기간) {info.get('인증_유효기간','')}",
        " ㅇ (인증비용) 공식자료 확인 필요",
        f" ㅇ (위반 시 제재) {info.get('위반시_제재','')}",
        "",
        "---",
        "",
        "# Ⅳ. 주요국 규제동향 및 규제수준 비교",
        "",
        "## 1. 주요국 기술규제 동향",
        "",
        country_comp,
        "",
        "## 2. 주요국 규제 수준 비교",
        "",
        f"| 구분 | {info.get('통보국','')} | 미국 | EU | 일본 | 중국 |",
        "|------|------|------|------|------|------|",
        "| 상위 법·제도 | 공식자료 확인 필요 | 공식자료 확인 필요 | 공식자료 확인 필요 | 공식자료 확인 필요 | 공식자료 확인 필요 |",
        "| 관리기관 | 공식자료 확인 필요 | 공식자료 확인 필요 | 공식자료 확인 필요 | 공식자료 확인 필요 | 공식자료 확인 필요 |",
        "| 사전허가·등록 | 공식자료 확인 필요 | 공식자료 확인 필요 | 공식자료 확인 필요 | 공식자료 확인 필요 | 공식자료 확인 필요 |",
        "",
        "---",
        "",
        "# Ⅴ. 예상 애로사항 및 파급효과",
        "",
        "## 1. 기술규제 영향 평가 검토",
        "",
        "### ㅇ 평가 항목별 영향 분석",
        "",
        "| 평가항목 | 평가결과 |",
        "|----------|----------|",
        "| 인증·신고 대응 부담 | 원문 분석 후 작성 |",
        "| 시험·문서 영향 | 원문 분석 후 작성 |",
        "| 표시·라벨 영향 | 원문 분석 후 작성 |",
        "| 사후관리 부담 | 원문 분석 후 작성 |",
        "",
        "## 2. TBT 협정문 위배 여부 판단",
        "",
        "| 연번 | 무역기술장벽 유형 | 위반사항 |",
        "|------|------------------|----------|",
        f"| 1 | 국제표준과 일치화 되지 않은 표준 | {info.get('TBT통보여부','원문 분석 후 작성')} |",
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
        f"| 중소기업 | 적용 여부 확인 | {info.get('대응방안_중소기업','')} |",
        f"| 중견기업 | 허가자료 준비 | {info.get('대응방안_중견기업','')} |",
        f"| 대기업 | 포트폴리오 관리 | {info.get('대응방안_대기업','')} |",
        "",
        " ㅇ 본 보고서는 우리 수출기업의 무역기술장벽 대응을 위한 해외 기술규제 정보를 분석 및 제공하기 위해 작성되었습니다.",
        " ㅇ 위 규제와 관련된 정보는 해외인증기술규제정보포털(knowtbt.kr)에서 열람 가능합니다.",
        "",
        "---",
        "",
        "# 참고 1 참고자료",
        "",
        f" ㅇ 규제 원문 파일: {os.path.basename(source_file)}",
        f" ㅇ 문서번호: {sym}",
        f" ㅇ 발행기관: {info.get('발행기관','')}",
        info.get('참고URL', ''),
        "",
        "---",
        "",
        "# 참고 2 규제원문(전문) 번역본",
        "",
        "> ※ 전문 번역본은 담당자가 원문 PDF를 기준으로 별도 작성합니다.",
        "",
    ]
    return '\n'.join(lines)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    if len(sys.argv) < 2:
        print("사용법: python3 scripts/tbt_report_pipeline.py <규제원문.pdf>")
        print("예시:   python3 scripts/tbt_report_pipeline.py sources/VNM408.pdf")
        sys.exit(1)

    pdf_path = sys.argv[1]
    if not os.path.exists(pdf_path):
        print(f"오류: 파일을 찾을 수 없습니다 — {pdf_path}")
        sys.exit(1)

    today = datetime.now().strftime('%Y-%m-%d')
    print(f"=== TBT 보고서 파이프라인 샌드박스 ({today}) ===")
    print(f"    입력 파일: {pdf_path}")
    print(f"    API 모드: {'Claude API 활성' if ANTHROPIC_API_KEY else '템플릿 모드 (ANTHROPIC_API_KEY 없음)'}")

    # Step 1: PDF 읽기
    print("\n[1/4] PDF 읽기...")
    pdf_bytes = read_pdf(pdf_path)
    print(f"  → {len(pdf_bytes):,} bytes")

    # Step 2: 번역 + 구조 추출
    print("\n[2/4] 번역 및 구조 추출 (Claude API)...")
    info = extract_info(pdf_bytes)
    print(f"  → 통보국: {info.get('통보국','')}")
    print(f"  → 규제명: {info.get('규제명_국문','')}")
    print(f"  → 시행일: {info.get('시행일','')}")

    # Step 3: 주요국 비교
    print("\n[3/4] 주요국 규제동향 생성...")
    country_comp = generate_country_comparison(pdf_bytes, info)

    # Step 4: 보고서 생성
    print("\n[4/4] KTL 서식 보고서 초안 생성...")
    report_md = generate_report(info, country_comp, today, pdf_path)

    # 저장
    out_dir  = os.path.join(os.path.dirname(__file__), '..', 'output', 'sandbox-reports')
    os.makedirs(out_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    out_path  = os.path.join(out_dir, f'{today}-{base_name}-report.md')

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(report_md)

    print(f"\n✅ 보고서 초안 생성 완료: {out_path}")
    print(f"   다음 단계: 담당자 검토 → HWP 양식에 붙여넣기 → 내부 결재 → knowtbt.kr 게시")
    return 0

if __name__ == '__main__':
    sys.exit(main())
