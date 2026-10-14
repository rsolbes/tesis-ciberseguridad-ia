import json, re, os, html, urllib.request, concurrent.futures as cf, collections
res = json.load(open('descargas.json', encoding='utf8'))
R = {r['clave']: r for r in json.load(open('02_para_cribado.json', encoding='utf8'))['registros']}
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml'}
def limpiar(h):
    h = re.sub(r'(?is)<(script|style|nav|header|footer|noscript)[^>]*>.*?</\1>', ' ', h)
    t = html.unescape(re.sub(r'(?s)<[^>]+>', ' ', h))
    return re.sub(r'\s+', ' ', t)
def intentar(clave):
    r = R[clave]
    urls = [u for u in [r['oa_url'], ('https://doi.org/' + r['doi']) if r['doi'] else ''] if u]
    for u in urls:
        try:
            req = urllib.request.Request(u, headers=UA)
            with urllib.request.urlopen(req, timeout=40) as resp:
                data = resp.read(); final = resp.geturl(); ct = resp.headers.get('Content-Type', '')
        except Exception:
            continue
        if 'html' not in ct.lower(): continue
        t = limpiar(data.decode('utf8', 'ignore'))
        # un artículo completo tiene secciones típicas y bastante texto
        secciones = sum(1 for s in ('introduction', 'conclusion', 'references', 'method', 'results') if s in t.lower())
        if len(t) > 25000 and secciones >= 3:
            with open(f'textos/{clave}.txt', 'w', encoding='utf8') as f:
                f.write(f'FUENTE: {final}\nPAGINAS: html\n\n' + t[:60000])
            return clave, 'ok_html', final
    return clave, 'no', ''
faltan = [c for c, e, _ in res if e == 'no']
with cf.ThreadPoolExecutor(max_workers=6) as ex:
    out = list(ex.map(intentar, faltan))
d = {c: (e, u) for c, e, u in res}
for c, e, u in out: d[c] = (e, u)
json.dump([[c, e, u] for c, (e, u) in d.items()], open('descargas.json', 'w', encoding='utf8'), indent=0)
print('reintentos', len(faltan), collections.Counter(e for _, e, _ in out))
print('dominios no recuperados', collections.Counter(re.sub(r'^https?://([^/]+).*', r'\1', R[c]['oa_url']) for c, e, _ in out if e == 'no').most_common(12))
