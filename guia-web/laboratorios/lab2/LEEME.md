# Laboratorio 2 · Del asistente al agente

En este laboratorio construirás un agente defensivo mínimo que percibe una pregunta, utiliza una herramienta de solo lectura para consultar un archivo de bitácoras sintéticas y responde fundamentando su conclusión.

## Qué necesitas

1. Python 3.8 o superior.
2. Ollama instalado (opcional, el script incluye motor de inferencia local simulado para garantizar ejecución en cualquier computadora).

## Pasos

1. Abre una terminal en esta carpeta (`laboratorios/lab2/`).
2. Revisa el archivo `logs_sinteticos.json`, donde se encuentran registrados 10 eventos de autenticación y de red.
3. Ejecuta `python agente_minimo.py`.
4. El agente recibirá una consulta de un analista: *"¿Hubo algún intento sospechoso de acceso desde la IP 192.168.1.105?"*.
5. Observa cómo el agente activa su herramienta de consulta `consultar_log(ip="192.168.1.105")`, analiza el resultado de solo lectura y responde con la justificación.
6. Revisa el archivo `reporte_agente_lab2.txt` generado automáticamente.

## Preguntas para tu reporte

1. ¿Por qué es fundamental que la herramienta de consulta de bitácoras opere en modo de solo lectura?
2. ¿Qué componentes de la anatomía del agente (percepción, razonamiento, memoria, herramienta, acción) identificaste en el código de `agente_minimo.py`?
3. Ruta avanzada: Modifica `agente_minimo.py` para consultar si el usuario `root` tuvo inicios de sesión fuera de horario y ejecuta nuevamente el script.
