---
title: Human-in-the-Loop Principle
tags: [ai, principle, quality-control, public-institution, workflow-design]
category: pattern
created: 2026-06-08
---

# Human-in-the-Loop Principle

## Definition
Every AI-assisted workflow follows the same structure:
> **AI generates draft → Human reviews → Human approves/corrects → Output published**

## Why This Pattern Appears Everywhere
This is an unconscious but consistent design principle across all of Jaewon's AI workflows.

### Structural reason
Results are published to public government sites — credibility and accuracy are non-negotiable.
AI errors in public documents damage institutional reputation.

### Practical reason  
AI still has known limitations (see [[ai-strengths-limitations]]):
- Cannot reliably match human writing style
- Inserts meta-comments not appropriate for final readers
- Rule-based reasoning misses contextual nuance

## Instances of This Pattern
- [[ai-workflow-tbt-report]]: AI drafts → researcher edits → internal approval → publish
- [[ai-workflow-newsletter]]: AI selects → human confirms → team summarizes → AI polishes → publish

## Hidden Insight
Most AI users treat the model as the final author. Jaewon's unconscious design treats AI
as a **first-draft assistant**, with the human as the **accountable author**.
This is the correct model for regulated/public-sector output.
