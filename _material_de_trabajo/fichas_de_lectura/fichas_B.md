# Fichas bibliográficas — Lote B
Tesis: *Agentes de IA en ciberseguridad* (Ing. en Sistemas Computacionales, UAT) + guía didáctica de iniciación (CETIS / universidad).
Fuente: textos extraídos de los PDF en `scratchpad/txt/`. Todas las cifras provienen del texto del artículo; lo que no aparece en el documento se señala como "no indicado".

---

## Ficha 1 — Lazer, Aryal, Gupta y Bertino (2026)

### 1. Referencia APA 7
Lazer, S. J., Aryal, K., Gupta, M., & Bertino, E. (2026). *A survey of agentic AI and cybersecurity: Challenges, opportunities and use-case prototypes* (arXiv:2601.05293) [Preprint]. arXiv. https://arxiv.org/abs/2601.05293

- Notas: versión v1, 8 de enero de 2026, categoría cs.CR, 36 páginas. El PDF dice "Manuscript submitted to ACM"; el DOI de ACM que aparece es un marcador de posición (`10.1145/nnnnnnn.nnnnnnn`), así que todavía **no hay revista, volumen ni DOI definitivos**. Cítalo como preprint.
- Afiliaciones: Tennessee Tech University, University of Nebraska Omaha y Purdue University (EE. UU.).

### 2. Cita en texto
(Lazer et al., 2026) / Lazer et al. (2026)

### 3. Tipo
Survey (revisión narrativa amplia, no sistemática con protocolo PRISMA) más **tres prototipos de caso de uso** implementados por los autores.

### 4. Objetivo
Revisar qué implica la IA agéntica para la ciberseguridad en tres frentes: la defensa, la ofensiva y la gobernanza. También analiza los riesgos sistémicos propios de los agentes, los marcos de seguridad y los benchmarks, y muestra con prototipos mínimos cómo se comporta un agente en flujos reales de seguridad.

### 5. Metodología
- Síntesis de literatura académica, reportes de la industria (Unit 42, Microsoft, IBM, OWASP, NVIDIA) y documentos de política pública. Incluye una tabla que compara 15 surveys previos para ubicar su aporte.
- Organiza los casos de uso por fase del incidente (antes, durante y después) y los relaciona con las seis funciones del ciclo de ciberdefensa NIST: *Govern, Identify, Protect, Detect, Respond, Recover*.
- Construye taxonomías propias: casos de uso en 4 dominios, ataques habilitados por agentes en 4 dominios, y una tabla de marcos, benchmarks y mitigaciones.
- Implementa 3 prototipos con un LLM local ligero (Mistral vía Ollama) sobre datos sintéticos: (a) simulación adaptativa red vs. blue, (b) agente de triaje para el SOC y (c) agente de anomalías/IDS. En los tres hay una "compuerta de política" de solo lectura y una bitácora de auditoría.

