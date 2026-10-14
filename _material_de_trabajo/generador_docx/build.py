import re, shutil, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from wlib import *
from data import TABLES, REFS, RESUMEN, ABSTRACT, KW_ES, KW_EN, TITLE

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'tpl')
OUT = os.path.join(HERE, 'out')
if os.path.exists(OUT):
    shutil.rmtree(OUT)
shutil.copytree(SRC, OUT)

docp = os.path.join(OUT, 'word', 'document.xml')
x = open(docp, encoding='utf8').read()
b = x.find('<w:body>')
pat = re.compile(r'<w:p\b[^>]*/>|<w:p\b[^>]*>.*?</w:p>|<w:tbl>.*?</w:tbl>', re.S)
spans = [(m.start(), m.end()) for m in pat.finditer(x, b)]
els = [x[s:e] for s, e in spans]

def set_text(el, new, keep=0):
    """Put `new` in the (keep)-th <w:t>, empty all later ones."""
    ts = list(re.finditer(r'<w:t(?: [^>]*)?>[^<]*</w:t>', el))
    out, pos = [], 0
    for i, m in enumerate(ts):
        out.append(el[pos:m.start()])
        if i < keep:
            out.append(m.group(0))
        elif i == keep:
            out.append(f'<w:t xml:space="preserve">{escape(new)}</w:t>')
        else:
            out.append('<w:t></w:t>')
        pos = m.end()
    out.append(el[pos:])
    return ''.join(out)

def expect(i, s):
    t = ''.join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', els[i]))
    assert s in t, (i, t[:80])

# ---- cover
expect(10, 'Título pertinente'); els[10] = set_text(els[10], TITLE)
expect(13, 'Ingeniero Civil'); els[13] = set_text(els[13], 'Ingeniero en Sistemas Computacionales')
expect(16, 'Nombre'); els[16] = set_text(els[16], 'Rodrigo Solbes Davalos')
expect(19, 'Nombre'); els[19] = set_text(els[19], 'Dr. Eduardo Álvarez Navarro')
expect(22, 'Nombres'); els[22] = set_text(els[22], 'Dr. Gabriel Chavira Juárez')
expect(24, 'Asesor'); els[24] = set_text(els[24], 'Asesora')
expect(25, 'Nombres'); els[25] = set_text(els[25], 'Dra. Adriana Montoto González')
expect(32, 'Mes, Año'); els[32] = els[32].replace('Mes, Año.', 'septiembre, 2026.')
for _ in range(2):  # longer date than the template placeholder: drop two tab stops
    k = els[32].rfind('<w:tab/></w:r>')
    st = els[32].rfind('<w:r ', 0, k)
    els[32] = els[32][:st] + els[32][k + len('<w:tab/></w:r>'):]
# template bug: heading-3 numbering only restarts at heading 1
nump = os.path.join(OUT, 'word', 'numbering.xml')
n = open(nump, encoding='utf8').read()
m = re.search(r'<w:abstractNum [^>]*w:abstractNumId="11".*?</w:abstractNum>', n, re.S)
fixed = m.group(0).replace('<w:lvlRestart w:val="1"/><w:pStyle w:val="Ttulo3"/>', '<w:pStyle w:val="Ttulo3"/>')
assert fixed != m.group(0)
open(nump, 'w', encoding='utf8').write(n.replace(m.group(0), fixed))

# ---- resumen / abstract
expect(97, 'El resumen deberá'); els[97] = set_text(els[97], RESUMEN)
expect(99, 'Palabras clave'); els[99] = set_text(els[99], KW_ES, keep=2)
expect(103, 'The monitoring'); els[103] = set_text(els[103], ABSTRACT)
expect(105, 'Key words'); els[105] = set_text(els[105], KW_EN, keep=2)

# ---- body (Introducción .. end of Metodología)
expect(108, 'Introducción'); expect(153, 'Metodología'); assert 'sectPr' in els[163]
expect(164, 'Resultados')

