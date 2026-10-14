"""Incorpora la fundamentación y arquitectura de gamificación en 'Avance de tesis.docx':
1. Amplía la fundamentación teórica de gamificación en el capítulo V (Estrategias didácticas).
2. Documenta el subsistema de gamificación (XP, rangos, micro-retos, confeti y audio) en el capítulo VII (7.4.3).
3. Añade las referencias de Deterding et al. (2011), Hamari et al. (2014) y Kapp (2012).
4. Reempaqueta y actualiza campos por COM.
"""
import os, sys, shutil, zipfile, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wlib
from wlib import p, reference

DOCX_ORIG = r"C:\Users\SISTEMAS10\Desktop\Estudio\TESIS NUEVA\Avance de tesis.docx"
DOCX_TEMP = os.path.join(HERE, "temp_docx_gam")
DOCX_OUT = r"C:\Users\SISTEMAS10\Desktop\Estudio\TESIS NUEVA\Avance de tesis.docx"

shutil.rmtree(DOCX_TEMP, ignore_errors=True)

with zipfile.ZipFile(DOCX_ORIG) as z:
    z.extractall(DOCX_TEMP)
    orden_entradas = z.namelist()

doc_xml_path = os.path.join(DOCX_TEMP, "word", "document.xml")
with open(doc_xml_path, "r", encoding="utf-8") as f:
    xml_content = f.read()

# 1. Ampliar el párrafo 347 sobre gamificación en Capítulo V (sin dos puntos internos)
texto_gam_fundamentos = (
    "Tres estrategias resultan especialmente pertinentes. La primera es la gamificación, entendida como el "
    "uso de mecánicas y dinámicas de juego en contextos formativos para incrementar el compromiso y la motivación "
    "intrínseca (Deterding et al., 2011; Kapp, 2012). La evidencia empírica confirma que la acumulación de experiencia, "
    "las insignias de maestría y la retroalimentación inmediata reducen la ansiedad técnica y mejoran la retención "
    "de conceptos complejos en estudiantes de computación (Hamari et al., 2014). Esta aproximación ha demostrado ser "
    "una estrategia preventiva efectiva para enseñar a adolescentes sobre riesgos digitales (Echeverri-Giraldo et al., 2024) "
    "y, en el campo de la ciberseguridad, adopta la forma natural de los retos tipo CTF, un formato que la propia "
    "investigación utiliza para medir el desempeño de los agentes (Balassone et al., 2025; Vladimirov y Voloshchenko, 2026). "
    "La segunda estrategia son los laboratorios con modelos locales, que permiten experimentar con agentes sin costos de "
    "nube y sin exponer datos sensibles, ya que la evidencia muestra que es posible ejecutar agentes de triaje y de "
    "detección de anomalías con modelos ligeros, datos sintéticos y permisos de solo lectura (Lazer et al., 2026). "
    "La tercera es el uso de la IA como tutor pedagógico. La plataforma SentinelSphere integró un asistente conversacional "
    "basado en un modelo cuantizado con RAG para la formación en concientización y obtuvo una satisfacción de 4.3 sobre 5, "
    "con 77.8 % de los participantes dispuestos a utilizarla como docentes (Tantaroudas et al., 2026). De este último "
    "estudio también se desprende una lección metodológica, pues para demostrar el aprendizaje no basta con medir la "
    "satisfacción inmediata, sino que se requieren mediciones pareadas y un seguimiento riguroso."
)

xml_gam_fundamentos = p(texto_gam_fundamentos)

patron_p347 = re.compile(
    r'<w:p\b[^>]*>(?:(?!</w:p>).)*?Tres estrategias resultan especialmente pertinentes.*?</w:p>',
    re.DOTALL
)
assert patron_p347.search(xml_content), "No se encontró el párrafo de estrategias didácticas"
xml_content = patron_p347.sub(xml_gam_fundamentos, xml_content, count=1)
print("1. Fundamentación de gamificación ampliada en el Capítulo V.")

# 2. Documentar la arquitectura de gamificación en la sección 7.4.3
texto_gam_arquitectura = (
    "Para favorecer la inmersión y responder a las características motivacionales de los estudiantes de bachillerato "
    "y primeros semestres universitarios, el sitio web incorpora una capa de gamificación nativa. Esta capa integra "
    "un sistema de puntos de experiencia acumulativos, una escala de progresión de cinco rangos (desde Recluta Digital "
    "hasta Comandante de Ciberdefensa), indicadores visuales de nivel en la cabecera y refuerzos sensoriales basados en "
    "audio sintetizado con la API Web Audio y confeti festivo en lienzo nativo. Asimismo, la plataforma cuenta con "
    "micro-retos interactivos ejecutables directamente en el navegador, como el simulador de filtrado de paquetes de cortafuegos "
    "en el módulo M2 y el entorno controlado de inyección de instrucciones en el módulo M7, los cuales permiten interactuar "
    "con las defensas sin requerir la instalación de herramientas en el equipo del alumno."
)
xml_gam_arquitectura = p(texto_gam_arquitectura)

