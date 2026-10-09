import json, sys, time
import pandas as pd, requests
UA = {"User-Agent": "ai-on-wikipedia/0.1 (https://github.com/brianckeegan/ai-on-wikipedia)"}
SP = sys.argv[1]
roots = {"en":"Artificial intelligence","ja":"人工知能","es":"Inteligencia artificial","ru":"Искусственный интеллект","fr":"Intelligence artificielle","de":"Künstliche Intelligenz","it":"Intelligenza artificiale","zh":"人工智能","pt":"Inteligência artificial","ar":"ذكاء اصطناعي","fa":"هوش مصنوعی","pl":"Sztuczna inteligencja","tr":"Yapay zekâ","nl":"Kunstmatige intelligentie","id":"Kecerdasan buatan","uk":"Штучний інтелект","sv":"Artificiell intelligens","cs":"Umělá inteligence","vi":"Trí tuệ nhân tạo","ko":"인공지능"}
rows = []
for depth in (0, 1):
    for w, c in roots.items():
        p = {"language": w, "project": "wikipedia", "categories": c, "depth": depth, "ns[0]": 1,
             "format": "json", "wikidata_item": "any", "doit": 1}
        for t in range(4):
            r = requests.get("https://petscan.wmcloud.org/", params=p, headers=UA, timeout=600)
            if r.status_code == 200: break
            time.sleep(15 * (t + 1))
        for x in r.json()["*"][0]["a"]["*"]:
            rows.append({"depth": depth, "wiki": w, "title": x["title"], "qid": x.get("q") or x.get("metadata", {}).get("wikidata")})
        time.sleep(2)
    d = pd.DataFrame(rows); d = d[d.depth == depth]
    print(f"depth {depth}: members {len(d)} distinct qids {d.qid.nunique()}", d.wiki.value_counts().to_dict(), flush=True)
pd.DataFrame(rows).to_csv(f"{SP}/broad_depth01.csv", index=False)
print("SWEEP_DONE")