### 6. Hallazgos clave (con cifras)
- El gasto global en IA para ciberseguridad pasaría de **24.8 mil millones de USD (2024) a 146.5 mil millones de USD (2034)**. La brecha de profesionales ronda los **4 millones** en el mundo (en otra sección los autores dan un rango de 4 a 5 millones).
- **Espectro de autonomía de 5 niveles (0–4)**, adaptado de NVIDIA y otras fuentes: 0 = inferencia estática (riesgo mínimo), 1 = asistivo (riesgo bajo), 2 = uso de herramientas con lógica preestablecida, por ejemplo RAG (riesgo moderado), 3 = adaptativo o semi-agéntico, que planifica, actúa y reflexiona con poca supervisión (riesgo alto), 4 = totalmente agéntico, que aprende de forma continua (riesgo muy alto y difícil de auditar).
- En el marco de ataque agéntico de Unit 42 (Palo Alto Networks), un agente completa **todo el ciclo de un ransomware en unos 25 minutos**. El tiempo medio de exfiltración bajó de **9 días (2021) a unos 2 días (2024)**, y en muchos incidentes tomó **menos de 1 hora**. Otro estudio de Unit 42 probó **9 escenarios de ataque** sobre frameworks como CrewAI y AutoGen.
- En un agente basado en Bash sin sandbox, **más del 75 % de los comandos maliciosos se ejecutan con éxito**. Con un sandbox en contenedor se bloquean casi todos (He et al., citado en el survey).
- Prototipo de triaje SOC (6 alertas sintéticas): las reglas base logran precisión de 1.00, *recall* de 0.75 y F1 de 0.86. El agente LLM llega a **1.00 en precisión, *recall* y F1**, y baja el MTTR simulado de **7.5 a 6.0 minutos**. Las **12 acciones** del agente cumplieron la política y quedaron registradas.
- Prototipo IDS con NetFlow sintético: la línea base (z-score + Isolation Forest) obtiene AUROC de 0.87 y F1 de 0.74. El agente con RAG obtiene **AUROC de 0.93 y F1 de 0.81**, y la utilidad de sus explicaciones promedia **0.83** en una rúbrica.
- En la simulación red vs. blue, a lo largo de 2 rondas, los agentes escalan sus tácticas sin guion humano: el agente rojo pasa de un RCE en Apache 2.4.49 a zero-day, phishing, malware polimórfico, *pass-the-hash* y DDoS, y el agente azul responde con parches, IDS/IPS, ATP, segmentación y monitoreo de la cadena de suministro.
- El benchmark FinGAIA contiene **407 tareas en 7 dominios financieros**.
- Hay patrones que se repiten en toda la literatura revisada. Predominan los diseños multiagente modulares con roles acotados. La autonomía se concede para acciones de bajo riesgo, y las acciones irreversibles quedan sujetas a supervisión humana. El agente funciona mejor como **aumento** del analista que como su reemplazo.

### 7. Definiciones y conceptos para el marco teórico (parafraseados)
- **IA agéntica**: es la etapa que sigue a la IA generativa. Parte de un modelo fundacional y le añade planificación, acción, memoria y adaptación, lo que permite resolver de forma autónoma problemas de varios pasos. Un LLM generativo es reactivo y responde una vez por *prompt*; un sistema agéntico mantiene estado y objetivos a lo largo de tareas largas. El survey retoma dos definiciones de terceros: una de la industria, que resalta el razonamiento y la planificación iterativa, y una académica, según la cual es un sistema sobre modelo fundacional que sigue instrucciones en lenguaje natural y razona, planifica e interactúa con herramientas y entornos para cumplir metas.
- **Componentes de la arquitectura**: memoria de corto plazo, episódica y de largo plazo; recuperación (bases vectoriales, RAG); herramientas y APIs (cómputo, navegación, ejecución de código); y conexión con entornos externos. Todo opera en un bucle de planificar, actuar, reflexionar y mejorar.
- **Cuatro características centrales**: razonamiento (descomponer problemas, *Chain-of-Thought*, reflexión), interacción (usar herramientas, consultar datos, colaborar con humanos), autonomía (actuar hacia metas con poca supervisión) y adaptabilidad (aprender de la memoria y la retroalimentación).
- **Arquitectura de un solo agente vs. multiagente**. En la de un agente hay un bucle de ejecución con planificación, acción y llamada a herramientas, más un LLM con *function calling*, memoria corta y un almacén vectorial. En la multiagente, un agente coordinador enruta subtareas a agentes especializados que comparten memoria de corto plazo y la capa de infraestructura.
- **Modelo de 4 capas de riesgo** (Wong y Saade): percepción (envenenamiento de datos, cadena de suministro), razonamiento (*prompt injection*, puertas traseras), acción (mal uso de APIs, ejecución de código no autorizado) y memoria (recuperaciones envenenadas, fuga de datos). Cada capa tiene sus defensas asociadas.
- **Dilema de doble uso**: las mismas capacidades que sirven para defender (planificar, recordar, orquestar herramientas) potencian el reconocimiento, la explotación y la ingeniería social.
- **Riesgos sistémicos**: colusión emergente entre agentes (incluida la esteganográfica), fallas en cascada, evasión de la supervisión, envenenamiento de memoria, "insider sintético" (un agente que actúa con credenciales válidas) y DoS por amplificación de costo (ataques tipo CRABS). El "impuesto de seguridad multiagente" es la pérdida de eficiencia que traen controles más estrictos.
- **Marcos citados**: OWASP Agentic Security Initiative, MAESTRO, ATFAA/SHIELD, la taxonomía de modos de falla de Microsoft, TRiSM, Cybersecurity Compass y NIST CSF. **Entornos de entrenamiento**: Cyberwheel (simulación y emulación con definición de red en grafos), ARCeR (genera cyber ranges desde lenguaje natural con multiagentes y RAG), CyberBattleSim, CybORG++ y "cyber gyms".
- **Supervisión**: *human-in-the-loop* (aprobación humana) y *human-on-the-loop* (escalamiento para acciones de alto impacto). También se mencionan la autonomía acotada y los "interruptores de apagado" (*kill switch*, como en RedTeamLLM).

