# inbox/

C2P 뉴스레터 .eml 파일을 이 폴더에 저장하세요.

## 사용 방법

1. Dooray에서 C2P Alert 메일 열기
2. 메일 저장 → `.eml` 형식으로 다운로드
3. 이 폴더(`inbox/`)에 업로드 (파일명 자유)
4. 터미널에서 실행:
   ```
   python3 scripts/process_newsletter.py inbox/파일명.eml
   ```
5. `_posts/YYYY-MM-DD-c2p-news.md` 초안 확인 후 수정
6. git push → GitHub Pages에 자동 게시

## 자동 실행 (파일명 지정 없이)
```
python3 scripts/process_newsletter.py
```
inbox/ 폴더의 가장 최신 .eml 파일을 자동으로 처리합니다.

## 선별 기준 (AI 자동 적용)
- 수출 파급력: 한국 주요 수출국(중국, EU, 베트남, 인도네시아 등) 관련성
- 규제 파급력: 배터리, 디스플레이, 섬유, 화장품 등 한국 수출 주력 품목
- 상태 우선순위: In force > Approved > Proposed

> ⚠️ .eml 파일은 .gitignore에 등록되어 있어 Git에 올라가지 않습니다.
