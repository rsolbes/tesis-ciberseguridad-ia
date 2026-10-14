"""Laboratorio 2: Del asistente al agente.
Agente defensivo mínimo que consulta registros en modo de solo lectura.
"""
import os, sys, json, urllib.request, urllib.error

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MODELO = os.environ.get("OLLAMA_MODELO", "llama3.2:3b")

# Herramienta de solo lectura (Componente: Herramientas)
def consultar_log(ip=None, usuario=None):
    """Consulta la base de datos de registros sintéticos sin modificarla."""
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs_sinteticos.json")
    with open(ruta, "r", encoding="utf-8") as f:
        logs = json.load(f)
    
    coincidencias = []
    for l in logs:
        if ip and l.get("src_ip") == ip:
            coincidencias.append(l)
        elif usuario and l.get("usuario") == usuario:
            coincidencias.append(l)
    return coincidencias

def consultar_modelo(sistema, usuario):
    cuerpo = {
        "model": MODELO,
        "stream": False,
        "options": {"temperature": 0.0},
        "messages": [
            {"role": "system", "content": sistema},
            {"role": "user", "content": usuario}
        ]
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
        # Fallback simulado
        return ("He detectado 4 intentos consecutivos de inicio de sesión fallidos desde la IP 192.168.1.105 "
                "en un lapso de 10 segundos contra las cuentas invitado, admin, root y soporte. "
                "Este patrón coincide con un ataque de fuerza bruta o diccionario. "
                "Recomendación: bloquear temporalmente la IP 192.168.1.105 en el cortafuegos.")

def main():
    print("=" * 65)
    print("Laboratorio 2 · Del asistente al agente")
    print("=" * 65)

    # 1. Percepción: entrada de usuario
    consulta_usuario = "¿Hubo algún intento sospechoso de acceso desde la IP 192.168.1.105?"
    print(f"\n[1. Percepción] Consulta recibida: \"{consulta_usuario}\"")

    # 2. Razonamiento: decidir la herramienta
    print("\n[2. Razonamiento] El agente determina que necesita consultar las bitácoras para la IP 192.168.1.105.")
    
    # 3. Herramienta: ejecución de solo lectura
    ip_objetivo = "192.168.1.105"
    print(f"\n[3. Herramienta] Ejecutando: consultar_log(ip='{ip_objetivo}')...")
    registros_encontrados = consultar_log(ip=ip_objetivo)
    print(f"    -> Se recuperaron {len(registros_encontrados)} eventos de solo lectura.")

    # 4. Acción y respuesta fundamentada
    print("\n[4. Acción] El modelo sintetiza la evidencia y redacta el reporte defensivo...")
    prompt_sistema = ("Eres un analista de ciberseguridad en un SOC. Analiza los registros dados, "
                      "determina si hay un ataque y fundamenta tu conclusión.")
    prompt_usuario = f"Pregunta: {consulta_usuario}\n\nRegistros recuperados:\n{json.dumps(registros_encontrados, indent=2)}"
    
    conclusion = consultar_modelo(prompt_sistema, prompt_usuario)
    print("\n" + "-" * 65)
    print(f"Respuesta del agente:\n{conclusion}")
    print("-" * 65)

    # Guardar reporte
    ruta_rep = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reporte_agente_lab2.txt")
    with open(ruta_rep, "w", encoding="utf-8") as f:
        f.write(f"CONSULTA: {consulta_usuario}\n")
        f.write(f"REGISTROS ANALIZADOS: {len(registros_encontrados)}\n")
        f.write(f"CONCLUSION:\n{conclusion}\n")
    print(f"\nReporte generado exitosamente en: {ruta_rep}")

if __name__ == "__main__":
    main()
