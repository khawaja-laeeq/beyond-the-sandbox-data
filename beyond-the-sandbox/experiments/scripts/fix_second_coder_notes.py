"""Replace 'no second coder' in qualification notes with the AI-second-coder wording."""
import sys
p = sys.argv[1]
t = open(p, encoding="utf-8").read()
n = t.count("no second coder")
open(p, "w", encoding="utf-8").write(t.replace("no second coder", "AI second coder (codex)"))
print("replaced", n)
