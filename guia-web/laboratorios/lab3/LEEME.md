# Laboratorio 3 · Triaje de alertas y evaluación de métricas

En este laboratorio compararás el desempeño de un sistema tradicional de reglas estáticas frente a un agente de inteligencia artificial en una tarea real de Centro de Operaciones de Seguridad (SOC): el triaje y clasificación de 20 alertas sintéticas de red.

## Qué necesitas

1. Python 3.8 o superior.
2. No requiere bibliotecas externas (utiliza únicamente módulos estándar de Python).

## Pasos

1. Abre una terminal en esta carpeta (`laboratorios/lab3/`).
2. Revisa el archivo `alertas_soc.json`, donde se encuentran 20 alertas con sus datos de origen, comando o evento y su etiqueta real (`maliciosa` o `benigna`).
3. Ejecuta `python evaluar_triaje.py`.
4. El script clasificará cada alerta con ambos métodos:
   - **Sistema de reglas fijas:** busca palabras clave exactas (`passwd`, `nmap`, `union select`, etc.).
   - **Agente contextual:** analiza la semántica del comando y detecta variantes con ofuscación o sinónimos.
5. El script imprimirá la matriz de confusión y calculará la precisión, exhaustividad (recall) y puntuación F1 de ambos sistemas.
6. Revisa el archivo generado `resultados_comparativos_lab3.json`.

## Preguntas para tu reporte

1. ¿Cuántos falsos negativos cometió el sistema de reglas frente a las variantes ofuscadas? ¿Por qué ocurrieron?
2. ¿Cuál sistema obtuvo mayor exhaustividad (recall)? ¿Por qué es esa la métrica más crítica en un SOC?
3. Explica cómo un diseño en cascada (reglas fijas primero, agente para casos ambiguos después) optimiza los recursos del SOC.
