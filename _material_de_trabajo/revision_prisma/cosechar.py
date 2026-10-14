import urllib.request, urllib.parse, json, time, re, datetime
import xml.etree.ElementTree as ET
from consultas import OPENALEX, ARXIV

def get(url, t=60):
    for i in range(6):
        try:
            with urllib.request.urlopen(url, timeout=t) as r: return r.read()
        except Exception as e:
            print('reintento', i, e); time.sleep(6 * (i + 1))
    raise RuntimeError(url)

def resumen(inv):
    if not inv: return ''
    pos = []
    for w, ps in inv.items():
        for p in ps: pos.append((p, w))
    return ' '.join(w for _, w in sorted(pos))

registros = []
for cadena, filt in OPENALEX.items():
    cursor = '*'
    while cursor:
        q = {'filter': filt, 'per-page': '200', 'cursor': cursor, 'mailto': 'tesis.prisma@example.org',
             'select': 'id,doi,title,publication_year,publication_date,type,language,primary_location,best_oa_location,open_access,abstract_inverted_index,ids'}
        j = json.loads(get('https://api.openalex.org/works?' + urllib.parse.urlencode(q)))
        for w in j['results']:
            pl = w.get('primary_location') or {}
            src = (pl.get('source') or {})
            boa = w.get('best_oa_location') or {}
            registros.append({
                'fuente': 'OpenAlex', 'cadena': cadena, 'id': w['id'], 'doi': (w.get('doi') or '').replace('https://doi.org/', '').lower(),
                'arxiv': ((w.get('ids') or {}).get('arxiv') or ''), 'titulo': w.get('title') or '', 'anio': w.get('publication_year'),
                'fecha': w.get('publication_date'), 'tipo': w.get('type'), 'idioma': w.get('language'),
                'venue': src.get('display_name') or '', 'venue_tipo': src.get('type') or '',
                'oa': (w.get('open_access') or {}).get('is_oa'), 'oa_url': boa.get('pdf_url') or boa.get('landing_page_url') or (w.get('open_access') or {}).get('oa_url') or '',
                'resumen': resumen(w.get('abstract_inverted_index')),
            })
        cursor = j['meta'].get('next_cursor')
        if not j['results']: break
        time.sleep(1.5)
    print('OpenAlex', cadena, sum(1 for r in registros if r['cadena'] == cadena and r['fuente'] == 'OpenAlex'))

ns = {'a': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}
for cadena, q in ARXIV.items():
    inicio, total = 0, 0
    while True:
        url = 'http://export.arxiv.org/api/query?' + urllib.parse.urlencode({'search_query': q, 'start': inicio, 'max_results': 100, 'sortBy': 'submittedDate', 'sortOrder': 'descending'})
        root = ET.fromstring(get(url))
        entradas = root.findall('a:entry', ns)
        if not entradas: break
        for e in entradas:
            pub = e.find('a:published', ns).text[:10]
            if not ('2022-01-01' <= pub <= '2026-09-30'): continue
            aid = e.find('a:id', ns).text.rsplit('/abs/', 1)[-1]
            doi = e.find('arxiv:doi', ns)
            registros.append({'fuente': 'arXiv', 'cadena': cadena, 'id': 'arXiv:' + aid, 'doi': (doi.text.lower() if doi is not None else ''),
                              'arxiv': aid, 'titulo': ' '.join(e.find('a:title', ns).text.split()), 'anio': int(pub[:4]), 'fecha': pub,
                              'tipo': 'preprint', 'idioma': 'en', 'venue': 'arXiv', 'venue_tipo': 'repository', 'oa': True,
                              'oa_url': 'https://arxiv.org/abs/' + aid, 'resumen': ' '.join(e.find('a:summary', ns).text.split())})
            total += 1
        inicio += 100
        time.sleep(4)
    print('arXiv', cadena, total)

json.dump({'fecha_busqueda': datetime.date.today().isoformat(), 'registros': registros}, open('01_identificados.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)
print('total', len(registros))
