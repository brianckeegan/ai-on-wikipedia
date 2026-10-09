"""LOI frame counts via WDQS (narrow mapping, sitelinks) and PetScan (broad category crawl)."""
import json, sys, time, urllib.parse
import pandas as pd, requests

UA = {"User-Agent": "ai-on-wikipedia/0.1 (https://github.com/brianckeegan/ai-on-wikipedia)"}
WIKIS = "en ja es ru fr de it zh pt ar fa pl tr nl id uk sv cs vi ko".split()
SP = sys.argv[1]
sys.path.insert(0, "src")
from ai_on_wikipedia.wp1 import load_wp1, narrow_titles

def sparql(q):
    for t in range(5):
        r = requests.post("https://query.wikidata.org/sparql", data={"query": q},
                          headers={**UA, "Accept": "application/sparql-results+json"}, timeout=300)
        if r.status_code == 200:
            return [{k: v["value"] for k, v in b.items()} for b in r.json()["results"]["bindings"]]
        time.sleep(10 * (t + 1))
    r.raise_for_status()

def article_iri(wiki, title):
    return f"<https://{wiki}.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'), safe='')}>"

# Seed category sitelinks
seed = sparql("""SELECT ?wiki ?title WHERE { ?a schema:about wd:Q558331; schema:isPartOf ?site; schema:name ?title.
  BIND(REPLACE(STR(?site), "https://([a-z-]+)\\\\.wikipedia\\\\.org/", "$1") AS ?wiki) FILTER(CONTAINS(STR(?site), "wikipedia.org")) }""")
roots = {r["wiki"]: r["title"] for r in seed if r["wiki"] in WIKIS}
print("seed roots:", len(roots), {w: roots.get(w) for w in WIKIS}, flush=True)

# Narrow: titles -> QIDs
narrow = narrow_titles(load_wp1("data/raw/wp1_artificial_intelligence_2026-10-09.tsv"))
rows = []
for i in range(0, len(narrow), 300):
    vals = " ".join(article_iri("en", t) for t in narrow["title"].iloc[i:i+300])
    rows += sparql("SELECT ?a ?item WHERE { VALUES ?a { %s } ?a schema:about ?item }" % vals)
    time.sleep(2)
q = {urllib.parse.unquote(r["a"].rsplit("/wiki/", 1)[1]).replace("_", " "): r["item"].rsplit("/", 1)[1] for r in rows}
narrow["qid"] = narrow["title"].map(q)
print("narrow titles", len(narrow), "mapped", narrow.qid.notna().sum(), "distinct", narrow.qid.nunique(), flush=True)
narrow.to_csv(f"{SP}/out_narrow_qids.csv", index=False)

def sitelinks(qids):
    out = []
    qids = sorted(qids)
    for i in range(0, len(qids), 400):
        vals = " ".join(f"wd:{x}" for x in qids[i:i+400])
        out += sparql("""SELECT ?item ?site ?title WHERE { VALUES ?item { %s }
          ?a schema:about ?item; schema:isPartOf ?site; schema:name ?title.
          FILTER(?site IN (%s)) }""" % (vals, ", ".join("<https://%s.wikipedia.org/>" % w for w in WIKIS)))
        time.sleep(2)
    df = pd.DataFrame(out)
    df["qid"] = df["item"].str.rsplit("/", n=1).str[1]
    df["wiki"] = df["site"].str.extract(r"https://([a-z-]+)\.wikipedia")[0]
    return df[["qid", "wiki", "title"]]

nl = sitelinks(set(narrow.qid.dropna()))
nl.to_csv(f"{SP}/out_narrow_sitelinks.csv", index=False)
print("narrow item-edition articles", len(nl), flush=True)

# Broad: PetScan per wiki, depth 2
broad = []
for w in WIKIS:
    root = roots.get(w)
    if not root:
        print("no root for", w, flush=True); continue
    params = {"language": w, "project": "wikipedia", "categories": root.split(":", 1)[1],
              "depth": 2, "ns[0]": 1, "format": "json", "wikidata_item": "any", "doit": 1}
    for t in range(4):
        r = requests.get("https://petscan.wmcloud.org/", params=params, headers=UA, timeout=600)
        if r.status_code == 200:
            break
        time.sleep(15 * (t + 1))
    pages = r.json()["*"][0]["a"]["*"]
    for p in pages:
        broad.append({"wiki": w, "page_id": p["id"], "title": p["title"], "qid": p.get("q") or p.get("metadata", {}).get("wikidata")})
    print(w, root, len(pages), flush=True)
    time.sleep(3)
b = pd.DataFrame(broad)
b.to_csv(f"{SP}/out_broad_members.csv", index=False)
bl = sitelinks(set(b.qid.dropna()))
bl.to_csv(f"{SP}/out_broad_sitelinks.csv", index=False)
print("broad members", len(b), "with qid", b.qid.notna().sum(), "distinct qids", b.qid.nunique(), "item-edition articles", len(bl), flush=True)
print("DONE")
