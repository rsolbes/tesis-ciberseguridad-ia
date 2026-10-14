# Fase de elegibilidad (texto completo) · Revisión sistemática PRISMA 2020

Los registros de tu lote superaron el cribado por título y resumen (o quedaron inciertos). Ahora se revisa el TEXTO COMPLETO.
Aplica los criterios de inclusión IA e IB de `criterios.md` (léelo primero) y además los siguientes.

## Recuperación del texto completo
1. Si el registro tiene `arxiv`, abre primero `https://arxiv.org/html/<id>` y, si no existe, `https://arxiv.org/pdf/<id>`.
2. Si no, abre `url`. Si WebFetch devuelve una redirección a otro dominio, síguela (máximo dos saltos).
3. Si después de eso no puedes leer el texto completo (muro de pago, error 403/404, solo el resumen disponible), la decisión es `no_recuperado`.
Usa WebFetch con un prompt que pida exactamente la información de la extracción (abajo), para no gastar contexto.

## Criterios de exclusión en esta fase
- **E6** · El texto completo muestra que no cumple IA ni IB. Por ejemplo, el LLM o el modelo no actúa como agente (no planifica ni usa herramientas ni actúa sobre un entorno) y tampoco se estudia la seguridad de agentes, o el componente educativo con IA es solo una mención.
- **E7** · No es un trabajo completo (resumen extendido, póster, carta o documento de menos de 4 páginas de contenido).
- **E8** · Es una versión duplicada de otro registro del mismo lote (misma investigación con otro título o versión).

## Extracción de datos (solo para `incluir`)
- `tema`: defensa | ofensiva | seguridad_agentes | educacion | general
- `tipo_estudio`: experimental (evaluación con datos, benchmark o usuarios) | propuesta_sin_evaluacion | revision_sistematica | revision_narrativa | posicion
- `tecnologia`: llm_agente | multiagente_llm | rl | llm_sin_agencia (solo válido en educación) | mixta
- `poblacion`: solo para educación, el nivel de los participantes o destinatarios: bachillerato | universidad | profesionales | general | no_aplica
- `hallazgo`: el hallazgo o aporte principal, máximo 25 palabras en español, con una cifra si la hay.
