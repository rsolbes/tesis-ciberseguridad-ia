from PIL import Image, ImageDraw
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
C = 'capturas/'

def borde(im, c=(190, 190, 190)):
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, im.width - 1, im.height - 1], outline=c, width=3)
    return im

def lado(a, b, gap=40, alto=None):
    alto = alto or min(a.height, b.height)
    a = a.resize((int(a.width * alto / a.height), alto))
    b = b.resize((int(b.width * alto / b.height), alto))
    m = Image.new('RGB', (a.width + b.width + gap, alto), 'white')
    m.paste(a, (0, 0))
    m.paste(b, (a.width + gap, 0))
    return m

op = lambda n: Image.open(C + n + '.png').convert('RGB')
por = borde(op('01_portada').crop((0, 0, 2560, 1240)))
mapa = borde(op('02_mapa').crop((0, 0, 2560, 2000)))
lado(por, mapa, alto=1240).save('fig/sitio_portada_mapa.png')
borde(op('03_m0_resultado')).save('fig/sitio_m0.png')
lado(borde(op('04_m7_contenido')), borde(op('07_movil')), alto=2000).save('fig/sitio_m7.png')
borde(op('05_autoevaluacion')).save('fig/sitio_autoevaluacion.png')
borde(op('06_asistente')).save('fig/sitio_asistente.png')
for f in ['navegacion', 'sitio_portada_mapa', 'sitio_m0', 'sitio_m7', 'sitio_autoevaluacion', 'sitio_asistente']:
    print(f, Image.open('fig/' + f + '.png').size)
