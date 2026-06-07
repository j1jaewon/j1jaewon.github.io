# Assignment Log — LLM Wiki & Automation
> Temporary file for tracking progress. Delete after assignment submission.

---

## Level 0: Archive — Build LLM Wiki

### Q0-1: Process to Build llm-wiki

#### Step 1 — Install oh-my-claudecode
- Installed `oh-my-claude-sisyphus` npm package (oh-my-claudecode v4.14.5) globally via:
  ```
  npm i -g oh-my-claude-sisyphus@latest
  ```
- Confirmed install at `/opt/node22/bin/omc`

#### Step 2 — Install /wiki skill into project
- Located the wiki skill files inside the npm package:
  - `/opt/node22/lib/node_modules/oh-my-claude-sisyphus/commands/wiki.md`
  - `/opt/node22/lib/node_modules/oh-my-claude-sisyphus/skills/wiki/SKILL.md`
- Copied `wiki.md` into `.claude/commands/wiki.md` in this repo
- Created `.omc/wiki/` directory for page storage
- Committed and pushed to branch `claude/zealous-franklin-vx4wn`

#### Step 3 — Choose knowledge source
- **Source A**: Exported conversation ZIP files from Gemini and Claude (too large to paste directly)
  - Plan: Upload relevant files into `sources/` folder in this repo, then ingest
- **Source B**: Self-interview — conducted in this Claude Code session

#### Step 4 — Ingest knowledge via /wiki
- (In progress — waiting for source files to be uploaded)
- Used `/wiki` slash command to ingest content into `.omc/wiki/*.md`

#### Step 5 — Run /wiki lint
- Health check to verify cross-references, orphan pages, and structure

---

### Q0-2: Key Insights (to fill in after ingestion)
- [ ] What patterns emerged that you didn't consciously realize you knew?
- [ ] What connections did the wiki surface between topics?
- [ ] What "hidden" knowledge became visible when structured?

---

## Level 1: Schedule — Daily Certification News Automation

### Q1-1: What did you ask the agent to do?
- Task: Monitor daily C2P certification industry email newsletters
- Process: Save email content to a designated file in the repo
- Agent reads the file, selects 2+ relevant news items, formats them as a post
- Output: Automatically creates a new `_posts/` entry in this GitHub Pages site

### Q1-2: Key lessons from autonomous tasks
- (To fill in after running the automation)

### Q1-3: Key elements to make the task useful
- (To fill in after running the automation)

---

## Repo Notes

### About this repo (j1jaewon.github.io)
- This is a personal GitHub Pages / Jekyll blog site
- The wiki is stored in `.omc/wiki/` (project-local, git-ignored by default)
- **Decision**: Keeping wiki here is fine for the assignment AND for long-term use,
  since this is already a personal knowledge repo. No need to move it.
- If you later want the wiki in a dedicated private repo, you can `mv .omc/wiki/ ../new-repo/`
  and it will work the same way.

---

## Self-Interview (to be conducted)
Questions to answer for wiki ingestion:
1. What topics have you most discussed with AI agents in the past year?
2. What problems were you trying to solve?
3. What did you learn that surprised you?
4. What knowledge do you apply repeatedly in your work?
5. What is your domain expertise (certification industry, C2P, etc.)?
