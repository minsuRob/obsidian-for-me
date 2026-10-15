import json, os, re, sys

S = os.path.dirname(os.path.abspath(__file__))
D = sys.argv[1]  # Personal/구직 directory
OUT = os.path.join(S, 'out')
SRC_DEV = os.path.join(S, 'orig_dev.md')
SRC_NON = os.path.join(S, 'orig_non.md')

dev_txt = open(SRC_DEV).read()
non_txt = open(SRC_NON).read()

# --- parse original dev entries (order preserved)
dev_entries = []
for blk in re.split(r'\n(?=### \d+\. )', dev_txt)[1:]:
    blk = blk.split('\n## ')[0]
    title = re.match(r'### \d+\. (.*)', blk).group(1).strip()
    pid = int(re.search(r'positions/(\d+)', blk).group(1))
    m = re.search(r'- 목록 노출 정보: (.*)', blk)
    dev_entries.append({'id': pid, 'title': title, 'listing': m.group(1).strip() if m else ''})

# --- parse original non-dev entries with category
non_entries = []
cat = None
for line in non_txt.split('\n'):
    if line.startswith('### '):
        cat = line[4:].strip()
    m = re.match(r'- \[(.*?)\]\(https://groupby\.kr/positions/(\d+)\)(?: — (.*))?', line)
    if m and cat:
        non_entries.append({'id': int(m.group(2)), 'title': m.group(1), 'listing': m.group(3) or '', 'cat': cat})

det = {}
for f in os.listdir(OUT):
    if f.endswith('.json'):
        try:
            o = json.load(open(os.path.join(OUT, f)))
            det[int(o['id'])] = o
        except Exception:
            pass

def done(pid):
    o = det.get(pid)
    return o is not None and o.get('status') == '완료'

def is_dev(e, default):
    o = det.get(e['id'])
    if o and o.get('status') == '완료' and isinstance(o.get('dev'), bool):
        return o['dev']
    return default

final_dev = [e for e in dev_entries if is_dev(e, True)] + [e for e in non_entries if is_dev(e, False)]
final_non = [e for e in non_entries if not is_dev(e, False)] + [dict(e, cat='개발 파일에서 이동') for e in dev_entries if not is_dev(e, True)]
moved_to_dev = [e for e in non_entries if is_dev(e, False)]
moved_to_non = [e for e in dev_entries if not is_dev(e, True)]

def clean(v):
    v = (v or '').strip().replace('\n', ' ')
    return v or '공고에 미기재'

def detail(n, e):
    pid = e['id']
    link = f'https://groupby.kr/positions/{pid}'
    o = det.get(pid)
    lines = []
    if done(pid):
        lines.append(f"### {n}. {clean(o.get('title') or e['title'])} — {clean(o.get('company'))}")
        lines.append('')
        lines.append(f"- 위치: {clean(o.get('location'))}")
        lines.append(f"- 가까운 역·도보: {clean(o.get('station'))}")
        lines.append(f"- 주요 업무: {clean(o.get('main'))}")
        lines.append(f"- 기술 스택: {clean(o.get('stack'))}")
        lines.append(f"- 회사 특징: {clean(o.get('features'))}")
        lines.append(f"- 회사 방향성: {clean(o.get('direction'))}")
        lines.append(f"- 공고 마감일: {(o.get('due') or '').strip() or '마감일 미기재'}")
        lines.append(f"- 원문: [그룹바이 공고]({link})")
    else:
        lines.append(f"### {n}. {e['title']}")
        lines.append('')
        lines.append('- 상세 조사: 미조사' + (f" ({o['reason']})" if o and o.get('reason') else ''))
        lines.append(f"- 원문: [그룹바이 공고]({link})")
    if e.get('listing'):
        lines.append(f"- 목록 노출 정보: {e['listing']}")
    return '\n'.join(lines)

total_links = len({e['id'] for e in dev_entries + non_entries})
dev_done = sum(done(e['id']) for e in final_dev)
non_done = sum(done(e['id']) for e in final_non)

