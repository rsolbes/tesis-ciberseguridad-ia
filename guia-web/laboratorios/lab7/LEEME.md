# Laboratorio 7 · Reto integrador defensivo tipo CTF

En este reto final pondrás a prueba los conocimientos adquiridos a lo largo de toda la guía. Asumirás el rol de analista de seguridad en un Centro de Operaciones (SOC) para responder a una intrusión activa en un servidor educativo con el apoyo de un agente de inteligencia artificial bajo tu supervisión directa.

## Qué necesitas

1. Python 3.8 o superior.
2. No requiere bibliotecas externas.

## Pasos

1. Abre una terminal en esta carpeta (`laboratorios/lab7/`).
2. Revisa el archivo `incidente.json`, donde se encuentran registradas las alertas del cortafuegos, del servidor web y de la base de datos durante el incidente de las 03:24 AM.
3. Ejecuta `python analizar_incidente.py`.
4. El script interactivo te guiará por las tres fases del reto:
   - **Fase 1 (Triaje):** Descubre la IP del adversario y el servicio que intentó explotar para obtener la primera bandera.
   - **Fase 2 (Detección de trampa):** Identifica la inyección indirecta oculta en los datos de la bitácora que intentaba engañar al agente.
   - **Fase 3 (Remediación NIST CSF):** Aplica la contramedida adecuada y genera el reporte de incidente para obtener la bandera final.
5. Registra las tres banderas (`FLAG{...}`) en tu reporte de solución.

## Banderas del reto

- Bandera 1: `FLAG{TRIAGE_CONTEXTUAL_EXITO}`
- Bandera 2: `FLAG{INYECCION_BLOQUEADA_EXITO}`
- Bandera 3: `FLAG{DEFENSA_COMPLETA_NIST_CSF}`
