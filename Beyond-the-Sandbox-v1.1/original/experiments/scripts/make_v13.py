import csv
from collections import Counter

rows = list(csv.DictReader(open('data/coded_evidence_v12.csv')))
D2_UNKNOWN = {('INC-OAI-ART', 'D2'), ('INC-OAI-HF', 'D2')}
UNCHK = {('INC-OAI-HF', 'D1'), ('INC-AISI-SOL', 'D5')}
out = []
for r in rows:
    k = (r['unit'], r['code'])
    st = r['status']
    note = []
    if k in D2_UNKNOWN:
        st = 'unknown'
        note.append('D2 rule (analyst): source (METR, R07) states a scorer objective, not the agent belief about permission -> unknown')
    # results/quote_check.json: 0 quotes NOT_FOUND, so no recode under reason (1)
    if st == 'unknown':
        support = 'n/a'
    else:
        support = 'inferred' if r['evidence_class'] == 'I' else 'direct'
    r2 = dict(r)
    r2['status'] = st
    r2['support_type'] = support
    r2['not_independently_checked'] = 'yes' if k in UNCHK else 'no'
    r2['v13_note'] = '; '.join(note)
    r2['applied_by'] = 'analyst (single party, not independent adjudication)' if note else ''
    out.append(r2)

fields = list(out[0].keys())
with open('data/coded_evidence_v13.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fields)
    w.writeheader()
    w.writerows(out)


def cnt(rs):
    return dict(Counter((x['status'], x['support_type']) for x in rs))


print('all', len(out), cnt(out))
s = [x for x in out if x['not_independently_checked'] == 'no']
print('sensitivity excluding R01/R24-only cells n=', len(s), cnt(s))
