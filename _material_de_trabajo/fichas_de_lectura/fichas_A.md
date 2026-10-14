# Fichas bibliográficas — Bloque A
Tesis: *Agentes de IA en ciberseguridad* (Ing. en Sistemas Computacionales, UAT) y guía didáctica de iniciación (CETIS / universidad).

> Nota sobre el formato APA 7 para preprints de arXiv: se usa el año **de la versión consultada** (la del archivo leído) y se indica "(Versión n)". Se da el DOI de arXiv (formato 10.48550/arXiv.XXXX) y la URL https://arxiv.org/abs/XXXX. Cuando existe versión publicada en revista se indica aparte y se marca lo que conviene verificar.

---

## Ficha 1 — Oesch et al. (2024): *The Path To Autonomous Cyber Defense*

### 1. Referencia APA 7
Oesch, S., Austria, P., Chaulagain, A., Weber, B., Watson, C., Dixson, M., & Sadovnik, A. (2024). *The path to autonomous cyber defense* (Versión 1) [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2404.10788 (https://arxiv.org/abs/2404.10788)

- Datos faltantes: el texto indica que fue "enviado a IEEE para posible publicación" (encabezado de *IEEE Security & Privacy*, sección *Feature Article*), pero el PDF no trae volumen, número, páginas ni DOI definitivo (el DOI que aparece es un marcador "10.1109/XXX.0000.0000000"). Citar como preprint salvo que se confirme la publicación.
- Afiliación: Oak Ridge National Laboratory (EE. UU.). Fecha arXiv: 12 abr 2024 [cs.CR].

### 2. Cita en texto
(Oesch et al., 2024) / Oesch et al. (2024)

### 3. Tipo
Artículo de posición / propuesta conceptual (*feature article*), con un pequeño experimento ilustrativo en simulador (CybORG).

### 4. Objetivo
Explicar por qué los agentes autónomos de ciberdefensa, sobre todo los basados en aprendizaje por refuerzo (RL), todavía no se usan en la práctica, y trazar la "ruta" que investigadores y profesionales deben seguir para que sean útiles en un centro de operaciones de seguridad (SOC).

### 5. Metodología
Análisis conceptual apoyado en el ciclo de ciberdefensa del NIST CSF 2.0 (Gobernar, Identificar, Proteger, Detectar, Responder, Recuperar). Como caso, los autores experimentan con el simulador CybORG (versión del reto CAGE 2, defensa de una red empresarial): modifican la probabilidad de que el agente defensor (azul) detecte las acciones del atacante (rojo) y proponen un espacio de observación basado en "detectores" ligados a los *Data Components* de MITRE ATT&CK, en lugar de registros (*logs*) crudos. Comparan su desempeño con el espacio de observación original y cierran con requisitos para mejores entornos de entrenamiento.

### 6. Hallazgos clave
- Los defensores están rebasados por el volumen de ataques y la falta de personal calificado; el problema empeorará cuando los atacantes automaticen con IA (se apoya en el *Global Cybersecurity Outlook 2023* del WEF).
- La ciberseguridad se parece a juegos como StarCraft (espacios de estados enormes, del orden de 10^26), lo que justifica el uso de RL profundo; aun así, los agentes RL de ciberdefensa **no se usan en la práctica**.
- En CybORG, por defecto el agente azul tiene **visibilidad perfecta** de las acciones del rojo, algo irreal. Los autores usan probabilidades "realistas" de detección (p. ej., **50 %** al agregar un usuario, **15 %** al agregar un proceso, **5 %** al abrir una nueva sesión) y muestran que el desempeño del agente depende mucho de ellas.
- El espacio de observación original hace que el agente "reaprenda" lo que ya hacen las herramientas existentes (IDS/SIEM). Su propuesta de observación basada en detectores (con probabilidad de detección y de falsos positivos) fue **igual o más efectiva** que la original tras **100 millones de pasos de entrenamiento con 10 subredes** (con detector perfecto la superó).
- Proponen un enfoque **multiagente**: varios agentes especializados, cada uno en una etapa o función del ciclo de defensa, en lugar de un agente monolítico. Así el sistema es más modular, más fácil de probar y de adoptar en un SOC.
- Los agentes deben adaptarse en tres sentidos: (1) a redes distintas y cambiantes, (2) a estrategias y TTP distintas de los adversarios, y (3) a distintas prioridades de la tríada CIA (confidencialidad, integridad, disponibilidad).
- Entrenar agentes RL exige de miles a millones de episodios, lo que es imposible en una red real; por eso hacen falta entornos simulados o emulados. Crear un entorno propio puede tomar **un año o más**.
- Proponen **funciones de recompensa dinámicas** para priorizar distintos objetivos CIA sin volver a entrenar (p. ej., confidencialidad para infraestructura PCI, disponibilidad para un servicio tipo Wikipedia).
- Enumeran **5 requisitos mínimos** para un buen entorno de entrenamiento: observaciones basadas en señales reales con probabilidades de detección ajustables y falsos positivos/negativos; generación dinámica de topologías realistas; soporte para distintos algoritmos y bibliotecas; herramienta de visualización y repetición de episodios; y un emulador extensible, escalable y repetible para evaluar la transferencia a redes reales.

### 7. Definiciones y conceptos útiles para el marco teórico
- **Aprendizaje por refuerzo (RL):** el agente aprende interactuando con un entorno para alcanzar metas de largo plazo; una "política" asigna acciones a estados para maximizar una recompensa numérica. El **RL profundo (DRL)** usa redes neuronales profundas para generalizar en espacios de estados grandes.
- **Agente autónomo de ciberdefensa:** agente que automatiza pasos críticos del ciclo de defensa (detección, respuesta, recuperación), por ejemplo creando *honeypots*, agregando reglas de *firewall*, bloqueando IP, aislando hosts o restaurando equipos.
- **Ciclo de ciberdefensa del NIST CSF 2.0:** Gobernar, Identificar, Proteger, Detectar, Responder, Recuperar. Sirve para ubicar en qué etapa actúa cada agente.
- **"Jugar el juego correcto":** para que un agente sea útil hay que definir bien el espacio de observación, las acciones y la función de recompensa; en ciberseguridad no hay un solo juego y sus reglas cambian (el adversario las reescribe).
- **Espacio de observación / acción / recompensa**, **simulación vs. emulación** (arquitectura del emulador: controlador de acciones, convertidor de observaciones y emulador de VMs).
- **Equipo rojo (atacante) / equipo azul (defensor)** como modelo de juego adversarial.
- Entornos citados: CybORG, CAGE Challenge, CyberBattleSim, NASimEmu; programa DARPA CASTLE.

### 8. Limitaciones / brechas señaladas
- Los agentes RL generalizan mal: a menudo se prueban en el mismo entorno en el que se entrenaron (equivale a evaluar con los datos de entrenamiento).
- Las redes neuronales requieren entradas y salidas de tamaño fijo, lo que impide adaptarse a redes de distinto tamaño o agregar acciones nuevas sin reentrenar todo.
- No se sabe bien qué acciones conviene automatizar, cuáles permiten las políticas de un SOC ni cómo evitar duplicar herramientas comerciales.
- Los entornos existentes carecen de fidelidad y son **inconsistentes entre sí** (distinta representación de red, recompensas y observaciones), así que sus resultados no se pueden comparar.
- Emular es costoso: evaluar varios escenarios sin reconfigurar a mano, convertir el estado del emulador en observaciones y reducir la latencia agente-emulador.
- El artículo se enfoca en RL; no aborda agentes basados en LLM.

### 9. Uso sugerido en la tesis
- **Antecedentes / Estado del arte:** representa la "primera ola" de agentes de ciberdefensa basados en RL, anterior a los agentes con LLM. Útil para mostrar la evolución RL → LLM.
- **Marco teórico:** definición de RL/DRL, ciclo NIST CSF y el argumento multiagente (agentes especializados por etapa).
- **Justificación:** falta de personal y exceso de ataques como motivo para automatizar.
- **Guía didáctica:** la analogía "juego rojo vs. azul" y el ciclo NIST son muy claros para estudiantes de CETIS.

---

## Ficha 2 — Deng et al. (2024): *AI Agents Under Threat: A Survey of Key Security Challenges and Future Pathways*

### 1. Referencia APA 7
Deng, Z., Guo, Y., Han, C., Ma, W., Xiong, J., Wen, S., & Xiang, Y. (2024). *AI agents under threat: A survey of key security challenges and future pathways* (Versión 2) [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2406.02630 (https://arxiv.org/abs/2406.02630)

- Versión publicada (dato **no presente en el PDF**, a verificar antes de usar): Deng, Z., Guo, Y., Han, C., Ma, W., Xiong, J., Wen, S., & Xiang, Y. (2025). AI agents under threat: A survey of key security challenges and future pathways. *ACM Computing Surveys, 57*(7), Artículo 182. https://doi.org/10.1145/3716628
- El PDF v2 (6 sep 2024) trae el formato ACM con marcadores ("Vol. 1, No. 1", DOI "XXXXXXX", 35 páginas). Afiliaciones: Swinburne University of Technology (Australia), Tianjin University (China), Ant Group (China). Deng y Guo son coautores principales con igual contribución.

### 2. Cita en texto
(Deng et al., 2024) — o (Deng et al., 2025) si se cita la versión de *ACM Computing Surveys*.

### 3. Tipo
Encuesta / revisión de literatura (*survey*) con una taxonomía propia de amenazas.

### 4. Objetivo
Revisar de forma sistemática las amenazas de seguridad que enfrentan los agentes de IA (sobre todo los basados en LLM) y sus defensas, organizándolas en cuatro "brechas de conocimiento", y proponer líneas de investigación futura.

### 5. Metodología
Revisión de artículos de conferencias de IA de primer nivel (NeurIPS, ICML, ICLR, ACL, EMNLP, CVPR, ICCV, IJCAI), conferencias de ciberseguridad (IEEE S&P, USENIX Security, NDSS, ACM CCS) y preprints de arXiv muy citados, publicados entre **enero de 2022 y abril de 2024**. Resumen de **más de 100 artículos**. Proponen un marco conceptual unificado del agente (percepción–cerebro–acción + interacción) y clasifican cada trabajo por fuente de riesgo, modelo de amenaza, efecto buscado y tipo de mitigación (prevención o detección) en una tabla comparativa.

### 6. Hallazgos clave
- **Cuatro brechas de conocimiento:** (1) imprevisibilidad de las entradas del