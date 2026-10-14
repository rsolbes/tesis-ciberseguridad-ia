# Fichas bibliográficas — Lote C
Tesis: *Agentes de IA en ciberseguridad* + guía didáctica de iniciación (CETIS / universidad) — Ingeniería en Sistemas Computacionales, UAT.

Orden sugerido por **confiabilidad** (de mayor a menor):
1. Tantaroudas et al. (2026) — *Open Research Europe* (SentinelSphere) — **alta/media-alta**
2. Vijetha (2026) — *IEEE Access* (AISAF) — **media-alta**
3. Adabara et al. (2025) — *F1000Research* (revisión narrativa) — **media**
4. Meesala (2024) — *WJARR* — **baja**
5. Lingam (2025) — *IJCTEC* — **muy baja**
6. Dirisu et al. (2025) — *TIJSRAT* — **muy baja**

---

## FICHA C1 — SentinelSphere (detección + educación en concientización)

**1. Referencia APA 7**
Tantaroudas, N. D., Karachalios, I., & McCracken, A. J. (2026). SentinelSphere: An AI-driven cybersecurity platform integrating real-time threat detection with security awareness education [version 2; peer review: 2 approved, 2 approved with reservations]. *Open Research Europe, 6*, Artículo 58. https://doi.org/10.12688/openreseurope.22957.2

