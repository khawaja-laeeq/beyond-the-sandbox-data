import csv, shutil
d = 'experiments/data/'
shutil.copy(d + 'coded_evidence.csv', d + 'coded_evidence_v12.csv')
b = {(r['unit'], r['code']): r for r in csv.DictReader(open(d + 'coded_evidence.baseline.csv'))}
n = {(r['unit'], r['code']): r for r in csv.DictReader(open(d + 'coded_evidence.csv'))}
w = csv.writer(open('experiments/results/coding_change_log.csv', 'w', newline=''))
w.writerow(['row', 'old', 'new', 'reason', 'anchor'])
for k, r in n.items():
    o = b[k]
    if o['status'] != r['status'] or o['evidence'] != r['evidence']:
        w.writerow([k[0] + '/' + k[1], o['status'], r['status'], r['change_log'], r['anchor_checks']])
print(open('experiments/results/coding_change_log.csv').read())
