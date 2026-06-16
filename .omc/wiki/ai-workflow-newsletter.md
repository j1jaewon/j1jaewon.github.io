---
title: AI Workflow — Daily Certification News Newsletter
tags: [ai, workflow, newsletter, c2p, automation, news-curation, team]
category: pattern
created: 2026-06-08
---

# AI Workflow — Daily Certification News Newsletter

## Overview
A 5-step daily workflow for curating global certification/regulation news from
C2P email newsletters and publishing to a public government information site.

## Source
- **Only source**: C2P email newsletter (daily)
- No other feeds or subscriptions used

## 5-Step Flow

### Step 1 — Ingest
Paste the full C2P email content into AI (ChatGPT)

### Step 2 — AI Prioritization
AI ranks news items by self-designed criteria:
- **수출 파급력** (export impact on Korean industry)
- **규제 파급력** (regulatory significance)
- **주제 중복성** (overlap with previously covered topics)

Output: ranked shortlist of top news items

### Step 3 — Human Gatekeeping
Researcher reads the selected items in full and confirms suitability.
This step is non-negotiable — AI selection is advisory, not final.

### Step 4 — Team Dispatch
Two team members each receive one news item to summarize independently.

### Step 5 — AI Final Review + Publish
Team member summaries fed back to AI for final polish → upload to public site.

## Key Design Insight
The **selection criteria in Step 2 were entirely self-designed** — not borrowed from
any framework. This is operationalized tacit expertise: Jaewon's years of TBT/regulation
experience encoded as an AI prompt.

## Tacit Knowledge
- This flow is an advanced AI orchestration pattern; most practitioners do all steps manually
- The human checkpoint in Step 3 is a [[human-in-the-loop-principle]] safeguard
  critical for public institution credibility

## Future Automation Target (Level 1)
- Automate: save C2P email → agent selects & drafts → auto-create `_posts/` in Jekyll site
- See [[level1-automation-plan]]

## Claude 대화 시작 프롬프트 (뉴스레터 처리용)

새 대화를 열 때 아래 프롬프트를 첫 메시지로 붙여넣고 .eml 파일을 업로드한다.

```
나는 KTL 수출지원센터 연구원이야. 매일 C2P 뉴스레터(.eml)를 받아서 한국 수출기업에 파급력 있는 규제 뉴스 2건을 선별하고, 팀원 2명(영서·현지 연구원님)에게 각각 요약 요청 이메일을 보내는 업무를 해.

.eml 파일을 올려줄게. 파일에서 규제 항목들을 추출하고, 아래 기준으로 점수 매겨서 TOP 2 선별해줘:

- 고영향 국가(EU, 중국, 미국, 인도, 인도네시아, 한국 등): +3점
- 고영향 분야(배터리, AI, 화장품, 제품안전, 사이버보안 등): +2점
- 상태(In force +3 / Approved +2 / Proposed +1)

중요: 이미 이전 대화에서 선정한 뉴스는 제외하고 선별해줘. 대화 시작 시 내가 기선정 목록을 알려줄게.

결과는 ① Top5 순위표 ② 팀원 발송용 이메일 초안으로 줘.
```

### 기선정 목록 관리
매 대화 시작 시 아래 형식으로 추가:
```
기선정 목록:
- [제목] ([날짜])
```

### 검토 기준 (Step 5)
팀원 번역 회신 검토 시 확인 항목:
- 사실 오류 (날짜, 수치, 고유명사)
- 핵심 내용 누락
- 용어 일관성
- 공개 게시 적합 문체

See also: [[professional-profile]] [[ai-workflow-tbt-report]] [[human-in-the-loop-principle]]
