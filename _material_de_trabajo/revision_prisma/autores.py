import json, os, time, urllib.request, urllib.parse, re, collections
import xml.etree.ElementTree as ET
os.chdir(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open('03_resultado.json', encoding='utf8'))
F = d['final']
R = {r['clave']: r for r in json.load(open('02_para_cribado.json', encoding='utf8'))['registros']}

# división de los no recuperados
nr = [k for k, v in F.items() if v['etapa'] == 'elegibilidad' and v['decision'] == 'no_recuperado']
sin_oa = sum(1 for k in nr if not (R[k]['oa'] and R[k]['oa_url']))
d['cifras']['no_recuperados_sin_oa'] = sin_oa
d['cifras']['no_recuperados_oa_bloqueado'] = len(nr) - sin_oa

def get(url):
    for i in range(5):
        try:
            with urllib.request.urlopen(url, timeout=40) as r:
                return r.read()
        except Exception as e:
            time.sleep(5 * (i + 1))
    return None

def apa_nombre(n):
    partes = n.split()
    if len(partes) < 2: return n
    return partes[-1]

inc = [k for k, v in F.items() if v['decision'] == 'incluir']
oa_ids = [R[k]['id'].rsplit('/', 1)[-1] for k in inc if R[k]['id'].startswith('https://openalex.org/')]
autores = {}
for i in range(0, len(oa_ids), 50):
    lote = oa_ids[i:i + 50]
    url = 'https://api.openalex.org/works?' + urllib.parse.urlencode({'filter': 'openalex:' + '|'.join(lote), 'per-page': 50,
                                                                        'select': 'id,authorships', 'mailto': 'tesis.prisma@example.org'})
    raw = get(url)
    if raw:
        for w in json.loads(raw)['results']:
            autores[w['id'].rsplit('/', 1)[-1]] = [a['author']['display_name'] for a in w.get('authorships', []) if a.get('author')]
    time.sleep(1.5)
ns = {'a': 'http://www.w3.org/2005/Atom'}
for k in inc:
    r = R[k]
    oid = r['id'].rsplit('/', 1)[-1] if r['id'].startswith('https://openalex.org/') else None
    lista = autores.get(oid) if oid else None
    if not lista and r['id'].startswith('arXiv:'):
        raw = get('http://export.arxiv.org/api/query?id_list=' + r['arxiv'])
        if raw:
            e = ET.fromstring(raw).find('a:entry', ns)
            if e is not None:
                lista = [a.find('a:name', ns).text for a in e.findall('a:author', ns)]
        time.sleep(3)
    lista = lista or []
    F[k]['autores_lista'] = lista
    F[k]['autores'] = (apa_nombre(lista[0]) + (' et al.' if len(lista) > 2 else (' y ' + apa_nombre(lista[1]) if len(lista) == 2 else ''))) if lista else 'Sin autor'
json.dump(d, open('03_resultado.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)
print('no recuperados', len(nr), 'sin OA', sin_oa, 'OA bloqueado', len(nr) - sin_oa)
print('con autores', sum(1 for k in inc if F[k]['autores'] != 'Sin autor'), 'de', len(inc))
print([F[k]['autores'] for k in inc[:8]])
