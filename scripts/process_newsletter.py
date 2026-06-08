#!/usr/bin/env python3
"""
C2P Newsletter Processor
------------------------
Usage:
  python3 scripts/process_newsletter.py inbox/latest.eml

Reads a C2P Alert .eml file, extracts all news/regulation items,
scores them by Korean export relevance, and writes a Jekyll post draft
to _posts/YYYY-MM-DD-c2p-news.md
"""

import email
import re
import sys
import os
from datetime import datetime
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Scoring criteria (재원 선생님이 설계한 기준)
# ---------------------------------------------------------------------------
KOREA_EXPORT_KEYWORDS = [
    'korea', 'korean', '한국', 'battery', 'batteries', 'ev', 'electric vehicle',
    'display', 'semiconductor', 'electronics', 'appliance', 'textile', 'cosmetic',
    'chemical', 'pfas', 'reach', 'rohs', 'ecodesign', 'energy efficiency',
    'ccc', 'china', 'eu', 'europe', 'vietnam', 'indonesia', 'malaysia',
    'saudi', 'uae', 'middle east', 'halal', 'wto', 'tbt',
]

HIGH_IMPACT_COUNTRIES = ['china', 'eu', 'europe', 'united states', 'usa', 'vietnam',
                          'indonesia', 'malaysia', 'saudi arabia', 'uae', 'japan']

HIGH_IMPACT_SECTORS = ['battery', 'batteries', 'electric', 'display', 'semiconductor',
                        'electronics', 'appliance', 'textile', 'cosmetic', 'chemical',
                        'ai', 'artificial intelligence', 'cybersecurity']


def parse_eml(filepath):
    with open(filepath, 'rb') as f:
        msg = email.message_from_bytes(f.read())

    html_content = None
    for part in msg.walk():
        if part.get_content_type() == 'text/html':
            html_content = part.get_payload(decode=True).decode('utf-8', errors='replace')
            break

    if not html_content:
        raise ValueError("No HTML content found in .eml file")

    date_str = msg.get('Date', '')
    return html_content, date_str


