# Markhub-LLMWiki

카파시(Andrej Karpathy)의 **LLM Wiki** 개념을 내 업무에 붙인 개인용 세컨드 브레인.
핵심 원칙: **원본은 절대 수정하지 않는다. AI가 읽고 wiki만 유기적으로 키운다.** (Knowledge Compounding)

## 🔁 데이터 흐름 (3-Layer)

```
 [inbox]  던진다        [raw]  아카이브        [wiki]  자란다
 ─────────           ─────────           ─────────
 회의록/메모  ──/ingest──▶  원본 보존   +   Feature/Vendor/Meeting 최신화
 (막 던짐)     클로드가        Processed:true      섹션·표만 정밀 수정 + [[링크]] 연결
              쪼개서 배달
                                    │
                         /daily ▶ reports/daily/  (오늘 한 일·막힌 일·내일 할 일)
                         /weekly ▶ reports/weekly/ (진행상황·결정·다음주 액션)
                         /lint  ▶ 채팅 리포트      (미처리·끊긴링크·오래된 문서)
```

## 📁 폴더

| 폴더 | 역할 | 누가 쓰나 |
|---|---|---|
| `inbox/` | 회의록·메모를 **막 던지는 곳** (섞여도 OK) | 나 |
| `raw/` | 처리 끝난 원본 아카이브 (`/ingest`가 이동) | 클로드 |
| `wiki/features/` | 기능/작업별 지식 (`Feature-*`) | 클로드 |
| `wiki/vendors/` | 벤더/계약 (`Vendor-*`, 수수료 표) | 클로드 |
| `wiki/meetings/` | 정제된 회의 요약본 | 클로드 |
| `reports/daily/` | 일일보고 | `/daily` |
| `reports/weekly/` | 주간회의 자료 | `/weekly` |
| `Tasks.base` | 업무 트래킹 보드 (상태·우선순위) | Obsidian Bases |
| `Templates/` | 새 문서 뼈대 (Templater) | 자동 |

## 🚀 매일 쓰는 법

1. **던진다** — 회의 끝나면 AI 요약을 `inbox/`에 새 노트로 붙여넣기 (Templater가 회의록 뼈대 자동 삽입).
2. **정리한다** — 클로드에게 **"/ingest"**. inbox가 wiki로 흡수되고 원본은 `raw/`로 이동.
3. **보고한다** — 하루 끝 **"/daily"**, 금요일 **"/weekly"**.
4. **점검한다** — 가끔 **"/lint"** 로 끊긴 링크·미처리·오래된 문서 확인.

## 🧩 스킬 (클로드에게 말하면 실행)

| 명령 | 하는 일 |
|---|---|
| `/ingest` | inbox 원본을 wiki에 정제 반영 + 원본 아카이브 |
| `/daily` | 오늘 변경분으로 일일보고 생성 |
| `/weekly` | 이번 주 종합해 주간회의 자료 생성 |
| `/lint` | vault 건강 검진 (수정 안 함, 리포트만) |

## 🏷 Frontmatter 규약

```yaml
유형: feature | task | vendor | meeting | daily | weekly
상태: 대기 | 진행중 | 완료 | 보류
우선순위: 높음 | 중간 | 낮음
관련: ["[[관련문서]]"]
최종수정: YYYY-MM-DD
```

## 💡 처음이라면
`inbox/2026-07-02_toss.md`(토스페이 회의록 샘플)가 이미 던져져 있습니다.
클로드에게 **"/ingest"** 라고 해보세요 — 일정과 수수료가 실제로 wiki에 반영되는 걸 볼 수 있습니다.
