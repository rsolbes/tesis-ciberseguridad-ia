import json, re, unicodedata, collections
d = json.load(open('01_identificados.json', encoding='utf8'))
R = d['registros']
def norm(t):
    t = unicodedata.normalize('NFD', (t or '').lower())
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]+', ' ', t).strip()
def arx(r):
    if r['arxiv']: return r['arxiv'].split('v')[0].replace('arxiv:', '').lower()
    m = re.search(r'10\.48550/arxiv\.([\d.]+)', r['doi'])
    return m.group(1) if m else ''
# prioridad: publicado en revista/conferencia > preprint; OpenAlex > arXiv
def prioridad(r):
    return (0 if r['tipo'] not in ('preprint',) and r['venue_tipo'] not in ('repository',) else 1, 0 if r['fuente'] == 'OpenAlex' else 1, 0 if r['resumen'] else 1)
grupos, clave_grupo = [], {}
for r in R:
    claves = [k for k in ('doi:' + r['doi'] if r['doi'] else '', 'ax:' + arx(r) if arx(r) else '', 'ti:' + norm(r['titulo'])) if k and k != 'ti:']
    g = next((clave_grupo[k] for k in claves if k in clave_grupo), None)
    if g is None:
        g = len(grupos); grupos.append([])
    grupos[g].append(r)
    for k in claves: clave_grupo[k] = g
unicos = []
for g in grupos:
    g.sort(key=prioridad)
    base = dict(g[0]); base['cadenas'] = sorted({x['cadena'] for x in g}); base['fuentes'] = sorted({x['fuente'] for x in g})
    base['versiones'] = len(g)
    if not base['resumen']:
        base['resumen'] = next((x['resumen'] for x in g if x['resumen']), '')
    unicos.append(base)
dup = len(R) - len(unicos)
TIPOS_NO = {'paratext', 'erratum', 'retraction', 'dataset', 'editorial', 'letter', 'peer-review', 'dissertation', 'report', 'standard', 'grant', 'other', 'supplementary-materials', 'book', 'software', 'software-paper', 'conference-abstract'}
fuera_tipo = [u for u in unicos if u['tipo'] in TIPOS_NO]
fuera_idioma = [u for u in unicos if u not in fuera_tipo and u['idioma'] not in (None, 'en', 'es')]
quedan = [u for u in unicos if u not in fuera_tipo and u not in fuera_idioma]
for i, u in enumerate(quedan): u['clave'] = f'R{i+1:04d}'
json.dump({'fecha_busqueda': d['fecha_busqueda'], 'identificados': {'OpenAlex': sum(r['fuente'] == 'OpenAlex' for r in R), 'arXiv': sum(r['fuente'] == 'arXiv' for r in R)},
           'duplicados': dup, 'fuera_tipo': len(fuera_tipo), 'fuera_idioma': len(fuera_idioma), 'tipos_excluidos': collections.Counter(u['tipo'] for u in fuera_tipo),
           'registros': quedan}, open('02_para_cribado.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)
print('identificados', len(R), '| duplicados', dup, '| unicos', len(unicos))
print('fuera por tipo', len(fuera_tipo), collections.Counter(u['tipo'] for u in fuera_tipo))
print('fuera por idioma', len(fuera_idioma), collections.Counter(u['idioma'] for u in fuera_idioma))
print('para cribado', len(quedan), '| sin resumen', sum(not u['resumen'] for u in quedan))
print('por cadena', collections.Counter(tuple(u['cadenas']) for u in quedan))
print('tipos', collections.Counter(u['tipo'] for u in quedan))
