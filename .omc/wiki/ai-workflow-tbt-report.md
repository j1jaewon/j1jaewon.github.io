---
title: AI Workflow — TBT Regulation Report Pipeline
tags: [ai, workflow, tbt, chatgpt, report, automation, prompt-engineering]
category: pattern
created: 2026-06-08
---

# AI Workflow — TBT Regulation Report Pipeline

## Overview
A semi-automated pipeline for producing overseas technical regulation (TBT) reports
from raw government gazette sources. Built and iterated over time using ChatGPT Projects.

## Pipeline Steps
1. **Source**: Government gazettes (관보) from any country — multilingual originals
2. **Translation**: AI translates raw gazette text
3. **Info Extraction**: AI extracts fields matching the standard report format
4. **Report Draft**: AI produces structured draft in the required format
5. **Human Review**: Researcher reviews and edits
6. **Internal Approval**: Internal review process
7. **Publication**: Upload to public government information site (대국민 공개 사이트)

## Implementation: ChatGPT Projects
- A dedicated ChatGPT Project contains:
  - Reference files (보고서 형식, 과거 예시)
  - Full workflow instructions (작업 흐름 지시사항)
- Trigger phrase: **"프로젝트 flow대로 보고서를 작성해줘"** → runs full pipeline
- This is an advanced prompt engineering pattern: persistent context + few-shot structure

## Current Pain Point
> AI inserts author-facing meta-comments into the final report body:
> - "원문에 따르면..."
> - "번역 내용 중 00 검토 필요"

These are appropriate for the drafter but inappropriate for the public-facing report.
**Status**: Still iterating on the system prompt to suppress this behavior.

## Key Lessons from Iteration
- Initial results were poor; prompt and reference files revised many times
- Getting AI to "stay in role" as a report writer (not a collaborator) is the hard part
- Prompt fix direction: explicitly instruct AI to write as if for a final reader, not an editor

## Tacit Knowledge
- The workflow was entirely self-designed — no template borrowed from elsewhere
- Follows unconscious [[human-in-the-loop]] principle: AI drafts, human approves

See also: [[professional-profile]] [[ai-workflow-newsletter]] [[human-in-the-loop-principle]]
