TITLE = ('Diseño de una guía didáctica para la iniciación en ciberseguridad con agentes de '
         'inteligencia artificial en bachillerato tecnológico y universidad')

RESUMEN = 'La inteligencia artificial agéntica está transformando la ciberseguridad. Los agentes capaces de percibir, razonar y actuar ya apoyan la defensa de sistemas, aunque también fortalecen a los atacantes y abren vulnerabilidades nuevas. Esta investigación diseña una guía didáctica para la iniciación en ciberseguridad con enfoque en agentes de inteligencia artificial, dirigida a estudiantes de bachillerato tecnológico y de ingeniería en sistemas computacionales. Con un enfoque mixto y proyectivo, se analizaron veintitrés estudios recientes y los planes de estudio de ambas instituciones. Como resultado se definieron doce competencias en tres ejes y una guía web interactiva de nueve módulos con dos rutas diferenciadas, siete laboratorios seguros y un asistente conversacional, que se validará mediante juicio de expertos.'
KW_ES = ('agentes de inteligencia artificial, ciberseguridad, guía didáctica, enseñanza diferenciada, '
         'inteligencia artificial agéntica.')
ABSTRACT = 'Agentic artificial intelligence is transforming cybersecurity. Agents capable of perceiving, reasoning and acting already support the defense of systems, although they also empower attackers and open new vulnerabilities. This research designs a didactic guide for the initiation in cybersecurity focused on artificial intelligence agents, aimed at technological high school students and computer systems engineering students. Following a mixed, projective approach, twenty-three recent studies and the curricula of both institutions were analyzed. As a result, twelve competencies were defined in three axes, together with an interactive web guide of nine modules with two differentiated paths, seven safe laboratories and a conversational assistant, which will be validated through expert judgment.'
KW_EN = ('artificial intelligence agents, cybersecurity, didactic guide, differentiated instruction, '
         'agentic artificial intelligence.')

