# Reto integrador tipo CTF

Has llegado al desafío culminante de la guía didáctica. A lo largo de los módulos anteriores aprendiste los fundamentos de la seguridad de la información (Eje A), comprendiste el funcionamiento y despliegue de los agentes de inteligencia artificial para la defensa (Eje B) y exploraste los riesgos y las salvaguardas que protegen a los propios agentes (Eje C).

En este reto integrador vas a demostrar todas tus competencias en un escenario simulado de respuesta a incidentes en un entorno seguro y controlado.

Al resolver este reto pondrás en práctica la investigación de incidentes en bitácoras, el uso supervisado de un agente inteligente para el análisis de eventos y la detección de intentos de manipulación adversaria mediante inyecciones ocultas.

## 1. El escenario del incidente

Trabajas como analista de seguridad en el Centro de Operaciones de una organización educativa. A las 03:24 de la madrugada el sistema de monitoreo generó una alerta de prioridad alta reportando un comportamiento anómalo en el servidor web principal.

El servidor alberga tanto el portal público de información como la base de datos de expedientes académicos.

Tu misión consiste en investigar la intrusión, contener el daño, identificar las técnicas empleadas por el adversario y documentar las medidas de mitigación requeridas.

Para ayudarte en esta tarea cuentas con un agente de inteligencia artificial defensivo que tiene acceso a herramientas de inspección de bitácoras en modo de solo lectura.

:::nota
El reto está diseñado bajo la modalidad Capture The Flag (CTF) defensivo. A lo largo de la investigación encontrarás banderas o evidencias clave (con el formato `FLAG{...}`) que confirman que has superado cada etapa del análisis.
:::

## 2. Las cuatro etapas de la investigación

La resolución del reto sigue una secuencia profesional estructurada en cuatro fases cronológicas.

En la **Fase 1 (Triaje y contexto)** analizas la alerta inicial del cortafuegos, identificas las direcciones IP involucradas y determinas qué servicios de red fueron contactados inicialmente por el atacante.

En la **Fase 2 (Correlación con el agente)** utilizas el agente defensivo para inspeccionar los registros del servidor web y de la base de datos. El agente te ayuda a sintetizar más de mil líneas de bitácora en una línea de tiempo comprensible.

En la **Fase 3 (Trampa y contramedida)** descubres que el atacante escondió una instrucción maliciosa en uno de los campos de entrada del registro intentando engañar a tu agente para que borre las evidencias del ataque. Deberás aplicar las técnicas del Módulo M7 para neutralizar la inyección y proteger la memoria del agente.

En la **Fase 4 (Remediación y lecciones aprendidas)** clasificas las acciones conforme a las funciones del marco NIST CSF 2.0 y formulas las reglas definitivas para cerrar la brecha de seguridad.

:::alerta
Ten presente la regla de oro de la supervisión agéntica: tú tienes el control final. Nunca apruebes una recomendación del agente que involucre reiniciar servicios o alterar reglas de cortafuegos sin contrastar previamente las evidencias en los registros crudos.
:::

:::avanzada
### Profundización: Reconstrucción forense y reporte MITRE ATT&CK

En la ruta avanzada deberás vincular cada paso observado del adversario con la matriz formal MITRE ATT&CK, identificando las técnicas de reconocimiento inicial (T1595), explotación para acceso inicial (T1190) e intento de evasión de defensas mediante manipulación de LLM (AML.T0054 en MITRE ATLAS).

Tu entrega incluirá además el cálculo del impacto potencial en la confidencialidad e integridad de la base de datos y la formulación de una regla de detección YARA o Sigma para prevenir eventos similares en el futuro.
:::

:::laboratorio Laboratorio 7: Entorno del Reto Integrador
Para comenzar el reto ingresa a la carpeta `laboratorios/lab7/`. Allí encontrarás el conjunto de datos del incidente (`incidente.json`), los scripts de consulta con el agente y el instructivo detallado con las preguntas guía para descubrir las tres banderas de seguridad.
:::

Una vez que hayas completado la investigación en el laboratorio, responde la autoevaluación final para validar tus resultados y acreditar tu insignia de Campeón de ciberdefensa.
