"""raw/posts_*.json을 읽어 공고별 text/<id>.txt와 인디스워크 Markdown 파일들을 만든다."""
import json, glob, re, html, pathlib, collections
HERE = pathlib.Path(__file__).parent
OUT = HERE.parent
RAW = HERE / "raw"
TXT = HERE / "text"; TXT.mkdir(exist_ok=True)
tags = json.loads((RAW / "tags.json").read_text())
cats = json.loads((RAW / "categories.json").read_text())
JOB_CATS = {"신입/인턴", "주니어경력"}  # 커리어TV·취업토크·교육/대외활동은 채용공고가 아니라서 뺀다
allposts = [p for f in sorted(RAW.glob("posts_*.json")) for p in json.loads(f.read_text())]
posts = [p for p in allposts if JOB_CATS & {cats.get(str(c)) for c in p["categories"]}]
META = {"스타트업", "IT개발", "채용시마감", "기한있음", "상시채용"}
AI = re.compile(r"\bAI\b|LLM|에이전트|Agent|Agentic|GPT|생성형|RAG|머신러닝|딥러닝|\bML\b|MLOps|FDE|Forward Deployed|바이브 ?코딩|Claude|Cursor|Copilot|LangChain|LangGraph|AX\b", re.I)
TOOL = re.compile(r"Claude|Cursor|Copilot|바이브 ?코딩|AI 코딩|코딩 에이전트|AI ?도구|AI ?툴|AI 활용", re.I)
TASK = re.compile(r"(담당\s*업무|주요\s*업무|하는\s*일|업무\s*내용|Responsibilit|What you.*do|합류하면)", re.I)
LOC = re.compile(r"(근무\s*(지|지역|장소|위치)|근무처|위치)\s*[:：]?\s*(.+)")
DUE = re.compile(r"(\d{4}\s*[.\-/년]\s*\d{1,2}\s*[.\-/월]\s*\d{1,2})[^\n]{0,15}(마감|까지)|(마감|접수\s*기간|접수\s*마감)[^\n]{0,30}?(\d{4}\s*[.\-/년]\s*\d{1,2}\s*[.\-/월]\s*\d{1,2})")

def text(h):
    t = html.unescape(re.sub(r"<[^>]+>", "\n", h)).replace("​", "")
    return "\n".join(l.strip() for l in t.splitlines() if l.strip())

def one(s, n=120):
    s = re.sub(r"\s+", " ", s).strip(" •·-–*|")
    return s if len(s) <= n else s[:n] + "…"

rows = []
for p in posts:
    t = text(p["content"]["rendered"])
    (TXT / f"{p['id']}.txt").write_text(t)
    title = html.unescape(p["title"]["rendered"]).strip()
    comp, _, pos = title.partition("｜") if "｜" in title else title.partition("|")
    if not pos: comp, pos = "", title
    tn = [tags.get(str(i), str(i)) for i in p["tags"]]
    lines = t.splitlines()
    tasks = []
    for i, l in enumerate(lines):
        if TASK.search(l) and len(l) < 40:
            tasks = [one(x, 80) for x in lines[i+1:i+8] if not re.match(r"^[\[\(ㅣ□■▶◆#]|자격|요건|우대", x)][:3]
            break
    loc = next((one(m.group(3), 60) for l in lines if (m := LOC.search(l)) and len(m.group(3)) > 1), "")
    dm = DUE.search(t)
    due = re.sub(r"\s", "", (dm.group(1) or dm.group(4))) if dm else ("상시채용" if "상시채용" in tn else "채용시 마감" if "채용시마감" in tn else "본문 확인")
    apply = re.search(r'<a[^>]+href="([^"]+)"[^>]*>(?:(?!</a>).)*지원하러', p["content"]["rendered"], re.S)
    rows.append(dict(id=p["id"], career="·".join(sorted({cats.get(str(c)) for c in p["categories"]} & JOB_CATS)), date=p["date"][:10], company=one(comp, 40), pos=one(pos, 100), link=p["link"],
        apply=html.unescape(apply.group(1)) if apply else "", jobs=[x for x in tn if x not in META],
        startup="스타트업" in tn, it="IT개발" in tn, ai=bool(AI.search(title + "\n" + t)), aititle=bool(AI.search(title)),
        tool=bool(TOOL.search(t)), tasks=tasks, loc=loc, due=due, short=len(t) < 200))