### 8. Limitaciones y brechas señaladas
- Ningún marco integra en un solo stack la autonomía, los riesgos del ciclo de vida y el control en tiempo de ejecución. Las defensas se concentran en percepción y razonamiento, mientras que la acción y la interacción multiagente están menos cubiertas.
- Faltan benchmarks estandarizados que midan fallas en cascada, adversarios adaptativos y efectos de largo plazo. Existe un compromiso entre amplitud y precisión diagnóstica, y otro entre automatización y fidelidad.
- Los entornos simulados se transfieren mal a la operación real (el problema *sim-to-real*).
- No hay garantías formales de seguridad ante cambios de distribución ni ante manipulación adversaria.
- Faltan medidas de impacto a largo plazo sobre el personal: erosión de habilidades, calibración de la confianza y rendición de cuentas.
- Límites de los propios prototipos: usan datos sintéticos y muestras mínimas (6 alertas), un solo LLM ligero y no se evalúan contra adversarios reales.
- Agenda futura: inspección de entradas en tiempo real, transparencia de la ejecución interna, planificación con restricciones formales, aislamiento de instrucciones y datos, coordinación multiagente segura, memoria segura y gobernanza integrada al diseño.

### 9. Uso sugerido en la tesis
- **Marco teórico**: es la fuente principal para definir la IA agéntica, sus componentes, las arquitecturas de uno y varios agentes, los 5 niveles de autonomía y el modelo de 4 capas de riesgo.
- **Antecedentes / Justificación**: aporta las cifras de mercado (24.8 → 146.5 mil millones de USD), la brecha de 4 millones de profesionales y la compresión de los tiempos de ataque (ransomware en 25 min, exfiltración de 9 a 2 días).
- **Estado del arte**: sirve para mapear los casos de uso defensivos y ofensivos y los benchmarks existentes.
- **Metodología / guía didáctica**: los tres prototipos con Mistral y Ollama se pueden replicar en un laboratorio de CETIS o universidad, porque corren en local, usan datos sintéticos y trabajan en modo de solo lectura. Son un buen modelo de práctica segura.

---

## Ficha 2 — Jin, Guo y Cheung (2026)

### 1. Referencia APA 7
Jin, S., Guo, R., & Cheung, R. C. C. (2026). *CapSeal: Capability-sealed secret mediation for secure agent execution* (arXiv:2604.16762) [Preprint]. arXiv. https://arxiv.org/abs/2604.16762

- Notas: v1, 18 de abril de 2026, cs.CR. Afiliaciones: City University of Hong Kong y Beijing Foreign Studies University. El PDF no indica revista ni conferencia, y no tiene DOI.

### 2. Cita en texto
(Jin et al., 2026) / Jin et al. (2026)

### 3. Tipo
Propuesta de arquitectura, con prototipo en Rust y evaluación experimental. Es un artículo de sistemas o seguridad aplicada.

