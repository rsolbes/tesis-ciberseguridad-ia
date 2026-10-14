import json, os, collections
os.chdir(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open('03_resultado.json', encoding='utf8'))
F, O, cif = d['final'], d['otros'], d['cifras']
R = {r['clave']: r for r in json.load(open('02_para_cribado.json', encoding='utf8'))['registros']}

def fix(n):
    return ' '.join(p.capitalize() if p.isupper() and len(p) > 2 else p for p in n.split())

estudios = []
for k, v in F.items():
    if v['decision'] != 'incluir': continue
    r = R[k]
    revisado = not (r['tipo'] == 'preprint' or r['venue_tipo'] == 'repository')
    estudios.append({'clave': k, 'autores': fix(v['autores']), 'anio': r['anio'], 'titulo': r['titulo'], 'venue': r['venue'] or 'arXiv',
                     'doi': r['doi'], 'url': r['oa_url'], 'revisado': revisado, 'tipo_pub': r['tipo'], 'origen': 'bases de datos',
                     **{c: v.get(c, '') for c in ('tema', 'tipo_estudio', 'tecnologia', 'poblacion', 'hallazgo')}})
for k, v in O.items():
    if v['decision'] != 'incluir': continue
    estudios.append({'clave': k, 'autores': v['autores'], 'anio': v['anio'], 'titulo': v['titulo'], 'venue': v['venue'], 'doi': '',
                     'url': '', 'revisado': v['venue'] not in ('arXiv', 'Preprints'), 'tipo_pub': 'otros', 'origen': 'otros métodos',
                     **{c: v.get(c, '') for c in ('tema', 'tipo_estudio', 'tecnologia', 'poblacion', 'hallazgo')}})
estudios.sort(key=lambda e: (e['tema'], -e['anio'], e['autores']))
json.dump(estudios, open('04_incluidos.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)

C = collections.Counter
N = len(estudios)
pct = lambda n: f'{100 * n / N:.1f}'
print('N', N)
for campo in ('tema', 'tipo_estudio', 'tecnologia', 'anio', 'revisado', 'origen'):
    c = C(e[campo] for e in estudios)
    print(campo, sorted(((k, n, pct(n)) for k, n in c.items()), key=lambda x: -x[1]))
edu = [e for e in estudios if e['tema'] == 'educacion']
print('educacion', len(edu), C(e['poblacion'] for e in edu), C(e['tecnologia'] for e in edu), C(e['tipo_estudio'] for e in edu))
print('tema x anio', sorted(C((e['anio'], e['tema']) for e in estudios).items()))
print('2025-2026', sum(e['anio'] >= 2025 for e in estudios), pct(sum(e['anio'] >= 2025 for e in estudios)))
print('experimental por tema', C(e['tema'] for e in estudios if e['tipo_estudio'] == 'experimental'))
for e in edu:
    print(' EDU', e['clave'], e['poblacion'], e['tecnologia'], e['anio'], e['titulo'][:90])
