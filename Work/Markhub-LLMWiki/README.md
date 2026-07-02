# Markhub-LLMWiki

카파시(Andrej Karpathy)식 **LLM Wiki**를 개인 업무에 맞춰 최대한 직관적으로 구성한 볼트입니다.
핵심 원칙: **원본(raw)은 절대 수정하지 않고, 위키(wiki)만 계속 성장한다.**

## 🔁 전체 흐름 (3-Layer)

```
00_Inbox  ──/ingest──▶  10_Wiki  ◀──링크──  20_Tracking (daily/weekly/tasks)
 (raw 투척)            (정제 지식)          (매일의 업무 사이클)
```

1. **던진다** → 회의록·메모·아이디어를 `00_Inbox`에 아무렇게나 넣는다.
2. **정제한다** → `/ingest` 실행 → AI가 읽고 `10_Wiki`에 개념/인물/프로젝트 페이지를 만들고 서로 **링크**로 엮는다. (원본은 그대로)
3. **트래킹한다** → 매일 `/daily`, 매주 `/weekly`로 보고를 만들고, 일감은 `tasks`로 관리한다.
4. **복리** → 위키가 쌓일수록 AI가 과거 맥락을 종합해 더 똑똑하게 답한다.

## 📁 폴더

| 폴더 | 용도 |
|---|---|
| `00_Inbox/` | 원본 raw 투척 (미정제, 미수정) |
| `10_Wiki/concepts` `entities` `projects` | AI가 정제한 지식 페이지 |
| `20_Tracking/daily` | 일일보고 (스탠드업: 어제/오늘/블로커) |
| `20_Tracking/weekly` | 주간회의 (데일리 취합 + KPT 회고) |
| `20_Tracking/tasks` | 일감 노트 (우선순위·상태) |
| `90_Reference/` | 외부 링크·자료 출처 |
| `_templates/` | Templater 템플릿 |

## ⚡ Claude 스킬

| 명령 | 하는 일 |
|---|---|
| `/daily` | 오늘 일일보고 생성 → 어제 "오늘 할 일"을 "어제 한 일"로 이월, 진행중 일감·블로커 자동 반영 |
| `/weekly` | 이번 주차 daily들을 읽어 성과/계획/리스크 + KPT 초안 자동 합성 |
| `/ingest` | `00_Inbox` 원본을 `10_Wiki` 페이지로 변환 + 양방향 링크 (원본 미수정) |

## 📊 대시보드 (Bases)

- `20_Tracking/일감보드.base` — 우선순위·상태별 일감 현황
- `20_Tracking/데일리현황.base` — 일일보고 목록 / 집중시간 / 블로커
- `10_Wiki/위키인덱스.base` — 위키 전체를 유형별로 탐색

`.base` 파일을 클릭하면 표 형태로 열립니다. (렌더 안 되면 Obsidian을 최신 버전으로 업데이트)

## 🚀 매일 쓰는 법

1. 아침: `/daily` → 오늘 보고 초안 생성 → 오늘 할 일만 다듬기
2. 수시: 새 이슈는 `tasks`에 노트로, 회의록은 `00_Inbox`에 → `/ingest`
3. 주간회의 전: `/weekly` → 한 주 자동 요약 + KPT 초안 확인

> 기존 `Work/todos/핵심요소..md`의 우선순위 일감은 `20_Tracking/tasks/`로 옮겨두었습니다.