rels_p = os.path.join(OUT, 'word', '_rels', 'document.xml.rels')
rels = open(rels_p, encoding='utf8').read()
FIGS = {}
from PIL import Image
for n, key in enumerate(['agente', 'fases', 'corpus', 'roadmap']):
    fname = key + '.png'
    rid = f'rIdTesis{n+1}'
    shutil.copy(os.path.join(HERE, 'fig', fname), os.path.join(OUT, 'word', 'media', 'tesis_' + fname))
    rels = rels.replace('</Relationships>',
        f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/tesis_{fname}"/></Relationships>')
    w, hgt = Image.open(os.path.join(HERE, 'fig', fname)).size
    cx = 5580000  # ~15.5 cm
    cy = int(cx * hgt / w)
    FIGS[key] = image(rid, cx, cy, 5000 + n, f'Figura tesis {n+1}')
open(rels_p, 'w', encoding='utf8').write(rels)

def render(fname):
    out = []
    for ln in open(os.path.join(HERE, fname), encoding='utf8').read().split('\n'):
        s = ln.strip()
        if not s:
            continue
        if s.startswith('### '): out.append(h(3, s[4:]))
        elif s.startswith('## '): out.append(h(2, s[3:]))
        elif s.startswith('# '): out.append(h(1, s[2:]))
        elif s.startswith('- '): out.append(bullet(s[2:]))
        elif re.match(r'^\d\) ', s): out.append(numbered(s[0], s[3:]))
        elif s == '@SECT': out.append(SECT)
        elif s.startswith('@FIG:'): out.append(FIGS[s[5:]])
        elif s.startswith('@CAP:'):
            kind, txt = s[5:].split('|', 1); out.append(caption(kind, txt))
        elif s.startswith('@SRC:'):
            txt = s[5:]; center = txt.endswith('|center')
            out.append(source(txt.replace('|center', ''), center))
        elif s.startswith('@TABLE:'):
            t = TABLES[s[7:]]; out.append(table(t['h'], t['r'], t['w']))
        elif s.startswith('@ANX:'):
            num, txt = s[5:].split('|', 1)
            out.append('<w:p><w:pPr><w:pStyle w:val="Sinespaciado"/><w:keepNext/><w:spacing w:before="240" w:after="120"/></w:pPr>'
                       + runs('**' + num + '** ' + txt) + '</w:p>')
        elif s.startswith('@NOTE:'):
            out.append('<w:p><w:pPr><w:pStyle w:val="Sinespaciado"/><w:keepNext/><w:spacing w:after="120"/><w:jc w:val="both"/></w:pPr>'
                       + runs(s[6:]) + '</w:p>')
        else:
            out.append(p(s))
    return out

body = render('content.txt')
assert body[-1] == SECT
body[-1] = els[163]          # original section break of the Metodología section

expect(164, 'Resultados'); assert 'sectPr' in els[179]; expect(180, 'Conclusiones')
resultados = render('results.txt')
assert resultados[-1] == SECT
resultados[-1] = els[179]

expect(197, 'Anexos'); expect(198, 'Anexo 1'); expect(200, 'Fuente')
anexos = render('annex.txt')

# ---- references
expect(191, 'Referencias'); expect(193, 'APA 7')
refs_xml = ''.join(reference(r) for r in REFS)

REPLACE = {108: ''.join(body), 164: ''.join(resultados), 192: refs_xml, 198: ''.join(anexos)}
DROP = set(range(109, 164)) | set(range(165, 180)) | {193, 194, 195} | {199, 200}

# rebuild: keep inter-element text (e.g. sectPr at body end, bookmarks between paragraphs)
res = [x[:spans[0][0]]]
for i, (s_, e) in enumerate(spans):
    if i in REPLACE:
        res.append(REPLACE[i])
    elif i not in DROP:
        res.append(els[i])
    nxt = spans[i + 1][0] if i + 1 < len(spans) else len(x)
    res.append(x[e:nxt])
x2 = ''.join(res)
# drop orphaned bookmarks
starts = set(re.findall(r'<w:bookmarkStart w:id="(\d+)"', x2))
ends = set(re.findall(r'<w:bookmarkEnd w:id="(\d+)"', x2))
for i in starts - ends:
    x2 = re.sub(r'<w:bookmarkStart w:id="%s"[^>]*/>' % i, '', x2)
for i in ends - starts:
    x2 = re.sub(r'<w:bookmarkEnd w:id="%s"[^>]*/>' % i, '', x2)
print('orphans removed', starts ^ ends)
open(docp, 'w', encoding='utf8').write(x2)
print('ok', len(x), '->', len(x2))
