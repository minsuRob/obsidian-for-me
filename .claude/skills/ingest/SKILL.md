---
name: ingest
description: Markhub LLM Wiki에 원본(raw) 문서를 흡수한다. "정리해줘", "위키에 반영해줘", "인제스트" 요청이나 raw/에 새 메모·회의록을 던졌을 때 사용. 원본은 수정하지 않고 wiki 페이지를 생성·갱신하고 INDEX·LOG를 갱신한다.
---

# /ingest — 원본을 위키로 흡수

Markhub LLM Wiki( `Work/Markhub-LLMWiki/` )의 인제스트 파이프라인.

## 먼저 할 일
1. `Work/Markhub-LLMWiki/CLAUDE.md`(스키마)를 읽고 관례를 따른다.

## 대상 결정
- 인자로 파일 경로가 주어지면 그 파일을 대상으로 한다.
- 없으면 `Work/Markhub-LLMWiki/raw/`(하위 `daily/` 포함)에서 아직 위키에 반영 안 된 것으로 보이는 파일을 찾아 사용자에게 어떤 걸 흡수할지 확인한다.

## 절차 (CLAUDE.md의 Ingest 워크플로우)
1. 대상 raw 파일을 읽는다. **원본은 절대 수정하지 않는다.**
2. 핵심 발견을 한두 줄로 사용자에게 짚어준다.
3. 관련 `wiki/` 페이지를 생성하거나 갱신한다 (유형: 일감/회의/개념/사람). 프론트매터·본문 구조·`갱신일`을 스키마대로.
4. 관련 페이지끼리 `[[링크]]`를 **양방향**으로 연결한다.
5. `Work/Markhub-LLMWiki/INDEX.md`에 페이지를 등록/갱신한다.
6. `Work/Markhub-LLMWiki/LOG.md` 맨 아래에 `## [YYYY-MM-DD] ingest | 요약` 형식으로 기록을 추가한다.

## 원칙
- 지어내지 않는다. 원본에 없는 사실은 "확인 필요"로 남긴다.
- 한 번에 여러 페이지를 건드릴 수 있다. 링크가 실제 파일명과 일치하는지 확인한다.
