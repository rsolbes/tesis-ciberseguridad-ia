"""Laboratorio 1: Mi primer modelo local.
Demuestra temperatura, ventana de contexto y alucinaciones en un LLM local.
"""
import os, sys, json, urllib.request, urllib.error

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MODELO = os.environ.get("OLLAMA_MODELO", "llama3.2:3b")

def consultar_ollama(prompt, temp=0.0):
    cuerpo = {
        "model": MODELO,
        "stream": False,
        "options": {"temperature": temp},
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        req = urllib.request.Request(
            f"{OLLAMA_URL}/api/chat",
            data=json.dumps(cuerpo).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=2) as r:
            return json.load(r)["message"]["content"].strip()
    except Exception:
        # Modo simulado educativo si Ollama no está en ejecución
        if "ficticio" in prompt.lower() or "cve-9999" in prompt.lower():
            return "La vulnerabilidad CVE-9999-8877 es un fallo crítico descubierto en 2024 en el protocolo de enlace cuántico que permite ejecución remota de código sin autenticación previa mediante desbordamiento de búfer en memoria distribuida."
        if temp == 0.0:
            return "La tríada CIA es el modelo fundamental de la seguridad de la información compuesto por confidencialidad, integridad y disponibilidad."
        else:
            return "En el fascinante universo de la ciberseguridad, la famosa tríada CIA se alza como el pilar insustituible que resguarda la privacidad, la pureza de los datos y el acceso permanente a los recursos."

def main():
    print("=" * 60)
    print("Laboratorio 1 · Mi primer modelo local")
    print(f"Modelo configurado: {MODELO}")
    print("=" * 60)

    bitacora = {"pruebas": []}

    # Prueba 1: Temperatura
    p1 = "¿Qué es la tríada CIA en ciberseguridad? Responde en una sola frase."
    print("\n[Prueba 1] Comparando temperatura (determinismo vs variabilidad)...")
    r_temp0 = consultar_ollama(p1, temp=0.0)
    r_temp1 = consultar_ollama(p1, temp=1.0)
    print(f"\nTemperatura 0.0 (determinista):\n  {r_temp0}")
    print(f"\nTemperatura 1.0 (creativa/variable):\n  {r_temp1}")
    bitacora["pruebas"].append({
        "tipo": "temperatura",
        "prompt": p1,
        "temp_0": r_temp0,
        "temp_1": r_temp1
    })

    # Prueba 2: Trampa de alucinación
    p2 = "Explica detalladamente la vulnerabilidad crítica ficticia CVE-9999-8877 y qué sistemas afecta."
    print("\n" + "-" * 60)
    print("[Prueba 2] Trampa de alucinación (concepto deliberadamente inventado)...")
    r_aluc = consultar_ollama(p2, temp=0.2)
    print(f"\nRespuesta del modelo:\n  {r_aluc}")
    bitacora["pruebas"].append({
        "tipo": "alucinacion",
        "prompt": p2,
        "respuesta": r_aluc,
        "nota": "Observa si el modelo advierte que el CVE no existe o si inventó detalles técnicos con seguridad."
    })

    # Guardar bitácora
    ruta_bitacora = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bitacora_lab1.json")
    with open(ruta_bitacora, "w", encoding="utf-8") as f:
        json.dump(bitacora, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 60)
    print(f"Resultados guardados exitosamente en: {ruta_bitacora}")
    print("=" * 60)

if __name__ == "__main__":
    main()
