import sys, html.parser, re
class P(html.parser.HTMLParser):
    def __init__(s): super().__init__(); s.out=[]; s.skip=0
    def handle_starttag(s,t,a):
        if t in('script','style','noscript','svg'): s.skip+=1
        if t in('p','br','div','li','h1','h2','h3','h4','tr','section','article'): s.out.append('\n')
    def handle_endtag(s,t):
        if t in('script','style','noscript','svg') and s.skip: s.skip-=1
    def handle_data(s,d):
        if not s.skip: s.out.append(d)
t=open(sys.argv[1],encoding='utf-8',errors='replace').read()
p=P(); p.feed(t); x=''.join(p.out)
x=re.sub(r'[ \t\r\f\v]+',' ',x); x=re.sub(r'\n\s*\n+','\n\n',x)
open(sys.argv[2], 'w', encoding='utf-8').write(x.strip() + '\n')
