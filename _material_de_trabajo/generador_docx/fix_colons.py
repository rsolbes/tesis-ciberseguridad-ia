import re
R = [
("ya no son un problema que se pueda ignorar: son una amenaza diaria", "ya no son un problema que se pueda ignorar, sino una amenaza diaria"),
("La literatura describe una evolución en cuatro etapas: la automatización basada en reglas (antes de 2010), la integración del aprendizaje automático (2010–2020), la IA generativa e híbrida (2020–2023) y, finalmente, la era de la IA agéntica, a partir de 2023",
 "La literatura describe una evolución en cuatro etapas, que van de la automatización basada en reglas (antes de 2010) a la integración del aprendizaje automático (2010–2020), después a la IA generativa e híbrida (2020–2023) y, finalmente, a la era de la IA agéntica, a partir de 2023"),
("El crecimiento de este campo ha sido acelerado: el gasto mundial", "El crecimiento de este campo ha sido acelerado. El gasto mundial"),
("Otros trabajos matizan esta conclusión: en 23 escenarios", "Otros trabajos matizan esta conclusión. En 23 escenarios"),
("que ya utiliza herramientas de IA en su vida cotidiana: en un estudio reciente", "que ya utiliza herramientas de IA en su vida cotidiana. En un estudio reciente"),
("hacia un eje que la literatura reciente señala como prioritario: los agentes de IA en ciberseguridad.", "hacia los agentes de IA en ciberseguridad, un eje que la literatura reciente señala como prioritario."),
("en la intersección de ambos campos: los agentes de IA aplicados a la ciberseguridad.", "en la intersección de ambos campos, es decir, en los agentes de IA aplicados a la ciberseguridad."),
("tiene piezas avanzadas del rompecabezas: entiende de sistemas", "tiene piezas avanzadas del rompecabezas. Entiende de sistemas"),
("El reto de diseño que surge de incluir a ambas poblaciones es considerable: ¿cómo puede", "El reto de diseño que surge de incluir a ambas poblaciones es considerable. ¿Cómo puede"),
("A ello se suma una dificultad propia del tema: la enseñanza práctica", "A ello se suma una dificultad propia del tema, ya que la enseñanza práctica"),
("que simule el diálogo con un tutor: al estudiante de la UAT", "que simule el diálogo con un tutor. Al estudiante de la UAT"),
("organizadas en tres ejes: fundamentos de ciberseguridad, agentes de IA para la defensa y seguridad de los propios agentes, seleccionando",
 "organizadas en tres ejes (fundamentos de ciberseguridad, agentes de IA para la defensa y seguridad de los propios agentes), seleccionando"),
("para el mercado laboral de hace una década: la IA agéntica está transformando", "para el mercado laboral de hace una década, porque la IA agéntica está transformando"),
("sin depender de servicios en la nube costosos: se han documentado", "sin depender de servicios en la nube costosos, pues se han documentado"),
("El primero son los fundamentos de la ciberseguridad: la tríada", "El primero son los fundamentos de la ciberseguridad, que incluyen la tríada"),
("El segundo son los agentes de IA aplicados a la defensa: qué es un agente,", "El segundo son los agentes de IA aplicados a la defensa, es decir, qué es un agente,"),
("El tercero es la seguridad y gobernanza de los propios agentes: el uso dual,", "El tercero es la seguridad y gobernanza de los propios agentes, que abarca el uso dual,"),
("se realizarán en entornos aislados y controlados: modelos que se ejecutan localmente,", "se realizarán en entornos aislados y controlados, con modelos que se ejecutan localmente,"),
("se basará en los perfiles específicos de dos grupos: los estudiantes", "se basará en los perfiles específicos de dos grupos, los estudiantes"),
("sobre tres pilares: los fundamentos técnicos,", "sobre tres pilares. Estos son los fundamentos técnicos,"),
("también para los agentes de IA: un agente defensivo debe", "también para los agentes de IA, ya que un agente defensivo debe"),
("El factor humano sigue siendo decisivo: una parte importante", "El factor humano sigue siendo decisivo, pues una parte importante"),
("en seis funciones: Gobernar, Identificar, Proteger, Detectar, Responder y Recuperar", "en seis funciones, que son Gobernar, Identificar, Proteger, Detectar, Responder y Recuperar"),
("en cuatro grandes familias: el aprendizaje automático y el aprendizaje profundo, para aprender patrones a partir de datos; el procesamiento de lenguaje natural, para interpretar texto como registros o reportes; la representación del conocimiento y el razonamiento, por ejemplo mediante ontologías; y los sistemas expertos basados en reglas",
 "en cuatro grandes familias. Estas son el aprendizaje automático y el aprendizaje profundo, que aprenden patrones a partir de datos, el procesamiento de lenguaje natural, que interpreta textos como registros o reportes, la representación del conocimiento y el razonamiento, por ejemplo mediante ontologías, y los sistemas expertos basados en reglas"),
("es la deriva de concepto (*concept drift*): el cambio, con el tiempo,", "es la deriva de concepto (*concept drift*), que consiste en el cambio, con el tiempo,"),
("Sin embargo, un LLM por sí solo es reactivo: responde a una instrucción y se detiene.", "Sin embargo, un LLM por sí solo es reactivo, ya que responde a una instrucción y se detiene."),
("como la etapa que sigue a la IA generativa: sistemas construidos sobre", "como la etapa que sigue a la IA generativa, formada por sistemas construidos sobre"),
("para alcanzar metas de largo plazo: una política asigna", "para alcanzar metas de largo plazo, de modo que una política asigna"),
("frente a un modelo generalista: en la detección de vulnerabilidades", "frente a un modelo generalista. En la detección de vulnerabilidades"),
("También coinciden en un diagnóstico: la mayoría de las implementaciones", "También coinciden en que la mayoría de las implementaciones"),
("organizar la guía como una progresión: primero comprender al asistente, después al agente que usa herramientas y, finalmente, los retos",
 "organizar la guía como una progresión que parte de comprender al asistente, continúa con el agente que usa herramientas y termina con los retos"),
("en las que los LLM y los agentes ya se aplican: el resumen de registros,", "en las que los LLM y los agentes ya se aplican, que son el resumen de registros,"),
("una envolvente de seguridad determinista y auditable: una capa de reglas detectó", "una envolvente de seguridad determinista y auditable. En ese estudio, una capa de reglas detectó"),
("Los resultados son prometedores pero todavía heterogéneos: el marco AutoSecAgent", "Los resultados son prometedores pero todavía heterogéneos. El marco AutoSecAgent"),
("en cuatro brechas de conocimiento: la imprevisibilidad", "en cuatro brechas de conocimiento, que son la imprevisibilidad"),
("un modelo de cuatro capas de riesgo: la percepción (envenenamiento", "un modelo de cuatro capas de riesgo, que comprende la percepción (envenenamiento"),
("de los agentes basados en LLM: un atacante puede ocultar", "de los agentes basados en LLM, ya que un atacante puede ocultar"),
("es la exposición de secretos en el momento de su uso: cuando las claves", "es la exposición de secretos en el momento de su uso. Cuando las claves"),
("dos principios que la guía enseñará desde el nivel básico: el mínimo privilegio y el aislamiento (*sandboxing*).", "dos principios que la guía enseñará desde el nivel básico, el mínimo privilegio y el aislamiento (*sandboxing*)."),
("y de la seguridad de la IA: la colusión secreta entre agentes, los ataques coordinados en enjambre y la propagación",
 "y de la seguridad de la IA, como la colusión secreta entre agentes, los ataques coordinados en enjambre y la propagación"),
("que adopta dos modalidades principales: el humano en el lazo", "que adopta dos modalidades principales. La primera es el humano en el lazo"),
("antes de ejecutarse, y el humano sobre el lazo", "antes de ejecutarse, y la segunda es el humano sobre el lazo"),
("propone organizar la gobernanza en tres capas: la del modelo", "propone organizar la gobernanza en tres capas, que son la del modelo"),
("para desarrollar una actitud profesional: toda práctica con agentes", "para desarrollar una actitud profesional, de manera que toda práctica con agentes"),
("tres funciones de este tipo de materiales: la orientación,", "tres funciones de este tipo de materiales, que son la orientación,"),
("para el diseño de materiales en entornos tecnológicos: definir el perfil del usuario, realizar un acercamiento a las herramientas, aplicar un cuestionario de diagnóstico e identificar los parámetros de diseño",
 "para el diseño de materiales en entornos tecnológicos, que consiste en definir el perfil del usuario, realizar un acercamiento a las herramientas, aplicar un cuestionario de diagnóstico e identificar los parámetros de diseño"),
("En la guía se aplicará sobre tres ejes: el contenido, presentando", "En la guía se aplicará sobre tres ejes. El primero es el contenido, presentando"),
("con distintos niveles de profundidad; el proceso, sugiriendo", "con distintos niveles de profundidad. El segundo es el proceso, sugiriendo"),
("laboratorios más complejos para la UAT; y el producto, mediante", "laboratorios más complejos para la UAT. El tercero es el producto, mediante"),
("esto implica un diseño modular con dos rutas: una básica,", "esto implica un diseño modular con dos rutas, una básica,"),
("sin costos de nube y sin exponer datos: la evidencia muestra", "sin costos de nube y sin exponer datos, ya que la evidencia muestra"),
("La tercera es el uso de la IA como tutor: la plataforma SentinelSphere", "La tercera es el uso de la IA como tutor. La plataforma SentinelSphere"),
("se desprende una lección metodológica: para demostrar el aprendizaje", "se desprende una lección metodológica, pues para demostrar el aprendizaje"),
("con tres referencias recientes: el NIST CSF 2.0, como ciclo de defensa (NIST, 2024); el NIST AI RMF, para la gestión de riesgos de la IA (NIST, 2023); y la lista OWASP",
 "con tres referencias recientes, que son el NIST CSF 2.0 como ciclo de defensa (NIST, 2024), el NIST AI RMF para la gestión de riesgos de la IA (NIST, 2023) y la lista OWASP"),
("en los tres ejes de la guía: fundamentos de ciberseguridad, agentes de IA para la defensa y seguridad de los propios agentes.", "en los tres ejes de la guía, es decir, fundamentos de ciberseguridad, agentes de IA para la defensa y seguridad de los propios agentes."),
("reveló carencias básicas: 92.3 % desconocía", "reveló carencias básicas, ya que 92.3 % desconocía"),
("Se distinguen tres muestras según la fase: para el diagnóstico,", "Se distinguen tres muestras según la fase. Para el diagnóstico se considerarán"),
("que acepten participar; para la validación, un panel", "que acepten participar; para la validación, se integrará un panel"),
("y para la prueba piloto, un grupo de cada institución", "y para la prueba piloto, se trabajará con un grupo de cada institución"),
("tiene una unidad de análisis documental: los artículos científicos,", "tiene una unidad de análisis documental, conformada por los artículos científicos,"),
("en la generación de una solución tangible: el diseño de una guía", "en la generación de una solución tangible, que es el diseño de una guía"),
("en lugar de una hipótesis: se supone que el diseño", "en lugar de una hipótesis. Se supone que el diseño"),
("## Riesgos: uso dual y seguridad de los agentes", "## Riesgos del uso dual y seguridad de los agentes"),
("formación en ciberseguridad antes de la vida profesional", "formación en ciberseguridad antes de la vida profesional"),
]
FIG_BULLETS_OLD = None

