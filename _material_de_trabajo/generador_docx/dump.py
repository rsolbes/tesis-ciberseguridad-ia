import re,sys
x=open(sys.argv[1],encoding='utf8').read()
body=x[x.find('<w:body>'):]
# split top-level elements roughly by paragraphs and tables
i=0
for m in re.finditer(r'<w:p[ >].*?</w:p>|<w:tbl>',body,re.S):
    p=m.group(0)
    if p=='<w:tbl>': print(i,'[TABLE]'); i+=1; continue
    st=re.search(r'<w:pStyle w:val="([^"]+)"',p)
    t=''.join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>',p))
    extra=''
    if 'w:sectPr' in p: extra+=' [SECT]'
    if 'w:drawing' in p or 'v:shape' in p: extra+=' [IMG]'
    if 'w:br w:type="page"' in p: extra+=' [PB]'
    if 'fldChar' in p or 'instrText' in p: extra+=' [FLD]'
    print(i,(st.group(1) if st else '-'),extra,'|',t[:160])
    i+=1
