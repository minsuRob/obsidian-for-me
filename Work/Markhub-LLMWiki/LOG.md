# LOG — 작업 이력

> append-only. AI는 작업할 때마다 맨 아래에 한 줄 형식으로 기록을 추가합니다.
> 형식: `## [YYYY-MM-DD] {ingest|query|daily|weekly|lint} | {요약}`

## [2026-07-02] ingest | 초기 구축 + 핵심요소 일감 시드
- LLM Wiki 3층 구조 생성 (CLAUDE.md 스키마, INDEX, LOG, raw/, wiki/, templates/).
- `Work/Markhub/핵심요소..md`를 첫 원본으로 흡수 → 일감 페이지 4개 생성:
  [[Unread 이슈]], [[Electron 버전 통일]], [[채팅창 Ctrl+Z 미동작]], [[이모지 Detail View]].

## [2026-07-03] ingest | MAKi 3개 과제 (모바일 멘션 / 웹 assign / Mac 빌드 검증)
- 07-02 데일리 삭제, [[2026-07-03]] 데일리 생성.
- MAKi 코드(`MobileMarkComposer.tsx`, `MessageContainer.web.tsx`, `staging-deploy.yml` + 원격 스크립트) 정독.
- 개념 1 + 일감 3 생성: [[멘션 인프라 (Lexical)]], [[모바일 컴포저 멘션]], [[웹 assign 일감 언급]], [[Mac 빌드 워크트리 유일성 검증]].
- 검증 발견: electron/ios는 런별 워크트리+락으로 견고, frontend validate는 공유 워크트리+무락 위험.
