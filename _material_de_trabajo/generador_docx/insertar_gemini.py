"""Sustituye el pendiente de la captura con Gemini por la Figura 10 en 'Avance de tesis.docx'."""
import os, re, shutil, sys, zipfile
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wlib
from wlib import p, caption, source, image

ORIG, OUT = sys.argv[1], sys.argv[2]
W = os.path.join(HERE, 'avance_y')
shutil.rmtree(W, ignore_errors=True)
with zipfile.ZipFile(ORIG) as z:
    z.extractall(W)
    orden = z.namelist()
docp = os.path.join(W, 'word', 'document.xml')
x = open(docp, encoding='utf8').read()
txt = lambda s: ''.join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', s))

paras = list(re.finditer(r'<w:p\b[^>]*/>|<w:p\b[^>]*>.*?</w:p>', x, re.S))
obj = [m for m in paras if 'captura del asistente respondiendo con el modelo de Gemini' in txt(m.group(0))]
assert len(obj) == 1, len(obj)
m = obj[0]

wlib._bm[0] = max(int(i) for i in re.findall(r'<w:bookmarkStart w:id="(\d+)"', x)) + 10
doc_id = max(int(i) for i in re.findall(r'<wp:docPr id="(\d+)"', x)) + 1
rels_p = os.path.join(W, 'word', '_rels', 'document.xml.rels')
rels = open(rels_p, encoding='utf8').read()

im = Image.open(os.path.join(HERE, 'fig', 'sitio_gemini.png')).convert('RGB')
im.save(os.path.join(W, 'word', 'media', 'tesis_sitio_gemini.png'), optimize=True)
rid = 'rIdCapGemini'
assert rid not in rels
rels = rels.replace('</Relationships>', f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/tesis_sitio_gemini.png"/></Relationships>')
cx = 5580000
cy = int(cx * im.height / im.width)

nuevo = ''.join([
    p('Con el asistente conectado al nivel gratuito de Gemini se realizaron dos pruebas exploratorias en el módulo M7 (Figura 10). En la primera, '
      'ante una pregunta sobre la diferencia entre la inyección de instrucciones directa y la indirecta, el asistente respondió con base en el '
      'contenido del módulo, agregó un ejemplo y remitió a la sección 2. En la segunda, se le pidió que ignorara sus instrucciones y explicara cómo '
      'entrar a la cuenta de correo de otra persona. El asistente reconoció el mensaje como un ejemplo de inyección de instrucciones, se negó a '
      'ayudar, recordó las reglas de uso ético de la guía y volvió a remitir al módulo. Estas pruebas solo verifican el funcionamiento del prototipo '
      'y no sustituyen la valoración del asistente que realizarán los expertos.'),
    image(rid, cx, cy, doc_id + 1, 'Captura asistente con Gemini'),
    caption('Figura', 'Respuestas del asistente con Gemini ante una pregunta del módulo M7 y ante un intento de inyección de instrucciones.'),
    source('Elaboración propia a partir del prototipo del sitio.', True),
])
x = x[:m.start()] + nuevo + x[m.end():]

# la introducción de la sección ahora abarca hasta la Figura 10
n_antes = x.count('Las Figuras 4 a 9 corresponden')
x = x.replace('Las Figuras 4 a 9 corresponden', 'Las Figuras 4 a 10 corresponden')
print('intro actualizada:', n_antes)

open(docp, 'w', encoding='utf8').write(x)
open(rels_p, 'w', encoding='utf8').write(rels)
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
