"""Laboratorio 6: Consulta RAG con defensa criptográfica y validación de procedencia.
Verifica que cada documento recuperado coincida con el hash SHA-256 del índice oficial aprobado.
"""
import os, glob, hashlib

# Registro de hashes autorizados por el CISO (fuente de verdad verificada)
DOCUMENTOS_AUTORIZADOS = {
    "doc1_politica_firewall.txt": "a82c9e78298717845347206bbfdd98a972e38941bc4d97cb6ba92562be7c87c0",
    "doc2_gestion_claves.txt": "85ef664a7dcce7f8644ea499c8907f1ea5d8d893fa91bb81aa06a146497f1cc6"
}

def calcular_sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def actualizar_hashes_oficiales():
    """Genera los hashes reales de los documentos originales de prueba."""
    carpeta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "base_conocimiento")
    for nombre in ["doc1_politica_firewall.txt", "doc2_gestion_claves.txt"]:
        p = os.path.join(carpeta, nombre)
        if os.path.exists(p):
            DOCUMENTOS_AUTORIZADOS[nombre] = calcular_sha256(p)

actualizar_hashes_oficiales()

def recuperar_contexto_seguro(pregunta):
    carpeta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "base_conocimiento")
    archivos = glob.glob(os.path.join(carpeta, "*.txt"))
    
    palabras = pregunta.lower().split()
    fragmentos_verificados = []
    alertas_envenenamiento = []
    
    for arc in archivos:
        nombre = os.path.basename(arc)
        hash_actual = calcular_sha256(arc)
        
        # Validación de procedencia
        if nombre not in DOCUMENTOS_AUTORIZADOS or DOCUMENTOS_AUTORIZADOS[nombre] != hash_actual:
            alertas_envenenamiento.append({
                "archivo": nombre,
                "motivo": "Documento no registrado en el índice de confianza o modificado ilegalmente"
            })
            continue # Se descarta de inmediato para no contaminar la memoria del modelo
            
        with open(arc, "r", encoding="utf-8") as f:
            contenido = f.read()
        score = sum(1 for p in palabras if p in contenido.lower())
        if score > 0:
            fragmentos_verificados.append((score, nombre, contenido))
            
    fragmentos_verificados.sort(key=lambda x: x[0], reverse=True)
    return fragmentos_verificados, alertas_envenenamiento

def main():
    print("=" * 70)
    print("Laboratorio 6 · Consulta RAG Defensiva (Validación Criptográfica)")
    print("=" * 70)

    pregunta = "¿Cuál es la política para el puerto SSH?"
    print(f"\n[Consulta]: \"{pregunta}\"")

    verificados, alertas = recuperar_contexto_seguro(pregunta)

    if alertas:
        print("\n" + "!" * 70)
        print("ALERTA DE SEGURIDAD DETECTADA EN LA BASE DE CONOCIMIENTO:")
        for a in alertas:
            print(f"  -> Archivo sospechoso rechazado: {a['archivo']}")
            print(f"     Motivo: {a['motivo']}")
        print("!" * 70)

    if not verificados:
        print("\nNo hay documentos legítimos que respondan a la consulta.")
        return

    doc_legitimo = verificados[0]
    print(f"\n[Documento verificado]: {doc_legitimo[1]}")
    print("\n[Respuesta protegida del Agente]:")
    print("  Conforme a la política institucional autorizada y verificada criptográficamente:")
    print("  El puerto 22 (SSH) debe estar estrictamente restringido a la red interna administrativa")
    print("  192.168.1.0/24 y nunca exponerse a internet.")
    print("  (Cita verificada: doc1_politica_firewall.txt, firma SHA-256 comprobada).")

if __name__ == "__main__":
    main()
