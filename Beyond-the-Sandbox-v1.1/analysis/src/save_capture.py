"""Extract a browser page-text capture from a tool-result JSON file into a cache text file (verbatim)."""
import json, sys, re
src, out = sys.argv[1], sys.argv[2]
raw = open(src, encoding='utf-8').read()
try:
    j = json.loads(raw); t = ''.join(x.get('text', '') for x in j) if isinstance(j, list) else str(j)
except Exception:
    t = raw
# javascript_tool wraps the string result as a JSON string literal
if t.startswith('"'):
    t = json.JSONDecoder().raw_decode(t)[0]
t = t.split('\n<<<PAD>>>\n')[0]
open(out, 'w', encoding='utf-8', newline='\n').write(t.rstrip() + '\n')
print(out, len(t))