hdr = f"""# 그룹바이 개발 채용공고 조사

> 조사 기준일: 2026-10-14
> 원본 목록: [그룹바이 개발 직군 (서울·경기 일부 지역, 최신순)](https://groupby.kr/positions?locations=271&locations=24&locations=25&locations=26&locations=27&locations=30&locations=31&locations=37&locations=38&locations=39&orderBy=-updatedAt&parentPositionTypes=%EA%B0%9C%EB%B0%9C)
> 수집 현황: 사이트 화면 표시 520개 / 실제 수집 링크 {total_links}개 (화면 표시 수보다 1개 적음 — 목록에서 실제로 수집되는 링크는 {total_links}개이며 차이 원인은 미확인)
> 이 파일: 개발 관련 {len(final_dev)}개 (상세 조사 완료 {dev_done}개 / 미조사 {len(final_dev) - dev_done}개) · 비개발·개발 인접 {len(final_non)}개는 [[그룹바이-비개발]]
> 분류 기준: 소프트웨어·데이터·AI/ML·로봇 소프트웨어·임베디드·DevOps·보안 솔루션 개발은 이 파일, QA·보안 컨설팅·하드웨어·기계/전장·설계·품질·비소프트웨어 연구는 비개발 파일.
> 표기 원칙: 공고에 없는 정보는 `공고에 미기재`, 마감일이 없으면 `마감일 미기재`. 역·도보 시간은 공고 명시값 우선, 주소 기반 보완 값은 `(추정)` 표시. 회사 특징·방향성은 공고 본문과 회사 소개에서 확인된 내용만 요약.
"""
if moved_to_dev:
    hdr += f"> 상세 확인 후 비개발 → 개발로 이동: {', '.join(str(e['id']) for e in moved_to_dev)}\n"
if moved_to_non:
    hdr += f"> 상세 확인 후 개발 → 비개발로 이동: {', '.join(str(e['id']) for e in moved_to_non)}\n"

body = '\n\n'.join(detail(i + 1, e) for i, e in enumerate(final_dev))
open(os.path.join(D, '그룹바이.md'), 'w').write(hdr + '\n## 개발 관련 공고 전체 목록\n\n' + body + '\n')

# --- non-dev file
cats = []
for e in final_non:
    if e['cat'] not in cats:
        cats.append(e['cat'])
nhdr = f"""# 그룹바이 비개발·개발 인접 채용공고

> 조사 기준일: 2026-10-14
> 기준: 소프트웨어 구현이 주업무가 아닌 QA·보안 컨설팅·하드웨어·기계/전장·설계·품질·비소프트웨어 연구 직무를 별도 분류함. AI/ML 연구, 데이터 사이언스, 로봇 소프트웨어처럼 코드와 모델 개발이 핵심인 직무는 [[그룹바이]]에 남김.
> 이 파일: {len(final_non)}개 (상세 조사 완료 {non_done}개 / 미조사 {len(final_non) - non_done}개) · 전체 실제 수집 링크 {total_links}개 (사이트 표시 520개)

## 분류된 공고
"""
parts = []
for c in cats:
    items = [e for e in final_non if e['cat'] == c]
    parts.append(f'### {c}\n\n' + '\n'.join(
        f"- [{e['title']}](https://groupby.kr/positions/{e['id']})" + (f" — {e['listing']}" if e.get('listing') and e['cat'] != '개발 파일에서 이동' else '')
        for e in items))
ndet = '\n\n'.join(detail(i + 1, e) for i, e in enumerate(final_non))
foot = '\n\n## 참고\n\n직무명이 개발과 겹치거나 코드가 일부 포함된 공고도 실제 주업무가 하드웨어·검증·설계·보안·QA인 경우 이 파일로 분류했다. 반대로 AI/ML 연구, 데이터 사이언스, 로봇 소프트웨어처럼 소프트웨어·모델 구현이 핵심인 공고는 개발 관련 파일에 남겼다.\n'
open(os.path.join(D, '그룹바이-비개발.md'), 'w').write(nhdr + '\n' + '\n\n'.join(parts) + '\n\n## 상세 조사\n\n' + ndet + foot)

print(json.dumps({'total_links': total_links, 'dev': len(final_dev), 'dev_done': dev_done, 'non': len(final_non), 'non_done': non_done,
                  'moved_to_dev': [e['id'] for e in moved_to_dev], 'moved_to_non': [e['id'] for e in moved_to_non], 'json_files': len(det)}, ensure_ascii=False))