### 4. Objetivo
Resolver la exposición de secretos en el momento de su uso: API keys y credenciales SSH que hoy se entregan al agente mediante variables de entorno, archivos o sockets. La idea es que el agente nunca reciba el secreto; en su lugar obtiene una "capacidad" acotada que ejecuta un intermediario (*broker*) local de confianza.

### 5. Metodología
- Diseña una arquitectura en la que un broker local funciona como monitor de referencia, con punto de aplicación (PEP) y punto de decisión de política (PDP). El secreto se guarda cifrado y la bitácora de auditoría es de solo anexado y encadenada por hash.
- Define un protocolo de 6 etapas (`register`, `req_cap`, evaluación de política, `invoke`, ejecución mediada, `audit.prove`) y dos tipos de capacidad: HTTP restringido por esquema (JSON Type Definition) y SSH ejecutado por el broker, con el host fijado por su llave (*known_hosts_pin*).
- Implementa un prototipo en Rust con un adaptador para MCP (Model Context Protocol), usando JSON-RPC sobre Unix Domain Sockets.
- Evalúa 6 escenarios con guion (en HTTP y SSH: uso benigno, fuga de llave y uso no autorizado) contra 2 líneas base con secreto directo (B1 y B2). Para la latencia compara contra la ejecución directa y dos baselines reconstruidas, S1 (estilo CaMeL) y S2 (estilo ClawKeeper): 10 rondas × 50 ensayos medidos, **n = 500 por sistema y protocolo**, con intervalos de confianza de Wilson al 95 %.

### 6. Hallazgos clave (con cifras)
- **Fuga de llave en HTTP: 1.000 en B1 y B2, y 0.000 con CapSeal.** En SSH ningún sistema filtró la llave (0.000 en los tres).
- Uso no autorizado de credenciales: **0.000 en todos los sistemas y protocolos** (IC 95 % [0.000, 0.037]).
- Tareas benignas completadas: **1.000** en todos los casos (IC 95 % [0.963, 1.000]), así que la mediación no degradó la disponibilidad.
- Latencia HTTP (mediana): directa 0.160 ms, S1 0.392 ms, S2 0.896 ms, **CapSeal 0.309 ms**. La sobrecarga es de **0.149 ms**, contra 0.232 ms de S1 y 0.736 ms de S2.
- Latencia SSH (mediana): directa 7.470 ms, S1 7.795 ms, S2 8.421 ms, **CapSeal 7.678 ms**. La sobrecarga es de **0.208 ms**, contra 0.325 ms y 0.951 ms. En el P95, CapSeal-SSH queda en 10.500 ms, ligeramente por encima de los demás.
- CapSeal es el sistema mediado con **menor latencia** en ambos protocolos.
- Cuatro objetivos de seguridad: G1, que el secreto no se revele; G2, que cada invocación cumpla una política fina (mínimo privilegio, cuotas, autenticación reforzada o *step-up*); G3, que la capacidad esté ligada a la sesión y resista la repetición (secuencia monótona, *nonce* único, marca de tiempo en milisegundos); G4, auditoría a prueba de manipulación.
- Amenazas propias de los agentes que el artículo enumera: *prompt injection*, envenenamiento de *skills*, envenenamiento de MCP y ataques a la cadena de suministro. Menciona casos reales: axios, liteLLM y Clawhub.

### 7. Definiciones y conceptos para el marco teórico (parafraseados)
- **Problema de exposición en tiempo de uso**: cifrar el secreto en reposo no basta, porque el agente necesita usarlo y en ese momento puede ser manipulado para revelarlo. Un *bearer token* da acceso a cualquiera que lo tenga (RFC 6750), y un LLM puede transformarlo, parafrasearlo o exfiltrarlo.
- **Capacidad (capability)**: un permiso acotado, ligado a la sesión y no exportable, para realizar una acción concreta. Reemplaza la entrega de la credencial. En palabras de los autores, se pasa de "darle la llave al modelo" a "concederle una capacidad de acción estrecha".
- **Base de cómputo confiable (TCB)**: el broker, el motor de políticas, el almacén de secretos y la auditoría. El agente, en cambio, se considera una zona no confiable.
- **MCP (Model Context Protocol)**: un estándar para que los agentes descubran e invoquen herramientas. Facilita la integración, pero amplía la superficie de ataque a las descripciones de herramientas y a la selección de la herramienta.
- Principios de seguridad relacionados: mínimo privilegio, atenuación de autoridad (como en las *Macaroons*), auditoría con árboles de Merkle (como en *Certificate Transparency*), TEE y *fail-closed* (denegar cuando algo falla).