# Insertar después del párrafo de los contenidos de cada módulo (p988)
patron_p988 = re.compile(
    r'(<w:p\b[^>]*>(?:(?!</w:p>).)*?Cada módulo presenta el núcleo común y la profundización.*?</w:p>)',
    re.DOTALL
)
assert patron_p988.search(xml_content), "No se encontró el párrafo 988 de la sección 7.4.3"
xml_content = patron_p988.sub(r'\1' + xml_gam_arquitectura, xml_content, count=1)
print("2. Arquitectura de gamificación incorporada en la sección 7.4.3.")

# Actualizar párrafo de figuras para reflejar los 10 módulos y la gamificación
patron_figuras = re.compile(
    r'(<w:p\b[^>]*>(?:(?!</w:p>).)*?)Las Figuras 5 a 11 corresponden al prototipo funcional del sitio.*?(</w:p>)',
    re.DOTALL
)
texto_figuras_actualizado = (
    "Las Figuras 5 a 11 corresponden al prototipo funcional del sitio web, en el que se encuentran integrados "
    "la portada, el mapa curricular, los módulos con sus autoevaluaciones e insignias, el subsistema de gamificación "
    "y el asistente conversacional en sus diversas modalidades."
)
xml_content = patron_figuras.sub(p(texto_figuras_actualizado), xml_content, count=1)
print("3. Párrafo descriptivo de figuras actualizado.")

# 3. Añadir referencias de gamificación en APA 7
ref_deterding = reference(
    "Deterding, S., Dixon, D., Khaled, R., & Nacke, L. (2011). From game design elements to gamefulness: "
    "Defining \"gamification\". *Proceedings of the 15th International Academic MindTrek Conference*, 9–15. "
    "https://doi.org/10.1145/2181037.2181040"
)
ref_hamari = reference(
    "Hamari, J., Koivisto, J., & Sarsa, H. (2014). Does gamification work? -- A literature review of empirical "
    "studies on gamification. *47th Hawaii International Conference on System Sciences*, 3025–3034. "
    "https://doi.org/10.1109/HICSS.2014.377"
)
ref_kapp = reference(
    "Kapp, K. M. (2012). *The gamification of learning and instruction: Game-based methods and strategies "
    "for training and education*. Pfeiffer."
)

# Insertar Deterding antes de Dirisu
patron_dirisu = re.compile(
    r'(<w:p\b[^>]*>(?:(?!</w:p>).)*?Dirisu, C\. D\..*?</w:p>)',
    re.DOTALL
)
assert patron_dirisu.search(xml_content), "No se encontró la referencia de Dirisu"
xml_content = patron_dirisu.sub(ref_deterding + r'\1', xml_content, count=1)

# Insertar Hamari antes de Jin et al.
patron_jin = re.compile(
    r'(<w:p\b[^>]*>(?:(?!</w:p>).)*?Jin, S\., Guo, R\..*?</w:p>)',
    re.DOTALL
)
assert patron_jin.search(xml_content), "No se encontró la referencia de Jin"
xml_content = patron_jin.sub(ref_hamari + r'\1', xml_content, count=1)

# Insertar Kapp antes de Lakera
patron_lakera = re.compile(
    r'(<w:p\b[^>]*>(?:(?!</w:p>).)*?Lakera\..*?</w:p>)',
    re.DOTALL
)
assert patron_lakera.search(xml_content), "No se encontró la referencia de Lakera"
xml_content = patron_lakera.sub(ref_kapp + r'\1', xml_content, count=1)

print("4. Referencias de Deterding, Hamari y Kapp añadidas en orden alfabético.")

# Guardar XML modificado
with open(doc_xml_path, "w", encoding="utf-8") as f:
    f.write(xml_content)

# Reempaquetar
with zipfile.ZipFile(DOCX_OUT, "w", zipfile.ZIP_DEFLATED) as z_out:
    done = set()
    for n in orden_entradas:
        p_file = os.path.join(DOCX_TEMP, n)
        if os.path.exists(p_file):
            z_out.write(p_file, n)
            done.add(n)
    for root, _, files in os.walk(DOCX_TEMP):
        for fl in files:
            rel = os.path.relpath(os.path.join(root, fl), DOCX_TEMP).replace(os.sep, "/")
            if rel not in done:
                z_out.write(os.path.join(root, fl), rel)

shutil.rmtree(DOCX_TEMP, ignore_errors=True)
print(f"Documento guardado con éxito en: {DOCX_OUT}")