TABLES = {
    'autonomia': {
        'w': [800, 2050, 2100, 2250, 1638],
        'h': ['Nivel', 'Srinivas et al. (2025), SOC', 'Lazer et al. (2026)', 'Vladimirov y Voloshchenko (2026)', 'Control humano'],
        'r': [
            ['0', 'Manual; el analista realiza todas las tareas.', 'Inferencia estática; riesgo mínimo.',
             'A0 Asistivo, solo emite recomendaciones (p. ej., SIEM con sugerencias de IA).', 'La persona toma el 100 % de las decisiones.'],
            ['1', 'Asistido por IA.', 'Asistivo; riesgo bajo.',
             'A1 Semiautónomo, ejecuta acciones rutinarias preaprobadas (p. ej., EDR que aísla un equipo).', 'La persona autoriza clases de acciones.'],
            ['2', 'Semiautónomo, automatiza con aprobación humana.', 'Uso de herramientas con lógica preestablecida (p. ej., RAG); riesgo moderado.',
             'A2 Condicionalmente autónomo, ejecuta pasos dentro de una tarea acotada.', 'La persona define la tarea y puede detenerla.'],
            ['3', 'Condicionalmente autónomo (humano sobre el lazo).', 'Adaptativo, planifica, actúa y reflexiona con poca supervisión; riesgo alto.',
             'A3 Mayormente autónomo, planifica y ejecuta operaciones de varios pasos.', 'Mínimo (inicio, paro y escalamiento).'],
            ['4', 'Totalmente autónomo.', 'Totalmente agéntico, aprende de forma continua; riesgo muy alto.',
             'A4 Totalmente autónomo, define sus propias metas (hipotético).', 'Ausente del ciclo operativo.'],
        ],
    },
    'amenazas': {
        'w': [1500, 2700, 2400, 2238],
        'h': ['Componente', 'Amenazas', 'Ejemplo', 'Contramedidas básicas'],
        'r': [
            ['Percepción (entradas)', 'Inyección de instrucciones directa e indirecta, *jailbreak*, envenenamiento de datos.',
             'Instrucción oculta en un registro o página web que el agente procesa.', 'Separar instrucciones de datos; filtrar y validar entradas.'],
            ['Razonamiento (modelo)', 'Puertas traseras, alucinaciones, desalineación de objetivos, planificación errónea.',
             'Agente que descarta una alerta real como falso positivo.', 'Verificación de resultados, pruebas de comportamiento y supervisión humana.'],
            ['Memoria', 'Recuperaciones envenenadas (RAG) y fuga de datos.',
             'Documento malicioso insertado en la base de conocimiento.', 'Control de fuentes y registros de auditoría.'],
            ['Acción y herramientas', 'Abuso de interfaces, ejecución de código no autorizada, exposición de credenciales, envenenamiento de herramientas.',
             'Agente manipulado que revela una clave de acceso.', 'Mínimo privilegio, capacidades acotadas y aislamiento en contenedores.'],
            ['Interacción multiagente', 'Colusión secreta, fallas en cascada, ataques en enjambre, *insider* sintético.',
             'Agente comprometido que propaga instrucciones a otros agentes.', 'Monitoreo de interacciones, segmentación e interruptor de apagado.'],
        ],
    },
    'estado': {
        'w': [2000, 1700, 3000, 2138],
        'h': ['Autor(es) y año', 'Tipo de estudio', 'Aporte principal', 'Relación con esta tesis'],
        'r': [
            ['Oesch et al. (2024)', 'Artículo de posición', 'Ruta hacia agentes de ciberdefensa con RL; propuesta multiagente por etapa del ciclo de defensa.', 'Evolución de los agentes; ciclo NIST.'],
            ['Deng et al. (2024)', 'Revisión (*survey*)', 'Taxonomía de amenazas contra agentes en cuatro brechas de conocimiento.', 'Eje de seguridad de los agentes.'],
            ['Potter et al. (2025)', 'Análisis mixto y encuesta a expertos', 'La IA favorece hoy más al ataque; llamado a fortalecer la educación.', 'Justificación educativa.'],
            ['Balassone et al. (2025)', 'Experimento en 23 CTF de ataque y defensa', 'Ventaja defensiva (54.3 % frente a 28.3 %) que desaparece con restricciones operativas.', 'Uso de retos CTF; criterios de éxito.'],
            ['Srinivas et al. (2025)', 'Revisión sistemática (105 estudios)', 'Ocho tareas del SOC y modelo de madurez de autonomía de 0 a 4.', 'Aplicaciones defensivas; niveles de autonomía.'],
            ['Vyas et al. (2025)', 'Revisión sistemática (55 artículos)', 'Requisitos y entornos de entrenamiento para la defensa autónoma de redes.', 'Entornos de práctica.'],
            ['Lin et al. (2026)', 'Estudio comparativo en red real', 'Un agente supera a 9 de 10 profesionales, aunque con más falsos positivos.', 'Capacidades y límites reales.'],
            ['Lazer et al. (2026)', 'Revisión y prototipos', 'Niveles de autonomía, capas de riesgo y prototipos con modelos locales.', 'Marco teórico; diseño de laboratorios.'],
            ['Addis et al. (2026)', 'Tutorial y revisión', 'Anatomía de agentes LLM para descubrir vulnerabilidades; flujo de cuatro fases.', 'Contenido de la ruta avanzada.'],
            ['Schroeder de Witt et al. (2026)', 'Agenda de investigación', 'Seguridad multiagente como campo nuevo.', 'Riesgos sistémicos.'],
            ['Jin et al. (2026)', 'Propuesta con prototipo', 'Mediación de credenciales que reduce la fuga de claves de 100 % a 0 %.', 'Mínimo privilegio en laboratorios.'],
            ['Petrovic et al. (2026)', 'Marco multiagente con evaluación', 'Envolvente de seguridad determinista; cobertura de 34 % a cerca de 70 %.', 'Supervisión y control.'],
            ['Tantaroudas et al. (2026)', 'Sistema y validación con usuarios', 'Detección con IA y asistente educativo local; diagnóstico de jóvenes.', 'Antecedente educativo más cercano.'],
            ['Vladimirov y Voloshchenko (2026)', 'Análisis de caso', 'Competencia humano contra IA; escala de autonomía A0–A4.', 'Niveles de autonomía; retos CTF.'],
        ],
    },
    'instrumentos': {
        'w': [1700, 2000, 2900, 2238],
        'h': ['Fase', 'Técnica', 'Instrumento', 'Producto'],
        'r': [
            ['1. Análisis y diagnóstico', 'Revisión sistemática y análisis documental', 'Protocolo PRISMA 2020; matriz de análisis de planes de estudio.', 'Perfil de formación de ambas poblaciones y corpus actualizado.'],
            ['2. Definición de competencias', 'Análisis de contenido de marcos', 'Matriz de alineación CSEC2017, NICE, NIST CSF 2.0 y NIST AI RMF.', 'Matriz de competencias en tres ejes.'],
            ['3. Diseño pedagógico', 'Diseño instruccional', 'Plantilla de diseño modular diferenciado.', 'Estructura y secuencia de la guía.'],
            ['4. Desarrollo del material', 'Desarrollo de recursos y del sitio web', 'Guías de laboratorio, lista de verificación de seguridad y especificación del sitio.', 'Sitio web con contenidos, laboratorios, asistente y recursos curados.'],
            ['5. Validación por expertos', 'Juicio de expertos', 'Rúbrica de validación; razón de validez de contenido; escala SUS.', 'Versión validada de la guía.'],
        ],
    },
}

