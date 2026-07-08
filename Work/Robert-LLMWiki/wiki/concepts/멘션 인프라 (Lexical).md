---
유형: 개념
생성일: 2026-07-03
갱신일: 2026-07-03
출처:
  - "[[2026-07-03]]"
---

# 멘션 인프라 (Lexical)

MAKi의 **사람·일감(todo/note) 멘션**은 웹(Lexical)에서 이미 완성돼 있고, [[모바일 컴포저 멘션]]과 [[웹 assign 일감 언급]] 둘 다 이 인프라 위에서 만든다. 지식 복리의 공통 뿌리 페이지.

## 핵심 구성요소 (MAKi 리포지토리)
- **MentionNode** — `apps/front/components/lexical/mention/MentionNode.ts`
  - `__mentionCategory`로 종류 구분: `"Members"`(사람) / `"Data Bucket"`(일감).
  - 일감은 `__mentionBadge`(`Todo`/`Note`) + `__mentionStatus` + `__mentionDisplay`(`inline`/`basic`)로 칩 렌더.
- **MentionsPlugin** — `.../mention/MentionsPlugin.tsx`
  - `@` 트리거 타입어헤드. 선택 시 `insertMentionNode()`로 노드 삽입.
  - **WebView 브릿지**: `postMessage {type:"MENTION_DATA", payload:{query,suggestions,isOpen}}` (→네이티브), `MENTION_SELECT {index}` (←네이티브).
- **제안 소스 훅**
  - `apps/front/hooks/use-conversation-mentions.ts` — 대화별 멤버 + TODO/NOTE 로드 조율.
  - `.../mention/useMentionSuggestions.ts` — 로컬 필터 + Cmd+S 서버 검색.
  - 사람: `packages/graphql-client/src/workspace/hooks.ts` → `useWorkspaceMembers`.
  - 일감: `packages/graphql-client/src/bucket-item/hooks.ts` → `useBucketItems`, `useSearchMyBucketItemsWithSemantic`(의미론적+키워드).
- **변환 유틸** — `.../mention/bucketUtils.ts` → `toBucketSuggestion` (BucketItem → MentionSuggestion).
- **칩 렌더** — `.../mention/component/BucketInlineLexical.tsx`, `BucketBasicLexical.tsx`, 사람은 `MentionUserLexical.tsx`.

## "2번 느낌" / "forward 느낌"의 정체
- **2번 느낌**(모바일 목표): 웹에서 `@` 입력 시 뜨는 멤버+최근 TODO/NOTE 멘션 메뉴 경험. 모바일엔 아직 없음.
- **forward 느낌**(웹 목표): `apps/front/components/forward/ForwardPanel.tsx`의 검색→선택→미리보기 UX. `buildBucketMentionForwardContent()`가 일감을 Lexical JSON 멘션으로 만들어 전송.

## 관련
- [[모바일 컴포저 멘션]]
- [[웹 assign 일감 언급]]
