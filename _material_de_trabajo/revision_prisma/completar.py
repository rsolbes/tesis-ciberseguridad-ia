import json, urllib.request, time
d = json.load(open('02_para_cribado.json', encoding='utf8'))
falta = [r for r in d['registros'] if not r['resumen']]
ids = []
for r in falta:
    if r['doi']: ids.append(('DOI:' + r['doi'], r))
    elif r['arxiv']: ids.append(('ARXIV:' + r['arxiv'].split('v')[0], r))
ok = 0
for i in range(0, len(ids), 100):
    lote = ids[i:i + 100]
    req = urllib.request.Request('https://api.semanticscholar.org/graph/v1/paper/batch?fields=abstract,tldr',
                                 data=json.dumps({'ids': [x for x, _ in lote]}).encode(), headers={'Content-Type': 'application/json'})
    for intento in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp: res = json.load(resp); break
        except Exception as e:
            print('reintento', e); time.sleep(10 * (intento + 1))
    else:
        continue
    for (_, r), s in zip(lote, res):
        if s and s.get('abstract'):
            r['resumen'] = s['abstract']; r['resumen_fuente'] = 'Semantic Scholar'; ok += 1
        elif s and s.get('tldr') and s['tldr'].get('text'):
            r['resumen'] = s['tldr']['text']; r['resumen_fuente'] = 'Semantic Scholar (TLDR)'; ok += 1
    time.sleep(3)
json.dump(d, open('02_para_cribado.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)
print('sin resumen antes', len(falta), '| con identificador', len(ids), '| completados', ok, '| siguen sin resumen', sum(not r['resumen'] for r in d['registros']))