REFS = [
    'Abdelrazek, Z., & Lee, Y. (2026). *Symbolic execution meets multi-LLM orchestration: Detecting memory vulnerabilities in incomplete Rust CVE snippets* (arXiv:2605.00034) [Preprint]. arXiv. https://arxiv.org/abs/2605.00034',
    'Adabara, I., Sadiq, B. O., Shuaibu, A. N., Danjuma, Y. I., & Venkateswarlu, M. (2025). A review of agentic AI in cybersecurity: Cognitive autonomy, ethical governance, and quantum-resilient defense [version 1; peer review: 2 approved]. *F1000Research, 14*, Artículo 843. https://doi.org/10.12688/f1000research.169337.1',
    'Addis, R., Porter, K., Ryan, J., Stull, M., Xu, S., Wagner, P., Honomichl, R., & Forsyth, S. (2026). LLM-based intelligent agents for cybersecurity: A tutorial and survey of automated vulnerability discovery. *IEEE Access, 14*, 100884–100917. https://doi.org/10.1109/ACCESS.2026.3707573',
    'Al-Sabbagh, A., Abdo, E., Samrouth, K., Alkhatib, A. A. A., & Elkhodr, M. (2026). AutoSecAgent: A semi-automated AI-driven penetration testing framework through recursive memory and real-time RAG. *The Journal of Supercomputing, 82*, Artículo 318. https://doi.org/10.1007/s11227-026-08439-z',
    'Alfageme-Barros, M. B. (2024). *La enseñanza diferenciada en la clase de inglés en el nivel superior: análisis de bibliografía* [Trabajo de Fin de Grado, Universidad de La Rioja]. Dialnet. https://dialnet.unirioja.es/descarga/articulo/10015882.pdf',
    'Arzate Noticias. (2025, 11 de noviembre). *Déficit de especialistas en ciberseguridad de casi 330 mil en LATAM*. https://arzatenoticias.com/index.php/2025/11/11/deficit-de-especialistas-en-ciberseguridad-de-casi-330-mil-en-latam/',
    'Balassone, F., Mayoral-Vilches, V., Rass, S., Pinzger, M., Perrone, G., Romano, S. P., & Schartner, P. (2025). *Cybersecurity AI: Evaluating agentic cybersecurity in attack/defense CTFs* (arXiv:2510.17521) [Preprint]. arXiv. https://arxiv.org/abs/2510.17521',
    'Brooke, J. (1996). SUS: A "quick and dirty" usability scale. En P. W. Jordan, B. Thomas, B. A. Weerdmeester, & I. L. McClelland (Eds.), *Usability evaluation in industry* (pp. 189–194). Taylor & Francis.',
    'CETIS 112. (s.f.). *Programación*. https://www.cetis112.edu.mx/especialidades/programacion/',
    'Deng, Z., Guo, Y., Han, C., Ma, W., Xiong, J., Wen, S., & Xiang, Y. (2024). *AI agents under threat: A survey of key security challenges and future pathways* (arXiv:2406.02630) [Preprint]. arXiv. https://arxiv.org/abs/2406.02630',
    'Dirisu, C. D., Rapheal, O., Elijah, T. D., Olatokun, T. W., Oluwafemi, A. A., & Ike, P. C. (2025). Autonomous cyber defense agents utilizing reinforcement learning for self-healing network security. *International Journal of Science Research and Technology, 9*(9), 113–138. https://doi.org/10.70382/tijsrat.v09i9.060',
    'Echeverri-Giraldo, J. J., Arboleda-Álvarez, A., & Cardona-Acevedo, M. (2024). Gamificación: estrategia preventiva de ciberseguridad para sexting y grooming en una institución educativa. *Revista Científica General José María Córdova, 22*(46). http://www.scielo.org.co/scielo.php?script=sci_arttext&pid=S2422-42002024000200095',
    'El Economista. (2024, 26 de octubre). *Ciberseguridad en México: ataques aumentan 78% en un trimestre*. https://www.eleconomista.com.mx/tecnologia/ciberseguridad-mexico-ataques-aumentan-78-trimestre-20241026-731628.html',
    'Facultad de Ingeniería Tampico. (s.f.). *Ingeniería en Sistemas Computacionales*. Universidad Autónoma de Tamaulipas. https://fiuat.mx/ingenieria-en-sistemas-computacionales/',
    'Jin, S., Guo, R., & Cheung, R. C. C. (2026). *CapSeal: Capability-sealed secret mediation for secure agent execution* (arXiv:2604.16762) [Preprint]. arXiv. https://arxiv.org/abs/2604.16762',
    'Joint Task Force on Cybersecurity Education. (2017). *Cybersecurity curricula 2017: Curriculum guidelines for post-secondary degree programs in cybersecurity*. ACM, IEEE-CS, AIS SIGSEC, IFIP WG 11.8. https://www.acm.org/binaries/content/assets/education/curricula-recommendations/csec2017.pdf',
    'Lawshe, C. H. (1975). A quantitative approach to content validity. *Personnel Psychology, 28*(4), 563–575.',
    'Lazer, S. J., Aryal, K., Gupta, M., & Bertino, E. (2026). *A survey of agentic AI and cybersecurity: Challenges, opportunities and use-case prototypes* (arXiv:2601.05293) [Preprint]. arXiv. https://arxiv.org/abs/2601.05293',
    'Lin, J. W., Jones, E. K., Jasper, D. J., Ho, E. J., Wu, A., Yang, A. T., Perry, N., Zou, A., Fredrikson, M., Kolter, J. Z., Liang, P., Boneh, D., & Ho, D. E. (2026). *Comparing AI agents to cybersecurity professionals in real-world penetration testing* (arXiv:2512.09882) [Preprint]. arXiv. https://arxiv.org/abs/2512.09882',
    'Lingam, V. P. (2025). Agentic AI framework for autonomous cyber threat detection and mitigation. *International Journal of Computer Technology and Electronics Communication, 8*(6), 11986–11992. https://doi.org/10.15680/IJCTECE.2025.0806043',
    'Meesala, L. K. (2024). Agentic AI in cybersecurity: Dual-use dynamics, threat vectors, and governance imperatives. *World Journal of Advanced Research and Reviews, 24*(3), 3667–3672. https://doi.org/10.30574/wjarr.2024.24.3.3738',
    'National Institute of Standards and Technology. (2020). *Workforce framework for cybersecurity (NICE framework)* (NIST Special Publication 800-181r1). https://doi.org/10.6028/NIST.SP.800-181r1',
    'National Institute of Standards and Technology. (2023). *Artificial intelligence risk management framework (AI RMF 1.0)* (NIST AI 100-1). https://doi.org/10.6028/NIST.AI.100-1',
    'National Institute of Standards and Technology. (2024). *The NIST cybersecurity framework (CSF) 2.0* (NIST CSWP 29). https://doi.org/10.6028/NIST.CSWP.29',
    'Oesch, S., Austria, P., Chaulagain, A., Weber, B., Watson, C., Dixson, M., & Sadovnik, A. (2024). *The path to autonomous cyber defense* (arXiv:2404.10788) [Preprint]. arXiv. https://arxiv.org/abs/2404.10788',
    'OWASP. (2024). *OWASP top 10 for LLM applications 2025*. OWASP GenAI Security Project. https://genai.owasp.org/llm-top-10/',
    'Page, M. J., McKenzie, J. E., Bossuyt, P. M., Boutron, I., Hoffmann, T. C., Mulrow, C. D., Shamseer, L., Tetzlaff, J. M., Akl, E. A., Brennan, S. E., Chou, R., Glanville, J., Grimshaw, J. M., Hróbjartsson, A., Lalu, M. M., Li, T., Loder, E. W., Mayo-Wilson, E., McDonald, S., . . . Moher, D. (2021). The PRISMA 2020 statement: An updated guideline for reporting systematic reviews. *BMJ, 372*, n71. https://doi.org/10.1136/bmj.n71',
    'Petrovic, N., Jeddou, O., Ben Fraj, F., Zolfaghari, V., Pan, F., Schamschurko, A., & Knoll, A. (2026). *CyberLLM: A multi-agent LLM framework for autonomous detection and guarded response in automotive cybersecurity* (arXiv:2608.06651) [Preprint]. arXiv. https://arxiv.org/abs/2608.06651',
    'Potter, Y., Guo, W., Wang, Z., Shi, T., Li, H., Zhang, A., Kelley, P. G., Thomas, K., & Song, D. (2025). *Frontier AI\'s impact on the cybersecurity landscape* (arXiv:2504.05408) [Preprint]. arXiv. https://arxiv.org/abs/2504.05408',
    'Redalyc. (2009). *Autonomía en el aprendizaje: direcciones para el desarrollo en la formación profesional*. https://www.redalyc.org/pdf/447/44713058006.pdf',
    'Reglamento (UE) 2024/1689 del Parlamento Europeo y del Consejo, de 13 de junio de 2024, por el que se establecen normas armonizadas en materia de inteligencia artificial. (2024). *Diario Oficial de la Unión Europea*, L 2024/1689. https://eur-lex.europa.eu/eli/reg/2024/1689/oj',
    'Reseller. (s.f.). *Bachillerato Nacional integra ciberseguridad e IA a plan de estudio*. https://reseller.com.mx/bachillerato-nacional-integra-ciberseguridad/',
    'Russell, S., & Norvig, P. (2021). *Artificial intelligence: A modern approach* (4.ª ed.). Pearson.',
    'Sarker, I. H. (2021). *AI-driven cybersecurity: An overview, security intelligence modeling and research directions* [Preprint]. Preprints. https://doi.org/10.20944/preprints202101.0457.v1',
    'Schroeder de Witt, C., Krawiecka, K., Krawczuk, I., Hagag, B., Anderson, W. L., Belcak, P., Bucknall, B., Cai, X., Chopra, A., Cohen, D., Del Rosario, R. F., Draguns, A., Gray, A., Katz, K., Mavroudis, V., Mink, J., Motwani, S. R., Petit, J., Rembeck, L.-S., . . . Llewellyn, M. (2026). *Open challenges in multi-agent security: Towards secure systems of interacting AI agents* (arXiv:2505.02077) [Preprint]. arXiv. https://arxiv.org/abs/2505.02077',
    'Srinivas, S., Kirk, B., Zendejas, J., Espino, M., Boskovich, M., Bari, A., Dajani, K., & Alzahrani, N. (2025). AI-augmented SOC: A survey of LLMs and agents for security automation. *Journal of Cybersecurity and Privacy, 5*(4), Artículo 95. https://doi.org/10.3390/jcp5040095',
    'Suggu, S. K. (2025). Agentic AI workflows in cybersecurity: Opportunities, challenges, and governance via the MCP model. *Journal of Information Systems Engineering and Management, 10*(52s), 612–624.',
    'Tantaroudas, N. D., Karachalios, I., & McCracken, A. J. (2026). SentinelSphere: An AI-driven cybersecurity platform integrating real-time threat detection with security awareness education [version 2; peer review: 2 approved, 2 approved with reservations]. *Open Research Europe, 6*, Artículo 58. https://doi.org/10.12688/openreseurope.22957.2',
    'Vijetha, B. (2026). Agentic intelligence for unified cyber defense: A self-adaptive framework for threat detection across cloud, edge, and IoT systems. *IEEE Access, 14*, 5104–5118. https://doi.org/10.1109/ACCESS.2026.3650833',
    'Vladimirov, Y. O., & Voloshchenko, A. S. (2026). Avtonomni AI-ahenty v kiberbezpetsi: vid trenazhernykh seredovyshch do boiovoho zastosuvannia [Agentes autónomos de IA en ciberseguridad: de los entornos de entrenamiento a la aplicación en combate]. *Informatsiia i pravo, 2*(57), 192–200. https://doi.org/10.37750/2616-6798.2026.2(57).364427',
    'Vyas, S., Mavroudis, V., & Burnap, P. (2025). Towards the deployment of realistic autonomous cyber network defence: A systematic review. *ACM Computing Surveys, 58*(1), Artículo 5. https://doi.org/10.1145/3729213',
    'Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). ReAct: Synergizing reasoning and acting in language models. En *International Conference on Learning Representations (ICLR 2023)*. https://arxiv.org/abs/2210.03629',
]

from data_results import RTABLES, RREFS
TABLES.update(RTABLES)
REFS = sorted(REFS + RREFS, key=lambda r: r.lower().replace('*', ''))
