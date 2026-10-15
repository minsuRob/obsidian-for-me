import json,os,re,sys,difflib
S=os.path.dirname(os.path.abspath(__file__))
t={}
for blk in re.split(r'\n(?=### \d+\. )', open(S+'/orig_dev.md').read())[1:]:
    m=re.search(r'- 목록 노출 정보: (.*?) · ',blk) ; pid=int(re.search(r'positions/(\d+)',blk).group(1))
    t[pid]=m.group(1) if m else re.match(r'### \d+\. (.*)',blk).group(1)
for m in re.finditer(r'- \[(.*?)\]\(https://groupby\.kr/positions/(\d+)\)', open(S+'/orig_non.md').read()):
    t[int(m.group(2))]=m.group(1)
bad=[]
for f in sorted(os.listdir(S+'/out')):
    o=json.load(open(S+'/out/'+f)); i=int(o['id'])
    if o.get('status')!='완료': continue
    a=re.sub(r'\W','',t.get(i,'')); b=re.sub(r'\W','',o.get('title',''))
    r=difflib.SequenceMatcher(None,a,b).ratio()
    if '표시 제한' in json.dumps(o,ensure_ascii=False) or (r<0.5 and not (a and (a in b or b in a))):
        bad.append((i,round(r,2),t.get(i),o.get('title'),o.get('company')))
for x in bad: print(x)
print('checked', len(os.listdir(S+'/out')), 'suspicious', len(bad))
