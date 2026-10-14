import json, glob, os, re, time, urllib.request, urllib.parse, concurrent.futures as cf
import pymupdf
hechos = {}
for f in glob.glob('elegibilidad/lote_*.jsonl'):
    for l in open(f, encoding='utf8'):
        if l.strip():
            x = json.loads(l); hechos[x['clave']] = x
pend = []
for f in sorted(glob.glob('lotes_eleg/lote_*.json')):
    for r in json.load(open(f, encoding='utf8')):
        if r['clave'] not in hechos or hechos[r['clave']]['decision'] == 'no_recuperado':
            pend.append(r)
R = {r['clave']: r for r in json.load(open('02_para_cribado.json', encoding='utf8'))['registros']}
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36 (tesis PRISMA; mailto:tesis.prisma@example.org)'}

def get(url, t=40):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=t) as r:
        return r.read(), r.headers.get('Content-Type', ''), r.geturl()

def candidatos(r):
    full = R[r['clave']]
    urls = []
    ax = r.get('arxiv') or ''
    m = re.search(r'10\.48550/arxiv\.([\d.]+)', full['doi']) or re.search(r'arxiv\.org/(?:abs|pdf)/([\d.]+)', full['oa_url'] or '')
    if not ax and m: ax = m.group(1)
    if ax: urls.append(f'https://arxiv.org/pdf/{ax}')
    # ubicaciones de OpenAlex
    if full['fuente'] == 'OpenAlex' and full['id'].startswith('https://openalex.org/'):
        try:
            j = json.loads(get('https://api.openalex.org/works/' + full['id'].rsplit('/', 1)[-1] + '?select=locations,best_oa_location&mailto=tesis.prisma@example.org')[0])
            for loc in [j.get('best_oa_location') or {}] + (j.get('locations') or []):
                if loc and loc.get('pdf_url'): urls.append(loc['pdf_url'])
        except Exception: pass
    # Semantic Scholar
    if full['doi'] and not full['doi'].startswith('10.48550'):
        try:
            j = json.loads(get('https://api.semanticscholar.org/graph/v1/paper/DOI:' + full['doi'] + '?fields=openAccessPdf,externalIds')[0])
            if (j.get('openAccessPdf') or {}).get('url'): urls.append(j['openAccessPdf']['url'])
            axid = (j.get('externalIds') or {}).get('ArXiv')
            if axid: urls.insert(0, f'https://arxiv.org/pdf/{axid}')
        except Exception: pass
    if full['oa_url']: urls.append(full['oa_url'])
    vistos, out = set(), []
    for u in urls:
        if u and u not in vistos: vistos.add(u); out.append(u)
    return out

def procesar(r):
    destino = f"textos/{r['clave']}.txt"
    if os.path.exists(destino): return r['clave'], 'ya', ''
    for u in candidatos(r):
        try:
            data, ct, final = get(u)
        except Exception as e:
            continue
        texto = ''
        if data[:4] == b'%PDF' or 'pdf' in ct.lower():
            try:
                doc = pymupdf.open(stream=data, filetype='pdf')
                texto = '\n'.join(p.get_text() for p in doc)
                paginas = len(doc)
            except Exception:
                continue
        else:
            continue          # páginas HTML de editoriales suelen no traer el texto completo
        if len(texto) > 4000:
            with open(destino, 'w', encoding='utf8') as f:
                f.write(f'FUENTE: {u}\nPAGINAS: {paginas}\n\n' + texto[:60000])
            return r['clave'], 'ok', u
    return r['clave'], 'no', ''

res = []
with cf.ThreadPoolExecutor(max_workers=6) as ex:
    for i, out in enumerate(ex.map(procesar, pend)):
        res.append(out)
        if i % 25 == 0: print(i, out, flush=True)
json.dump(res, open('descargas.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)
import collections
print('pendientes', len(pend), collections.Counter(x[1] for x in res))
