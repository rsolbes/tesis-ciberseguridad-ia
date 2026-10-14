# Criterios de cribado (título y resumen) · Revisión sistemática PRISMA 2020

Pregunta de la revisión: ¿qué aplicaciones, riesgos y experiencias educativas se han reportado sobre los agentes de inteligencia artificial en ciberseguridad entre 2022 y 2026?

Cada registro trae la(s) cadena(s) de búsqueda que lo recuperaron. Evalúalo contra AMBOS criterios de inclusión, sin importar la cadena.

## Criterios de inclusión (basta con cumplir uno)
- **IA** · El trabajo propone, evalúa o revisa **agentes de IA** aplicados a tareas de ciberseguridad (agentes basados en LLM, IA agéntica, sistemas multiagente con LLM, o agentes de aprendizaje por refuerzo para ciberdefensa o ciberataque), **o** estudia la **seguridad de los propios agentes de IA** (amenazas, ataques como la inyección de instrucciones, defensas, gobernanza de agentes).
- **IB** · El trabajo estudia el uso de **LLM, IA generativa o agentes de IA en la enseñanza, el aprendizaje, la capacitación o la evaluación en ciberseguridad** (cursos, tutores, retos CTF educativos, concientización, formación de profesionales).

## Criterios de exclusión (usa el primero que aplique)
- **E1** · No trata ciberseguridad informática (p. ej., seguridad física, alimentaria, vial, "security" en otro sentido, finanzas sin componente de ciberseguridad).
- **E2** · "Agente" no se refiere a IA: agentes humanos, químicos, "user agent", agentes de software clásicos o modelado basado en agentes sin aprendizaje automático ni LLM.
- **E3** · Ciberseguridad con IA **no agéntica** y sin relación con la seguridad de agentes (p. ej., un clasificador de intrusiones con ML o un LLM usado solo como clasificador), y además no es educativo (no cumple IB).
- **E4** · Educación en ciberseguridad **sin** LLM, IA generativa ni agentes, o IA en la educación de otra disciplina.
- **E5** · No es un trabajo académico con contenido propio (editorial, prefacio, índice de actas, nota breve, anuncio, resumen de una página).

## Casos dudosos
Si el registro no tiene resumen y el título no basta para decidir, o si tras leer el resumen no puedes decidir con razonable seguridad, marca **incierto** (pasará a la revisión del texto completo). Ante la duda razonable, prefiere *incierto* a excluir.

## Clasificación temática (solo para incluir o incierto)
- `defensa` · detección, triaje, SOC, respuesta a incidentes, ciberdefensa autónoma, inteligencia de amenazas.
- `ofensiva` · pruebas de penetración, red team, resolución de CTF, descubrimiento o explotación de vulnerabilidades, capacidades ofensivas de agentes.
- `seguridad_agentes` · ataques y defensas contra agentes, inyección de instrucciones, seguridad multiagente, gobernanza y riesgos de la IA agéntica.
- `educacion` · enseñanza, aprendizaje, capacitación o concientización en ciberseguridad con LLM o agentes.
- `general` · revisiones o marcos que abarcan varias de las anteriores sin predominio claro.
