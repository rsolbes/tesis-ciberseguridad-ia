import json, glob, collections
def jl(pat):
    d = {}
    for f in sorted(glob.glob(pat)):
        for l in open(f, encoding='utf8'):
            if l.strip():
                x = json.loads(l); d[x['clave']] = x
    return d
crib = jl('decisiones/lote_*.jsonl')
e1 = jl('elegibilidad/lote_*.jsonl')
e2 = jl('elegibilidad2/lote_*.jsonl')
base = json.load(open('02_para_cribado.json', encoding='utf8'))
R = {r['clave']: r for r in base['registros']}
RECLAS = {'R0762': 'Defensor con optimización bayesiana, sin LLM ni RL', 'R0288': 'Pipeline de ML determinista etiquetado como agéntico',
          'R0443': 'Agente de RL usado solo como clasificador'}
final = {}
for k, c in crib.items():
    if c['decision'] == 'excluir':
        final[k] = {'etapa': 'cribado', 'decision': 'excluir', 'criterio': c['criterio']}
        continue
    if k in e2: x = dict(e2[k])
    elif k in e1 and e1[k]['decision'] in ('incluir', 'excluir'): x = dict(e1[k])
    else: x = {'decision': 'no_recuperado', 'criterio': 'NR'}
    if k in RECLAS and x['decision'] == 'incluir':
        x.update(decision='excluir', criterio='E6', nota_revisor=RECLAS[k])
    x['etapa'] = 'elegibilidad'; x['tema_cribado'] = c['tema']
    final[k] = x
C = collections.Counter
cr = [v for v in final.values() if v['etapa'] == 'cribado']
el = [v for v in final.values() if v['etapa'] == 'elegibilidad']
nr = [v for v in el if v['decision'] == 'no_recuperado']
ev = [v for v in el if v['decision'] != 'no_recuperado']
inc = {k: v for k, v in final.items() if v['decision'] == 'incluir'}
sin_oa = sum(1 for k, v in final.items() if v['etapa'] == 'elegibilidad' and v['decision'] == 'no_recuperado' and not (R[k]['oa'] and R[k]['oa_url']))
cifras = {
    'identificados': base['identificados'], 'duplicados': base['duplicados'], 'fuera_tipo': base['fuera_tipo'], 'fuera_idioma': base['fuera_idioma'],
    'cribados': len(final), 'excluidos_cribado': len(cr), 'excluidos_cribado_por': C(v['criterio'] for v in cr),
    'buscados': len(el), 'no_recuperados': len(nr), 'no_recuperados_sin_oa': sin_oa, 'no_recuperados_oa_bloqueado': len(nr) - sin_oa,
    'evaluados': len(ev), 'excluidos_elegibilidad_por': C(v['criterio'] for v in ev if v['decision'] == 'excluir'), 'incluidos': len(inc),
}
json.dump({'cifras': cifras, 'final': final}, open('03_resultado.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0, default=dict)
for k, v in cifras.items(): print(k, dict(v) if isinstance(v, collections.Counter) else v)
print('tema', C(v.get('tema') for v in inc.values()))
print('tipo_estudio', C(v.get('tipo_estudio') for v in inc.values()))
print('tecnologia', C(v.get('tecnologia') for v in inc.values()))
print('criterio', C(v.get('criterio') for v in inc.values()))
print('poblacion (educacion)', C(v.get('poblacion') for v in inc.values() if v.get('tema') == 'educacion'))
print('anio', sorted(C(R[k]['anio'] for k in inc).items()))
print('tipo pub', C(R[k]['tipo'] for k in inc))
