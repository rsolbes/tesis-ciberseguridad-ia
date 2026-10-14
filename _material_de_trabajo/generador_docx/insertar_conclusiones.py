"""Sustituye las indicaciones de la plantilla en el capítulo VIII por las conclusiones redactadas."""
import os, re, shutil, sys, zipfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wlib
from wlib import p, h

ORIG, OUT = sys.argv[1], sys.argv[2]
W = os.path.join(HERE, 'avance_z')
shutil.rmtree(W, ignore_errors=True)
with zipfile.ZipFile(ORIG) as z:
    z.extractall(W)
    orden = z.namelist()
docp = os.path.join(W, 'word', 'document.xml')
x = open(docp, encoding='utf8').read()
txt = lambda s: ''.join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', s))

ps = list(re.finditer(r'<w:p\b[^>]*/>|<w:p\b[^>]*>.*?</w:p>', x, re.S))
ini = [k for k, m in enumerate(ps) if 'Conclusiones y Recomendaciones' in txt(m.group(0)) and 'Ttulo1' in m.group(0)]
assert len(ini) == 1
i = ini[0]
fin = next(k for k in range(i + 1, len(ps)) if 'sectPr' in ps[k].group(0))
assert 'Conclusiones de cada objetivo' in txt(ps[i + 1].group(0)), txt(ps[i + 1].group(0))
assert 'Referencias' in txt(ps[fin + 1].group(0))

wlib._bm[0] = max(int(n) for n in re.findall(r'<w:bookmarkStart w:id="(\d+)"', x)) + 10
bloques = []
for ln in open(os.path.join(HERE, 'conclusiones.txt'), encoding='utf8').read().split('\n'):
    s = ln.strip()
    if not s:
        continue
    if s.startswith('### '): bloques.append(h(3, s[4:]))
    elif s.startswith('## '): bloques.append(h(2, s[3:]))
    else: bloques.append(p(s))

x = x[:ps[i + 1].start()] + ''.join(bloques) + x[ps[fin].start():]
open(docp, 'w', encoding='utf8').write(x)

with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    hechos = set()
    for n in orden:
        f = os.path.join(W, n)
        if os.path.isfile(f):
            z.write(f, n); hechos.add(n)
    for raiz, _, archivos in os.walk(W):
        for a in archivos:
            n = os.path.relpath(os.path.join(raiz, a), W).replace(os.sep, '/')
            if n not in hechos:
                z.write(os.path.join(raiz, a), n)
print('ok', len(bloques), 'bloques')