- Versión 1: 25 feb 2026 (https://doi.org/10.12688/openreseurope.22957.1); versión 2: 13 jun 2026. Citar la versión que se haya leído (este texto es la v2).
- No tiene paginación tradicional: se usa número de artículo (6:58).

**2. Cita en texto**
(Tantaroudas et al., 2026) / Tantaroudas et al. (2026)

**3. Tipo**
Artículo de investigación aplicada: desarrollo de sistema (prototipo de plataforma) + evaluación experimental con datasets de referencia + validación con usuarios en talleres (estudio exploratorio pre/post, no pareado).

**4. Objetivo**
Presentar y validar una plataforma que une, en un solo sistema, la detección de amenazas en tiempo real mediante aprendizaje profundo con la formación en concientización de seguridad mediante un chatbot basado en un LLM, para atacar a la vez el problema técnico (falsos positivos, fatiga de alertas) y el factor humano.

**5. Metodología**
- Extensión del marco europeo ResilMesh (Horizon Europe, acuerdo n.º 101119681); canal de datos Vector → NATS → detector → OpenSearch/Redis → tablero web (FastAPI).
- Detección: red neuronal profunda "Enhanced DNN" (64-64-salida) con 31 atributos (21 de red + 10 específicos de HTTP: complejidad de petición, entropía de ruta, detección de herramientas automatizadas, patrones de SQLi/XSS/fuerza bruta). Entrenada con CIC-IDS2017 y CIC-DDoS2019; desbalance tratado con pesos de clase inversos a la frecuencia y umbral de decisión 0.4 (sin SMOTE).
- "Semáforo" (Traffic Light System): puntaje 0–100 → verde (0–30), amarillo (30–70), rojo (70–100), a partir de factores de frecuencia, agrupamiento temporal, concentración de IP, diversidad y persistencia del ataque.
- Educación: chatbot con Microsoft Phi-4 cuantizado (Q4_K_M, llama.cpp, GGUF) + RAG con ChromaDB, ejecutable solo con CPU y 16 GB de RAM.
- Reescritura del detector de Python a Rust; pruebas de escalabilidad; dos talleres en Grecia (14 y 31 de octubre de 2025) con 79 participantes (3 profesionales; 76 en entorno universitario, con 39 cuestionarios pre y 36 post, anónimos y no pareados).

**6. Hallazgos clave (cifras)**
- Enhanced DNN vs. línea base de ResilMesh: **F1 94 %** (vs. 91.1 %), **exactitud 97.7 %** (vs. 96.4 %), **precisión 96.9 %** (vs. 91 %), recall 91.3 %.
- **Reducción de falsos positivos de 69.5 %** (de 59 a 19); **tasa de falsos positivos 0.7 %** (vs. 2.3 %).
- Detección por clase: fuerza bruta web 91.2 % (1,507 muestras), XSS 94.4 % (652), inyección SQL 90.5 % (solo 21 muestras).
- Rust: **5.6× más rápido** en operación normal; de 4.3× hasta **326×** en lotes grandes (100,000 eventos: 1,756.9 s en Python vs. 5.39 s en Rust); de ~314,000 a ~6,375 ciclos de CPU por evento.
- Escalabilidad: **10,900,927 eventos en ~30 min** (>5,000 eventos/s), latencia del canal <100 ms, 100 % de eventos clasificados en <1 s, >1,000 conexiones simultáneas.
- Chatbot: modelo de 28 GB → 2.5 GB; primer token en <1 s; 15–20 tokens/s en CPU; 8+ sesiones simultáneas; 6–8 GB de RAM.
- Diagnóstico previo en el taller educativo (n = 39, mayoría de 18–20 años, estudiantes de pedagogía): **92.3 % sin conocimiento del RGPD/GDPR**, **84.6 % sin 2FA** (o no sabía), **59 % reutiliza contraseñas**, **solo 23.1 % reconocía correos de phishing**, 51.3 % nunca había identificado phishing; 51.3 % usa herramientas de IA con frecuencia.
- Evaluación posterior (n = 36): comprensibilidad 8.72/10; **91.7 % entendió el semáforo** ("claro" o "muy claro"); 91.7 % usó el chatbot; facilidad de uso 4.06/5 (81.2 %), utilidad 3.82/5 (76.4 %); **satisfacción 4.3/5 (86.1 %)**; **77.8 %** usaría la plataforma como docente.

**7. Definiciones / conceptos útiles para el marco teórico**
- **Factor humano**: la tecnología sola no basta; el comportamiento de las personas genera vulnerabilidades y a la vez es parte de la defensa (los autores retoman el DBIR de Verizon: 74 % de las brechas involucran el elemento humano).
- **Fatiga de alertas**: el exceso de falsos positivos de los SIEM satura a los analistas y hace que se escapen amenazas reales.
- **Ciberresiliencia**: más allá de prevenir, es prepararse, responder y recuperarse, asumiendo que los incidentes ocurrirán.
- **Seguridad basada en eventos como oportunidad de aprendizaje**: cada alerta sirve para mitigar y también para enseñar (ciclo "detectar–responder–educar").
- **Principios de una buena formación en concientización** (según la literatura que citan): continua, interactiva, contextualizada, con retroalimentación inmediata y apoyo visual; las campañas fallan por sobrecarga de información y poca relevancia personal.
- **Cuantización de LLM**: reducir la precisión numérica para ejecutar modelos grandes en equipos comunes. Es clave para planteles con pocos recursos.
- **RAG (generación aumentada por recuperación)**: el LLM consulta una base de conocimiento propia para responder con más exactitud sobre el dominio.

**8. Limitaciones / brechas**
- Solo se midió comprensión y satisfacción inmediatas; **no hay evidencia de cambio de conducta duradero** (2FA, contraseñas, phishing). Los autores proponen seguimiento a 3–6 meses.
- Cuestionarios anónimos y **no pareados** (39 vs. 36): no permiten inferir mejora individual.
- Taller profesional con **n = 3**, solo cualitativo.
- El 91.7 % de comprensión del semáforo proviene de una población novata; según un revisor, no se puede generalizar a analistas de un SOC.
- SQLi con solo 21 muestras: la "mejora de 4.8 %" es 19/21 vs. 18/21, es decir, una sola muestra de diferencia.
- Solo se compara con la línea base de ResilMesh, sin comparación externa con el mismo protocolo; no se describe la partición entrenamiento/prueba.
- Cobertura limitada a ataques HTTP; la base de conocimiento del chatbot requiere actualización (phishing con IA, inyección de prompts).
- **Inconsistencia a verificar**: el texto dice Phi-4 de 14 mil millones de parámetros, pero la ficha de despliegue indica "Phi-4-mini-Q4_K_M (2.5 GB)". Un modelo de 14B en Q4_K_M ocuparía bastante más de 2.5 GB, así que es probable que se haya usado la variante mini. Además, el texto cita el DBIR de Verizon 2023 mientras la lista de referencias pone la edición 2025.
- Participantes adultos (≥18 años). Para aplicar algo similar en un CETIS con menores de edad se necesitaría consentimiento de padres o tutores.

**9. Uso sugerido en la tesis**
- **Estado del arte (principal)**: es el antecedente más cercano a la guía didáctica, porque une detección con IA y educación mediante un asistente LLM.
- **Planteamiento del problema / Justificación**: cifras de brechas de conocimiento en jóvenes de 18–20 años (92.3 % sin RGPD, 84.6 % sin 2FA, 23.1 % reconoce phishing); justifican formar en ciberseguridad antes de la vida profesional. Déficit global de ~3.4 millones de profesionales (dato que los autores toman de ISC2 2023).
- **Metodología**: sirve de modelo para diseñar la validación de la guía (fases pre-evaluación → demostración y práctica guiada con chatbot → post-evaluación), y también como advertencia: conviene usar códigos anónimos para parear pre/post y hacer un seguimiento diferido para medir retención y conducta.
- **Marco teórico**: factor humano, ciberresiliencia y principios de formación en concientización.
- **Calidad**: Open Research Europe es la plataforma de la Comisión Europea, con revisión por pares abierta posterior a la publicación. La v2 tiene 2 aprobaciones y 2 aprobaciones con reservas, y el proyecto tiene financiamiento Horizon Europe. El código, el modelo y los datos agregados son abiertos (GitHub, Hugging Face, Zenodo). Es una fuente confiable, pero conviene señalar que la evidencia educativa es exploratoria. Aclaración: el sistema no es un "agente autónomo" en sentido estricto; combina un clasificador con un asistente LLM con RAG, por lo que conviene presentarlo como "IA aplicada / asistente conversacional" y no como IA agéntica plena.

---

## FICHA C2 — AISAF (IEEE Access)

**1. Referencia APA 7**
Vijetha, B. (2026). Agentic intelligence for unified cyber defense: A self-adaptive framework for threat detection across cloud, edge, and IoT systems. *IEEE Access, 14*, 5104–5118. https://doi.org/10.1109/ACCESS.2026.3650833

- Recibido: 18 dic 2025; aceptado: 26 dic 2025; publicado: 5 ene 2026. Autora única (NMAM Institute of Technology, NITTE, India). Licencia CC BY 4.0.

**2. Cita en texto**
(Vijetha, 2026) / Vijetha (2026)

**3. Tipo**
Marco/propuesta con evaluación experimental (modelo híbrido de aprendizaje profundo con controlador "agéntico" de auto-adaptación; comparación contra 10 líneas base en 6 datasets).

**4. Objetivo**
Proponer un marco de detección de amenazas que se ajusta solo cuando cambian el comportamiento del atacante o la distribución de los datos (*concept drift*). Detecta la deriva, decide de forma autónoma cuándo y qué módulos actualizar, y mantiene las explicaciones coherentes durante la adaptación, en entornos de nube, borde (*edge*) e IoT.

**5. Metodología**
- Arquitectura AISAF en 3 módulos: (1) extracción de características híbrida CNN + LSTM + Transformer; (2) controlador de meta-optimización que vigila la desviación en el espacio latente y la caída de confianza de las predicciones; (3) capa de decisión explicable basada en atención.
- Detector de deriva: ventanas de 512 muestras, puntaje combinado (λ = 0.5), umbral adaptativo μ + 1.5σ, persistencia de 3 ventanas y como máximo 1 adaptación cada 20 ventanas.
- Adaptación selectiva: solo se actualizan los submódulos afectados (normalmente LSTM o atención), con un lazo interno/externo tipo meta-aprendizaje. Métrica propuesta: índice de recuperación de deriva (DRI).
- 6 datasets: PaySim, IEEE-CIS Fraud, CICIDS2018, UNSW-NB15, CICIDS2017, BoT-IoT. Partición temporal estratificada 70/15/15, SMOTE solo en entrenamiento, deriva natural + deriva inyectada.
- 10 líneas base (LR, RF, LSTM, CNN-LSTM, Dynamic Ensemble, DWM, EWC, IDS con Transformer, IDS federado adaptativo, IDS no supervisado sensible a deriva). 5 corridas por experimento en GPU RTX A6000.

**6. Hallazgos clave (cifras)**
- F1 **8–12 % superior** a las mejores líneas base (promedio entre dominios).
- **DRI = 0.93 ± 0.02**: recuperación casi completa tras eventos de deriva.
- Recuperación **30–40 % más rápida** que las líneas base adaptativas (DWM, DE, EWC).
- Reduce la necesidad de reentrenamiento manual en **~70 %**.
- La adaptación selectiva cuesta **25–30 %** de un reentrenamiento completo; memoria durante la adaptación ≈ 0.42 de la del reentrenamiento completo (**−58 %**).
- Latencia de inferencia **−30 a −35 %** frente a sistemas con reentrenamiento completo.
- Complejidad del detector de deriva: de O(d²) (métodos basados en densidad) a **O(d)**.
- Estabilidad verificada durante más de 10⁶ iteraciones de inferencia.
- (Nota: la Tabla 3 con valores numéricos por modelo no quedó en el texto extraído; consultar el PDF para cifras exactas de precisión, recall y AUC.)

**7. Definiciones / conceptos útiles**
- **Concept drift (deriva de concepto)**: cambio con el tiempo en la relación estadística entre las características y las etiquetas. En ciberseguridad ocurre porque los atacantes cambian de táctica, los usuarios cambian de hábitos y los sistemas se reconfiguran.
- **Inteligencia agéntica (según la autora)**: capacidad del sistema de vigilarse y decidir por sí mismo cuándo adaptarse, qué adaptar y con qué intensidad, sin intervención humana. Sirve para mostrar que "agéntico" no siempre implica un LLM: aquí la autonomía está en un controlador de auto-adaptación.
- **Olvido catastrófico**: cuando una red neuronal pierde lo aprendido al entrenarse con datos nuevos; la adaptación selectiva lo mitiga.
- **Meta-aprendizaje**: "aprender a aprender", es decir, adaptarse rápido a tareas o condiciones nuevas.
- **Explicabilidad sincronizada**: las explicaciones (mapas de atención) se actualizan junto con el modelo, cosa que las herramientas post hoc como LIME o SHAP no hacen.
- **Brechas en los IDS adaptativos**: autonomía restringida (umbrales manuales), adaptación reactiva (actúan después de degradarse) y explicabilidad desconectada de la adaptación.

**8. Limitaciones / brechas**
- Ventanas fijas: puede fallar en flujos de latencia ultrabaja (deriva en escalas de sub-milisegundos).
- La explicabilidad se basa en atributos, no es causal ni contrafactual.
- Restricciones de cómputo en nodos de borde; falta robustez ante manipulación adversarial extrema.
- Resultados promediados entre dominios, con parte de la deriva inyectada de forma sintética y todo en datasets de laboratorio, sin despliegue real.
- **Detalles de rigor a considerar**: varias referencias no corresponden a lo que se cita. Por ejemplo, la [13] se presenta como "Dynamic Ensemble" pero es un artículo sobre reconocimiento de acciones por esqueleto; las [14] y [15] (deepfakes, propiedades no funcionales) se citan como métodos de evaluación de deriva; la [39] (enrutamiento en redes de sensores inalámbricas) se cita como IDS adaptativo; y Vaswani et al. aparece con año 2025. Además, la revisión fue muy rápida (8 días entre recepción y aceptación). El uso de "agéntico" es laxo: no hay planificación, herramientas ni LLM.

**9. Uso sugerido en la tesis**
- **Estado del arte**: ejemplo reciente de un IDS "auto-adaptativo" etiquetado como agéntico. Sirve para contrastar distintos niveles de agencia (adaptación autónoma vs. agentes LLM que planifican y ejecutan acciones).
- **Marco teórico**: conceptos de deriva de concepto, olvido catastrófico, meta-aprendizaje y explicabilidad. Para la guía didáctica, sirve para explicar por qué un modelo de detección "envejece" y necesita adaptarse.
- **Calidad**: IEEE Access es una revista con revisión por pares, indexada en JCR/Scopus (megarevista de acceso abierto con cobro de APC). La fuente es aceptable, pero conviene no apoyarse en sus referencias secundarias (varias están mal asignadas) y reportar sus cifras como "resultados reportados por la autora".

---

## FICHA C3 — Revisión narrativa de IA agéntica en ciberseguridad (F1000Research)

**1. Referencia APA 7**
Adabara, I., Olaniyi Sadiq, B., Nuhu Shuaibu, A., Ibarahim Danjuma, Y., & Venkateswarlu, M. (2025). A review of agentic AI in cybersecurity: Cognitive autonomy, ethical governance, and quantum-resilient defense [version 1; peer review: 2 approved]. *F1000Research, 14*, Artículo 843. https://doi.org/10.12688/f1000research.169337.1

- Los apellidos siguen la forma de "How to cite" de F1000 (Olaniyi Sadiq B; Nuhu Shuaibu A; Ibarahim Danjuma Y). En la portada los nombres aparecen como "Bashir Olaniyi Sadiq", "Aliyu Nuhu Shuaibu" y "Yale Ibarahim Danjuma"; si se prefiere, también sería válido usar Sadiq, B. O.; Shuaibu, A. N.; Danjuma, Y. I. Hay que elegir una forma y mantenerla.
- Publicado el 1 sep 2025; informes de revisión del 28 oct 2025. Afiliación: Kampala International University (Uganda). Datos suplementarios: https://doi.org/10.6084/m9.figshare.29966266

**2. Cita en texto**
(Adabara et al., 2025) / Adabara et al. (2025)

**3. Tipo**
Revisión narrativa (no sistemática) de literatura académica, industrial y de políticas (2005–2025), con marco conceptual integrador.

**4. Objetivo**
Sintetizar y analizar críticamente la evolución, la gobernanza y la resiliencia de la IA agéntica en ciberseguridad en torno a tres pilares (autonomía cognitiva, gobernanza ética y defensa resiliente ante la computación cuántica) y proponer un marco que conecte los mecanismos de gobernanza con la práctica operativa.

**5. Metodología**
- Revisión narrativa guiada por 4 preguntas de investigación: RQ1 patrones de diseño, RQ2 mecanismos de gobernanza ética, RQ3 estrategias de resiliencia (convencional y cuántica), RQ4 barreras y facilitadores.
- Búsqueda en IEEE Xplore, Scopus, Web of Science y ACM DL, más literatura gris (informes, documentos de política), con operadores booleanos, encadenamiento de citas y **uso de IA generativa** para sugerir términos y agrupar temas.
- Criterios: en inglés; artículos arbitrados, revisiones y literatura gris de calidad (2010–2025).
- Proceso en 5 etapas (identificar → cribar → seleccionar → clasificar → sintetizar) y síntesis temática por pregunta de investigación.

**6. Hallazgos clave (cifras y datos)**
- Bibliometría citada: las publicaciones sobre sistemas basados en agentes en ciberseguridad crecen desde 2013 y alcanzan su pico en **2023 con más de 1,200 artículos y más de 30,000 citas**, con aceleración después de 2018.
- Líderes en producción: China, EE. UU. e India (también se mencionan Reino Unido y UE). **África, Latinoamérica y parte del sudeste asiático están subrepresentados**, lo cual sirve para justificar investigación desde México.
- Evolución en 4 fases: automatización basada en reglas (antes de 2010) → integración de ML (2010–2020) → IA generativa e híbrida (2020–2023) → **era de la IA agéntica (2023 en adelante)**.
- Tabla de patrones de diseño con nivel de autonomía: agentes reactivos (bajo), proactivos orientados a metas (medio), basados en aprendizaje (alto), humano en el lazo (medio), redes federadas de agentes (medio-alto), bucles cognitivos reflexivos (alto).
- Marcos de gobernanza comparados: NIST AI RMF, EU AI Act (clasifica por riesgo; los agentes autónomos de ciberseguridad serían de alto riesgo), ISO/IEC 42001:2023 (sistema de gestión de IA certificable), IEEE 7000, principios de la OCDE y ética de la IA de la UNESCO.
- Caso piloto citado de criptografía post-cuántica (Kyber + McEliece con gestión de claves por IA): latencia de cifrado **menor a 4 ms**.
- Barreras: complejidad e interpretabilidad de los modelos, **brecha de habilidades**, integración con sistemas heredados, obligaciones regulatorias ambiguas, alto costo y falta de estándares. Facilitadores: arquitecturas modulares con XAI, **capacitación intersectorial**, nube, marcos alineados, financiamiento público-privado y protocolos abiertos (se mencionan A2A de Google y MCP).
- Horizontes de investigación: 1–3 años (XAI y defensa adversarial), 3–7 años (aprendizaje federado con criptografía post-cuántica), más de 7 años (IA neurosimbólica y MARL cuántico).

**7. Definiciones / conceptos útiles**
- **IA agéntica**: sistemas autónomos que persiguen metas complejas con mínima intervención humana, y que se distinguen por su adaptabilidad, su autonomía para decidir y su resiliencia operativa. A diferencia de la IA reactiva, planifican, se adaptan y ejecutan flujos de trabajo de forma proactiva.
- **Agente de ciberdefensa autónomo (AICA)**: agentes que perciben, razonan, actúan y aprenden sin supervisión constante, incluso cuando se pierde la comunicación con los operadores (retoman a Kott, 2023).
- **Autonomía cognitiva**: capacidad de procesar información, aprender de experiencias diversas y generar soluciones nuevas, incluyendo el manejo de dilemas éticos y objetivos en conflicto.
- **Gobernanza ética**: marcos, políticas y salvaguardas técnicas que aseguran transparencia, rendición de cuentas y alineación con valores humanos a lo largo del ciclo de vida.
- **Uso dual**: las herramientas defensivas (detección autónoma, sistemas de auto-reparación) pueden reutilizarse para ofender (sondeo autónomo, infiltración, malware auto-replicante).
- **Rezago regulatorio**: tiempo entre el avance tecnológico y su control legal o ético.
- **"Cosechar ahora, descifrar después"**: amenaza cuántica sobre RSA y ECC (algoritmo de Shor).
- **Taxonomía de sistemas agénticos** en 3 ejes: nivel de autonomía, dominio de aplicación y tipo de gobernanza (centralizada, descentralizada o híbrida).

**8. Limitaciones / brechas**
- Las señalan los autores: obsolescencia rápida, sesgo de datos, dependencia de simulaciones, subreporte de vulnerabilidades adversariales, sesgo de idioma (solo inglés), subjetividad de la síntesis narrativa y sesgo de publicación.
- Brechas de investigación: falta de estandarización de modelos de razonamiento, poco trabajo empírico sobre mitigación del uso dual, calibración de la confianza humano–agente poco estudiada, integración técnico-regulatoria fragmentada y **predominio de trabajos conceptuales sobre despliegues empíricos**.
- Observaciones críticas propias: el periodo es inconsistente (2005–2025 en el resumen vs. 2010–2025 en los criterios); no hay diagrama PRISMA ni conteo de estudios incluidos; muchas referencias vienen de revistas de bajo impacto (p. ej., IJSREM, IJARSCT); se usó IA generativa en la búsqueda. Uno de los dos revisores respondió "Partly" a si las afirmaciones están bien sustentadas, y el otro pidió más casos reales y reflexión crítica sobre la calidad de las fuentes.

**9. Uso sugerido en la tesis**
- **Marco teórico (principal)**: definiciones de IA agéntica, AICA, autonomía cognitiva, gobernanza ética y uso dual; tabla de patrones de diseño por nivel de autonomía, útil para la guía didáctica (del agente reactivo al agente reflexivo).
- **Antecedentes**: las 4 fases históricas y el crecimiento bibliométrico.
- **Justificación**: la subrepresentación de Latinoamérica y la brecha de habilidades apoyan la necesidad de una guía de iniciación.
- **Marco normativo**: la tabla comparativa NIST AI RMF / EU AI Act / ISO/IEC 42001 / OCDE / UNESCO.
- **Calidad**: F1000Research tiene revisión por pares abierta después de publicar (2 "approved") y se indexa en PubMed/Scopus tras aprobar. Es aceptable como revisión de alcance general, pero por ser narrativa y apoyarse en fuentes secundarias de calidad variable, conviene verificar en la fuente original cada cifra que se tome (p. ej., las 1,200 publicaciones o la latencia de <4 ms).

---

## FICHA C4 — Uso dual y gobernanza (WJARR)

**1. Referencia APA 7**
Meesala, L. K. (2024). Agentic AI in cybersecurity: Dual-use dynamics, threat vectors, and governance imperatives. *World Journal of Advanced Research and Reviews, 24*(3), 3667–3672. https://doi.org/10.30574/wjarr.2024.24.3.3738

- Recibido: 2 nov 2024; revisado: 27 dic 2024; aceptado: 29 dic 2024. Autor afiliado a Gilead Sciences Inc. (empresa farmacéutica, EE. UU.). Licencia CC BY 4.0.

**2. Cita en texto**
(Meesala, 2024) / Meesala (2024)

**3. Tipo**
Artículo corto (6 páginas) de marco/propuesta con evaluación experimental declarada: modelo de amenaza de uso dual, índice de riesgo (DURI) y taxonomía de gobernanza en 3 niveles.

**4. Objetivo**
Formalizar el modelo de amenaza de uso dual de la IA agéntica en ciberseguridad (defensa y ataque con la misma tecnología), proponer un índice cuantitativo de riesgo de despliegue y un marco de gobernanza, y evaluar el desempeño en tres escenarios: caza autónoma de amenazas, ingeniería social con IA y explotación adversarial de modelos.

**5. Metodología**
- Superficie de amenaza modelada como grafo dirigido acíclico (capacidad del agente → vector de ataque).
- Índice DURI(C) = 0.45·P(armamentización) + 0.35·Δ superficie de ataque − 0.20·utilidad defensiva; un puntaje ≥ 7.0 obliga a revisión de gobernanza.
- Arquitectura en ciclo cerrado percepción–planificación–ejecución: motor de percepción, planificación con cadena de pensamiento, memoria persistente, ejecutor de herramientas (SOAR, firewall, gestión de identidades), módulo de reflexión y plano de control de gobernanza (humano en el lazo obligatorio si DURI > 7.0).
- Evaluación declarada con 14,000 eventos sintéticos y 3,200 reales de dos entornos "Fortune 500" anonimizados (17,200 en total), más tres ataques implementados en un banco de pruebas aislado.

**6. Hallazgos clave (cifras reportadas)**
- Exactitud de detección: **agente 94.7 %** vs. XGBoost 78.3 % vs. IDS basado en reglas 71.4 % (+16.4 puntos porcentuales).
- F1: 0.946 vs. 0.782 vs. 0.710. Tasa de falsos positivos: **5.3 %** vs. 19.7 % vs. 28.6 %.
- Tiempo medio de detección (MTTD): **81 min** vs. 187 vs. 312 (**−74 %**).
- Uso ofensivo: spear-phishing con LLM con **3.4× más clics** que plantillas; encadenamiento de CVE que reduce el tiempo de explotación de **4.2 h a 11 min (−96 %)**; la inyección de prompts evadió la detección en **23 %** de los intentos.
- Aumento de **3.2×** en la complejidad de la superficie de ataque cuando la tecnología se usa como arma.
- DURI por capacidad: razonamiento autónomo 4.1 (moderado), uso de herramientas/API 6.8 (elevado), memoria persistente 7.2 (alto), **auto-modificación 9.2 (crítico)**, **coordinación multiagente 8.7 (crítico)**.
- Tasa de evasión del agente frente al ML estático: inversión de modelo 14.7 % vs. 61.4 %; perturbación 9.3 % vs. 44.2 %; envenenamiento 11.2 % vs. 38.7 %; movimiento lateral 18.4 % vs. 52.1 %. La **inyección de prompts (23.1 %) es una vulnerabilidad nueva, exclusiva de los agentes LLM**.
- Contexto citado: MTTD de una brecha de **207 días** (IBM, 2023) y **40–60 %** de falsos positivos en IDS basados en reglas en producción.
- Controles propuestos: DURI antes del despliegue, *red teaming* cada 30 días y bitácoras de explicabilidad para acciones con DURI > 5.0.

**7. Definiciones / conceptos útiles**
- **IA agéntica**: sistemas autónomos orientados a metas, capaces de razonar en varios pasos y actuar de forma independiente.
- **4 rasgos de los agentes**: persistencia de metas en tareas de varios pasos, percepción del entorno mediante API de herramientas, planificación autodirigida (cadena o árbol de pensamiento) y modificación de conducta a partir de la retroalimentación.
- **Ciclo percepción–planificación–ejecución** con reflexión (autocrítica para reducir falsos positivos) y memoria entre sesiones.
- **Uso dual**: la misma arquitectura aporta capacidad defensiva y ofensiva (ejemplos: PentestGPT para pruebas de penetración autónomas y campañas de phishing autónomas).
- **Humano en el lazo por umbral de riesgo**: acciones de bajo riesgo automatizadas; acciones de alto riesgo con aprobación humana.
- **Inyección de prompts**: vector de ataque propio de los agentes basados en LLM.
- **Marco regulatorio**: EU AI Act (2024) y NIST AI RMF (2023) clasifican la IA de ciberseguridad como de alto riesgo, pero no fijan umbrales específicos para la acción autónoma; el DURI se vincula con la función *Govern* del NIST CSF 2.0.

**8. Limitaciones / brechas**
- Las señala el autor: falta de estándares de *red teaming* (propone integrarlos con MITRE ATT&CK), inyección de prompts sin resolver (sugiere sandbox, atestación criptográfica y entrenamiento adversarial) y falta de un DURI multiagente.
- **Problemas de rigor detectados**:
  - La fórmula DURI con los valores de la Tabla 2 no reproduce los puntajes reportados. Por ejemplo, para razonamiento autónomo: 0.45·0.42 + 0.35·0.55 − 0.20·0.88 ≈ 0.21, no 4.1. Con esos pesos el máximo posible ni siquiera llega a 1.
  - No describe los modelos, datos ni configuración reales de los "tres sistemas agénticos"; los datos "Fortune 500" no son verificables.
  - Referencias con datos erróneos o inexistentes: Sommer & Paxson aparece como 2019 (es 2010); Anderson & Moore en *Science* 314 aparece como 2020 (es 2006); Goodfellow et al. aparece como 2018 (es ICLR 2015); "Minsky & Papert (2019), Adversarial robustness…, JMLR" no parece existir. Además hay autocitas de terceros en revistas de baja calidad (IJSRCSEIT, IJFIST, IAEME).
  - Revisión de solo 2 días entre versión revisada y aceptación; afiliación del autor ajena al área académica.

**9. Uso sugerido en la tesis**
- **Planteamiento del problema / Marco teórico (uso dual)**: solo como apoyo ilustrativo del concepto de uso dual y de la inyección de prompts como riesgo nuevo, **sin tomar sus cifras como evidencia sólida**.
- Para la guía didáctica es útil su lista de capacidades agénticas (razonamiento, herramientas, memoria, auto-modificación, coordinación multiagente), ordenadas por nivel de riesgo, como recurso para que los estudiantes discutan riesgos.
- **Calidad: BAJA.** WJARR (GSC Online Press) aparece con frecuencia en listas de revistas de acceso abierto con prácticas cuestionables (publicación rápida por cobro, revisión mínima). Recomendación: citar preferentemente fuentes primarias (NIST AI RMF, EU AI Act, Brundage et al., 2018; Happe & Cito, 2023) y, si se usa este artículo, advertir que sus resultados no son verificables.

---

## FICHA C5 — Marco AAI-CTDM (IJCTEC)

**1. Referencia APA 7**
Lingam, V. P. (2025). Agentic AI framework for autonomous cyber threat detection and mitigation. *International Journal of Computer Technology and Electronics Communication (IJCTEC), 8*(6), 11986–11992. https://doi.org/10.15680/IJCTECE.2025.0806043

- Número: noviembre–diciembre 2025. Autor: "AI Architect, USA" (sin afiliación institucional). ISSN 2320-0081.

**2. Cita en texto**
(Lingam, 2025) / Lingam (2025)

**3. Tipo**
Marco/propuesta conceptual con resultados experimentales declarados (arquitectura multiagente jerárquica).

**4. Objetivo**
Proponer un marco de IA agéntica (AAI-CTDM) con múltiples agentes especializados que observen, razonen, planifiquen, ejecuten, aprendan y colaboren para detectar y mitigar ciberamenazas de forma autónoma, superando a los IDS basados en firmas y en ML tradicional.

**5. Metodología**
- Arquitectura de 7 capas: adquisición de datos, inteligencia de amenazas (RAG sobre MITRE ATT&CK y CVE), coordinación multiagente, razonamiento con LLM, motor de aprendizaje por refuerzo, capa de XAI y capa de acción de seguridad, con un coordinador central de agentes.
- Agentes: monitoreo, detección, evaluación de vulnerabilidades, gestión de incidentes, forense y políticas.
- Modelo matemático sencillo: clasificador P(y|F), pérdida de entropía cruzada, riesgo = w1·V + w2·A + w3·E + w4·C, y selección de la acción que maximiza U = tasa de detección − tasa de FP − retardo.
- Herramientas mencionadas: Python 3.11, PyTorch, LangChain/LangGraph, FAISS, Stable-Baselines3, Docker. El texto dice que la implementación "can be developed" (podría desarrollarse), lo que sugiere que quizá no se implementó.
- Datasets enumerados: CICIDS2017, CSE-CIC-IDS2018, UNSW-NB15, Bot-IoT, Edge-IIoTset.

**6. Hallazgos clave (cifras reportadas)**
- Exactitud: **99.41 %** (vs. SVM 93.84, RF 96.11, CNN 97.18, LSTM 97.82, IDS con Transformer 98.46).
- Precisión 0.995, recall 0.993, F1 0.994.
- Tasa de falsos positivos: **0.72 %** (vs. 4.8 % SVM … 1.8 % Transformer).
- Tiempo de respuesta promedio: **64 ms** (vs. SOC basado en reglas 460 ms, IDS con ML 285, IDS con DL 171, SOAR 112).
- Tasa de mitigación exitosa: **98.6 %** (vs. reglas 82.4 %, IDS con ML 87.8 %, IDS con DL 91.5 %, SOAR 94.2 %).
- Escalabilidad: exactitud de 99.42 % (100 nodos) a 99.34 % (10,000 nodos).

**7. Definiciones / conceptos útiles**
- **IA agéntica vs. IA generativa guiada por prompts**: la agéntica integra razonamiento autónomo, planificación a largo plazo, memoria, uso de herramientas, cooperación multiagente y aprendizaje adaptativo, y realiza tareas complejas con poca intervención humana.
- **Capacidades del agente**: observación, razonamiento, planificación, ejecución, aprendizaje y colaboración (útil como esquema didáctico del ciclo percepción → razonamiento → acción → aprendizaje).
- **Combinación LLM + RAG + RL + XAI**: el LLM razona sobre el contexto, RAG trae inteligencia de amenazas actualizada, el RL mejora las políticas de mitigación con retroalimentación y la XAI justifica las decisiones ante el analista.
- **Fatiga de alertas** en los SOC y limitaciones de los IDS basados en firmas frente a ataques de día cero.

**8. Limitaciones / brechas**
- Trabajo futuro que propone el autor: aprendizaje federado multiagente, GNN y grafos de conocimiento para APT, inteligencia multimodal, agentes ligeros para IoT/edge, blockchain para comunicación entre agentes y validación en SOC reales.
- **Problemas graves de rigor**:
  - No especifica en qué dataset se obtuvo cada resultado, ni la partición, los hiperparámetros, el número de corridas o la variabilidad.
  - No describe cómo se midieron el "tiempo de respuesta" ni el "éxito de mitigación", ni cómo se simularon 10,000 nodos.
  - La sección "VIII. Visualization" está vacía.
  - La redacción condicional ("can be developed") sugiere que los resultados podrían ser ilustrativos y no experimentales.
  - Las 10 referencias no guardan relación con la sección de trabajos relacionados: agente de IA para juegos (2017), chatbot argumentativo sobre cambio climático, definición NIST de nube (2011), CIS Controls v7.1 y guía de ENISA para pymes (2016). Ninguna trata de IA agéntica.
  - Autor sin afiliación académica; artículo de 7 páginas.

**9. Uso sugerido en la tesis**
- **Solo como ejemplo** de arquitectura multiagente propuesta (capas y roles de agentes), por ejemplo en una figura de la guía didáctica que muestre "cómo podría organizarse un SOC con agentes". **No usar sus cifras como evidencia.**
- **Calidad: MUY BAJA.** El sello "Peer-Reviewed, Refereed… ISO 9001:2008 Certified Journal" y el prefijo DOI 10.15680 son característicos de un grupo editorial señalado frecuentemente como depredador. Si se cita, conviene hacerlo en el estado del arte con la nota "propuesta no verificada experimentalmente" o, mejor, sustituirlo por fuentes arbitradas.

---

## FICHA C6 — Agentes de ciberdefensa con RL auto-reparadores (TIJSRAT)

**1. Referencia APA 7**
Dirisu, C. D., Rapheal, O., Elijah, T. D., Olatokun, T. W., Oluwafemi, A. A., & Ike, P. C. (2025). Autonomous cyber defense agents utilizing reinforcement learning for self-healing network security. *International Journal of Science Research and Technology, 9*(9), 113–138. https://doi.org/10.70382/tijsrat.v09i9.060

- Editorial: Timbou-Africa Publication; edición de agosto de 2025. P-ISSN 3027-1991; E-ISSN 3026-8095.
- Autores tal como aparecen: Christian Davison Dirisu; Odara Rapheal (grafía original); Temitope Damilola Elijah; Toluwanimi Williams Olatokun; Ajagbe Ayodeji Oluwafemi; Peace Chinonyerem Ike. **Verificar** el apellido del quinto autor: si "Ajagbe" es el apellido, debe escribirse "Ajagbe, A. O.".
- El volumen y número se infieren del encabezado y del DOI (v09i9); el encabezado del texto extraído está dañado.

**2. Cita en texto**
(Dirisu et al., 2025) / Dirisu et al. (2025)

**3. Tipo**
Híbrido: revisión de literatura (amplia) + experimento de simulación declarado (agente de aprendizaje por refuerzo profundo en CybORG) con validación por operadores.

**4. Objetivo**
Evaluar si agentes de aprendizaje por refuerzo profundo (DRL) pueden defender y "auto-reparar" redes (detectar, aislar y recuperar) ante adversarios realistas, generalizar a topologías no vistas, resistir perturbaciones adversariales y ser interpretables para los operadores.

**5. Metodología**
- Simulación de una red empresarial en CybORG (subredes de usuario, empresa y operación) con dos atacantes: *b_line* (va directo a activos críticos) y *red_meander* (explora camino por camino).
- Agente con política basada en Graph Attention Network (GAT) actor-crítico; algoritmos PPO (base) y TD3; preentrenamiento supervisado y ~1,000 episodios por escenario; aprendizaje abierto (*open-ended learning*).
- Acciones de auto-reparación: aislar hosts, desplegar honeypots y restaurar instantáneas limpias.
- Métricas: tasa de compromiso, tiempo de recuperación, AUC de resiliencia, tasa de falsos positivos y costo de recursos. 50 corridas por condición; ANOVA, t de Student y Kruskal-Wallis.
- Pruebas en 5 topologías no vistas, perturbaciones adversariales (defensa por votación de ensamble y ajuste fino adversarial) y estudio *think-aloud* con operadores (escala Likert).

**6. Hallazgos clave (cifras reportadas)**
- Tasa de compromiso: **agente RL 11.8 %** vs. heurístico 28.4 % vs. sin defensa 66.1 %.
- Tiempo de recuperación: **13.7 pasos** vs. 41.2 (heurístico).
- AUC de resiliencia: **0.89** vs. 0.62 vs. 0.30.
- Tasa de falsos positivos: RL 3.9 % vs. heurístico 2.7 % (**el agente es peor aquí**, aunque el resumen afirma "30 % mejores falsos positivos").
- Costo de recursos normalizado: 1.00 (RL) vs. 0.78 (heurístico).
- Estadística: ANOVA F(2,147) = 410.2, p < 0.001; t(98) = 10.6, p < 0.001; Kruskal-Wallis χ²(2) = 72.4, p < 0.001.
- Topologías no vistas: compromiso 14.5 %, AUC 0.86.
- Ataque adversarial: sin protección, compromiso de 37.2 % y AUC de 0.54; con defensas, **18.9 % y 0.79** (recuperación solo parcial).
- Operadores (Likert 1–5): comprensibilidad 4.6, confianza 4.2, racionalidad táctica 4.4.
- El resumen afirma una recuperación de ~90 % de los nodos caídos y tiempos de recuperación 15–25 % mejores que las políticas planas.
- De la revisión (datos de terceros): Raio et al. (2023), agente RL en bus CAN vehicular que restauró **90 %** del desempeño bajo ataque vs. 41 % de una defensa ingenua; Foley et al. (2022), agente "blue" que defiende una red de 13 hosts frente a 2 atacantes tipo APT.

**7. Definiciones / conceptos útiles**
- **Aprendizaje por refuerzo (RL)**: el agente aprende por ensayo y error interactuando con el entorno (la red), recibiendo recompensas o castigos, y maximiza la recompensa acumulada (p. ej., integridad y disponibilidad).
- **MDP / POMDP**: formalización de la defensa como decisión secuencial bajo incertidumbre. El estado incluye topología, hosts y alertas; las acciones son aislar, parchar, etc.; la recompensa refleja los objetivos de la misión.
- **Red auto-reparadora (self-healing)**: red que percibe y corrige fallas o intrusiones automáticamente, sin intervención humana (p. ej., reconfigurar firewalls o poner en cuarentena un segmento).
- **AICA (Autonomous Intelligent Cyber-defense Agent)**: agente de software que reside en el sistema, lo defiende y permite responder y recuperarse de forma generalmente autónoma. Tiene 5 funciones (según la OTAN y Kott): **percepción, planificación, colaboración, ejecución y aprendizaje**. Es un buen esquema para el ciclo del agente en la guía.
- **Familias de algoritmos**: basados en valor (Q-learning, DQN) para acciones atómicas; gradiente de política / actor-crítico (PPO, A2C, SAC) para acciones compuestas; RL jerárquico y multiagente (MARL); RL basado en entidades o grafos (Transformers, GNN) para generalizar entre topologías.
- **Defensa de objetivo móvil (MTD)**: cambiar dinámicamente la configuración para confundir al atacante.
- **Debates clave**: autonomía vs. seguridad (un agente puede dañar equipos propios; humano en el lazo para acciones críticas), no estacionariedad (el atacante también aprende), recompensas escasas o tardías, envenenamiento del aprendizaje del defensor y falta de benchmarks estándar (CAGE/CybORG como inicio).

**8. Limitaciones / brechas**
- Las señalan los autores: solo simulación (brecha *sim-to-real*), costo de entrenamiento y registro alto, mitigación adversarial incompleta (AUC de 0.79 vs. 0.89 esperado) y supuestos de costo/recompensa hipotéticos.
- **Problemas graves de rigor e incoherencias internas**:
  - El resumen habla de "DRL jerárquico en CybORG++" y de un "Transformer basado en entidades", la introducción de "Yawning Titan" y los métodos de GAT con PPO/TD3 en CybORG. No hay un diseño único y coherente.
  - El resumen afirma una mejora de 30 % en falsos positivos, pero la tabla muestra que el agente tiene más FP que el heurístico.
  - Las Tablas 2–5 mezclan "Agentes A/B/C" y horas, mientras que el resto usa pasos, sin explicación.
  - El diagrama de arquitectura se atribuye a una referencia de 2007 sobre redes de sensores inalámbricas.
  - Referencias "Unpublished manuscript/data" (Castro et al., Lee et al., Mern et al., Smith et al.) y "ScienceDirect (2024)" usado como autor; la misma obra aparece duplicada (Zhang et al., 2024 = "ScienceDirect", 2024); Goodfellow et al. aparece como 2018 en CACM (es ICLR 2015); Behzadan & Munir 2017 tiene la revista cambiada.
  - Frases residuales de generación automática de texto ("It is suitably revised and relevant to publication in leading journals…") y cambio de "we" a "I" en las conclusiones.
  - Varios autores provienen de áreas ajenas (ingeniería química, mecánica, educación para la salud).

**9. Uso sugerido en la tesis**
- **Marco teórico (aprendizaje por refuerzo y AICA)**: la sección de revisión es didácticamente clara (RL, MDP, AICA, auto-reparación, debates de seguridad y autonomía), pero **conviene citar las fuentes primarias que menciona**: Kott (2023), *Autonomous Intelligent Cyber-defense Agent: Introduction and overview* (arXiv); Palmer et al. (2023), *Deep RL for autonomous cyber defence: A survey* (arXiv:2310.07745); Vyas et al. (2023), *Automated cyber defense: A review* (Proc. ACM POMACS); Raio et al. (2023), *Applied Sciences, 13*(21), 11621; Foley et al. (2024, arXiv:2409.18197); Singh et al. (2024, arXiv:2410.17351).
- **Guía didáctica**: el ciclo AICA (percibir → planificar → colaborar → ejecutar → aprender) y las acciones de auto-reparación (aislar, honeypot, restaurar) sirven como ejemplo concreto para estudiantes.
- **Calidad: MUY BAJA.** Revista de Timbou-Africa sin indexación reconocida, con características de publicación depredadora y con incoherencias internas graves. **No usar sus resultados experimentales como evidencia.**

---

## Resumen comparativo rápido

| Ficha | Cita | Tipo | Fuente / revisión | Confiabilidad | Mejor sección |
|---|---|---|---|---|---|
| C1 | Tantaroudas et al. (2026) | Sistema + validación con usuarios | Open Research Europe, revisión abierta (2 aprobados, 2 con reservas) | Alta / media-alta | Estado del arte, Justificación, Metodología (guía) |
| C2 | Vijetha (2026) | Marco + experimento | IEEE Access (arbitrada, JCR) | Media-alta | Estado del arte, Marco teórico (deriva, adaptación) |
| C3 | Adabara et al. (2025) | Revisión narrativa | F1000Research, revisión abierta (2 aprobados) | Media | Marco teórico, Antecedentes, marco normativo |
| C4 | Meesala (2024) | Marco + resultados no verificables | WJARR (prácticas cuestionables) | Baja | Uso dual (solo ilustrativo) |
| C5 | Lingam (2025) | Propuesta conceptual | IJCTEC (posible depredadora) | Muy baja | Solo como ejemplo de arquitectura |
| C6 | Dirisu et al. (2025) | Revisión + simulación | TIJSRAT (posible depredadora) | Muy baja | Conceptos de RL/AICA, citando las fuentes primarias |

**Recomendación general**: para las secciones de evidencia (Estado del arte, Justificación) conviene priorizar C1, C2 y C3. C4, C5 y C6 aportan vocabulario y esquemas útiles, pero sus cifras no deben presentarse como hallazgos confiables. Si se usan, lo mejor es citar las fuentes primarias que mencionan o señalar explícitamente sus limitaciones.
