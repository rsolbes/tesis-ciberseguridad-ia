"""Integra la revisión sistemática PRISMA en 'Avance de tesis.docx' editando el XML en su lugar."""
import os, re, shutil, sys, zipfile, json
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'prisma'))
import wlib
from wlib import p, h, caption, source, image, table, reference, runs
from xml.sax.saxutils import escape
import consultas

ORIG, OUT = sys.argv[1], sys.argv[2]
W = os.path.join(HERE, 'avance_p')
shutil.rmtree(W, ignore_errors=True)
with zipfile.ZipFile(ORIG) as z:
    z.extractall(W); orden = z.namelist()
docp = os.path.join(W, 'word', 'document.xml')
x = open(docp, encoding='utf8').read()
PAT = re.compile(r'<w:p\b[^>]*/>|<w:p\b[^>]*>.*?</w:p>', re.S)
txt = lambda s: ''.join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', s))

# ---------- 1. renumerar menciones en el cuerpo (no en pies ni en listas) ----------
def renum_parrafo(par):
    if 'SEQ ' in par or 'w:pStyle w:val="TDC' in par or 'w:pStyle w:val="Tabladeilustraciones"' in par:
        return par
    def en_t(m):
        s = m.group(2)
        s = re.sub(r'Figuras 4 a 10', 'Figuras 5 a 11', s)
        s = re.sub(r'\b(Figura) (\d+)\b', lambda k: f'{k.group(1)} {int(k.group(2)) + 1}' if int(k.group(2)) >= 3 else k.group(0), s)
        s = re.sub(r'\b(Tabla) (\d+)\b', lambda k: f'{k.group(1)} {int(k.group(2)) + 2}' if int(k.group(2)) >= 7 else k.group(0), s)
        s = re.sub(r'\b(Tablas) (\d+) y (\d+)\b', lambda k: f'Tablas {int(k.group(2)) + 2} y {int(k.group(3)) + 2}' if int(k.group(2)) >= 7 else k.group(0), s)
        return m.group(1) + s + m.group(3)
    return re.sub(r'(<w:t(?: [^>]*)?>)([^<]*)(</w:t>)', en_t, par)
antes = txt(x)
x = PAT.sub(lambda m: renum_parrafo(m.group(0)), x)
print('menciones cambiadas:', sum(1 for a, b in zip(re.findall(r'(?:Figura|Tabla)s? \d+', antes), re.findall(r'(?:Figura|Tabla)s? \d+', txt(x))) if a != b))

wlib._bm[0] = max(int(n) for n in re.findall(r'<w:bookmarkStart w:id="(\d+)"', x)) + 10
doc_id = [max(int(n) for n in re.findall(r'<wp:docPr id="(\d+)"', x)) + 1]
rels_p = os.path.join(W, 'word', '_rels', 'document.xml.rels')
rels = open(rels_p, encoding='utf8').read()

