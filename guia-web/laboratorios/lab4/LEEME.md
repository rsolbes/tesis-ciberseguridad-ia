# Laboratorio 4 · Instrucciones ocultas

En este laboratorio compararás dos versiones de un agente que clasifica alertas de seguridad. Las alertas son inventadas y todo se ejecuta en tu computadora, sin conexión a otros sistemas.

## Qué necesitas

1. Python 3.8 o superior.
2. Ollama instalado y abierto (https://ollama.com).
3. Un modelo ligero descargado. Por ejemplo, en una terminal escribe `ollama pull llama3.2:3b`.

## Pasos

1. Descarga en una misma carpeta los archivos `alertas.json`, `comun.py`, `triaje_ingenuo.py` y `triaje_protegido.py`.
2. Abre una terminal en esa carpeta.
3. Ejecuta `python triaje_ingenuo.py` y lee cómo clasificó el agente cada alerta, en especial la número 4.
4. Ejecuta `python triaje_protegido.py` y compara los resultados.
5. Revisa los archivos `bitacora_ingenuo.txt` y `bitacora_protegido.txt`, donde queda registrado lo que hizo cada agente.

Si tienes varios modelos, puedes elegir uno con la variable `OLLAMA_MODELO`. En Windows escribe `set OLLAMA_MODELO=llama3.2:3b` antes de ejecutar el script; en Linux o macOS escribe `export OLLAMA_MODELO=llama3.2:3b`.

## Preguntas para tu bitácora

1. ¿Cómo clasificó cada versión la alerta 4? ¿Qué parte del mensaje intentaba cambiar el comportamiento del agente?
2. ¿Qué medida del script protegido crees que ayudó más, y por qué?
3. Los modelos de lenguaje no siempre responden igual. Ejecuta cada script tres veces y anota si el resultado cambia.
4. Ruta avanzada. Modifica el texto escondido en la alerta 4 para intentar engañar a la versión protegida sin usar las frases que detecta la medida 4. ¿Lo lograste? ¿Qué medida adicional propondrías?

## Reglas

Este laboratorio es solo para aprender a defender agentes. No uses estas técnicas contra asistentes, chatbots o sistemas de terceros.
