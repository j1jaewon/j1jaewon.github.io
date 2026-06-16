#!/usr/bin/env python3
"""
WTO TBT Daily Briefing
-----------------------
매일 자동 실행: WTO TBT 신규 통보문 수집 → 한국 수출 관련성 점수 → 브리핑 포스트 생성
"""

import urllib.request
import urllib.parse
import json
import os
import sys
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# 한국 수출 관련성 점수 기준
# ---------------------------------------------------------------------------
HIGH_IMPACT_COUNTRIES = [
    'china', 'eu', 'european union', 'united states', 'vietnam', 'indonesia',
    'malaysia', 'saudi arabia', 'uae', 'japan', 'india', 'brazil', 'mexico',
    'turkey', 'thailand', 'philippines', 'taiwan', 'australia',
]
HIGH_IMPACT_SECTORS = [
    'battery', 'electric vehicle', 'display', 'semiconductor', 'electronics',
    'appliance', 'textile', 'cosmetic', 'chemical', 'pfas', 'reach', 'rohs',
    'ecodesign', 'energy efficiency', 'ccc', 'artificial intelligence',
    'cybersecurity', 'solar', 'led', 'medical', 'food', 'halal',
    'wireless', 'telecom', 'radio', 'automotive', 'toy',
]

def score(title, member=''):
    text = (title + ' ' + member).lower()
    s = 0
    for c in HIGH_IMPACT_COUNTRIES:
        if c in text:
            s += 3
    for sec in HIGH_IMPACT_SECTORS:
        if sec in text:
            s += 2
    return s

# ---------------------------------------------------------------------------
# WTO TBT 통보문 수집 (ePing 공개 API)
# ---------------------------------------------------------------------------
def fetch_tbt_notifications(days_back=1):
    """
    WTO ePing에서 최근 TBT 통보문 수집
    공개 검색 엔드포인트 사용
    """
    since = (datetime.utcnow() - timedelta(days=days_back)).strftime('%Y-%m-%d')

    # ePing 공개 검색 API
    url = (
        'https://eping.wto.org/api/v1/notifications/search'
        f'?domain=TBT&dateFrom={since}&pageSize=50&page=1'
    )

    headers = {
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (KTL TBT Monitor)',
    }

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode('utf-8'))
    except Exception as e:
        print(f"ePing API 시도 실패: {e}")
        return None

def fetch_tbt_wto_api(days_back=1):
    """
    WTO 공식 API (apiportal.wto.org) 시도
    API key 없이 공개 접근 가능한 엔드포인트
    """
    since = (datetime.utcnow() - timedelta(days=days_back)).strftime('%Y-%m-%d')

    url = (
        'https://api.wto.org/tbt/v1/notifications'
        f'?dateFrom={since}&pageSize=50'
    )

    headers = {
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0',
    }

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode('utf-8'))
    except Exception as e:
        print(f"WTO API 시도 실패: {e}")
        return None

def parse_notifications(data):
    """다양한 API 응답 형식 파싱"""
    items = []

    if not data:
        return items

    # 리스트 형식
    if isinstance(data, list):
        raw_items = data
    # 딕셔너리 형식 (페이지네이션 포함)
    elif isinstance(data, dict):
        raw_items = (data.get('notifications') or
                     data.get('items') or
                     data.get('results') or
                     data.get('data') or [])
    else:
        return items

    for item in raw_items:
        title = (item.get('title') or
                 item.get('subject') or
                 item.get('description') or
                 item.get('titleText') or '')
        symbol = (item.get('symbol') or
                  item.get('notificationSymbol') or
                  item.get('id') or '')
        member = (item.get('member') or
                  item.get('country') or
                  item.get('notifyingMember') or '')
        date = (item.get('distributionDate') or
                item.get('date') or
                item.get('notificationDate') or '')

        if title:
            items.append({
                'title': title,
                'symbol': symbol,
                'member': member,
                'date': date,
                'score': score(title, member),
            })

    return items

# ---------------------------------------------------------------------------
# 포스트 생성
# ---------------------------------------------------------------------------
def generate_post(items, today, source_note=''):
    top = sorted(items, key=lambda x: x['score'], reverse=True)

    lines = [
        '---',
        'layout: post',
        f'title: "WTO TBT 일일 브리핑 ({today})"',
        f'date: {today}',
        'categories: [regulation, tbt, briefing]',
        '---',
        '',
        f'> 🤖 매일 자동 생성 | WTO TBT 신규 통보문 기준 | {today}',
        '',
    ]

    if not items:
        lines += [
            '오늘 신규 TBT 통보문이 없거나 API 응답을 받지 못했습니다.',
            '',
            f'> {source_note}',
        ]
        return '\n'.join(lines)

    lines += [
        f'## 📊 오늘의 TBT 통보문 — {len(items)}건 수집',
        '',
        '## ⭐ 한국 수출 관련성 상위 5건',
        '',
    ]

    for i, item in enumerate(top[:5], 1):
        lines += [
            f'### {i}. {item["title"]}',
        ]
        if item['member']:
            lines.append(f'- **통보국**: {item["member"]}')
        if item['symbol']:
            lines.append(f'- **문서번호**: {item["symbol"]}')
        if item['date']:
            lines.append(f'- **배포일**: {item["date"]}')
        lines += [
            f'- **관련성 점수**: {item["score"]}점',
            '',
        ]

    lines += [
        '---',
        '## 📋 전체 목록',
        '',
        '| # | 통보국 | 제목 | 점수 |',
        '|---|--------|------|------|',
    ]

    for i, item in enumerate(top, 1):
        mark = ' ⭐' if i <= 5 else ''
        t = item['title'][:60] + ('…' if len(item['title']) > 60 else '')
        lines.append(f'| {i}{mark} | {item["member"]} | {t} | {item["score"]} |')

    lines += [
        '',
        '---',
        f'*자동 생성 | {source_note}*',
    ]

    return '\n'.join(lines)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    today = datetime.now().strftime('%Y-%m-%d')
    days_back = int(os.environ.get('DAYS_BACK', '1'))

    print(f"=== WTO TBT 브리핑 생성 ({today}) ===")

    # API 순차 시도
    data = None
    source = ''

    print("1) ePing API 시도...")
    data = fetch_tbt_notifications(days_back)
    if data is not None:
        source = 'Source: WTO ePing SPS&TBT Platform'

    if data is None:
        print("2) WTO API 시도...")
        data = fetch_tbt_wto_api(days_back)
        if data is not None:
            source = 'Source: WTO API Portal'

    items = parse_notifications(data)
    print(f"   → {len(items)}건 수집")

    post = generate_post(items, today, source)

    out_dir = os.path.join(os.path.dirname(__file__), '..', '_posts')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f'{today}-wto-tbt-briefing.md')

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(post)

    print(f"✅ 포스트 생성: {out_path}")
    return len(items)

if __name__ == '__main__':
    count = main()
    sys.exit(0 if count >= 0 else 1)
