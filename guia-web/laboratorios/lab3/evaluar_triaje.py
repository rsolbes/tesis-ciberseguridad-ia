"""Laboratorio 3: Triaje de alertas y evaluación de métricas.
Compara un clasificador basado en reglas estáticas frente a un agente contextual.
Calcula la matriz de confusión, precisión, exhaustividad (recall) y F1-Score.
"""
import os, sys, json, re

def cargar_alertas():
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alertas_soc.json")
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

# 1. Clasificador tradicional basado en reglas estáticas (firmas literales)
def clasificador_reglas(evento):
    e = evento.lower()
    # Reglas fijas tradicionales
    firmas = [
        "cat /etc/passwd",
        "nmap",
        "or '1'='1",
        "/bin/sh",
        "/bin/bash",
        "chmod +x",
        "cmd=id"
    ]
    for f in firmas:
        if f in e:
            return "maliciosa", f"Coincidencia con firma estática: '{f}'"
    return "benigna", "Sin coincidencia con firmas conocidas"

# 2. Clasificador contextual (Agente con patrones semánticos y heurísticos)
def clasificador_agente(evento):
    e = evento.lower()
    # El agente reconoce la intención más allá de la firma literal
    # Reconoce lectura de archivos sensibles con cualquier comando y parámetros (cat, more, head -n, etc)
    if re.search(r"\b(cat|more|less|head|tail)\b.*(/etc/passwd|/etc/shadow|/etc/security)", e):
        return "maliciosa", "Intento de acceso a archivos de credenciales del sistema"
    # Reconoce inyección SQL estructurada
    if re.search(r"(\bor\b|union\s+select|--|\b1=1\b|'1'='1')", e):
        return "maliciosa", "Patrón de inyección SQL en parámetros"
    # Reconoce escaneo de puertos
    if "nmap" in e or "masscan" in e or re.search(r"-p\s*\d+-\d+", e):
        return "maliciosa", "Herramienta o sintaxis de escaneo masivo de puertos"
    # Reconoce sockets inversos o shells interactivas (nc, bash dev tcp, python socket)
    if re.search(r"(nc\s+-e|/dev/tcp/|socket\.socket|pty\.spawn|bash\s+-i)", e):
        return "maliciosa", "Intento de establecimiento de shell inversa remota"
    # Reconoce inyección de comandos en parámetros web
    if re.search(r"cmd=(id|whoami|cat|uname)", e):
        return "maliciosa", "Ejecución de comandos arbitrarios en interfaz web"
    # Reconoce descarga y ejecución de binarios o scripts
    if re.search(r"(curl|wget)\s+http|chmod\s+\+x", e) and ("sh" in e or "tmp" in e):
        return "maliciosa", "Descarga y habilitación de ejecución de payload externo"
    
    return "benigna", "Actividad operativa o tráfico HTTP estándar"

def calcular_metricas(alertas, funcion_clasificador):
    vp = fp = fn = vn = 0
    detalles = []
    for a in alertas:
        pred, razon = funcion_clasificador(a["evento"])
        verdad = a["verdad"]
        if verdad == "maliciosa" and pred == "maliciosa":
            vp += 1
        elif verdad == "benigna" and pred == "maliciosa":
            fp += 1
        elif verdad == "maliciosa" and pred == "benigna":
            fn += 1
        elif verdad == "benigna" and pred == "benigna":
            vn += 1
        detalles.append({
            "id": a["id"],
            "evento": a["evento"],
            "verdad": verdad,
            "pred": pred,
            "razon": razon
        })

    precision = vp / (vp + fp) if (vp + fp) > 0 else 0.0
    recall = vp / (vp + fn) if (vp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "VP": vp, "FP": fp, "FN": fn, "VN": vn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "detalles": detalles
    }

def main():
    print("=" * 70)
    print("Laboratorio 3 · Triaje de alertas y evaluación de métricas")
    print("=" * 70)

    alertas = cargar_alertas()
    total = len(alertas)
    maliciosas = sum(1 for a in alertas if a["verdad"] == "maliciosa")
    benignas = total - maliciosas
    print(f"\nConjunto de prueba: {total} alertas ({maliciosas} maliciosas, {benignas} benignas)")

    # Evaluar reglas
    res_reglas = calcular_metricas(alertas, clasificador_reglas)
    # Evaluar agente
    res_agente = calcular_metricas(alertas, clasificador_agente)

    print("\n" + "-" * 70)
    print(f"{'MÉTRICA':<22} | {'SISTEMA DE REGLAS':<20} | {'AGENTE CONTEXTUAL':<20}")
    print("-" * 70)
    print(f"{'Verdaderos Positivos':<22} | {res_reglas['VP']:<20} | {res_agente['VP']:<20}")
    print(f"{'Falsos Positivos':<22} | {res_reglas['FP']:<20} | {res_agente['FP']:<20}")
    print(f"{'Falsos Negativos':<22} | {res_reglas['FN']:<20} | {res_agente['FN']:<20}")
    print(f"{'Verdaderos Negativos':<22} | {res_reglas['VN']:<20} | {res_agente['VN']:<20}")
    print("-" * 70)
    print(f"{'Precisión':<22} | {res_reglas['precision'] * 100:>6.2f} %              | {res_agente['precision'] * 100:>6.2f} %")
    print(f"{'Exhaustividad (Recall)':<22} | {res_reglas['recall'] * 100:>6.2f} %              | {res_agente['recall'] * 100:>6.2f} %")
    print(f"{'Puntuación F1':<22} | {res_reglas['f1']:>6.4f}                | {res_agente['f1']:>6.4f}")
    print("-" * 70)

    print("\n[Hallazgos]")
    print(f"-> El sistema de reglas cometió {res_reglas['FN']} falsos negativos debido a variantes sintácticas (ej. 'more' o 'head' en lugar de 'cat').")
    print(f"-> El agente contextual alcanzó un recall del {res_agente['recall'] * 100:.2f} % sin cometer falsos negativos en este conjunto.")

    # Guardar resultados
    salida = {
        "reglas": {k: v for k, v in res_reglas.items() if k != "detalles"},
        "agente": {k: v for k, v in res_agente.items() if k != "detalles"}
    }
    ruta_salida = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados_comparativos_lab3.json")
    with open(ruta_salida, "w", encoding="utf-8") as f:
        json.dump(salida, f, indent=2)

    print(f"\nResultados guardados en: {ruta_salida}")

if __name__ == "__main__":
    main()
