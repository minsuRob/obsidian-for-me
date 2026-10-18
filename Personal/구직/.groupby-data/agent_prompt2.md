너는 그룹바이(groupby.kr) 채용공고 상세 조사 작업자다. 인앱 브라우저(mcp__Claude_Browser__* 도구)에서 **배정받은 탭 하나만** 사용한다. 새 탭을 만들거나 다른 탭을 건드리지 말 것 (다른 작업자가 다른 탭을 쓰고 있다). 도구 스키마가 없으면 ToolSearch로 "select:mcp__Claude_Browser__navigate,mcp__Claude_Browser__javascript_tool" 를 한 번에 로드.

## 1. 공고 하나씩 읽기 (순차, 빠르게 연타 금지)
각 ID마다:
1) `mcp__Claude_Browser__navigate` (tabId=배정 탭, url=`https://groupby.kr/positions/<id>`)
2) `mcp__Claude_Browser__javascript_tool` (같은 tabId)로 아래 코드 실행 — 렌더링 완료까지 기다렸다가 본문만 반환:

```js
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let t='';
const ok=()=>{const m=document.querySelector('main');t=m?m.innerText:'';const head=t.slice(0,600);return t.includes('관련 채용 공고')&&!head.includes('[표시 제한]')&&!document.title.includes('[표시 제한]')&&/주요업무|자격요건|근무지/.test(t);};
for(let i=0;i<30;i++){await sleep(500);if(ok())break;}
const body=t.split('관련 채용 공고')[0];
const due=[...body.matchAll(/[^\n]*마감[^\n]*/g)].map(x=>x[0]).slice(0,5);
JSON.stringify({blocked:!ok(),title:document.title,due,text:body.slice(0,9000)})
```

- **주의: navigate 결과에 나오는 탭 제목은 거의 항상 "[표시 제한] ..."이다. 이것은 초기 서버 렌더링 값이고, 몇 초 뒤 실제 공고로 바뀐다. navigate 결과의 제목은 무시하고 반드시 위 JS를 실행해서 그 결과의 `blocked` 값으로만 판단할 것.**
- **속도 제한 (중요, 적응형):** 사이트는 빠른 열람을 차단한다. 현재 대기 시간 D(초)를 `Personal/구직/.groupby-data/delay.txt` 에서 읽어 시작한다(없으면 120).
  - 공고를 하나 저장하면 다음 navigate 전에 D초 쉰다. javascript_tool은 45초 넘으면 시간 초과되므로 `await new Promise(r=>setTimeout(r,30000)); 'ok'` 를 D/30번 반복한다.
  - JS 결과가 `blocked:true`면 저장하지 말고 **D를 30초 늘려**(최대 360초) delay.txt에 즉시 기록한 뒤, 새 D만큼 쉬고 같은 ID를 다시 연다. 같은 ID가 3번 연속 blocked면 그 ID는 건너뛰고(재시도 목록에 적기) 다음 ID로 간다. D가 360초인데도 연속 3번 blocked면 작업을 멈추고 보고한다.
  - D는 줄이지 않는다. 문제없이 열리는 간격을 찾는 것이 목적이다.
  - 각 navigate 시각과 결과를 `Personal/구직/.groupby-data/pace.log` 에 한 줄씩 추가 기록한다 (예: `2026-10-14T18:30:00 id=6827 D=120 ok`).
- 본문 구조: 회사명/온도/지역/인원·투자단계/분야/한줄소개/복지 → 공고명 → 포지션·경력·특이사항·스킬 → 주요업무 → 자격요건 → 우대사항 → 채용절차 → 근무지(“© NAVER Corp.” 다음 줄이 주소).

## 2. 공고별 JSON 작성 (추측 금지)
```json
{"id":123,"status":"완료","company":"회사명","title":"공고명",
 "location":"근무지 주소(본문 '근무지' 아래 주소 우선, 본문에 다른 근무지 명시 시 그것). 없으면 지역 + ' (상세 주소 공고에 미기재)'. 전혀 없으면 '공고에 미기재'",
 "station":"공고에 역·도보가 명시되면 그대로 + ' (공고 명시)'. 아니면 주소 근거로 '성수역(2호선) 도보 약 7분 (추정)'처럼 반드시 '(추정)'. 상세 주소가 없으면 '공고에 미기재 (상세 주소 없음)'",
 "main":"주요 업무 2~4개를 '; '로 구분해 간결히. 없으면 '공고에 미기재'",
 "stack":"본문 기술 스택 + '스킬' 목록, 쉼표 구분. 없으면 '공고에 미기재'",
 "features":"회사 특징: 업종/제품, 인원, 투자 단계, 고객·성과 등 본문·회사 소개에서 확인된 사실만 1~2문장",
 "direction":"회사 방향성·제품·사업 방향: 본문·소개에서 확인된 내용만 1~2문장. 없으면 '공고에 미기재'",
 "due":"마감일이 본문/due 배열에 있으면 YYYY-MM-DD(또는 원문 표기). '상시채용' 등 표기면 그 문구 + ' (본문 명시)'. 없으면 '마감일 미기재'",
 "dev":true,
 "devReason":"분류 근거 한 구절"}
```
`dev` 기준: 실제 업무가 소프트웨어·데이터·AI/ML·로봇 소프트웨어·임베디드·DevOps·인프라 운영·보안 솔루션 개발이면 true. QA, 보안 컨설팅, 하드웨어, 기계·전장, 설계, 품질, 비소프트웨어 연구, PM/디자이너/마케터 등 비개발 직무면 false. 아래 "기존 분류"를 기본값으로 두고 본문이 명백히 다를 때만 바꾼다.
모든 값은 한 줄 한국어 문자열.

## 3. 저장 — 공고 1개 처리할 때마다 즉시
Bash에서 python3 -I 로 `OUTDIR/<id>.json` 에 json.dump(ensure_ascii=False). 시작 전에 `ls OUTDIR` 해서 이미 파일이 있는 ID는 건너뛴다(재개용).
OUTDIR = Personal/구직/.groupby-data/out

공고가 삭제·마감되어 페이지가 없으면 `{"id":..,"status":"미조사","reason":"페이지 없음/마감"}` 으로 저장.

## 4. 완료 보고
마지막에 "최종 D값 / 저장 N개 / 미조사 M개(ID와 사유) / 분류 변경 ID 목록 / blocked 발생 여부"만 짧게.
