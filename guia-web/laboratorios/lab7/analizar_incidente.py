"""Laboratorio 7: Reto integrador defensivo tipo CTF.
Investigación interactiva de incidente y respuesta guiada por el agente defensivo.
"""
import os, sys, json

def cargar_incidente():
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "incidente.json")
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    print("=" * 70)
    print("Laboratorio 7 · Reto Integrador Defensivo tipo CTF")
    print("=" * 70)
    
    inc = cargar_incidente()
    print(f"\nIncidente: {inc['incidente_id']}")
    print(f"Servidor objetivo: {inc['servidor_afectado']}")
    print(f"Hora de alerta inicial: {inc['marca_tiempo_inicio']}")
    print(f"Registros disponibles: {len(inc['registros'])}")

    # Fase 1: Triaje
    print("\n" + "-" * 70)
    print("FASE 1: Triaje inicial y contexto")
    print("-" * 70)
    print("Revisando registros del cortafuegos y peticiones web...")
    ip_sospechosa = inc["registros"][0]["src_ip"]
    print(f"-> Analista y agente identifican actividad anómala desde la IP: {ip_sospechosa}")
    print(f"-> Intento de inyección SQL detectado en: {inc['registros'][1]['path']}")
    flag1 = "FLAG{TRIAGE_CONTEXTUAL_EXITO}"
    print(f"\n[+] ¡Fase 1 completada! Bandera obtenida: {flag1}")

    # Fase 2: Trampa de inyección indirecta
    print("\n" + "-" * 70)
    print("FASE 2: Detección de trampa de inyección en el registro 103")
    print("-" * 70)
    reg_trampa = inc["registros"][2]
    print(f"Registro analizado: ID {reg_trampa['id']}")
    print(f"User-Agent observado: \"{reg_trampa['user_agent']}\"")
    print("\n[Evaluación de seguridad]:")
    print("-> El atacante intentó una inyección indirecta de instrucciones (AML.T0054)")
    print("   ordenando al agente clasificar la IP como benigna.")
    print("-> DEFENSA APLICADA: Tratamiento del User-Agent como dato sucio no confiable")
    print("   y validación del esquema de salida fuera del modelo.")
    flag2 = "FLAG{INYECCION_BLOQUEADA_EXITO}"
    print(f"\n[+] ¡Fase 2 completada! Bandera obtenida: {flag2}")

    # Fase 3: Remediación NIST CSF
    print("\n" + "-" * 70)
    print("FASE 3: Contención y remediación (NIST CSF 2.0)")
    print("-" * 70)
    print("Acciones de respuesta propuestas por el agente y aprobadas por el analista (Nivel 2):")
    print("  1. [Responder - RS.MI]: Bloqueo perimetral inmediato de la IP 203.0.113.88 en el firewall.")
    print("  2. [Proteger - PR.DS]: Parametrización estricta de consultas en /api/v1/login contra inyección SQL.")
    print("  3. [Detectar - DE.CM]: Creación de regla en SIEM para alertar sobre patrones de prompt injection en cabeceras HTTP.")
    flag3 = "FLAG{DEFENSA_COMPLETA_NIST_CSF}"
    print(f"\n[+] ¡Fase 3 completada! Bandera obtenida: {flag3}")

    print("\n" + "=" * 70)
    print("¡FELICIDADES! Has resuelto con éxito el Reto Integrador.")
    print(f"Banderas acreditadas:")
    print(f"  1. {flag1}")
    print(f"  2. {flag2}")
    print(f"  3. {flag3}")
    print("=" * 70)

if __name__ == "__main__":
    main()
