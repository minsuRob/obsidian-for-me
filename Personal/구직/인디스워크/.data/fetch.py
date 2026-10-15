"""인디스워크 WP REST API에서 스타트업 또는 IT개발 태그의 진행 중 공고를 받아 raw/에 저장한다."""
import json, time, urllib.request, pathlib
BASE = "https://inthiswork.com/wp-json/wp/v2"
TAG_STARTUP, TAG_IT, CAT_CLOSED = 191700265, 191700187, 191700169
RAW = pathlib.Path(__file__).parent / "raw"
UA = {"User-Agent": "Mozilla/5.0 (personal job search)"}

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return json.load(r), r.headers

page, total = 1, None
while True:
    url = f"{BASE}/posts?per_page=100&page={page}&tags={TAG_STARTUP},{TAG_IT}&categories_exclude={CAT_CLOSED}&orderby=date&order=desc"
    data, h = get(url)
    total = int(h["X-WP-TotalPages"])
    (RAW / f"posts_{page:02d}.json").write_text(json.dumps(data, ensure_ascii=False))
    print(page, "/", total, len(data), flush=True)
    if page >= total: break
    page += 1; time.sleep(3)

ids = sorted({t for f in RAW.glob("posts_*.json") for p in json.loads(f.read_text()) for t in p["tags"]})
tags = {}
for i in range(0, len(ids), 100):
    d, _ = get(f"{BASE}/tags?per_page=100&include={','.join(map(str, ids[i:i+100]))}")
    tags.update({t["id"]: t["name"] for t in d}); time.sleep(3)
cats, _ = get(f"{BASE}/categories?per_page=100")
(RAW / "tags.json").write_text(json.dumps(tags, ensure_ascii=False))
(RAW / "categories.json").write_text(json.dumps({c["id"]: c["name"] for c in cats}, ensure_ascii=False))
print("tags", len(tags))
