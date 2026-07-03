---
유형: 일감
상태: 진행중
우선순위: 최우선
생성일: 2026-07-03
갱신일: 2026-07-03
출처:
  - "[[2026-07-03]]"
---

# 웹 assign 일감 언급 (Lexical)

## 배경
웹 assign에서 **todo/note 일감 언급**을 추가한다. 목표 경험은 "forward 느낌"(= `ForwardPanel`의 검색→선택→미리보기). **Lexical로 개발**.

- 대상 파일: `apps/front/components/message/adaptive/container/MessageContainer.web.tsx`
- 공유 뿌리: [[멘션 인프라 (Lexical)]]

## 현황
- 웹 Lexical 멘션 인프라는 **대부분 이미 완성**돼 있음:
  - `@` 멘션 메뉴에 이미 bucketSuggestions(TODO/NOTE) 포함, 칩 렌더(`BucketInlineLexical`/`BucketBasicLexical`)와 Cmd+S 서버 검색까지 동작.
  - Forward 흐름: `ForwardPanel.tsx` → `buildBucketMentionForwardContent()`가 일감을 Lexical JSON 멘션으로 만들어 `createMessage`.
  - `MessageContainer.web.tsx`는 상태관리 + 에디터 마운트 지점. assign 훅: `useCreateBucketItem`, `useAssignBucketItemUser`.
- **없는 것**: 에디터 안에서 "forward처럼" 일감을 골라 넣는 UX, 그리고 **멘션 선택 후 자동 할당** 연결.

## 구현 방향 (결정 ✅ 2026-07-03: /assign 슬래시 커맨드)
- **채택: A. `/assign` 슬래시 커맨드** — 기존 `SlashPrefixPlugin` 활용. `/assign` 입력 → ForwardPanel류 모달(검색·선택·미리보기) → 선택 시 MentionNode 삽입 + `useAssignBucketItemUser` 자동 할당.
- 반려: B(`/` 메뉴 액션), C(`@` 멘션 강화).
- 이유: "forward 느낌"을 가장 직접적으로 재현하고, 기존 SlashPrefix·ForwardPanel 자산을 최대 재사용.

## 만들 조각
- 삽입 후 액션 훅 연결: `handleMentionSelect` → `useAssignBucketItemUser` (선택 시 실제 할당까지).
- 필요 시 MentionNode에 필드 추가(assignee/deadline) — 현재 badge/status로도 대부분 커버.

## 타임라인
- 2026-07-03: MAKi 코드 조사. 멘션/포워드 인프라 대부분 존재, "에디터 내 forward UX + 선택 후 자동 할당"만 신규로 확인 (출처: [[2026-07-03]]).
- 2026-07-03: **`/assign` 슬래시 커맨드 방식 채택** 결정.

## 관련
- [[멘션 인프라 (Lexical)]]
- [[모바일 컴포저 멘션]]
