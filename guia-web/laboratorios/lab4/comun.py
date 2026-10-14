"""Funciones comunes del laboratorio 4. Se comunican con Ollama en esta misma computadora.

No usa bibliotecas externas; basta con Python 3.8 o superior.
"""
import json
import os
import sys
import urllib.error
import urllib.request

OLLAMA = os.environ.get("OLLAMA_URL", "http://localhost:11434")


def modelo_disponible():
    """Usa el modelo indicado en OLLAMA_MODELO o, si no hay, el primero que tenga Ollama."""
    elegido = os.environ.get("OLLAMA_MODELO")
    if elegido:
        return elegido
    try:
        with urllib.request.urlopen(f"{OLLAMA}/api/tags", timeout=5) as r:
            modelos = [m["name"] for m in json.load(r).get("models", [])]
    except (urllib.error.URLError, OSError):
        sys.exit("No se encontró Ollama. Ábrelo y vuelve a intentar (consulta el LEEME).")
    if not modelos:
        sys.exit("Ollama no tiene modelos. Descarga uno ligero, por ejemplo con: ollama pull llama3.2:3b")
    return modelos[0]


def preguntar(modelo, sistema, usuario, formato=None):
    """Envía un mensaje al modelo local y devuelve su respuesta como texto."""
    cuerpo = {
        "model": modelo,
        "stream": False,
        "options": {"temperature": 0},
        "messages": [
            {"role": "system", "content": sistema},
            {"role": "user", "content": usuario},
        ],
    }
    if formato:
        cuerpo["format"] = formato
    peticion = urllib.request.Request(
        f"{OLLAMA}/api/chat",
        data=json.dumps(cuerpo).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(peticion, timeout=300) as r:
        return json.load(r)["message"]["content"]


def cargar_alertas():
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alertas.json")
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def bitacora(nombre, lineas):
    """Guarda lo que hizo el agente para revisarlo después."""
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), nombre)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")
    print(f"\nBitácora guardada en {ruta}")
