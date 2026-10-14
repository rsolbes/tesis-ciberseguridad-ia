import re,sys
x=open('tpl/word/document.xml',encoding='utf8').read()
b=x.find('<w:body>')
pat=re.compile(r'<w:p\b[^>]*/>|<w:p\b[^>]*>.*?</w:p>|<w:tbl>.*?</w:tbl>',re.S)
els=[(m.start(),m.group(0)) for m in pat.finditer(x,b)]
if sys.argv[1]=='list':
  for i,(s,p) in enumerate(els):
    t=''.join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>',p))
    st=re.search(r'<w:pStyle w:val="([^"]+)"',p)
    print(i,s,(st.group(1) if st else '-'),'SECT' if 'sectPr' in p else '',t[:70].encode('ascii','replace').decode())
else:
  for a in sys.argv[1:]:
    print('-----',a); print(els[int(a)][1][:int(4000)])