### 8. Limitaciones y brechas señaladas
- No cubre a un adversario con privilegios de root o control del kernel, ni canales laterales, ni la federación de brokers entre hosts o entornos multi-inquilino. El almacenamiento respaldado por hardware (TEE/TPM) queda como extensión futura.
- El modelo SSH en el que ejecuta el broker sacrifica compatibilidad: rompe los flujos que usan *agent forwarding*.
- El ecosistema MCP cambia rápido, por lo que el envenenamiento de herramientas se trata solo como experimento de extensión.
- Hay límites de validez. Las baselines S1 y S2 son reconstrucciones deterministas sin LLM real ni AgentDojo. En SSH ninguna baseline filtró la llave, así que el beneficio solo se observa en HTTP. La evaluación SSH con hosts remotos reales no se hizo por falta de aprobación de infraestructura. Varios resultados se describen como "plan de evaluación".

### 9. Uso sugerido en la tesis
- **Planteamiento del problema**: ilustra que los agentes crean superficies de ataque nuevas (*prompt injection*, envenenamiento de MCP, robo de credenciales), un riesgo que la guía didáctica debe enseñar.
- **Estado del arte (seguridad *de* los agentes)**: es un ejemplo de defensa por diseño con cifras claras (fuga de 100 % a 0 %, sobrecarga menor a 0.21 ms).
- **Marco teórico**: aporta los conceptos de mínimo privilegio aplicado a agentes, TCB, MCP y *bearer token*.
- **Guía didáctica**: sirve como caso para explicar a bachillerato por qué no se deben poner API keys en variables de entorno que el agente pueda leer.

---

## Ficha 3 — Abdelrazek y Lee (2026)

### 1. Referencia APA 7
**Como preprint (recomendada, porque tiene identificador verificable):**
Abdelrazek, Z., & Lee, Y. (2026). *Symbolic execution meets multi-LLM orchestration: Detecting memory vulnerabilities in incomplete Rust CVE snippets* (arXiv:2605.00034) [Preprint]. arXiv. https://arxiv.org/abs/2605.00034

