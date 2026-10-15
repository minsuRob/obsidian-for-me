import json,sys
d=json.loads(sys.stdin.read())
assert "[표시 제한]" not in d.get("company","")+d.get("title","")
O="/private/tmp/claude-501/-Users-robertlee-Workspace-Personal-obsidian-for-me/0717e407-2481-4534-91b8-f19fd45cde7c/scratchpad/out/%d.json"%d["id"]
json.dump(d,open(O,"w"),ensure_ascii=False)
print("saved",d["id"])
