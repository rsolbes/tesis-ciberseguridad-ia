# Laboratorio 1 · Mi primer modelo local

En este laboratorio vas a interactuar directamente con un modelo de lenguaje que se ejecuta de forma local y sin conexión en tu computadora. Aprenderás a variar el parámetro de temperatura, observarás cómo cambia la coherencia del texto y registrarás tu primera alucinación en una bitácora.

## Qué necesitas

1. Python 3.8 o superior.
2. Ollama instalado y abierto (https://ollama.com).
3. Un modelo ligero descargado. Por ejemplo: `ollama pull llama3.2:3b` o `ollama pull qwen2.5:3b`.

*(Nota: si no tienes Ollama abierto en este momento, el script cuenta con un modo simulado para que puedas observar el comportamiento).*

## Pasos

1. Abre una terminal en esta carpeta (`laboratorios/lab1/`).
2. Ejecuta `python probar_modelo.py`.
3. El script realizará tres pruebas:
   - Comparación de respuestas a temperatura 0.0 frente a temperatura 1.0.
   - Demostración de ventana de contexto con un resumen técnico.
   - Trampa de alucinación para observar cómo inventa respuestas sobre temas inexistentes.
4. Abre el archivo generado `bitacora_lab1.json` y revisa las respuestas registradas.

## Preguntas para tu reporte

1. ¿Qué diferencia notaste entre la respuesta generada con temperatura 0.0 y la de temperatura 1.0?
2. En la prueba de alucinación, ¿cómo reaccionó el modelo ante el concepto ficticio? ¿Reconoció que no lo conocía o inventó una explicación convincente?
3. Explica por qué es peligroso confiar a ciegas en comandos de consola generados por un modelo sin verificar su sintaxis.