**Como ponencia (según los metadatos del PDF):**
Abdelrazek, Z., & Lee, Y. (2026, 9–12 de junio). Symbolic execution meets multi-LLM orchestration: Detecting memory vulnerabilities in incomplete Rust CVE snippets. En *Proceedings of the 6th International Workshop on Software Security Engineering (SSE '26), co-located with EASE 2026* (11 pp.). ACM. [DOI no disponible: el PDF muestra el marcador `10.1145/XXXXXXX.XXXXXXX`]

- Notas: arXiv v1, 28 de abril de 2026, cs.CR. Afiliación: Texas A&M University–San Antonio. La sede es Glasgow, Escocia. Faltan el ISBN definitivo (aparece como 978-1-4503-XXXX-X) y el rango de páginas. Replicación: https://github.com/Zeyad-Ab/SymbolicExecution-with-Multi-LLM-Architecture-for-Rust-Security

### 2. Cita en texto
(Abdelrazek & Lee, 2026) / Abdelrazek y Lee (2026)

### 3. Tipo
Experimento o evaluación empírica de una propuesta: un sistema multiagente con LLM combinado con ejecución simbólica (KLEE).

### 4. Objetivo
Permitir el análisis profundo de vulnerabilidades de memoria en código Rust `unsafe` a partir de fragmentos de CVE incompletos, sin *structs*, *imports* ni `Cargo.toml`, que ninguna herramienta formal puede compilar. Para ello usa 4 agentes LLM especializados que generan *harnesses* FFI compatibles con KLEE.

### 5. Metodología
- Es un pipeline secuencial de 4 agentes que se comunican con JSON estructurado:
  1. **Oracle/Validator** (GPT-4 Turbo): planea y clasifica la vulnerabilidad, y recomienda de 8 a 12 funciones FFI.
  2. **Safety Checker** (Claude Opus 4.5): analiza a fondo, asigna un riesgo de 0 a 10 y marca las líneas críticas.
  3. **Code Specialist** (Claude Sonnet 4.5): genera el *wrapper* FFI en Rust (con `max_tokens` = 2500) y a partir de él se sintetiza el arnés en C.
  4. **Fast Filter** (GPT-4o-mini): elige los parámetros de KLEE (DFS, BFS o *random-path*, límites y profundidad).
- Después KLEE ejecuta el análisis simbólico y `graph_klee.py` construye una base de datos en grafo (nodos CVE, CWE, ErrorType y SymPath) exportada en JSON-LD.
- El dataset son **31 CVE reales de Rust** (el subconjunto de seguridad de memoria de HALURust) que abarcan **11 categorías CWE**.
- Compara contra Kani, Prusti, Creusot y Haybale (verificación formal), Miri, Clippy y cargo-geiger (herramientas prácticas), y contra una baseline de un solo agente (Claude Sonnet 4.5 con `max_tokens` = 1500).
- Si la compilación falla, hasta 2 reintentos se corrigen con el error del compilador; después se recurre a una plantilla de respaldo.

### 6. Hallazgos clave (con cifras)
- **Compilación de *wrappers*: 90.3 %** (28 de 31), contra **0 %** en las cuatro herramientas formales.
- **Detección: 26 de 31 archivos (83.9 %)**, con **1,206 errores críticos**: 124 de puntero (`ptr.err`) y 1,082 externos o de *panic*. Clippy produjo 14 advertencias en 11 archivos (**35.5 %**). Miri marcó comportamiento indefinido genérico en los 31, pero sin detallar el tipo de fallo.
- **Multiagente vs. un solo agente**: compilación de 58.0 % a 90.3 %, uso de plantilla de respaldo de 42.0 % a 9.7 %, detección de 51.6 % a **83.9 %** (+32 puntos porcentuales) y errores de 487 a **1,206** (unas 2.5 veces más). El tiempo por archivo sube de 4.2 a 6.8 minutos.
- Frente a Clippy: 15 archivos detectados solo por el sistema, 0 solo por Clippy, 11 por ambos y 5 por ninguno. Hubo 417 errores que Clippy no vio. En volumen, el sistema produce unas 86 veces más hallazgos.
- **9 de 11 CWE con 100 % de detección**. Las excepciones son CWE-190 (desbordamiento de enteros, 1 de 3) y CWE-416 (*use-after-free*, 6 de 9).
- La distribución está sesgada: dos CVE (2020-35904 con 752 errores y 2022-36008 con 381) suman **1,133 de 1,206 (93.9 %)**.
- El contexto que falta en los fragmentos: *imports* y `Cargo.toml` en el 100 %, definiciones de *struct* en el 90.3 % y *traits* en el 61.3 %.
- El grafo resultante tiene 31 nodos CVE, 5 ErrorType, 11 CWE y 1,206 SymPath, con 1,310 aristas.
- La planificación del agente Oracle es la que más explica la mejora sobre el agente único.

### 7. Definiciones y conceptos para el marco teórico (parafraseados)
- **Sistema multiagente LLM con especialización de roles**: dividir una tarea compleja entre agentes con roles distintos y contexto enfocado reduce las alucinaciones y mejora la calidad frente a un modelo generalista. El artículo lo relaciona con ChatDev y MetaGPT.
- **Paso de contexto estructurado (JSON)**: la salida de cada agente restringe el espacio de acción del siguiente.
- **Ejecución simbólica**: explorar un programa con entradas simbólicas (en KLEE, `klee_make_symbolic`) para encontrar rutas que provocan fallos y generar contraejemplos concretos.
- **"Problema del código incompleto"** y **aproximación semántica**: el *wrapper* no reconstruye el programa original, sino que reproduce la *clase* de fallo en tipos compatibles.
- Taxonomía de trabajos relacionados en seguridad multiagente: AutoAttacker (pentesting automatizado), PentestGPT (guía de pentesting) y LLM4Vuln (razonamiento sobre vulnerabilidades).

### 8. Limitaciones y brechas señaladas
- Los *wrappers* aproximan la clase de vulnerabilidad pero no la ruta exacta de explotación, y la detección baja en CWE-416 y CWE-190.
- Los LLM no son deterministas: se usó la temperatura por defecto y cada corrida puede dar resultados distintos. Los resultados dependen también de las versiones de los modelos.
- El conteo de errores refleja rutas simbólicas, no vulnerabilidades distintas. Algunos errores externos son artefactos de las funciones de respaldo.
- El dataset es pequeño y desbalanceado: 31 CVE, con 9 de CWE-416 frente a 1 de CWE-134. No es una muestra estratificada.
- El "100 %" de Miri es engañoso, porque solo da etiquetas genéricas.
- Trabajo futuro: un dataset más grande, más contexto desde los repositorios, *fine-tuning* del Code Specialist y retroalimentación de KLEE hacia los agentes.

### 9. Uso sugerido en la tesis
- **Estado del arte (agentes defensivos para gestión de vulnerabilidades)**: muestra con cifras que la arquitectura multiagente supera a la de un solo agente (+32 pp de detección).
- **Marco teórico**: es un ejemplo concreto de roles especializados, orquestación y uso de herramientas externas (KLEE) por parte de agentes LLM.
- **Metodología**: sirve de modelo de diseño experimental con baseline de agente único, ablación, amenazas a la validez y paquete de replicación público.
- **Guía didáctica**: el caso de CVE-2020-35904 ayuda a explicar qué es un CVE/CWE y por qué Rust `unsafe` puede fallar. Para bachillerato conviene presentarlo de forma conceptual.

---

## Ficha 4 — Petrovic et al. (2026)

### 1. Referencia APA 7
Petrovic, N., Jeddou, O., Ben Fraj, F., Zolfaghari, V., Pan, F., Schamschurko, A., & Knoll, A. (2026). *CyberLLM: A multi-agent LLM framework for autonomous detection and guarded response in automotive cybersecurity* (arXiv:2608.06651) [Preprint]. arXiv. https://arxiv.org/abs/2608.06651

- Notas: v1, 6 de agosto de 2026, cs.CR. Afiliación: Chair of Robotics, Artificial Intelligence and Real-Time Systems, Technical University of Munich. Financiado por European Chips JU (HAL4SDV, n.º 101139789) y el BMFTR de Alemania (16MEE00471K). El PDF no indica revista ni conferencia. En la línea de autores el nombre es "Jeddou", aunque el correo dice "jaddou"; se respeta la línea de autores. Código: https://github.com/Jeddou10/CyberLLM

### 2. Cita en texto
(Petrovic et al., 2026) / Petrovic et al. (2026)

### 3. Tipo
Propuesta de marco o framework multiagente con implementación y evaluación experimental sobre un benchmark propio con etiquetas de verdad de referencia.

### 4. Objetivo
Detectar vulnerabilidades de forma autónoma en código, logs y topologías de despliegue de vehículos definidos por software (SDV), y ejecutar remediaciones escalonadas. Todo ocurre dentro de una "envolvente de seguridad" determinista y auditable, que impide que el agente cometa acciones inseguras aunque lo manipulen.

### 5. Metodología
- **Detección en capas**. Primero una capa determinista siempre activa: reglas regex en YAML, analizadores AST (Bandit y Semgrep) y verificación de invariantes de topología (TOP-001 a TOP-008). Encima, un paso de refinamiento con LLM anclado a esas reglas (estilo RAG) y un segundo paso crítico que pregunta "¿qué se te escapó?".
- **Agente de decisión**: elige un nivel de respuesta (ninguna, suave, moderada o dura) y una confianza entre 0 y 1. Una política determinista que