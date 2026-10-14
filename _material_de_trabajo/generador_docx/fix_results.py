lines = open('results.txt', encoding='utf8').read().split('\n')

def need(n, s):
    assert lines[n - 1].startswith(s), (n, lines[n - 1][:50])

need(2, 'En este capítulo'); need(37, 'Cabe señalar'); need(39, '### Diagnóstico de conocimientos'); need(42, '==[Pendiente] Aplicar')
need(95, '### Validación por expertos'); need(96, 'El material se someterá'); need(100, '### Prueba piloto'); need(104, '@SECT')

lines[1] = ('En este capítulo se presentan los resultados obtenidos hasta el momento, organizados de acuerdo con los cuatro objetivos particulares. '
            'Los productos que derivan del análisis documental y del trabajo de diseño, como la caracterización de la literatura, la comparación de los planes de estudio, '
            'la matriz de competencias, la estructura de la guía, los laboratorios y la arquitectura del sitio web, se reportan completos. La validación por expertos, que es el único '
            'apartado que requiere la participación de personas, se deja indicada junto con el procedimiento que se seguirá, y se completará cuando se realice.')

lines[36] = ('La información del Cetis corresponde a la descripción de la carrera técnica publicada por el CETIS 112, que se tomó como referencia del programa de la especialidad.')

perfil = [
    '### Perfil de entrada de los destinatarios',
    ('Como la tesis no contempla trabajo de campo con estudiantes, el perfil de entrada de cada población se construyó a partir de la comparación de los planes de estudio y de la evidencia '
     'reportada en la literatura. El estudiante de la ruta básica, que corresponde al Cetis, llega con bases de programación y de administración de sistemas operativos, pero sin formación '
     'explícita en redes, seguridad ni inteligencia artificial. El estudiante de la ruta avanzada, que corresponde a ISC, llega con formación en programación, bases de datos, redes, '
     'sistemas operativos y seguridad en redes, y con la materia de IA cursada o en curso, pero sin contacto formal con los agentes de IA ni con su seguridad.'),
    '',
    ('En cuanto a los hábitos digitales, se tomó como referencia el diagnóstico de Tantaroudas et al. (2026) con jóvenes de 18 a 20 años, en el que solo el 23.1 % reconocía correos de phishing, '
     'el 84.6 % no utilizaba la autenticación en dos pasos, el 59 % reutilizaba contraseñas y el 51.3 % usaba herramientas de IA con frecuencia. Aunque esa población no es idéntica a la de '
     'esta tesis, los datos indican que el uso frecuente de la IA no va acompañado de hábitos básicos de seguridad, por lo que la guía incluye estos temas desde el módulo M1 en ambas rutas.'),
    '',
    ('Dado que cada estudiante puede apartarse de estos perfiles generales, la guía no asigna la ruta según la institución de procedencia, sino según una autoevaluación de entrada en el '
     'módulo M0. Esa autoevaluación retoma los indicadores anteriores y algunos conceptos básicos de ciberseguridad e IA, y recomienda la ruta básica o la avanzada, aunque el estudiante '
     'puede cambiar de ruta en cualquier momento.'),
]

sitio = [
    '### Arquitectura del sitio web y del asistente',
    ('La guía se desarrolla como un sitio web estático, es decir, un conjunto de páginas que se ejecutan por completo en el navegador del estudiante y que no requieren un servidor propio '
     'ni una cuenta de usuario. Se eligió esta arquitectura por tres razones. Puede alojarse sin costo, funciona en computadoras modestas y en teléfonos, y no recolecta datos personales, '
     'ya que el progreso, las insignias y la ruta elegida se guardan únicamente en el navegador de cada estudiante.'),
    '',
    ('Cada módulo presenta el núcleo común y la profundización de la ruta avanzada, las instrucciones y los archivos de sus laboratorios, una autoevaluación con retroalimentación inmediata '
     'y las insignias que se obtienen al completarla. Los contenidos se escriben en archivos de texto separados del código, de modo que puedan actualizarse sin modificar el sitio, lo cual '
     'es importante en un tema que cambia con tanta rapidez.'),
    '',
    ('El sitio integra un asistente conversacional que responde preguntas sobre el módulo que el estudiante está consultando. Para limitar los errores, el asistente recibe junto con cada '
     'pregunta el texto del módulo y responde con base en él, siguiendo el principio de la generación aumentada por recuperación descrito en el capítulo de fundamentos. Sus instrucciones le '
     'indican que se limite a los temas de la guía, que se niegue a apoyar usos no autorizados, que advierta que puede equivocarse y que remita al módulo correspondiente. El asistente no guarda '
     'las conversaciones. De acuerdo con los niveles de autonomía revisados, se trata de un sistema de nivel 1, ya que asiste al estudiante pero no ejecuta acciones, y esta característica se '
     'aprovecha como material de estudio en los módulos M5 y M7.'),
    '',
    ('La conexión con el modelo de lenguaje se diseñó como un componente intercambiable. En el prototipo que se presentará a los expertos se emplea el nivel gratuito de la API de Gemini, '
     'que no tiene costo por tokens (Google, s.f.), a través de un intermediario que protege la clave de acceso. Esta opción solo es adecuada para el prototipo, porque los términos de ese '
     'servicio prohíben su uso en aplicaciones dirigidas a menores de 18 años y, en el nivel gratuito, permiten que el contenido enviado se utilice para mejorar sus productos (Google, 2026). '
     'Por ello, el mismo componente admite conectarse a un modelo local mediante Ollama, que es la opción recomendada para cualquier uso con estudiantes, pues ninguna pregunta sale de la '
     'computadora del estudiante o de la red del plantel.'),
    '',
    '==[Pendiente] Agregar capturas de pantalla del sitio y el mapa de navegación cuando el prototipo esté terminado.==',
    '',
]

valid = [
    '### Validación por expertos',
    ('El sitio se someterá a la evaluación de un panel de cinco a siete expertos en ciberseguridad, inteligencia artificial y pedagogía, mediante la rúbrica que se presenta en el Anexo 1. '
     'Cada experto valorará los nueve módulos y el reto integrador según cuatro criterios, que son la pertinencia, la claridad, la suficiencia y la seguridad, e indicará si cada módulo es '
     'esencial, útil pero no esencial o no necesario. Además, valorará una sola vez el desempeño del asistente conversacional y responderá la escala SUS sobre la usabilidad del sitio '
     '(Brooke, 1996). Con el juicio de necesidad se calculará la razón de validez de contenido de cada módulo y se comparará con el valor crítico que corresponde al número de expertos '
     '(Lawshe, 1975). Los módulos que no alcancen ese valor se ajustarán y volverán a evaluarse.'),
    '',
    ('==[Pendiente] Reportar la conformación del panel, la razón de validez de contenido por módulo y criterio, la valoración del asistente, el puntaje SUS del sitio, las observaciones '
     'cualitativas de los expertos y los ajustes realizados al material.=='),
    '@SECT',
]

out = lines[:38] + perfil + [''] + lines[43:94] + sitio + valid
open('results.txt', 'w', encoding='utf8').write('\n'.join(out))

a = open('annex.txt', encoding='utf8').read()
a = a[a.index('@ANX:Anexo 2.'):].replace('@ANX:Anexo 2.', '@ANX:Anexo 1.')
a = a.replace('Cada experto aplica la rúbrica a cada uno de los nueve módulos y al reto integrador.',
              'Cada experto aplica la rúbrica a cada uno de los nueve módulos y al reto integrador, y evalúa una sola vez al asistente conversacional.')
open('annex.txt', 'w', encoding='utf8').write(a)
print('ok')
