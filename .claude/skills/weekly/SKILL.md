---
name: weekly
description: Markhub-LLMWiki에서 이번 주 일일보고와 wiki 변경을 종합해 주간회의 자료를 생성한다. 사용자가 "/weekly", "주간회의", "주간보고", "위클리"라고 하면 사용.
---

# /weekly — 주간회의 자료 자동 생성

기준 경로: `Work/Markhub-LLMWiki/` (이하 `WIKI/`). 대상 산출물: `WIKI/reports/weekly/<YYYY-Www>.md` (ISO 주차, 예: 2026-W27).

## 처리 순서

### 1. 이번 주 범위 수집
- 이번 주(월~일) 날짜 범위와 ISO 주차를 계산한다.
- 이번 주 `WIKI/reports/daily/*.md` 일일보고들.
- 이번 주 `최종수정`이 이번 주인 `WIKI/wiki/**` 문서들.
- `git -C <vault> log --since="7 days ago" --stat`으로 주간 변경 파일 교차 확인 가능.

### 2. 보고서 작성
`WIKI/reports/weekly/<YYYY-Www>.md`에 작성(있으면 갱신):
```markdown
---
유형: weekly
주차: <YYYY-Www>
기간: <시작> ~ <끝>
담당: 나
최종수정: <오늘>
태그: [주간회의]
---

# 주간회의 <YYYY-Www> (<시작>~<끝>)

## 📈 진행 상황 (Feature별)
| Feature | 상태 | 우선순위 | 이번 주 변화 |
|---|---|---|---|

## ✅ 결정 사항
- (이번 주 확정된 것, 관련 [[문서]])

## 🎯 다음 주 액션 아이템
- [ ] (담당) 할 일

## 🔗 관련 회의
- [[이번 주 회의 요약들]]
```

### 3. 규칙
- Feature별 상태/우선순위는 `WIKI/wiki/features/*` frontmatter에서 가져온다.
- 결정 사항은 각 문서 `## 결정 사항`과 meetings 요약에서 취합.
- 액션 아이템은 열린 이슈·미완료 액션에서 우선순위순으로.
- 링크는 `[[ ]]`로. 지어내지 않는다. 완료 후 경로 + 핵심 요약 보고.
