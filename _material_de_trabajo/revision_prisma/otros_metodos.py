import json, collections, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open('03_resultado.json', encoding='utf8'))
F = d['final']
F['R0532']['tema'] = 'educacion'

def inc(k, criterio, tema, tipo, tec, pob, hall):
    F[k].update(decision='incluir', criterio=criterio, tema=tema, tipo_estudio=tipo, tecnologia=tec, poblacion=pob, hallazgo=hall,
                fuente_leida='PDF del corpus inicial', recuperado_por='texto completo aportado por el investigador')

inc('R0098', 'IA', 'defensa', 'experimental', 'rl', 'no_aplica', 'Agente de RL en CybORG reporta 11.8 % de compromiso frente a 28.4 % heurístico; resultados poco verificables.')
inc('R0231', 'IA', 'ofensiva', 'revision_narrativa', 'mixta', 'no_aplica', 'Tutorial y revisión de agentes LLM para descubrir vulnerabilidades; propone un flujo de cuatro fases con supervisión humana.')
inc('R0508', 'IB', 'educacion', 'experimental', 'llm_sin_agencia', 'universidad', 'Une detección con red neuronal y asistente local con RAG; satisfacción de 4.3 sobre 5 en talleres universitarios.')
F['R0677'].update(decision='excluir', criterio='E8', nota_revisor='Preprint de R0508 (SentinelSphere)',
                  recuperado_por='texto completo aportado por el investigador')

OTROS = [
    ('O01', 'Oesch et al.', 2024, 'The path to autonomous cyber defense', 'arXiv', 'incluir', 'IA', 'defensa', 'posicion', 'rl',
     'Ruta hacia agentes de ciberdefensa con RL; propone agentes especializados por etapa del ciclo de defensa.'),
    ('O02', 'Deng et al.', 2024, 'AI agents under threat: A survey of key security challenges and future pathways', 'arXiv', 'incluir', 'IA',
     'seguridad_agentes', 'revision_narrativa', 'llm_agente', 'Organiza las amenazas contra agentes en cuatro brechas de conocimiento a partir de más de cien trabajos.'),
    ('O03', 'Potter et al.', 2025, "Frontier AI's impact on the cybersecurity landscape", 'arXiv', 'incluir', 'IA', 'general', 'experimental',
     'llm_agente', 'Benchmarks, evaluación y encuesta a expertos indican que hoy la IA favorece más al ataque que a la defensa.'),
    ('O04', 'Schroeder de Witt et al.', 2026, 'Open challenges in multi-agent security: Towards secure systems of interacting AI agents', 'arXiv',
     'incluir', 'IA', 'seguridad_agentes', 'posicion', 'multiagente_llm', 'Propone la seguridad multiagente como campo y describe amenazas como la colusión secreta entre agentes.'),
    ('O05', 'Jin et al.', 2026, 'CapSeal: Capability-sealed secret mediation for secure agent execution', 'arXiv', 'incluir', 'IA',
     'seguridad_agentes', 'experimental', 'llm_agente', 'Mediar credenciales con capacidades acotadas redujo la fuga de claves de 100 % a 0 % en HTTP.'),
    ('O06', 'Abdelrazek y Lee', 2026, 'Symbolic execution meets multi-LLM orchestration: Detecting memory vulnerabilities in incomplete Rust CVE snippets',
     'arXiv', 'incluir', 'IA', 'ofensiva', 'experimental', 'multiagente_llm', 'Cuatro agentes especializados elevaron la detección de 51.6 % a 83.9 % frente a un solo agente.'),
    ('O07', 'Vladimirov y Voloshchenko', 2026, 'Avtonomni AI-ahenty v kiberbezpetsi: vid trenazhernykh seredovyshch do boiovoho zastosuvannia',
     'Informatsiia i pravo', 'incluir', 'IA', 'general', 'posicion', 'llm_agente', 'Analiza una competencia humano contra IA y propone una escala de autonomía A0 a A4.'),
    ('O08', 'Vyas et al.', 2025, 'Towards the deployment of realistic autonomous cyber network defence: A systematic review', 'ACM Computing Surveys',
     'incluir', 'IA', 'defensa', 'revision_sistematica', 'rl', 'Revisión de 55 artículos; el RL profundo jerárquico supera a otros enfoques, con brechas de transferencia.'),
    ('O09', 'Lingam', 2025, 'Agentic AI framework for autonomous cyber threat detection and mitigation',
     'International Journal of Computer Technology and Electronics Communication', 'incluir', 'IA', 'defensa', 'propuesta_sin_evaluacion',
     'multiagente_llm', 'Arquitectura multiagente de siete capas; reporta 99.41 % de exactitud sin describir datos ni procedimiento.'),
    ('O10', 'Srinivas et al.', 2025, 'AI-augmented SOC: A survey of LLMs and agents for security automation', 'Journal of Cybersecurity and Privacy',
     'incluir', 'IA', 'defensa', 'revision_sistematica', 'mixta', 'Revisión de 105 estudios; ocho tareas del SOC y modelo de madurez de autonomía de 0 a 4.'),
    ('O11', 'Al-Sabbagh et al.', 2026, 'AutoSecAgent: A semi-automated AI-driven penetration testing framework through recursive memory and real-time RAG',
     'The Journal of Supercomputing', 'incluir', 'IA', 'ofensiva', 'experimental', 'llm_agente',
     'Agente de pentesting con memoria y RAG; 92.4 % de detección y 58.1 % de explotación en laboratorio.'),
    ('O12', 'Sarker', 2021, 'AI-driven cybersecurity: An overview, security intelligence modeling and research directions', 'Preprints',
     'excluir', 'E6', '', '', '', 'Panorámica de IA en ciberseguridad sin agentes y anterior al periodo de la revisión.'),
    ('O13', 'Vijetha', 2026, 'Agentic intelligence for unified cyber defense: A self-adaptive framework for threat detection across cloud, edge, and IoT systems',
     'IEEE Access', 'excluir', 'E6', '', '', '', 'Controlador de autoadaptación de un modelo de detección, sin LLM ni RL.'),
]
otros = {}
for c, aut, anio, tit, venue, dec, cri, tema, tipo, tec, hall in OTROS:
    otros[c] = {'etapa': 'otros_metodos', 'autores': aut, 'anio': anio, 'titulo': tit, 'venue': venue, 'decision': dec, 'criterio': cri,
                'tema': tema, 'tipo_estudio': tipo, 'tecnologia': tec, 'poblacion': 'no_aplica', 'hallazgo': hall,
                'fuente_leida': 'PDF del corpus inicial'}

C = collections.Counter
el = [v for v in F.values() if v['etapa'] == 'elegibilidad']
nr = [v for v in el if v['decision'] == 'no_recuperado']
ev = [v for v in el if v['decision'] != 'no_recuperado']
cif = d['cifras']
cif.update(no_recuperados=len(nr), evaluados=len(ev),
           excluidos_elegibilidad_por=dict(C(v['criterio'] for v in ev if v['decision'] == 'excluir')),
           incluidos_bd=sum(v['decision'] == 'incluir' for v in F.values()),
           otros_identificados=23, otros_ya_en_bd=10, otros_evaluados=len(otros),
           otros_excluidos=sum(v['decision'] == 'excluir' for v in otros.values()),
           otros_incluidos=sum(v['decision'] == 'incluir' for v in otros.values()))
cif['incluidos_total'] = cif['incluidos_bd'] + cif['otros_incluidos']
json.dump({'cifras': cif, 'final': F, 'otros': otros}, open('03_resultado.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)
for k, v in cif.items():
    print(k, v)
