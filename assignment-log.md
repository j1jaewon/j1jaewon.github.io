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
- 예상치 못한 발견: 피싱성 메시지에 속아 AI 채팅창에 토큰을 입력한 적이 있었는데, Claude 메모리에 그대로 남아있는 걸 확인했다. 즉시 삭제해서 해결했지만, 대화 이력을 직접 들여다보기 전까지는 몰랐을 것이다.

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

1. **툴이 바뀌어도 지식은 남는다** — 항상 AI 툴이 교체될 때마다 맥락을 어떻게 이어갈지가 고민이었다. Claude, ChatGPT, 자기 인터뷰 대화를 하나의 위키로 통합하고 나니, 어떤 툴로 갈아타더라도 내 지식 베이스는 유지된다는 안도감이 생겼다. 위키를 만들기 전까지는 이 불안감 자체를 의식하지 못했다.

2. **대화 이력에 무엇이 남아있는지 아무도 모른다** — 인터뷰 대화를 정리하다가 예전에 AI 채팅창에 입력했던 토큰이 Claude 메모리에 그대로 남아있는 걸 발견했다. 즉시 삭제해서 해결했지만, 이 과정이 없었다면 영원히 몰랐을 것이다. 위키 구축은 단순한 지식 정리가 아니라 보안 감사이기도 했다.

3. **아직 위키는 시작 단계다** — 현재 위키는 단편적인 내용이 많다. 이번 과제를 계기로 구조를 잡았지만, 실제로 쓸모 있는 위키가 되려면 업무 경험이 쌓일수록 계속 채워나가야 한다. 지금은 뼈대를 세운 것에 가깝다.

4. **5단계 뉴스레터 워크플로우** — 당연하게 해오던 흐름을 글로 써보고 나서야, 이게 의식적으로 설계된 구조였다는 걸 처음 알았다. 선별 기준(수출 파급력·규제 파급력·중복성)을 내가 직접 정의하고, 팀 분업까지 AI로 조율하는 체계가 이미 완성되어 있었던 것.

5. **Human-in-the-loop 일관성** — 모든 AI 활용이 "AI 초안 → 인간 검토 → 수정"의 구조로 일관됨. 공공기관 보고서의 신뢰성 요건에 맞는 원칙인데, 의도한 게 아니라 자연스럽게 형성된 습관이었다.

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
- 완성하고 나서야 깨달았다. 내가 매일 파일을 올려야 실행되는 구조라면, 자율 루틴이 아니라 내가 트리거인 것이다. → WTO TBT 완전 자동화로 전환

### Q1-2: 자율 태스크 설계에서 배운 교훈
1. **"자동화"와 "반자동화"의 차이** — 처음엔 C2P 이메일 파이프라인을 완성했을 때 자동화라고 생각했다. 그런데 매일 아침 내가 파일을 업로드해야 돌아가는 구조였다. 자율 루틴의 핵심은 내가 자리를 비워도 실행된다는 것이다.
2. **공개 API 우선 전략** — 사내 시스템(Dooray) 의존보다 공개 데이터 소스(WTO ePing)를 활용하는 것이 구현 속도와 안정성 면에서 유리. C2P 유료 서비스의 핵심 가치(WTO 미통보 각국 관보 커버)는 향후 Dooray API로 보완 예정.
3. **파이프라인이 살아있다는 것** — Actions가 처음 실패했을 때 당황했지만, 빈 결과라도 포스트가 올라오는 걸 보고 안도했다. "0건 수집"이라는 출력이 "정상 실행"의 증거였다. 오류로 멈추는 것과 빈 결과를 내는 것은 다르다.
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

### 구현 환경
- **플랫폼**: Windows 11, Docker Desktop + PowerShell
- **에이전트**: NousResearch Hermes Agent (`nousresearch/hermes-agent` Docker 이미지)
- **모델**: Claude Opus 4.6 (Anthropic provider)
- **실행 명령어**:
  ```powershell
  docker run -it -v ${HOME}/.hermes:/root/.hermes -e ANTHROPIC_API_KEY=sk-ant-... nousresearch/hermes-agent
  ```

### Q2-1: 에이전트에게 맡긴 작업

**태스크**: WTO TBT/SPS 최신 통보문 모니터링 및 한국어 요약

