#!/usr/bin/env python3
"""
C2P Newsletter Text Processor
------------------------------
Usage:
  python3 scripts/process_newsletter_text.py inbox/input.txt

Reads plain text copied from C2P email, extracts news items,
scores them, and writes a Jekyll post draft to _posts/.
"""

import re
import sys
import os
from datetime import datetime

# ---------------------------------------------------------------------------
# Scoring criteria
# ---------------------------------------------------------------------------
HIGH_IMPACT_COUNTRIES = [
    'china', 'eu', 'europe', 'european', 'united states', 'usa', 'vietnam',
    'indonesia', 'malaysia', 'saudi', 'uae', 'japan', 'korea', 'india',
    'brazil', 'mexico', 'turkey', 'thailand', 'philippines',
]
HIGH_IMPACT_SECTORS = [
    'battery', 'batteries', 'electric vehicle', 'ev ', 'display', 'semiconductor',
    'electronics', 'appliance', 'textile', 'cosmetic', 'chemical', 'pfas',
    'reach', 'rohs', 'ecodesign', 'energy efficiency', 'ccc', 'wto', 'tbt',
    'ai ', 'artificial intelligence', 'cybersecurity', 'solar', 'photovoltaic',
    'led', 'lighting', 'medical', 'food', 'halal',
]
STATUS_BOOST = {'in force': 3, 'approved': 2, 'proposed': 1}


def score_item(title, status='', projects=''):
    text = (title + ' ' + status + ' ' + projects).lower()
    score = 0
    for c in HIGH_IMPACT_COUNTRIES:
        if c in text:
            score += 3
    for s in HIGH_IMPACT_SECTORS:
        if s in text:
            score += 2
    for st, boost in STATUS_BOOST.items():
        if st in text:
            score += boost
    return score


def parse_text(content):
    lines = [l.strip() for l in content.split('\n') if l.strip()]
    items = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # News & Analysis items (long title lines before "by Compliance")
        if (i + 1 < len(lines)
                and lines[i + 1].startswith('by ')
                and len(line) > 50
                and line not in ('Read full article', 'News & Analysis')):
            desc = ''
            for j in range(i + 2, min(i + 6, len(lines))):
                if lines[j].startswith('On ') and len(lines[j]) > 30:
                    desc = lines[j][:200]
                    break
            items.append({
                'type': 'NEWS',
                'title': line,
                'description': desc,
                'status': '',
                'projects': '',
            })
            i += 1
            continue

        # Regulation/Standard items
        if line in ('REGULATION', 'STANDARD', 'SUPPORTING'):
            item_type = line
            title = lines[i + 1] if i + 1 < len(lines) else ''
            status = ''
            projects = ''
            for j in range(i + 2, min(i + 12, len(lines))):
                if lines[j] == 'Status:' and j + 1 < len(lines):
                    status = lines[j + 1]
                if lines[j] == 'Projects:' and j + 1 < len(lines):
                    proj_parts = []
                    for k in range(j + 1, min(j + 5, len(lines))):
                        if lines[k] in ('REGULATION', 'STANDARD', 'SUPPORTING',
                                        'Status:', 'Projects:', 'New', 'Older Added',
                                        'Status Changes', 'Dates'):
                            break
                        proj_parts.append(lines[k])
                    projects = ', '.join(proj_parts)
                    break
            if title and len(title) > 20:
                items.append({
                    'type': item_type,
                    'title': title,
                    'description': '',
                    'status': status,
                    'projects': projects,
                })
        i += 1

    return items


def generate_post(items, today):
    scored = sorted(
        [(score_item(it['title'], it['status'], it['projects']), it) for it in items],
        key=lambda x: x[0], reverse=True
    )

    lines = [
        '---',
        'layout: post',
        f'title: "글로벌 인증·규제 뉴스 ({today})"',
        f'date: {today}',
        'categories: [regulation, newsletter]',
        'published: false',  # 담당자 검토 후 true로 변경
        '---',
        '',
        f'> 📧 Source: C2P Alert ({today}) | AI 선별 초안 — 발행 전 `published: true` 로 변경하세요',
        '',
        '## ✅ 추천 뉴스 (상위 2건)',
        '',
    ]

    for rank, (score, item) in enumerate(scored[:2], 1):
        lines += [
            f'### {rank}. {item["title"]}',
        ]
        if item['status']:
            lines.append(f'- **상태**: {item["status"]}')
        if item['projects']:
            lines.append(f'- **분야**: {item["projects"]}')
        if item['description']:
            lines.append(f'- **개요**: {item["description"]}')
        lines += [
            f'- **관련성 점수**: {score}점',
            '',
            '**요약**: (팀원 작성 후 추가)',
            '',
            '---',
            '',
        ]

    lines += [
        '## 📋 전체 선별 목록',
        '',
        '| 순위 | 구분 | 제목 | 상태 | 점수 |',
        '|------|------|------|------|------|',
    ]
    for rank, (score, item) in enumerate(scored, 1):
        marker = ' ⭐' if rank <= 2 else ''
        title_short = item['title'][:55] + ('…' if len(item['title']) > 55 else '')
        status_short = item['status'][:25] + ('…' if len(item['status']) > 25 else '')
        lines.append(f'| {rank}{marker} | {item["type"]} | {title_short} | {status_short} | {score} |')

    lines += [
        '',
        '---',
        '*본 초안은 AI가 자동 생성했습니다. 내용 검토 후 published: true로 변경하여 발행하세요.*',
    ]

    return '\n'.join(lines)


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else 'inbox/input.txt'

    if not os.path.exists(input_path):
        print(f"❌ 파일 없음: {input_path}")
        print("inbox/input.txt 에 C2P 이메일 텍스트를 붙여넣으세요.")
        sys.exit(1)

    with open(input_path, encoding='utf-8') as f:
        content = f.read()

    if len(content.strip()) < 100:
        print("❌ inbox/input.txt 가 비어 있거나 너무 짧습니다.")
        sys.exit(1)

    items = parse_text(content)
    print(f"✅ {len(items)}개 항목 추출됨")

    if not items:
        print("⚠️  항목을 찾지 못했습니다. 이메일 텍스트가 올바르게 붙여넣어졌는지 확인하세요.")
        sys.exit(1)

    today = datetime.now().strftime('%Y-%m-%d')
    post = generate_post(items, today)

    out_dir = os.path.join(os.path.dirname(__file__), '..', '_posts')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f'{today}-c2p-news.md')

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(post)

    print(f"📝 초안 생성: {out_path}")


if __name__ == '__main__':
    main()
