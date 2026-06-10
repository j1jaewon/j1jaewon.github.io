# Assignment Log — LLM Wiki & Automation
> 과제 제출 후 삭제 예정인 임시 파일

---

## 원본 과제 지문 (전문)

### Level 0: Archive (required)
Externalize your tacit knowledge using the /wiki skill of oh-my-claudecode (https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

For the source knowledge, you can use one of the following: 1) your original writings if you have written some notes; 2) the past conversation with your choice of AI agents (Gemini, Claude, ChatGPT); 3) interview yourself.

**Question 0-1:** Describe the process you took to build llm-wiki.
**Question 0-2:** What are the key insights you found from wiki. What are the hidden insights in your tacit knowledge.

### Level 1: Schedule (required)
Design and run one daily autonomous routine using either scheduled feature of Claude Cowork or Automations on Codex. The task could be related with your class team project or something personal to you.

**Question 1-1:** What have you asked the agent to do?
**Question 1-2:** What are your key lessons you learn from learning autonomous tasks?
**Question 1-3:** What are key elements to make the task useful to you?

### Level 2: Persistent (optional, bonus +10)
Build a persistent autonomous agent using Hermes Agent (https://github.com/nousresearch/hermes-agent) on your docker or VPS.

If you would like to install on your machine, please make sure that it is on docker (https://hermes-agent.nousresearch.com/docs/user-guide/docker). Otherwise, your autonomous agent might make a really serious impact on your own files.

**Question 2-1:** What have you asked the persistent agent to do?
**Question 2-2:** What are your key lessons you learn from learning the persistent agent?
**Question 2-3:** What are key elements to make the persistent agent useful to you?

### Level 3: Company-Relevant Sandbox (optional, bonus +10)
Pick a workflow you actually do at your current company (or your most recent one), something you'd love to automate but can't get IT permission for in time. Reproduce it OUTSIDE the company perimeter using synthetic or public data, then write the 1-pager you would send to your manager.

Safety rule: Do NOT use real internal data, credentials, or customer personally identifiable information (PII). If a workflow can't be desensitized, pick a different one.

**Deliverable:** (a) the working sandbox agent, (b) a 1-page proposal memo addressed to a real stakeholder at your company (you don't have to send it), (c) a short reflection on what would change if this ran on the real data inside the company perimeter.

**Question 3-1:** Which workflow did you pick, and why is this one worth closing the loop on at your company?
**Question 3-2:** If you handed this proposal to your manager on Monday, what is the first objection you would expect, and how would you answer it?

---

## 프로필 요약 (정재원 / Jaewon Jeong)
- **소속**: 한국산업기술시험원(KTL) 수출지원센터 연구원
- **전문분야**: 해외 기술규제(TBT) 분석, 디스플레이/웨어러블 국제표준화(IEC TC110, TC124)
- **경력**: 한국무역협회(인턴) → 한국디스플레이산업협회(표준화 R&D) → KTL(현재)
- **학력**: 서울시립대 경영학 학사 → KAIST 정보경영 석사 예정(2025.9~)
- **IEC**: 2024 IEC Young Professional 한국대표

---

## Level 0: Archive — LLM Wiki 구축

### Q0-1: 프로세스

#### Step 1 — oh-my-claudecode 설치
- `npm i -g oh-my-claude-sisyphus@latest` 로 v4.14.5 전역 설치
- `/wiki` 커맨드 파일 위치 확인: `/opt/node22/lib/node_modules/oh-my-claude-sisyphus/commands/wiki.md`

#### Step 2 — /wiki 스킬 프로젝트에 설치
- `.claude/commands/wiki.md` 로 복사
- `.omc/wiki/` 디렉토리 생성 (페이지 저장소)
- 브랜치 `claude/zealous-franklin-vx4wn` 에 커밋 & 푸시

#### Step 3 — 소스 파일 정리
- `sources/` 폴더 구조 생성:
  - `sources/claude/` — Claude export (conversations, memories, projects)
  - `sources/chatgpt/` — ChatGPT export (conversations x2, chat.html, user.json)
  - `sources/gemini/` — 준비 중
- 보안 이슈: GitHub Personal Access Token이 파일 내 포함되어 업로드 차단됨 → 민감정보 제거 후 재시도

#### Step 4 — 자기 인터뷰 진행
- 이력서(PDF) 기반 + 6개 인터뷰 질문으로 암묵지 외재화
- AI 활용 업무 3가지, 작업 흐름, AI 강점/한계, 미래 계획 정리

#### Step 5 — Wiki 인제스트
- `/wiki` 스킬로 인터뷰 내용 → `.omc/wiki/*.md` 생성
- 카테고리: `professional-profile`, `ai-workflow`, `tbt-regulation`, `newsletter`, `future-plans`

#### Step 6 — Wiki Lint
- 고아 페이지, 교차 참조 오류 등 구조 검증

---

### Q0-2: 핵심 인사이트 (인터뷰에서 발굴된 암묵지)

1. **5단계 뉴스레터 워크플로우** — 단순 AI 요약이 아니라, 선별 기준(수출 파급력·규제 파급력·중복성)을 직접 설계하고 팀 분업까지 AI로 조율하는 체계가 이미 완성되어 있음. 본인은 이걸 당연하게 여기지만, 이는 고급 AI 워크플로우 설계 역량임.

2. **ChatGPT 프로젝트 기반 컨텍스트 구조화** — "프로젝트 flow대로 해줘" 한 마디로 작동하도록 학습시킨 구조는 프롬프트 엔지니어링의 advanced 패턴(few-shot + persistent context). 대부분의 사용자는 매번 처음부터 설명함.

3. **AI 한계를 정확히 식별** — "보고서에 작성자 코멘트를 남기는 문제"를 구체적으로 인지하고 개선 중. 이는 단순 사용자가 아닌 AI 출력 품질을 설계하는 시각.

4. **Human-in-the-loop 일관성** — 모든 AI 활용이 "AI 초안 → 인간 검토 → 수정"의 구조로 일관됨. 이는 공공기관 보고서의 신뢰성 요건에 맞는 무의식적 설계 원칙.

5. **국제표준화 × AI의 희소 조합** — IEC 표준 + 다국어 관보 분석을 AI로 처리하는 노하우는 해당 분야에서 드문 전문성. 이 지식이 위키로 구조화되면 팀 내 공유 자산이 됨.

---

## Level 1: Schedule — 일일 인증 뉴스 자동화

### Q1-1: 에이전트에게 맡긴 작업

**최종 구현: WTO TBT 일일 브리핑 자동화**
- **입력**: WTO ePing 공개 API (`https://eping.wto.org/api/v1/notifications/search`) + WTO 공식 API 이중화
- **작업**: 전날 신규 TBT 통보문 수집 → 한국 수출 관련성 점수 산정 (HIGH_IMPACT_COUNTRIES +3, HIGH_IMPACT_SECTORS +2) → 상위 5건 추출
- **출력**: Jekyll 포스트 `_posts/YYYY-MM-DD-wto-tbt-briefing.md` 자동 생성 → GitHub Pages 게시
- **트리거**: GitHub Actions cron `0 0 * * 1-5` (평일 매일 오전 9시 KST), 수동 실행 버튼 지원
- **파일**: `scripts/wto_tbt_briefing.py`, `.github/workflows/wto_tbt_daily.yml`

**초기 시도 (반자동화)**: C2P 이메일(.eml) 업로드 기반 팀원 배정 이메일 초안 자동화
- 구현 완료 (`scripts/process_newsletter.py`, `output/` 폴더), 하지만 매번 수동 업로드 필요 → "반자동화"로 판정
- 진정한 자율 루틴이 아님을 인식 → WTO TBT 완전 자동화로 전환

### Q1-2: 자율 태스크 설계에서 배운 교훈
1. **"자동화"와 "반자동화"의 차이** — 사람이 트리거를 눌러야 시작되면 자율 루틴이 아님. 진정한 자율 태스크는 사람의 개입 없이 스케줄대로 실행되어야 함.
2. **공개 API 우선 전략** — 사내 시스템(Dooray) 의존보다 공개 데이터 소스(WTO ePing)를 활용하는 것이 구현 속도와 안정성 면에서 유리. C2P 유료 서비스의 핵심 가치(WTO 미통보 각국 관보 커버)는 향후 Dooray API로 보완 예정.
3. **에러 처리와 graceful degradation** — API가 실패해도 "0건 수집" 포스트를 생성하여 파이프라인이 끊기지 않도록 설계. 빈 결과도 "정상 실행" 기록으로 남음.
4. **보안 설계** — API 토큰·민감 이메일은 .gitignore + 환경변수로 격리. 자동화 코드에 자격증명을 하드코딩하면 안 된다는 원칙을 실제 구현에서 적용.

### Q1-3: 유용한 자율 태스크의 핵심 요소
1. **완전한 트리거 자율성**: 사람이 시작 버튼을 누르지 않아도 실행됨 (cron 스케줄)
2. **명확한 입출력 경계**: 입력(공개 API) → 처리(점수 기반 선별) → 출력(게시 포스트)이 코드로 완전히 정의됨
3. **반복 가능성과 멱등성**: 같은 날 여러 번 실행해도 같은 파일을 덮어쓰고, 변경이 없으면 커밋하지 않음
4. **실패 안전성**: API 오류 시 빈 포스트 생성 → 파이프라인 중단 없음, 다음 날 자동 재시도
5. **도메인 관련성**: 단순 시연용이 아니라 실제 업무(TBT 규제 모니터링)와 직결되어 출력 결과에 실용 가치가 있음

---

## Level 2: Persistent Agent (보너스 +10)

### 개요
- Hermes Agent (https://github.com/nousresearch/hermes-agent) Docker로 설치
- 지속 실행되는 자율 에이전트 구축

### Q2-1: 에이전트에게 맡긴 작업
- (구현 후 작성 예정)

### Q2-2: Persistent Agent에서 배운 교훈
- (구현 후 작성 예정)

### Q2-3: Persistent Agent를 유용하게 만드는 핵심 요소
- (구현 후 작성 예정)

### 구현 계획
1. Docker 환경에서 Hermes Agent 설치 (공식 가이드: https://hermes-agent.nousresearch.com/docs/user-guide/docker)
2. TBT 뉴스 모니터링 또는 뉴스레터 자동화 태스크 할당
3. 장기 실행 결과 관찰 및 기록

---

## Level 3: Company-Relevant Sandbox (보너스 +10)

### 선택한 워크플로우
**TBT 심층분석보고서 자동 초안 생성 파이프라인**
- 실제 업무: WTO TBT 통보문/해외 관보 → 번역 → 6장 구조 보고서 초안 작성 → 내부 검토 → knowtbt.kr 공개 게시
- 현황: 주당 7-8건 처리, 건당 약 2일 소요 (번역 0.5일 + 구조화 0.5일 + 초안 1일)
- 샌드박스: 규제 원문 PDF 직접 입력 → Claude API 번역+구조 추출 → KTL master template 서식 초안 자동 생성
- 실제 업무와 동일한 입력 방식: `python3 scripts/tbt_report_pipeline.py VNM408.pdf`

### 산출물
- **(a) 작동하는 샌드박스 에이전트**: `scripts/tbt_report_pipeline.py`
  - **입력**: 규제 원문 PDF 파일 (베트남어, 영어 등 다국어 지원)
  - **처리**: Claude API가 PDF를 직접 읽어 번역 + KTL 서식 필드 구조 추출
  - **출력**: KTL 6장 보고서 초안 마크다운 → `output/sandbox-reports/`
  - API key 없는 환경에서는 빈 템플릿 구조 생성 (graceful degradation)
  - 테스트 파일: `sources/VNM408.pdf` (베트남 내무부 제품 위험도 분류 규정)
- **(b) 1페이지 제안서**: `docs/level3-proposal.md` (수출지원센터장 수신)
- **(c) 실제 데이터 반영 시 변화**: 아래 reflection 참고

### Q3-1: 이 워크플로우를 선택한 이유
TBT 심층분석보고서는 KTL 수출지원센터의 핵심 대국민 서비스이자 주당 7-8건씩 생산하는 고반복 작업이다. 현재 ChatGPT를 활용하지만 번역→서식 적용→초안 작성까지 여전히 2일이 소요된다. 이 워크플로우를 선택한 이유:

1. **반복성**: 동일한 6장 구조(규제 개요→세부내용→인증정보→주요국 비교→애로사항→대응방안)가 매번 반복되어 자동화 효율이 극대화됨
2. **공개 데이터 가용성**: WTO 통보문 및 각국 관보 PDF는 공개 자료 → 내부 데이터 없이 완전 재현 가능
3. **측정 가능한 임팩트**: 처리 건수·소요 시간이 수치로 측정되어 자동화 효과를 입증하기 쉬움
4. **Human-in-the-loop 자연스러운 유지**: 공공기관 보고서 특성상 AI 초안 → 담당자 검토·승인 구조가 자연스럽게 내포됨

### Q3-2: 매니저 첫 번째 반대 의견 및 답변
**예상 반대**: "AI가 생성한 보고서가 원문 근거 없이 잘못된 인증정보·기관명을 생성하면 대국민 서비스 신뢰성이 훼손된다. 책임 소재도 불명확하다."

**답변**: 
- 파이프라인은 AI 완성본이 아니라 **검토 가능한 초안**을 생성한다. 원문 근거가 없는 항목은 "원문상 확인되지 않음" / "공식자료 확인 필요"로 자동 표시되어 담당자가 어디를 검토해야 하는지 즉시 식별 가능하다.
- 현재도 ChatGPT 초안을 담당자가 검토·수정하는 동일 구조로 운영 중이며, 책임 소재는 최종 승인 담당자에게 있다. 자동화는 이 책임 구조를 바꾸지 않는다.
- 시범 운영(4주) 동안 수동 작성 보고서와 자동 초안을 병행하여 오류율을 측정하고, 통과 기준을 수립한 후 확대 적용한다.

### Reflection: 실제 사내 데이터 적용 시 달라지는 것
1. **입력 확장**: WTO 미통보 규제(C2P가 각국 관보에서 수집하는 내용)까지 커버 가능 → 현재 샌드박스가 놓치는 80%의 규제를 포착
2. **서식 완성도**: 과거 보고서 데이터로 few-shot 학습 시 AI가 KTL 문체·수준에 맞는 초안 생성 가능
3. **knowtbt.kr 직접 연동**: 초안 승인 후 자동 업로드까지 파이프라인 확장 가능 (IT 시스템 연동 필요)
4. **리스크**: 내부 보고서 데이터를 외부 API에 전송 시 보안 검토 필요 → Phase 1은 공개 데이터만 사용하여 회피

---

## 자기 인터뷰 전문

### AI 활용 TOP 3
1. **TBT 규제 문서 번역·분석·보고서 작성** — 글로벌 관보 다국어 원문 번역 후 보고서 초안 자동 생성
2. **홈페이지/코딩 작업** — AI 없이는 불가능한 수준의 개발 작업 수행 (이 사이트 포함)
3. **일일 글로벌 인증·규제 뉴스레터 선별 및 요약**

### TBT 보고서 작업 흐름
- 관보 원문 → 번역 → 보고서 형식에 맞는 정보 수집 요청
- ChatGPT 프로젝트에 참고파일 + 작업 흐름 학습 → "프로젝트 flow대로 작성해줘" 한 마디로 실행
- **현재 개선 중**: AI가 "원문에 따르면", "검토 필요" 등 작성자용 코멘트를 보고서 본문에 삽입하는 문제

### 뉴스레터 5단계 Flow
1. C2P 이메일 전체 → AI에 붙여넣기
2. AI가 수출 파급력·규제 파급력·주제 중복성 기준으로 우선순위 선별
3. 담당자가 세부 내용 직접 검토 후 적합성 판단
4. 팀원 2명에게 뉴스 1개씩 요약 요청
5. 팀원 요약본 → AI 최종 검토 → 대국민 공개 사이트 업로드

### AI 강점과 한계
- **강점**: 요약, 보고서 초안 작성, 정보 구조화
- **한계**: 인간 문체 재현 어려움, 룰베이스 특성으로 유연한 사고 부족

### 미래 계획
- KAIST 석사: AI 분석 능력 활용한 논문 작성, 수업 보조도구 활용
