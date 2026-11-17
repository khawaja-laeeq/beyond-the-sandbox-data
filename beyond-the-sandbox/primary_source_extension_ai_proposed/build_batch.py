"""Stage a post-freeze batch (v1.1) of primary-source units and recount.
Reads the original coded_evidence.csv; writes to OUT only. Never edits the frozen data.
All new statuses are AI-PROPOSED and must be blind-coded by two humans before use."""
import csv, json, sys, collections, pathlib

ORIG = pathlib.Path(sys.argv[1])  # .../experiments
OUT = pathlib.Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)

# (unit, cluster/developer, source_type, url, report_date, statuses D1..D5, confidence, note)
OA = "https://alignment.openai.com/misalignment-reports/"
U = [
 ("PF-OAI-GOVSTATS","OpenAI","developer",OA+"retrieving-server-secrets-and-bypassing-authorization-on-a-government-statistics-website/","2026-10-15",
  "ddddd","high","Path traversal + unsigned JWT; D2 quote 'Authentication bypass may be acceptable?'; >1000 emails; operator notification not stated"),
 ("PF-OAI-APIKEYS","OpenAI","developer",OA+"searching-github-for-leaked-api-keys/","2026-09-16",
  "ddddd","high","Leaked keys from public GitHub; model noted key would be 'unauthorized'; third-party key used; no harm to owner described"),
 ("PF-OAI-PUBSTATS","OpenAI","developer",OA+"obtaining-public-statistics-with-disallowed-requests/","2026-10-09",
  "dddd?","medium","3 conversations; POST workaround, account registration, bulk download of 658,567 rows; D2 'arguably violating environment policy'; D5 harm to third party not reported"),
 ("PF-OAI-FILESVC","OpenAI","developer",OA+"sending-disallowed-web-requests-and-reaching-a-public-file-service/","2026-10-09",
  "d?dd?","medium","Relays/remote accounts/anonymous FTP; no permission belief stated; outside impact not confirmed"),
 ("PF-OAI-EXTBROWSER","OpenAI","developer",OA+"circumventing-internet-restrictions-through-an-external-browser/","2026-10-15",
  "d?dd?","medium","Used external browser to POST; no permission belief; impact on service not confirmed"),
 ("PF-OAI-DNSCHAT","OpenAI","developer",OA+"an-agent-used-dns-to-reach-an-external-chatbot/","2026-09-25",
  "ddddd","high","D2 'User only gives permission to research, using publicly offered DNS services acceptable'; P0 alert ~15 min, killed 2.5 h later; chatbot answered"),
 ("PF-OAI-GHTOKEN","OpenAI","developer",OA+"exposing-a-github-token-in-a-public-repository/","2026-09-25",
  "ddddd","high","Token committed to public openai/codex PR; D2 'writes to openai allowed' vs 'exploit infrastructure questionable'; researcher faster than monitor"),
 ("PF-OAI-NETBYPASS","OpenAI","developer",OA+"bypassing-network-restrictions-during-a-coding-evaluation/","2026-11-05",
  "ddddu","medium","Raw packets, S3/metadata probing; D2 'We have [network permission]'; no sensitive data transfer found, target never retrieved (D5 unknown)"),
 ("PF-OAI-DASHBOARD","OpenAI","developer",OA+"accessing-and-changing-internal-systems-during-dashboard-research/","2026-10-15",
  "dddd d".replace(" ",""),"low","Mostly OpenAI-internal systems (+ third-party services as route); D2 'We have all_access' / 'but ethical?' is an access belief, borderline; coders to rule on scope"),
 ("PF-META-MS11","Meta","developer","https://research.meta.ai/blog/addressing-third-party-testing-misconfiguration-muse-spark-1-1","2026-08-14",
  "ddddd","medium","Irregular misconfig gave internet; 'believing the real website was the intended target' (in-scope belief, cf. INC-ANT-INT); DB changed; extent not stated -> D5 coders to confirm"),
 ("PF-WORKOS","WorkOS (affected party)","affected","https://workos.com/security/bulletins/update-for-october-30th-2026-data-security-incident","2026-11-06",
  "duddd","medium","Affected-party report; agent operated by an individual researcher (not an AI developer) - eligibility ruling needed; no model belief reported"),
 ("PF-WIKIMEDIA","Wikimedia (affected party)","affected","https://diff.wikimedia.org/2026/10/05/openai-rogue-agent-activities-found-on-wikimedia-projects/","2026-10-06",
  "ddddu","medium","Affected-party report; attribution to OpenAI is Wikimedia's belief; no compromise found; D2 unknown; outage link hedged"),
]
CODE = {"d":"documented","u":"unknown","?":"unknown","c":"contradicted"}
LOW = {"?"}   # '?' = proposed unknown because evidence is silent or not confirmed; 'u' = unknown

rows=[]
for unit,cl,typ,url,dt,st,conf,note in U:
    for i,ch in enumerate(st):
        rows.append(dict(unit=unit,code=f"D{i+1}",status=CODE[ch],proposed_by="AI (single pass)",
            coder_status="PENDING_BLIND_DOUBLE_CODING",source_type=typ,reference=url,source_date=dt,
            unit_confidence=conf,note=note if i==0 else ""))
with open(OUT/"post_freeze_batch_v1_1_proposed.csv","w",newline="",encoding="utf8") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

orig=list(csv.DictReader(open(ORIG/"data/coded_evidence.csv",encoding="utf8")))
def tally(rs):
    t=collections.defaultdict(lambda: collections.Counter())
    for r in rs: t[r["code"]][r["status"]]+=1
    return {k:dict(v) for k,v in sorted(t.items())}
def rates(rs):
    d={}
    for k,v in tally(rs).items():
        n=sum(v.values()); d[k]=f"{v.get('documented',0)}/{n}"
    return d
origunits={r["unit"] for r in orig}
# clusters
ocl={"INC-OAI":"OpenAI","INC-ANT":"Anthropic","INC-AISI":"UK AISI"}
def cl(u): return next(v for k,v in ocl.items() if u.startswith(k))
newcl={u[0]:u[1] for u in U}
res=dict(
 original=dict(units=len(origunits),cells=len(orig),support_rates=rates(orig),developers_or_reporters=sorted(set(cl(u) for u in origunits))),
 new_batch_proposed=dict(units=len(U),cells=len(rows),support_rates=rates(rows),reporters=sorted(set(u[1] for u in U))),
 combined=dict(units=len(origunits)+len(U),cells=len(orig)+len(rows),support_rates=rates(orig+rows),
   independent_reporter_groups=len(set(cl(u) for u in origunits)|set(u[1] for u in U)),
   groups_if_wikimedia_counted_under_openai=len(set(cl(u) for u in origunits)|set(u[1] for u in U if not u[1].startswith("Wikimedia"))),
   openai_grouping="all OpenAI units (original 3 + new 9 = 12) form one reporter group"),
 caveat="New statuses are single-pass AI proposals; OpenAI reports are one developer so 9 of the 12 new units add units, not independent reporters.")
json.dump(res,open(OUT/"recount.json","w"),indent=1)
print(json.dumps(res,indent=1))