```
WTO ePing (https://eping.wto.org) API를 사용해서 오늘 날짜 기준 최신 TBT/SPS 통보문 상위 5건을 가져와서 다음 형식으로 한국어로 요약해줘:
- 통보번호, 통보국, 유형, 대상 제품 (HS코드 포함), 주요 내용, 의견제출 마감일
한국 수출 기업에 영향이 큰 규제 변경사항 위주로 정렬해줘.
```

**실행 결과 (2026-06-10)**:
- WTO ePing API에서 당일 통보문 5건 성공적으로 수집
- 한국어 요약 자동 생성:
  1. G/SPS/N/EU/956 — EU 동물사료용 향미화합물 승인 갱신
  2. G/SPS/N/EU/957 — EU 제3국산 식품·사료 공식 관리 강화 (아르헨티나 땅콩 아플라톡신, 인도 커민씨 농약 검사빈도 상향 등)
  3. G/SPS/N/KOR/846 — 한국 꿀벌 사료용 꿀·벌화분 동물검역 추가 (의견제출 마감 2026-08-09)
  4. G/TBT/N/BHR/704/Rev.1 — GCC 7개국 잼·젤리·마멀레이드 기술규정
  5. G/TBT/N/KWT/683/Rev.1 — GCC 쿠웨이트 측 동일 통보

### Q2-2: Persistent Agent에서 배운 교훈

1. **채팅창과 다를 게 없었다** — WTO 통보문 요약 태스크를 실행하고 결과를 받은 순간, 이건 그냥 ChatGPT에 물어보는 것과 다를 바 없다는 걸 깨달았다. Hermes Agent의 진짜 가치는 파일 읽기·쓰기와 자율적 멀티스텝 실행인데, 내 첫 태스크는 그 어느 것도 활용하지 않은 단순 질의응답이었다. 좋은 도구를 갖춰놓고 라면만 끓여먹는 기분이었다.

2. **처음으로 터미널에서 작업했다** — 항상 채팅창이나 Claude Cowork 같은 UI 환경에서만 작업해왔는데, 이번에 처음으로 API 크레딧을 직접 결제하고 Docker를 띄우고 터미널에서 에이전트를 실행했다. 생각보다 별거 아니었다. 그리고 그 순간 조금 멋있었다.

3. **이제 중요한 건 아이디어다** — Claude Cowork, Codex, Hermes Agent — 도구는 충분히 준비되어 있다. 커틀러리도 있고 식재료도 있다. 남은 건 무엇을 어떻게 만들지다. 다음 단계는 더 나은 도구를 찾는 게 아니라, 도구로 해결할 진짜 문제를 정의하는 것이다.

4. **크레딧 비용의 현실** — 첫 실행은 "credit balance too low" 오류로 차단됐다. API 기반 에이전트는 실행 전에 과금 체계를 반드시 확인해야 한다. 한 번 실행 비용은 약 $0.05~0.07(Opus 기준)으로 저렴하지만, 상시 구동 에이전트는 누적 비용 설계가 필요하다.

### Q2-3: Persistent Agent를 유용하게 만드는 핵심 요소

1. **명확한 태스크 범위** — 에이전트에게 "무엇이든 해줘"가 아니라 "WTO ePing → 상위 5건 → 한국어 요약"처럼 입력·처리·출력이 명확한 태스크를 주어야 결과 품질이 일관됨.

2. **공개 API 활용** — 내부 시스템 없이도 공개 데이터 소스(WTO ePing API)로 실용적 결과물 생성 가능. 인증/권한 문제 없이 즉시 실행 가능한 소스를 우선 활용.

3. **지속성 활용 설계** — 매번 같은 태스크라면 에이전트 메모리에 컨텍스트를 저장해두고 "오늘 통보문 요약해줘"처럼 짧은 명령어만으로 재사용할 수 있도록 초기 세팅에 투자.

4. **Human-in-the-loop 검증 포인트** — 에이전트 출력을 그대로 사용하지 않고, 의견제출 마감일·기관명·HS코드 같은 핵심 필드는 원문 대조 검증 단계를 명시적으로 유지함. 자동화는 초안 생성까지, 최종 확인은 사람이.

5. **비용 상한 설정** — 상시 구동 에이전트는 Anthropic 콘솔에서 월별 지출 한도를 설정하여 예상치 못한 과금 방지.

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

이 제안서를 실제로 제출할 의향이 있다. Phase 1은 공개 데이터만 사용하고 추가 시스템이 필요 없어, IT 승인 없이도 내일 당장 시작할 수 있기 때문이다.

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
