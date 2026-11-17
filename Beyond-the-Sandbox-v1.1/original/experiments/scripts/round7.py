"""Round 7: promote coded_evidence_v13.csv to coded_evidence.csv (v12 stays as data/coded_evidence_v12.csv),
log the two D2 recodes (ART, HF) in change_log, archive agreement/kappa outputs.
Run from experiments/: python3 -I scripts/round7.py"""
import csv, shutil, os
TARGETS = [("INC-OAI-ART", "D2"), ("INC-OAI-HF", "D2")]
rows = list(csv.DictReader(open('data/coded_evidence_v13.csv', encoding='utf-8')))
MSG = ("RECODED documented->unknown (round 7): R07 (METR) states a scorer-manipulation objective, "
       "not the agent's belief about permission; codebook D2 requires a stated permission belief, so the source is silent on D2")
for r in rows:
    if (r['unit'], r['code']) in TARGETS and 'RECODED documented->unknown (round 7)' not in r['change_log']:
        r['change_log'] = (r['change_log'] + '; ' if r['change_log'] else '') + MSG
    r['qualification'] = r['qualification'].replace('AI second coder (codex)', 'single coder').replace('no second coder', 'single coder')
with open('data/coded_evidence.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
shutil.copy('data/coded_evidence.csv', 'data/coded_evidence_v13.csv')
base = {}
for r in csv.DictReader(open('data/coded_evidence.baseline.csv', encoding='utf-8')):
    base[(r['unit'], r['code'])] = r
logp = 'results/coding_change_log.csv'
have = open(logp, encoding='utf-8').read()
with open(logp, 'a', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    for u, c in TARGETS:
        key = u + '/' + c
        if ('\n' + key + ',') not in have:
            w.writerow([key, base[(u, c)]['status'], 'unknown', MSG, ''])
os.makedirs('archive_unused', exist_ok=True)
for p in ['results/agreement.json', 'results/disagreements.csv', 'scripts/agreement.py', 'scripts/disagreements.py']:
    if os.path.exists(p):
        shutil.move(p, 'archive_unused/' + os.path.basename(p))