def extract_items(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    lines = [l.strip() for l in soup.get_text(separator='\n').split('\n') if l.strip()]

    items = []

    # --- News & Analysis section ---
    in_news = False
    i = 0
    while i < len(lines):
        if lines[i] == 'News & Analysis':
            in_news = True
            i += 1
            continue
        if lines[i] == 'Standards and regulations':
            in_news = False
        if in_news and i + 1 < len(lines):
            line = lines[i]
            # Long lines that aren't bylines or UI text
            if (len(line) > 60
                    and not line.startswith('by ')
                    and line not in ('Read full article', '→', 'Unassessed', 'Relevant', 'Maybe', 'No')
                    and not line.startswith('On ')):
                # Grab description from next lines
                desc = ''
                for j in range(i + 1, min(i + 4, len(lines))):
                    if lines[j].startswith('by ') or lines[j] in ('Read full article', '→'):
                        break
                    if lines[j].startswith('On ') or len(lines[j]) > 30:
                        desc = lines[j]
                        break
                items.append({
                    'section': 'News & Analysis',
                    'type': 'NEWS',
                    'title': line,
                    'description': desc,
                    'status': '',
                    'projects': [],
                })
        i += 1

    # --- Standards and regulations section ---
    i = 0
    while i < len(lines):
        if lines[i] in ('REGULATION', 'STANDARD', 'SUPPORTING'):
            item_type = lines[i]
            title = lines[i + 1] if i + 1 < len(lines) else ''
            status = ''
            projects = []
            # Look ahead for Status and Projects
            for j in range(i + 2, min(i + 10, len(lines))):
                if lines[j] == 'Status:' and j + 1 < len(lines):
                    status = lines[j + 1]
                if lines[j] == 'Projects:' and j + 1 < len(lines):
                    for k in range(j + 1, min(j + 5, len(lines))):
                        if lines[k] in ('REGULATION', 'STANDARD', 'SUPPORTING', 'Status:', 'Projects:'):
                            break
                        if lines[k] not in ('Unassessed', 'Relevant', 'Maybe', 'No', 'Entered into Force'):
                            projects.append(lines[k])
                    break
            if title and len(title) > 20:
                items.append({
                    'section': 'Standards and regulations',
                    'type': item_type,
                    'title': title,
                    'description': '',
                    'status': status,
                    'projects': projects,
                })
        i += 1

    return items


def score_item(item):
    text = (item['title'] + ' ' + item['description'] + ' ' + ' '.join(item['projects'])).lower()
    score = 0

    # Export impact: mention of high-impact countries
    for country in HIGH_IMPACT_COUNTRIES:
        if country in text:
            score += 3

    # Sector relevance: Korean export-heavy sectors
    for sector in HIGH_IMPACT_SECTORS:
        if sector in text:
            score += 2

    # General Korea-export keywords
    for kw in KOREA_EXPORT_KEYWORDS:
        if kw in text:
            score += 1

    # Boost for "In force" (immediate action needed)
    if 'in force' in item['status'].lower():
        score += 2

    # Boost for high approval probability
    if 'news' in item['section'].lower():
        score += 1  # News/Analysis items are pre-curated

    return score


def generate_post(items, date_str, eml_path):
    today = datetime.now().strftime('%Y-%m-%d')

    # Score and rank
    scored = [(score_item(item), item) for item in items]
    scored.sort(key=lambda x: x[0], reverse=True)
    top_items = scored[:5]  # Top 5 for human review; mark top 2 as recommended

    lines = [
        '---',
        'layout: post',
        f'title: "글로벌 인증·규제 뉴스 ({today})"',
        f'date: {today}',
        'categories: [regulation, newsletter]',
        '---',
        '',
        f'> 📧 Source: C2P Alert ({today}) — AI 선별 초안, 담당자 최종 검토 필요',
        '',
        '## ✅ 추천 뉴스 (상위 2건)',
        '',
    ]

    for rank, (score, item) in enumerate(top_items[:2], 1):
        lines.append(f'### {rank}. {item["title"]}')
        if item['status']:
            lines.append(f'- **상태**: {item["status"]}')
        if item['projects']:
            lines.append(f'- **분야**: {", ".join(item["projects"])}')
        if item['description']:
            lines.append(f'- **개요**: {item["description"]}')
        lines.append(f'- **관련성 점수**: {score}점')
        lines.append('')
        lines.append('**요약** (팀원 작성 후 이 자리에 추가)')
        lines.append('')
        lines.append('---')
        lines.append('')

    lines.append('## 📋 전체 선별 목록 (검토용)')
    lines.append('')
    lines.append('| 순위 | 구분 | 제목 | 상태 | 점수 |')
    lines.append('|------|------|------|------|------|')
    for rank, (score, item) in enumerate(top_items, 1):
        marker = '⭐' if rank <= 2 else ''
        title_short = item['title'][:60] + ('...' if len(item['title']) > 60 else '')
        lines.append(f'| {rank}{marker} | {item["type"]} | {title_short} | {item["status"][:30]} | {score} |')

    lines.append('')
    lines.append('---')
    lines.append('*본 초안은 AI가 자동 생성했습니다. 발행 전 담당자 검토 필수.*')

    return '\n'.join(lines)


def main():
    if len(sys.argv) < 2:
        # Default to latest .eml in inbox/
        inbox = os.path.join(os.path.dirname(__file__), '..', 'inbox')
        emls = sorted([f for f in os.listdir(inbox) if f.endswith('.eml')])
        if not emls:
            print("Usage: python3 scripts/process_newsletter.py <path-to.eml>")
            sys.exit(1)
        eml_path = os.path.join(inbox, emls[-1])
    else:
        eml_path = sys.argv[1]

    print(f"Processing: {eml_path}")
    html_content, date_str = parse_eml(eml_path)
    items = extract_items(html_content)
    print(f"Extracted {len(items)} items")

    post = generate_post(items, date_str, eml_path)

    today = datetime.now().strftime('%Y-%m-%d')
    out_dir = os.path.join(os.path.dirname(__file__), '..', '_posts')
    out_path = os.path.join(out_dir, f'{today}-c2p-news.md')

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(post)

    print(f"✅ Draft post written to: {out_path}")
    return out_path


if __name__ == '__main__':
    main()
