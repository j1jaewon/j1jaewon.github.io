#!/usr/bin/env python3
"""
C2P Newsletter Processor
-------------------------
Usage:
  python3 scripts/process_newsletter.py [path-to.eml]

Reads a C2P Alert .eml, picks top 2 news by Korean market relevance,
and writes two files:
  - output/YYYY-MM-DD-email-draft.md  : copy-paste ready email to team
  - output/YYYY-MM-DD-selection.md    : full ranked list for reference
"""

import email
import re
import sys
import os
from datetime import datetime
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Team member names (edit as needed)
# ---------------------------------------------------------------------------
TEAM = ['영서 연구원님', '현지 연구원님']

# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------
HIGH_IMPACT_COUNTRIES = [
    'eu', 'europe', 'european', 'china', 'united states', 'usa', 'vietnam',
    'indonesia', 'malaysia', 'saudi', 'uae', 'japan', 'india', 'korea',
    'brazil', 'mexico', 'turkey', 'thailand',
]
HIGH_IMPACT_SECTORS = [
    'battery', 'batteries', 'electric vehicle', 'ev ', 'display', 'semiconductor',
    'electronics', 'appliance', 'textile', 'cosmetic', 'chemical', 'pfas',
    'reach', 'rohs', 'ecodesign', 'energy efficiency', 'ccc', 'wto', 'tbt',
    'artificial intelligence', 'ai ', 'cybersecurity', 'solar', 'photovoltaic',
    'led', 'lighting', 'medical', 'food', 'halal', 'critical raw material',
    'digital', 'data', 'product safety',
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


# ---------------------------------------------------------------------------
# Parse .eml
# ---------------------------------------------------------------------------
def parse_eml(filepath):
    with open(filepath, 'rb') as f:
        msg = email.message_from_bytes(f.read())

    html_content = None
    for part in msg.walk():
        if part.get_content_type() == 'text/html':
            html_content = part.get_payload(decode=True).decode('utf-8', errors='replace')
            break

    if not html_content:
        raise ValueError("No HTML part found in .eml")

    return html_content, msg.get('Date', '')


def extract_items(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    lines = [l.strip() for l in soup.get_text(separator='\n').split('\n') if l.strip()]

    # Extract all links: title → href
    link_map = {}
    for a in soup.find_all('a', href=True):
        text = a.get_text(strip=True)
        href = a['href']
        if len(text) > 30 and 'compliance2product.com' in href:
            # Clean up href (quoted-printable artifacts)
            href = href.replace('=3D', '=').replace('\n', '').replace(' ', '')
            link_map[text] = href

    items = []
    i = 0
    while i < len(lines):
        line = lines[i]

        # News & Analysis
        if (i + 1 < len(lines)
                and lines[i + 1].startswith('by ')
                and len(line) > 50
                and line not in ('Read full article', 'News & Analysis')):
            desc = ''
            for j in range(i + 2, min(i + 5, len(lines))):
                if lines[j].startswith('On ') and len(lines[j]) > 30:
                    desc = lines[j][:300]
                    break
            url = link_map.get(line, '')
            items.append({
                'type': 'NEWS',
                'title': line,
                'description': desc,
                'status': '',
                'projects': '',
                'url': url,
            })

        # Regulation / Standard / Supporting
        elif line in ('REGULATION', 'STANDARD', 'SUPPORTING'):
            title = lines[i + 1] if i + 1 < len(lines) else ''
            status, projects = '', ''
            for j in range(i + 2, min(i + 12, len(lines))):
                if lines[j] == 'Status:' and j + 1 < len(lines):
                    status = lines[j + 1]
                if lines[j] == 'Projects:' and j + 1 < len(lines):
                    parts = []
                    for k in range(j + 1, min(j + 5, len(lines))):
                        if lines[k] in ('REGULATION', 'STANDARD', 'SUPPORTING',
                                        'Status:', 'Projects:', 'New', 'Older Added',
                                        'Status Changes', 'Dates'):
                            break
                        parts.append(lines[k])
                    projects = ', '.join(parts)
                    break
            url = link_map.get(title, '')
            if title and len(title) > 20:
                items.append({
                    'type': line,
                    'title': title,
                    'description': '',
                    'status': status,
                    'projects': projects,
                    'url': url,
                })
        i += 1

    return items


# ---------------------------------------------------------------------------
# Generate outputs
# ---------------------------------------------------------------------------
def generate_email_draft(top2, today):
    lines = [
        f'Subject: 인증 뉴스 정리 부탁드립니다.',
        '',
        '안녕하세요, 연구원님들.',
        '수출지원센터 정재원입니다.',
        '',
        '아래의 뉴스 정리를 부탁드립니다.',
        '',
    ]
    for idx, (score, item) in enumerate(top2):
        name = TEAM[idx] if idx < len(TEAM) else f'연구원{idx+1}님'
        lines.append(f'{idx + 1}. {name}')
        lines.append(f'{item["title"]}')
        if item['url']:
            lines.append(f'링크: {item["url"]}')
        lines.append('')

    lines += ['감사합니다.', '정재원 드림']
    return '\n'.join(lines)


def generate_selection_report(scored, today):
    lines = [
        f'# C2P 뉴스 선별 리포트 — {today}',
        '',
        '## ✅ 선정된 뉴스 2건',
        '',
    ]
    for idx, (score, item) in enumerate(scored[:2]):
        lines += [
            f'### {idx + 1}. {item["title"]}',
            f'- **유형**: {item["type"]}',
        ]
        if item['status']:
            lines.append(f'- **상태**: {item["status"]}')
        if item['projects']:
            lines.append(f'- **분야**: {item["projects"]}')
        if item['url']:
            lines.append(f'- **링크**: {item["url"]}')
        lines += [f'- **관련성 점수**: {score}점', '']

    lines += [
        '---',
        '## 📋 전체 후보 목록',
        '',
        '| 순위 | 유형 | 제목 | 상태 | 점수 |',
        '|------|------|------|------|------|',
    ]
    for rank, (score, item) in enumerate(scored, 1):
        mark = ' ⭐' if rank <= 2 else ''
        t = item['title'][:55] + ('…' if len(item['title']) > 55 else '')
        s = item['status'][:25] + ('…' if len(item['status']) > 25 else '')
        lines.append(f'| {rank}{mark} | {item["type"]} | {t} | {s} | {score} |')

    lines += ['', '---', '*AI 자동 선별 — 최종 선정은 담당자 판단으로 조정 가능*']
    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    if len(sys.argv) < 2:
        inbox = os.path.join(os.path.dirname(__file__), '..', 'inbox')
        emls = sorted([f for f in os.listdir(inbox) if f.endswith('.eml')])
        if not emls:
            print("Usage: python3 scripts/process_newsletter.py <path.eml>")
            sys.exit(1)
        eml_path = os.path.join(inbox, emls[-1])
    else:
        eml_path = sys.argv[1]

    print(f"Processing: {eml_path}")
    html_content, _ = parse_eml(eml_path)
    items = extract_items(html_content)
    print(f"Extracted {len(items)} items")

    scored = sorted(
        [(score_item(it['title'], it['status'], it['projects']), it) for it in items],
        key=lambda x: x[0], reverse=True
    )

    today = datetime.now().strftime('%Y-%m-%d')
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    os.makedirs(out_dir, exist_ok=True)

    # Email draft
    email_path = os.path.join(out_dir, f'{today}-email-draft.md')
    with open(email_path, 'w', encoding='utf-8') as f:
        f.write(generate_email_draft(scored[:2], today))
    print(f"📧 이메일 초안: {email_path}")

    # Selection report
    report_path = os.path.join(out_dir, f'{today}-selection.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(generate_selection_report(scored, today))
    print(f"📋 선별 리포트: {report_path}")


if __name__ == '__main__':
    main()
