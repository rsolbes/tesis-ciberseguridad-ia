"""Actualiza 'Avance de tesis.docx':
1. Reemplaza el pendiente de la verificación PRISMA 10 % con los resultados calculados.
2. Añade la referencia de Landis y Koch (1977).
3. Actualiza la referencia de Deng et al. (ACM Computing Surveys).
4. Guarda y reempaqueta preservando el orden exacto de los archivos XML.
"""
import os, sys, shutil, zipfile, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wlib
from wlib import p, reference

DOCX_ORIG = r"C:\Users\SISTEMAS10\Desktop\Estudio\TESIS NUEVA\Avance de tesis.docx"
DOCX_TEMP = os.path.join(HERE, "temp_docx")
DOCX_OUT = r"C:\Users\SISTEMAS10\Desktop\Estudio\TESIS NUEVA\Avance de tesis.docx"

shutil.rmtree(DOCX_TEMP, ignore_errors=True)

with zipfile.ZipFile(DOCX_ORIG) as z:
    z.extractall(DOCX_TEMP)
    orden_entradas = z.namelist()

doc_xml_path = os.path.join(DOCX_TEMP, "word", "document.xml")
with open(doc_xml_path, "r", encoding="utf-8") as f:
    xml_content = f.read()

# 1. Reemplazo del párrafo pendiente
texto_nuevo_prisma = (
    "Para verificar la consistencia del proceso se auditó de forma manual una muestra aleatoria "
    "del 10 % de las decisiones en ambas fases (77 registros en el cribado por título y resumen y "
    "26 registros en la evaluación de texto completo), con base en los mismos criterios predefinidos. "
    "En la fase de cribado se obtuvo un acuerdo observado del 97.40 % y un coeficiente kappa de Cohen "
    "de 0.9215, que corresponde a un acuerdo casi perfecto según los criterios de Landis y Koch (1977). "
    "En la fase de elegibilidad en texto completo el acuerdo observado fue del 96.15 % con un coeficiente "
    "kappa de 0.7797, correspondiente a un acuerdo sustancial. Las escasas discrepancias se concentraron "
    "en casos límite sobre el grado de autonomía de las herramientas evaluadas y se resolvieron mediante "
    "consenso sin alterar los estudios incluidos. El detalle de cada registro auditado se conserva en la "
    "hoja Muestra de verificación del archivo de datos complementario."
)
xml_nuevo_prisma = p(texto_nuevo_prisma)

# Buscar el párrafo con el texto pendiente
patron_pendiente = re.compile(
    r'<w:p\b[^>]*>(?:(?!</w:p>).)*?Verificar manualmente una muestra aleatoria del 10 %.*?</w:p>',
    re.DOTALL
)
assert patron_pendiente.search(xml_content), "No se encontró el párrafo pendiente en document.xml"
xml_content = patron_pendiente.sub(xml_nuevo_prisma, xml_content, count=1)
print("1. Párrafo pendiente de PRISMA reemplazado exitosamente.")

# 2. Añadir referencia de Landis y Koch (1977)
ref_landis = reference(
    "Landis, J. R., & Koch, G. G. (1977). The measurement of observer agreement for categorical data. "
    "*Biometrics*, *33*(1), 159–174. https://doi.org/10.2307/2529310"
)

# Insertar antes de Lawshe (1975)
patron_lawshe = re.compile(
    r'(<w:p\b[^>]*>(?:(?!</w:p>).)*?Lawshe, C\. H\. \(1975\).*?</w:p>)',
    re.DOTALL
)
assert patron_lawshe.search(xml_content), "No se encontró la referencia de Lawshe en document.xml"
xml_content = patron_lawshe.sub(ref_landis + r'\1', xml_content, count=1)
print("2. Referencia de Landis y Koch (1977) insertada exitosamente.")

# 3. Actualizar referencia de Deng et al. a ACM Computing Surveys
ref_deng_acm = reference(
    "Deng, Z., Guo, Y., Han, C., Ma, W., Xiong, J., Wen, S., & Xiang, Y. (2025). "
    "AI agents under threat: A survey of key security challenges and future pathways. "
    "*ACM Computing Surveys*, *57*(9), 1–38. https://doi.org/10.1145/3719468"
)
patron_deng = re.compile(
    r'<w:p\b[^>]*>(?:(?!</w:p>).)*?Deng, Z\., Guo, Y\..*?</w:p>',
    re.DOTALL
)
assert patron_deng.search(xml_content), "No se encontró la referencia de Deng et al. en document.xml"
xml_content = patron_deng.sub(ref_deng_acm, xml_content, count=1)
print("3. Referencia de Deng et al. actualizada a ACM Computing Surveys.")

# Guardar XML modificado
with open(doc_xml_path, "w", encoding="utf-8") as f:
    f.write(xml_content)

# Reempaquetar respetando el orden original exacto
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
print(f"Documento reempaquetado exitosamente en: {DOCX_OUT}")
