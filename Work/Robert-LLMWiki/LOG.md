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

## [2026-07-03] query | 3개 과제 구현 방향 결정
- [[모바일 컴포저 멘션]]: 옵션 B 완전 네이티브(iOS SwiftUI + Android Compose) 채택.
- [[웹 assign 일감 언급]]: /assign 슬래시 커맨드 방식 채택.
- [[Mac 빌드 워크트리 유일성 검증]]: 지금은 위키 기록만, 실측/코드변경 보류.

## [2026-07-03] query | MAKi MCP 메시지 포맷 차이 정리
- Cursor 전송본과 Codex 전송본의 렌더링 차이를 관찰하고, raw/daily와 wiki/concepts에 각각 반영했다.
- 권장 포맷은 `제목 + 번호 목록 + 하위 bullet` 구조.

## [2026-07-08] ingest | 리서치 갈래 신설 + 클로드 활용 리서치 개설
- raw/research/, wiki/research/ 구조 신설 (CLAUDE.md·INDEX 반영)
- 주제 "클로드 활용 / deep dive" 폴더(_sources.md + instagram/youtube/web)와 [[클로드 활용 리서치]] 스켈레톤 생성. 데이터 수집 대기.

## [2026-07-08] ingest | AI 시대 개발자 성장 (카파시 1000x) 자료 수집 + 정제
- 웹에서 7개 소스 수집 → raw/research/AI시대-개발자-성장/ (youtube 1 + web 6, instagram 없음)
- 1차(Sequoia Ascent transcript)·해설·비판(주니어 파이프라인/comprehension debt) 균형 확보
- [[AI 시대 개발자 성장]] 정제 페이지 생성, [[클로드 활용 리서치]]와 양방향 링크, INDEX 등록
- 예외 기록: 사용자 지시로 AI가 raw에 수집 대행(기존 raw 미수정, 새 주제 폴더에만 추가)
