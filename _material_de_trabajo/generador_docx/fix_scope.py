import sys
L = {}  # line number -> new text (whole line)
L[51] = ('Diseñar una guía didáctica (*roadmap*) en formato de sitio web interactivo para la iniciación en ciberseguridad con enfoque en agentes de inteligencia artificial, '
         'que sirva como una ruta de aprendizaje estructurada, flexible y segura, adaptada a las necesidades de los estudiantes de Ingeniería en Sistemas Computacionales de la UAT '
         'y de los estudiantes de la especialidad de Programación del Cetis.')
L[54] = ('- Caracterizar y comparar la formación previa y el contexto educativo de los estudiantes del Cetis y de ISC-UAT en ciberseguridad e inteligencia artificial, '
         'mediante el análisis de sus planes de estudio y una revisión sistemática de la literatura sobre agentes de IA en ciberseguridad.')
L[57] = ('- Desarrollar el sitio web de la guía, con su contenido, sus laboratorios en entornos aislados, su asistente conversacional y la curaduría de recursos, '
         'y validarlo mediante juicio de expertos.')
L[78] = ('En cuanto a la población, el diseño de la guía se basará en los perfiles específicos de dos grupos, los estudiantes de la especialidad técnica en Programación del Cetis '
         'y los estudiantes de 7º a 9º semestre de ISC en la Facultad de Ingeniería Tampico de la UAT. Estos perfiles se caracterizarán a partir de sus planes de estudio y de la literatura, '
         'sin realizar trabajo de campo con estudiantes. Aunque la guía podría ser útil para otros, su diseño se fundamenta en las necesidades de estos dos perfiles concretos.')
L[80] = ('En cuanto al producto, se trata de un proyecto de investigación y diseño. Los entregables son la guía didáctica (el *roadmap*), desarrollada como un sitio web interactivo '
         'que integra los módulos, los laboratorios, las autoevaluaciones y un asistente conversacional de apoyo, y esta tesis, que documenta y justifica el proceso de fundamentación, '
         'diseño y validación. La validación se realizará únicamente mediante juicio de expertos, quienes valorarán la pertinencia, la claridad, la suficiencia, la seguridad y la '
         'usabilidad de la guía. La aplicación de la guía con estudiantes del Cetis o de la UAT, su implementación formal en los programas de estudio y la evaluación de su efecto '
         'en el aprendizaje no forman parte del alcance; ese sería un valioso estudio posterior que se recomendará en las conclusiones.')
L[214] = ('El estudio se desarrollará en la zona sur del estado de Tamaulipas, México, y se dirige a dos poblaciones destinatarias. La primera está conformada por los estudiantes de la '
          'especialidad técnica en Programación del Cetis, y la segunda, por los estudiantes de 7º a 9º semestre de Ingeniería en Sistemas Computacionales de la Facultad de Ingeniería '
          'Tampico de la UAT. Dado que la tesis no contempla la aplicación de la guía con estudiantes, estas poblaciones no se muestrearán, sino que se caracterizarán a partir de sus '
          'planes de estudio y de la literatura.')
L[216] = ('La única muestra de participantes corresponde a la fase de validación. Se integrará un panel de cinco a siete expertos en ciberseguridad, inteligencia artificial y pedagogía, '
          'seleccionados mediante un muestreo no probabilístico de tipo intencional con base en su formación y experiencia, y cuya participación será voluntaria.')
L[222] = ('La presente investigación se enmarca en un enfoque mixto, cualitativo y cuantitativo, y se clasifica como proyectiva o tecnológica. Su propósito trasciende la descripción '
          'teórica del problema para centrarse en la generación de una solución tangible, que es el diseño de una guía didáctica para la iniciación en ciberseguridad con enfoque en '
          'agentes de IA. El diseño es no experimental y no contempla la aplicación de la guía con estudiantes, por lo que la evidencia de su validez proviene del análisis documental '
          'y del juicio de expertos.')
