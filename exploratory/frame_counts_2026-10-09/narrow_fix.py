"""Narrow frame mapped by exact title (WDQS schema:name), redirects resolved via the API, then sitelinks."""
import sys, time
import pandas as pd, requests
sys.path.insert(0, "src")
from ai_on_wikipedia.wp1 import load_wp1, narrow_titles
from ai_on_wikipedia.client import mw_query

UA = {"User-Agent": "ai-on-wikipedia/0.1 (https://github.com/brianckeegan/ai-on-wikipedia)"}
WIKIS = "en ja es ru fr de it zh pt ar fa pl tr nl id uk sv cs vi ko".split()
SP = sys.argv[1]

def sparql(q):
    for t in range(5):
        r = requests.post("https://query.wikidata.org/sparql", data={"query": q},
                          headers={**UA, "Accept": "application/sparql-results+json"}, timeout=300)
        if r.status_code == 200:
            return [{k: v["value"] for k, v in b.items()} for b in r.json()["results"]["bindings"]]
        time.sleep(10 * (t + 1))
    r.raise_for_status()

def lit(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"@en'

narrow = narrow_titles(load_wp1("data/raw/wp1_artificial_intelligence_2026-10-09.tsv"))
titles = narrow["title"].tolist()
q = {}
for i in range(0, len(titles), 200):
    vals = " ".join(lit(t) for t in titles[i:i+200])
    for r in sparql(f"SELECT ?name ?item WHERE {{ VALUES ?name {{ {vals} }} ?a schema:name ?name; schema:isPartOf <https://en.wikipedia.org/>; schema:about ?item }}"):
        q[r["name"]] = r["item"].rsplit("/", 1)[1]
    time.sleep(2)
narrow["qid"] = narrow["title"].map(q)
narrow["mapped_via"] = narrow["qid"].notna().map({True: "sitelink", False: None})
print("by exact title:", narrow.qid.notna().sum(), flush=True)

# Unmapped titles: resolve redirects through the API (few calls), then map targets.
miss = narrow.loc[narrow.qid.isna(), "title"].tolist()
target = {}
for i in range(0, len(miss), 50):
    for chunk in mw_query("https://en.wikipedia.org/w/api.php", {"titles": "|".join(miss[i:i+50]), "redirects": "1",
                                                                "prop": "pageprops", "ppprop": "wikibase_item"}):
        back = {}
        for r in chunk.get("normalized", []) + chunk.get("redirects", []):
            back[r["to"]] = back.get(r["from"], r["from"])
        for p in chunk.get("pages", []):
            qid = p.get("pageprops", {}).get("wikibase_item")
            if qid:
                target[back.get(p["title"], p["title"])] = qid
m = narrow.qid.isna() & narrow.title.isin(target)
narrow.loc[m, "qid"] = narrow.loc[m, "title"].map(target)
narrow.loc[m, "mapped_via"] = "redirect_or_normalized"
print("after redirects:", narrow.qid.notna().sum(), "distinct", narrow.qid.nunique(),
      "unmapped", narrow.qid.isna().sum(), flush=True)
narrow.to_csv(f"{SP}/narrow_qids_final.csv", index=False)

qids = sorted(narrow.qid.dropna().unique())
out = []
for i in range(0, len(qids), 400):
    vals = " ".join(f"wd:{x}" for x in qids[i:i+400])
    out += sparql(f"""SELECT ?item ?site ?title WHERE {{ VALUES ?item {{ {vals} }}
      ?a schema:about ?item; schema:isPartOf ?site; schema:name ?title.
      FILTER(?site IN ({", ".join(f"<https://{w}.wikipedia.org/>" for w in WIKIS)})) }}""")
    time.sleep(2)
sl = pd.DataFrame(out)
sl["qid"] = sl["item"].str.rsplit("/", n=1).str[1]
sl["wiki"] = sl["site"].str.extract(r"https://([a-z-]+)\.wikipedia")[0]
sl[["qid", "wiki", "title"]].to_csv(f"{SP}/narrow_sitelinks_final.csv", index=False)
print("narrow item-edition articles", len(sl), flush=True)
print(sl.groupby("wiki").size().reindex(WIKIS).to_string(), flush=True)
print("NARROW_DONE")