c = open('content.txt', encoding='utf8').read()
for a, b in R:
    if a not in c:
        print('NOT FOUND:', a[:70])
    c = c.replace(a, b)

# figure-1 component bullets -> prose
start = c.index('- **Percepción:**')
end = c.index('Un patrón representativo de este ciclo')
prose = ('En la percepción, el agente recibe información de su entorno, como instrucciones del usuario, registros, alertas o resultados de herramientas. '
 'Esa información pasa al núcleo de razonamiento y planificación, que puede ser un LLM o una política aprendida, donde el problema se descompone en pasos, se decide qué hacer y se reflexiona sobre los resultados. '
 'El agente se apoya en una memoria de corto plazo, que corresponde al contexto de la tarea actual, y en memorias episódica y de largo plazo, frecuentemente implementadas mediante bases vectoriales y generación aumentada por recuperación (RAG), la cual permite al modelo consultar una base de conocimiento propia para responder con mayor exactitud (Lazer et al., 2026; Tantaroudas et al., 2026).\n\n'
 'Para actuar más allá del texto, el agente utiliza herramientas como interfaces de programación, escáneres, ejecución de código o consultas a un SIEM. Estándares como el Model Context Protocol (MCP) facilitan que los agentes descubran e invoquen herramientas, aunque también amplían su superficie de ataque (Jin et al., 2026). '
 'Por último, el agente ejecuta la acción, observa el resultado y ajusta su plan en un bucle continuo de planificar, actuar, reflexionar y mejorar.\n\n')
c = c[:start] + prose + c[end:]
open('content.txt', 'w', encoding='utf8').write(c)

left = [m for m in re.findall(r'[^\n]{60}[^0-9 \n]: [^\n]{30}', c) if not m.lstrip().startswith('@')]
print('remaining colons:', len(left))
for m in left: print('  ', m)