(HERE / "posts.json").write_text(json.dumps(rows, ensure_ascii=False, indent=0))

def entry(r):
    flags = []
    if r["aititle"]: flags.append("🤖AI직무")
    elif r["ai"]: flags.append("AI언급")
    if r["tool"]: flags.append("🛠AI도구활용")
    out = [f"### {r['company']} — {r['pos']}", "",
           f"- 게시일: {r['date']} · 마감: {r['due']}" + (f" · {' '.join(flags)}" if flags else ""),
           f"- 구분: {r['career']}" + (" · 스타트업" if r["startup"] else "") + f" · 분야: {', '.join(r['jobs']) or '-'}",
           f"- 근무지: {r['loc'] or '본문에 미기재'}"]
    if r["tasks"]: out.append(f"- 주요 업무: {'; '.join(r['tasks'])}")
    elif r["short"]: out.append("- 주요 업무: 본문이 이미지 위주라 텍스트 추출 불가 (원문 확인)")
    out.append(f"- 원문: {r['link']}" + (f" · [지원]({r['apply']})" if r["apply"] else ""))
    return "\n".join(out)

def write(name, title, rs, note):
    c = collections.Counter(j for r in rs for j in r["jobs"])
    head = [f"# {title}", "", "> 출처: 인디스워크(inthiswork.com) WordPress 공개 API · 수집일: 2026-10-15 · 마감 처리된 공고 제외",
            "> 관련 문서: [[인디스워크-개요]]", "", note, "",
            f"- 공고 수: **{len(rs)}**", f"- 제목에 AI 직무 표시: {sum(r['aititle'] for r in rs)} · 본문에 AI 언급: {sum(r['ai'] for r in rs)} · AI 도구 활용 언급: {sum(r['tool'] for r in rs)}",
            f"- 분야 상위: {', '.join(f'{k} {v}' for k, v in c.most_common(12))}", ""]
    rs = sorted(rs, key=lambda r: r["date"], reverse=True)
    rs = sorted(rs, key=lambda r: (not r["aititle"]))
    body = ["## AI 직무 공고 (제목 기준)", ""] + [entry(r) + "\n" for r in rs if r["aititle"]] + \
           ["## 그 외 공고 (최신순)", ""] + [entry(r) + "\n" for r in rs if not r["aititle"]]
    (OUT / name).write_text("\n".join(head + body))

it = [r for r in rows if r["it"]]
st_only = [r for r in rows if r["startup"] and not r["it"]]
write("인디스워크-IT개발.md", "인디스워크 IT개발 공고", it, "IT개발 태그가 붙은 공고 전체다. 스타트업 여부는 각 공고의 '분야' 줄 끝에 표시했다.")
write("인디스워크-스타트업-비개발.md", "인디스워크 스타트업 공고 (IT개발 태그 없음)", st_only, "스타트업 태그는 있지만 IT개발 태그가 없는 공고다. 데이터분석·PM 등 개발 인접 직무도 여기 있다.")
print(len(allposts), len(rows), len(it), len(st_only), sum(r['startup'] and r['it'] for r in rows),
      sum(r['aititle'] for r in it), sum(r['tool'] for r in it), sum(r['short'] for r in rows),
      sum(bool(r['loc']) for r in rows), sum(r['due'] not in ('본문 확인',) for r in rows), sum(bool(r['tasks']) for r in rows), sum(bool(r['apply']) for r in rows))