L[225] = ('Dado que el proyecto es de diseño y no experimental, se parte de un supuesto de trabajo en lugar de una hipótesis. Se supone que una guía didáctica basada en los principios '
          'del aprendizaje autónomo y de la enseñanza diferenciada, que introduzca los agentes de IA de manera progresiva según sus niveles de autonomía y que emplee laboratorios '
          'seguros con modelos locales, será valorada por expertos como pertinente, clara, suficiente y segura para que estudiantes con distintos niveles de madurez (Cetis) y de '
          'conocimientos previos (UAT) se inicien de forma estandarizada y flexible en la ciberseguridad y en el uso y la protección de los agentes de IA.')
L[228] = ('Para alcanzar los objetivos se estructuró un procedimiento sistemático dividido en cinco fases secuenciales e iterativas, que se ilustran en la Figura 2 y se describen a continuación.')
L[234] = ('**Fase 1. Análisis y diagnóstico.** El proceso inicia con la caracterización de los destinatarios y de su contexto. Se realizará una revisión sistemática de la literatura '
          'sobre agentes de IA en ciberseguridad siguiendo la declaración PRISMA 2020 (Page et al., 2021), con el fin de actualizar y ampliar el corpus inicial. Simultáneamente, se '
          'llevará a cabo un análisis documental comparativo de los planes de estudio del bachillerato tecnológico y de ISC, para identificar la formación previa de ambas poblaciones '
          'en programación, redes, ciberseguridad e inteligencia artificial. Esta fase responde al primer objetivo particular.')
L[236] = L_236 = None
L[240] = ('**Fase 4. Desarrollo del material.** Consiste en la construcción de la guía como sitio web interactivo. Se redactará el contenido adaptando el lenguaje técnico a los '
          'distintos niveles de madurez académica; se diseñarán laboratorios en entornos aislados con modelos de lenguaje que se ejecutan localmente, datos sintéticos y permisos '
          'restringidos; se integrará un asistente conversacional que responda preguntas sobre el contenido de cada módulo; y se prepararán casos de estudio basados en escenarios '
          'documentados, junto con una curaduría de lecturas, videos y plataformas de práctica.')
L[242] = ('**Fase 5. Validación por expertos.** El sitio será evaluado por el panel de expertos mediante una rúbrica que valore la pertinencia, la claridad, la suficiencia y la '
          'seguridad de cada módulo, y la usabilidad del sitio se medirá con la escala SUS (Brooke, 1996). La validez de contenido se estimará con la razón de validez de contenido de '
          'Lawshe (1975). Si los resultados no son satisfactorios, se identificarán las áreas de oportunidad y se ajustará el material, repitiendo el ciclo hasta obtener una versión '
          'validada. Las fases 4 y 5 responden al cuarto objetivo particular.')
L[244] = None  # remove Fase 6
L[254] = ('La participación de los expertos será voluntaria y se solicitará su consentimiento informado. Sus valoraciones se tratarán de forma confidencial y únicamente con fines '
          'académicos, conforme a la normativa mexicana de protección de datos personales. La investigación no involucra la participación de estudiantes ni de menores de edad. '
          'Además, el sitio web no solicita registro ni recolecta datos personales de quienes lo usan, y el progreso de cada estudiante se guarda únicamente en su propio navegador.')

lines = open('content.txt', encoding='utf8').read().split('\n')
checks = {51: 'Diseñar una guía', 54: '- Diagnosticar', 57: '- Desarrollar y validar', 78: 'En cuanto a la población', 80: 'En cuanto al producto',
          214: 'El estudio se desarrollará', 216: 'Dado que se trata', 222: 'La presente investigación', 225: 'Dado que el proyecto', 228: 'Para alcanzar',
          234: '**Fase 1.', 240: '**Fase 4.', 242: '**Fase 5.', 244: '**Fase 6.', 254: 'Debido a que'}
for n, s in checks.items():
    assert lines[n - 1].startswith(s), (n, lines[n - 1][:40])
for n in sorted(L, reverse=True):
    if n == 236:
        continue
    if L[n] is None:
        del lines[n - 1]
    else:
        lines[n - 1] = L[n]
c = '\n'.join(lines)
c = c.replace('El producto no será un curso rígido, sino un *roadmap* flexible que simule',
              'El producto no será un curso rígido, sino un *roadmap* flexible, desarrollado como sitio web interactivo, que simule')
assert 'desarrollado como sitio web interactivo, que simule' in c
open('content.txt', 'w', encoding='utf8').write(c)
print('ok')
