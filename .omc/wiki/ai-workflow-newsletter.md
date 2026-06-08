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

See also: [[professional-profile]] [[ai-workflow-tbt-report]] [[human-in-the-loop-principle]]
