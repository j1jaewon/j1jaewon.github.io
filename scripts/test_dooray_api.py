#!/usr/bin/env python3
"""
Dooray API 테스트 스크립트
Usage:
  DOORAY_TOKEN=your_token python3 scripts/test_dooray_api.py

토큰은 환경변수로만 전달하세요. 절대 코드에 직접 입력하지 마세요.
"""

import os
import json
import urllib.request
import urllib.error

TOKEN = os.environ.get('DOORAY_TOKEN', '')
if not TOKEN:
    print("❌ DOORAY_TOKEN 환경변수가 없습니다.")
    print("   실행 방법: DOORAY_TOKEN=your_token python3 scripts/test_dooray_api.py")
    exit(1)

HEADERS = {
    'Authorization': f'dooray-api {TOKEN}',
    'Content-Type': 'application/json',
}

# Dooray API base URL (gov-dooray = 공공기관용)
# KTL은 gov-dooray.com 사용
BASES = [
    'https://api.dooray.com',
    'https://api.gov-dooray.com',
]

def get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode()), r.status
    except urllib.error.HTTPError as e:
        return {'error': e.reason, 'code': e.code}, e.code
    except Exception as e:
        return {'error': str(e)}, 0

print("=== Dooray API 탐색 ===\n")

for base in BASES:
    print(f"--- Base: {base} ---")

    # 1. 내 정보 확인
    data, status = get(f'{base}/common/v1/members/me')
    print(f"[{status}] GET /common/v1/members/me")
    if status == 200:
        print(f"  → {json.dumps(data, ensure_ascii=False)[:200]}")

    # 2. 메일함 목록
    data, status = get(f'{base}/mail/v1/mailboxes')
    print(f"[{status}] GET /mail/v1/mailboxes")
    if status == 200:
        print(f"  → {json.dumps(data, ensure_ascii=False)[:200]}")

    # 3. 받은 메일함
    data, status = get(f'{base}/mail/v1/mails?folderType=inbox&size=5')
    print(f"[{status}] GET /mail/v1/mails?folderType=inbox")
    if status == 200:
        print(f"  → {json.dumps(data, ensure_ascii=False)[:300]}")

    # 4. 대안 경로
    data, status = get(f'{base}/v1/mails')
    print(f"[{status}] GET /v1/mails")

    print()
