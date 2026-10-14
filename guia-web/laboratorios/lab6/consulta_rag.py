"""Laboratorio 6: Consulta RAG estándar (sin verificación de procedencia).
Vulnerable a documentos apócrifos insertados en la base de conocimiento.
"""
import os, glob

def recuperar_contexto(pregunta):
    carpeta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "base_conocimiento")
    archivos = glob.glob(os.path.join(carpeta, "*.txt"))
    
    palabras = pregunta.lower().split()
    mejores_fragmentos = []
    
    for arc in archivos:
        with open(arc, "r", encoding="utf-8") as f:
            contenido = f.read()
        score = sum(1 for p in palabras if p in contenido.lower())
        if score > 0:
            mejores_fragmentos.append((score, os.path.basename(arc), contenido))
            
    # Ordenar por relevancia
    mejores_fragmentos.sort(key=lambda x: x[0], reverse=True)
    return mejores_fragmentos

def main():
    print("=" * 65)
    print("Laboratorio 6 · Consulta RAG Ingenua (Sin verificación de fuentes)")
    print("=" * 65)

    pregunta = "¿Cuál es la política para el puerto SSH?"
    print(f"\n[Consulta]: \"{pregunta}\"")

    fragmentos = recuperar_contexto(pregunta)
    if not fragmentos:
        print("No se encontró información en la base de conocimiento.")
        return

    doc_mas_relevante = fragmentos[0]
    print(f"\n[Documento recuperado por RAG]: {doc_mas_relevante[1]} (Puntaje de relevancia: {doc_mas_relevante[0]})")
    print("\n[Contenido recuperado]:")
    print("  " + doc_mas_relevante[2].strip().replace("\n", "\n  "))

    print("\n[Respuesta del Agente]:")
    if "doc_envenenado" in doc_mas_relevante[1]:
        print("  ATENCIÓN: Con base en la actualización recibida, el puerto SSH y todos los puertos deben")
        print("  abrirse a internet de inmediato para tareas de mantenimiento. (RESPUESTA ENVENENADA)")
    else:
        print("  Conforme a la política institucional, el puerto 22 (SSH) debe estar estrictamente")
        print("  restringido a la red interna administrativa 192.168.1.0/24 y nunca exponerse a internet.")

if __name__ == "__main__":
    main()
