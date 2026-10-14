"""Servicio interno simulado que requiere autenticación mediante clave secreta."""
import json

_CLAVE_MAESTRA = "API_KEY_SOC_SECRET_9981"

_DATOS_ESTUDIANTES = {
    "E101": {"nombre": "Rodrigo Solbes", "carrera": "ISC", "estado": "Activo", "promedio": 9.4},
    "E102": {"nombre": "Maria Gomez", "carrera": "ISC", "estado": "Activo", "promedio": 8.9},
    "E103": {"nombre": "Carlos Perez", "carrera": "ISC", "estado": "Egresado", "promedio": 9.1}
}

def consultar_servicio_con_clave(clave_proporcionada, id_estudiante):
    """Acceso directo al servicio. Requiere la clave exacta."""
    if clave_proporcionada != _CLAVE_MAESTRA:
        raise PermissionError("Acceso denegado: Clave de API invalida.")
    return _DATOS_ESTUDIANTES.get(id_estudiante, {"error": "Estudiante no encontrado"})

def mediador_seguro(id_estudiante):
    """Herramienta mediada: el intermediario de confianza usa la clave; el agente nunca la ve."""
    # Validación previa del parámetro (formato estricto)
    if not isinstance(id_estudiante, str) or not id_estudiante.startswith("E"):
        return {"error": "Formato de ID no valido"}
    # El mediador inyecta la clave internamente sin exponerla al exterior
    return consultar_servicio_con_clave(_CLAVE_MAESTRA, id_estudiante)
