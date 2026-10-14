"""Inserta las capturas del sitio en 'Avance de tesis.docx' editando el XML en su lugar."""
import os, re, shutil, sys, zipfile
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wlib
from wlib import p, caption, source, image

ORIG = sys.argv[1]            # copia de trabajo del documento del usuario
OUT = sys.argv[2]             # docx resultante
W = os.path.join(HERE, 'avance_x')
shutil.rmtree(W, ignore_errors=True)
with zipfile.ZipFile(ORIG) as z:
    z.extractall(W)
    orden = z.namelist()

docp = os.path.join(W, 'word', 'document.xml')
x = open(docp, encoding='utf8').read()

# párrafo pendiente a sustituir
paras = list(re.finditer(r'<w:p\b[^>]*/>|<w:p\b[^>]*>.*?</w:p>', x, re.S))
objetivo = [m for m in paras if 'Agregar capturas de pantalla del sitio' in ''.join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', m.group(0)))]
assert len(objetivo) == 1, len(objetivo)
m = objetivo[0]

# identificadores libres
wlib._bm[0] = max(int(i) for i in re.findall(r'<w:bookmarkStart w:id="(\d+)"', x)) + 10
doc_id = max(int(i) for i in re.findall(r'<wp:docPr id="(\d+)"', x)) + 1

rels_p = os.path.join(W, 'word', '_rels', 'document.xml.rels')
rels = open(rels_p, encoding='utf8').read()

def fig(nombre):
    global rels, doc_id
    src = os.path.join(HERE, 'fig', nombre + '.png')
    im = Image.open(src).convert('RGB')
    if im.width > 2000:
        im = im.resize((2000, int(im.height * 2000 / im.width)), Image.LANCZOS)
    destino = f'tesis_{nombre}.png'
    im.save(os.path.join(W, 'word', 'media', destino), optimize=True)
    rid = f'rIdCap{nombre}'
    assert rid not in rels
    rels = rels.replace('</Relationships>', f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{destino}"/></Relationships>')
    cx = 5580000
    cy = int(cx * im.height / im.width)
    if cy > 4300000:                      # que no exceda ~12 cm de alto
        cx = int(cx * 4300000 / cy); cy = 4300000
    doc_id += 1
    return image(rid, cx, cy, doc_id, f'Captura {nombre}')

FUENTE = 'Elaboración propia a partir del prototipo del sitio.'
bloques = [
    p('Las Figuras 4 a 9 corresponden al prototipo funcional del sitio, en el que ya están disponibles la portada, el mapa completo de la guía, '
      'el módulo M0 y el módulo M7 con su laboratorio, su autoevaluación y el asistente. La Figura 4 presenta el mapa de navegación, que muestra '
      'cómo se relacionan las páginas del sitio y dónde se guarda el progreso del estudiante.'),
    fig('navegacion'), caption('Figura', 'Mapa de navegación del sitio web de la guía.'), source('Elaboración propia.', True),
    p('La portada presenta la guía y conduce al punto de partida, mientras que el mapa organiza los módulos por eje e indica el estado y la duración '
      'de cada uno según la ruta elegida (Figura 5). Los módulos que aún no se desarrollan aparecen marcados como próximos, de modo que el estudiante '
      'conoce desde el inicio la estructura completa de su ruta.'),
    fig('sitio_portada_mapa'), caption('Figura', 'Portada y mapa de la guía con la ruta básica elegida.'), source(FUENTE, True),
    p('En el módulo M0 el estudiante responde la autoevaluación de entrada. Al terminar, el sitio calcula un puntaje, recomienda una ruta, ofrece '
      'consejos según los hábitos de seguridad que el estudiante reportó y le permite elegir cualquiera de las dos rutas. Enseguida se presentan las '
      'reglas de uso ético, cuya aceptación es requisito para desbloquear los laboratorios (Figura 6).'),
    fig('sitio_m0'), caption('Figura', 'Resultado de la autoevaluación de entrada y reglas de uso ético del módulo M0.'), source(FUENTE, True),
    p('La Figura 7 muestra cómo se materializa la enseñanza diferenciada dentro de un módulo. El núcleo común es visible para todos, los recuadros '
      'de la ruta básica ofrecen analogías y los de la ruta avanzada profundizan en los fundamentos técnicos. Cada estudiante ve solo los recuadros '
      'de su ruta, aunque puede mostrar también los de la otra. La misma figura incluye la vista en un teléfono, ya que el diseño se adapta a '
      'pantallas pequeñas.'),
    fig('sitio_m7'), caption('Figura', 'Contenido diferenciado del módulo M7 y su vista en un teléfono.'), source(FUENTE, True),
    p('Al final del módulo, la autoevaluación califica cada respuesta, explica por qué es correcta o incorrecta y, cuando el estudiante alcanza el '
      '70 %, otorga la insignia del módulo (Figura 8). El número de preguntas depende de la ruta, con ocho en la básica y once en la avanzada.'),
    fig('sitio_autoevaluacion'), caption('Figura', 'Retroalimentación de la autoevaluación del módulo M7 e insignia obtenida.'), source(FUENTE, True),
    p('Por último, la Figura 9 muestra el asistente conversacional abierto sobre el módulo M7. En la captura funciona en su modo de respaldo, sin '
      'modelo de lenguaje, y responde con las preguntas frecuentes del módulo. Este modo garantiza que la guía siga siendo útil cuando no hay '
      'conexión con Ollama ni con Gemini.'),
    fig('sitio_asistente'), caption('Figura', 'Asistente conversacional del módulo M7 en modo de preguntas frecuentes.'), source(FUENTE, True),
    p('==[Pendiente] Agregar una captura del asistente respondiendo con el modelo de Gemini, una vez realizada la prueba.=='),
]
x = x[:m.start()] + ''.join(bloques) + x[m.end():]
open(docp, 'w', encoding='utf8').write(x)
open(rels_p, 'w', encoding='utf8').write(rels)

ct = open(os.path.join(W, '[Content_Types].xml'), encoding='utf8').read()
assert 'Extension="png"' in ct

with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    hechos = set()
    for n in orden:
        f = os.path.join(W, n)
        if os.path.isfile(f):
            z.write(f, n); hechos.add(n)
    for raiz, _, archivos in os.walk(W):
        for a in archivos:
            n = os.path.relpath(os.path.join(raiz, a), W).replace(os.sep, '/')
            if n not in hechos:
                z.write(os.path.join(raiz, a), n)
print('ok', OUT)
