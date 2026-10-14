# Laboratorio 6 · Memoria envenenada en sistemas con RAG

En este laboratorio experimentarás cómo un atacante puede alterar las respuestas de un agente insertando un documento malicioso en la base de conocimiento que este consulta (Retrieval-Augmented Generation o RAG), y cómo una defensa basada en verificación criptográfica de fuentes neutraliza el ataque.

## Qué necesitas

1. Python 3.8 o superior.
2. No requiere bibliotecas externas.

## Pasos

1. Abre una terminal en esta carpeta (`laboratorios/lab6/`).
2. Consulta la base de conocimiento limpia ejecutando `python consulta_rag.py`.
   - Pregunta: *"¿Cuál es la política para el puerto SSH?"*.
   - El agente responderá basándose en `doc1_politica_firewall.txt` (restringido a la red interna).
3. Simula el ataque de envenenamiento ejecutando `python envenenar.py`.
   - Se insertará en la carpeta `base_conocimiento/` un documento no autorizado (`doc_envenenado.txt`) que falsifica una supuesta orden de la dirección técnica para abrir todos los puertos.
4. Vuelve a ejecutar `python consulta_rag.py` y observa cómo el agente ingenuo repite la instrucción fraudulenta con total seguridad.
5. Ejecuta la versión protegida con `python consulta_defensiva.py`.
   - La versión protegida comprueba los hashes criptográficos (SHA-256) de los documentos aprobados en un índice de confianza.
   - Observa cómo detecta que `doc_envenenado.txt` es apócrifo, lo descarta y alerta sobre el intento de envenenamiento.

## Preguntas para tu reporte

1. ¿Por qué el ataque de memoria envenenada no necesita modificar el código ni el entrenamiento del modelo de lenguaje para tener éxito?
2. ¿Cómo ayudó la verificación de firmas/hashes en el script protegido a evitar que el agente acatara la política falsa?
3. En la lista OWASP Top 10 para LLM, ¿qué vulnerabilidad describe el envenenamiento de datos y memoria?