def fig(nombre):
    global rels
    im = Image.open(os.path.join(HERE, 'fig', nombre + '.png')).convert('RGB')
    destino = f'tesis_{nombre}.png'
    im.save(os.path.join(W, 'word', 'media', destino), optimize=True)
    rid = f'rIdPrisma{nombre}'
    rels = rels.replace('</Relationships>', f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{destino}"/></Relationships>')
    cx = 5580000; cy = int(cx * im.height / im.width)
    doc_id[0] += 1
    return image(rid, cx, cy, doc_id[0], f'Figura {nombre}')

def parrafo_por_texto(inicio):
    ms = [m for m in PAT.finditer(x) if txt(m.group(0)).startswith(inicio)]
    assert len(ms) == 1, (inicio, len(ms))
    return ms[0]

def reemplazar(inicio, nuevo_xml):
    global x
    m = parrafo_por_texto(inicio)
    x = x[:m.start()] + nuevo_xml + x[m.end():]

# ---------- 2. tablas ----------
TABLAS = {
    'caracteristicas': {
        'w': [2300, 3838, 1300, 1400], 'h': ['Característica', 'Categoría', 'n', '%'],
        'r': [['Tema', 'Defensa', '98', '39.2'], ['', 'Ofensiva', '68', '27.2'], ['', 'Educación', '38', '15.2'],
              ['', 'Seguridad de los agentes', '23', '9.2'], ['', 'General', '23', '9.2'],
              ['Tipo de estudio', 'Experimental', '179', '71.6'], ['', 'Propuesta sin evaluación', '28', '11.2'],
              ['', 'Revisión narrativa', '22', '8.8'], ['', 'Artículo de posición', '14', '5.6'], ['', 'Revisión sistemática', '7', '2.8'],
              ['Tecnología', 'Agente basado en LLM', '87', '34.8'], ['', 'Aprendizaje por refuerzo', '58', '23.2'],
              ['', 'Sistema multiagente con LLM', '41', '16.4'], ['', 'Mixta', '35', '14.0'], ['', 'IA generativa sin agencia', '29', '11.6'],
              ['Revisión por pares', 'Sí', '110', '44.0'], ['', 'No (preprint)', '140', '56.0'],
              ['Año', '2022 a 2024', '40', '16.0'], ['', '2025', '82', '32.8'], ['', '2026', '128', '51.2']],
    },
    'educacion_poblacion': {
        'w': [2600, 2400, 2100, 1738], 'h': ['Población', 'IA generativa sin agencia', 'Agentes de IA', 'Total'],
        'r': [['Universidad', '20', '7', '27'], ['Profesionales', '4', '1', '5'], ['Público general', '4', '1', '5'],
              ['Bachillerato', '1', '0', '1'], ['Total', '29', '9', '38']],
    },
}

def render(ruta):
    out = []
    for ln in open(ruta, encoding='utf8').read().split('\n'):
        s = ln.strip()
        if not s: continue
        if s.startswith('### '): out.append(h(3, s[4:]))
        elif s.startswith('@FIG:'): out.append(fig(s[5:]))
        elif s.startswith('@CAP:'):
            k, t = s[5:].split('|', 1); out.append(caption(k, t))
        elif s.startswith('@SRC:'):
            t = s[5:]; out.append(source(t.replace('|center', ''), t.endswith('|center')))
        elif s.startswith('@TABLE:'):
            tb = TABLAS[s[7:]]; out.append(table(tb['h'], tb['r'], tb['w']))
        else: out.append(p(s))
    return ''.join(out)

# ---------- 3. resultados 7.1.1 ----------
reemplazar('Este análisis corresponde al corpus inicial.', render(os.path.join(HERE, 'prisma', 'resultados_prisma.txt')))

# ---------- 4. metodología, fase 1 ----------
reemplazar('Fase 1. Análisis y diagnóstico.', p(
    '**Fase 1. Análisis y diagnóstico.** El proceso inicia con la caracterización de los destinatarios y de su contexto. Se realiza una revisión '
    'sistemática de la literatura sobre agentes de IA en ciberseguridad conforme a la declaración PRISMA 2020 (Page et al., 2021), con búsquedas en '
    'OpenAlex, un índice abierto que reúne los registros de IEEE, ACM, Springer, Elsevier y MDPI, entre otras editoriales (Priem et al., 2022), y en arXiv. '
    'Semantic Scholar se emplea para completar resúmenes y localizar textos completos (Allen Institute for AI, s.f.). El cribado por título y resumen y la '
    'evaluación del texto completo se realizan con criterios de inclusión y exclusión explícitos, con apoyo de herramientas de IA y con la verificación de una '
    'muestra de las decisiones. El protocolo, las cadenas de búsqueda y los criterios se presentan en el Anexo 2. Simultáneamente, se lleva a cabo un análisis '
    'documental comparativo de los planes de estudio del bachillerato tecnológico y de ISC, para identificar la formación previa de ambas poblaciones en '
    'programación, redes, ciberseguridad e inteligencia artificial. Esta fase responde al primer objetivo particular.'))

# ---------- 5. conclusiones y recomendaciones ----------
reemplazar('El primer objetivo particular consistió', p(
    'El primer objetivo particular consistió en caracterizar y comparar la formación previa y el contexto de ambas poblaciones, así como el estado del '
    'conocimiento sobre los agentes de IA en ciberseguridad. Se concluye que se trata de un campo muy reciente y todavía poco consolidado. La revisión '
    'sistemática, que incluyó 250 estudios, mostró que el 84 % se publicó en 2025 o 2026 y que más de la mitad son preprints, lo que obliga a presentar sus '
    'cifras en la guía como resultados reportados y no como hechos definitivos. Se concluye también que la dimensión educativa es la menos atendida en lo que '
    'respecta a los agentes. Aunque 38 estudios abordan la enseñanza de la ciberseguridad con IA, 29 de ellos emplean IA generativa sin agencia, solo 9 '
    'trabajan con agentes y únicamente uno se dirige a estudiantes de bachillerato, sin emplear agentes. Este hallazgo confirma, con evidencia sistemática, '
    'el vacío que motivó la investigación.'))
reemplazar('Se recomienda concluir la revisión sistemática', p(
    'Se recomienda que un segundo revisor verifique de forma independiente una muestra de las decisiones de la revisión sistemática y que la búsqueda se '
    'amplíe a bases de suscripción, como Scopus o IEEE Xplore, para recuperar los 384 reportes que no estuvieron disponibles en acceso abierto. Dado el ritmo '
    'de publicación del campo, conviene además actualizar la búsqueda al menos una vez al año. También se recomienda desarrollar los módulos restantes y los '
    'laboratorios 5 y 6 con el mismo formato del módulo M7, antes de someter la guía completa al juicio de expertos, para que la valoración abarque la '
    'totalidad del producto.'))

# ---------- 6. resumen y abstract ----------
n = x.count('se analizaron veintitrés estudios recientes y los planes de estudio de ambas instituciones')
x = x.replace('se analizaron veintitrés estudios recientes y los planes de estudio de ambas instituciones',
              'se realizó una revisión sistemática de 250 estudios y se compararon los planes de estudio de ambas instituciones')
m_ = x.count('twenty-three recent studies and the curricula of both institutions were analyzed')
x = x.replace('twenty-three recent studies and the curricula of both institutions were analyzed',
              'a systematic review of 250 studies was conducted and the curricula of both institutions were compared')
print('resumen', n, 'abstract', m_)

# ---------- 7. referencias ----------
def insertar_despues(inicio, xml_nuevo):
    global x
    m = parrafo_por_texto(inicio)
    x = x[:m.end()] + xml_nuevo + x[m.end():]
insertar_despues('Alfageme-Barros, M. B. (2024).', reference('Allen Institute for AI. (s.f.). *Semantic Scholar Academic Graph API*. https://www.semanticscholar.org/product/api'))
insertar_despues('Potter, Y., Guo, W.', reference('Priem, J., Piwowar, H., & Orr, R. (2022). *OpenAlex: A fully-open index of scholarly works, authors, venues, institutions, and concepts* (arXiv:2205.01833) [Preprint]. arXiv. https://arxiv.org/abs/2205.01833'))

# ---------- 8. anexos 2 y 3 ----------
def anexo_titulo(num, t):
    return ('<w:p><w:pPr><w:pStyle w:val="Sinespaciado"/><w:keepNext/><w:spacing w:before="240" w:after="120"/></w:pPr>'
            + runs('**' + num + '** ' + t) + '</w:p>')
def nota(t):
    return ('<w:p><w:pPr><w:pStyle w:val="Sinespaciado"/><w:keepNext/><w:spacing w:after="120"/><w:jc w:val="both"/></w:pPr>' + runs(t) + '</w:p>')
proto = [
    ['Pregunta', '¿Qué aplicaciones, riesgos y experiencias educativas se han reportado sobre los agentes de IA en ciberseguridad entre 2022 y 2026?'],
    ['Fuentes', 'OpenAlex y arXiv. Semantic Scholar se usó para completar resúmenes y localizar textos completos.'],
    ['Fecha y periodo', 'Búsqueda realizada el 30 de septiembre de 2026 para publicaciones del 1 de enero de 2022 al 30 de septiembre de 2026.'],
    ['Cadena A en OpenAlex', consultas.OPENALEX['A']],
    ['Cadena B en OpenAlex', consultas.OPENALEX['B']],
    ['Cadena A en arXiv', consultas.ARXIV['A'] + ' (publicaciones de 2022 a 2026)'],
    ['Cadena B en arXiv', consultas.ARXIV['B'] + ' (publicaciones de 2022 a 2026)'],
    ['Inclusión IA', 'Propone, evalúa o revisa agentes de IA aplicados a tareas de ciberseguridad (basados en LLM, multiagente o de aprendizaje por refuerzo) o estudia la seguridad de los propios agentes.'],
    ['Inclusión IB', 'Estudia el uso de LLM, IA generativa o agentes de IA en la enseñanza, el aprendizaje, la capacitación o la evaluación en ciberseguridad.'],
    ['Exclusión en cribado', 'E1 no trata ciberseguridad informática. E2 «agente» no se refiere a IA. E3 IA no agéntica sin relación con la seguridad de agentes ni con la educación. E4 educación en ciberseguridad sin IA generativa ni agentes. E5 no es un trabajo académico con contenido propio.'],
    ['Exclusión en texto completo', 'E6 el texto completo muestra que no cumple IA ni IB. E7 no es un trabajo completo (resumen extendido, póster o menos de 4 páginas). E8 versión duplicada de otro registro.'],
    ['Eliminación previa', 'Duplicados por DOI, identificador de arXiv o título normalizado; tipos no académicos (tesis, conjuntos de datos, software, reseñas, resúmenes de congreso); idiomas distintos de inglés o español.'],
    ['Procedimiento', 'Cribado y evaluación de texto completo realizados con apoyo de herramientas de IA bajo los criterios escritos, con auditoría de una muestra aleatoria de decisiones. Los datos de cada registro se conservan en el archivo complementario de la revisión.'],
]
incl = json.load(open(os.path.join(HERE, 'prisma', '04_incluidos.json'), encoding='utf8'))
TEMA = {'defensa': 'Defensa', 'ofensiva': 'Ofensiva', 'educacion': 'Educación', 'seguridad_agentes': 'Seguridad de agentes', 'general': 'General'}
orden_t = ['defensa', 'ofensiva', 'seguridad_agentes', 'educacion', 'general']
incl.sort(key=lambda e: (orden_t.index(e['tema']), -e['anio'], e['autores'].lower()))
filas = [[str(i), f"{e['autores']} ({e['anio']})", e['titulo'], e['venue'] or 'arXiv', TEMA[e['tema']]] for i, e in enumerate(incl, 1)]
anexos = ''.join([
    anexo_titulo('Anexo 2.', 'Protocolo de la revisión sistemática.'),
    nota('Las cadenas se reproducen en la sintaxis de cada fuente. En OpenAlex, title.search busca en el título y title_and_abstract.search en el título y el resumen; en arXiv, ti busca en el título y abs en el resumen.'),
    table(['Elemento', 'Descripción'], proto, [2600, 9838]),
    source('Elaboración propia.'),
    anexo_titulo('Anexo 3.', 'Estudios incluidos en la revisión sistemática (n = 250).'),
    nota('Los estudios se ordenan por tema y, dentro de cada tema, del más reciente al más antiguo. Los datos completos de cada estudio, incluidos su DOI, el tipo de estudio, la tecnología y el hallazgo principal, se encuentran en el archivo complementario de la revisión.'),
    table(['N.º', 'Autores (año)', 'Título', 'Fuente', 'Tema'], filas, [700, 2500, 5838, 2100, 1300]),
    source('Elaboración propia a partir de la revisión sistemática.'),
])
fin = x.rfind('<w:sectPr')
x = x[:fin] + anexos + x[fin:]

open(docp, 'w', encoding='utf8').write(x)
open(rels_p, 'w', encoding='utf8').write(rels)
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    hechos = set()
    for nme in orden:
        f = os.path.join(W, nme)
        if os.path.isfile(f): z.write(f, nme); hechos.add(nme)
    for raiz, _, archivos in os.walk(W):
        for a in archivos:
            nme = os.path.relpath(os.path.join(raiz, a), W).replace(os.sep, '/')
            if nme not in hechos: z.write(os.path.join(raiz, a), nme)
print('ok', OUT)
