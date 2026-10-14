# Iniciación en Ciberseguridad con Agentes de Inteligencia Artificial

[![Live Demo](https://img.shields.io/badge/Demo-tesis.rodrigosolbes.com-1baf7a?style=for-the-badge&logo=vercel)](https://tesis.rodrigosolbes.com)
[![License](https://img.shields.io/badge/Licencia-MIT-2a78d6?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Institución](https://img.shields.io/badge/UAT-Facultad%20de%20Ingenier%C3%ADa%20Tampico-orange?style=for-the-badge)](https://www.uat.edu.mx)

> **Tesis de Licenciatura en Ingeniería en Sistemas Computacionales (ISC)**  
> **Alumno:** Rodrigo Solbes Davalos  
> **Comité Asesor:** Dr. Eduardo Álvarez Navarro (Director), Dr. Gabriel Chavira Juárez (Co-Director), Dra. Adriana Montoto González (Asesora)  
> **Facultad de Ingeniería Tampico · Universidad Autónoma de Tamaulipas (UAT)**  

---

## Resumen del Proyecto

Este proyecto diseña y desarrolla una **guía didáctica interactiva y gamificada** orientada a la iniciación en ciberseguridad mediante **agentes de inteligencia artificial**, dirigida tanto a estudiantes de bachillerato tecnológico (especialidad técnica en Programación) como a estudiantes universitarios de ingeniería en sistemas computacionales.

A diferencia de los cursos tradicionales centrados en herramientas estáticas, este trabajo aborda a los agentes de IA desde una triple perspectiva:
1. **Qué son y cómo funcionan:** Arquitecturas cognitivas (ReAct), percepción, memoria a corto/largo plazo y llamadas a funciones (*Function Calling*).
2. **Cómo se usan para defender:** Triaje de alertas en el SOC, correlación de bitácoras y enriquecimiento de incidentes frente a sistemas tradicionales de reglas.
3. **Cómo se atacan y cómo se protegen:** Mitigación de inyecciones de instrucciones directas e indirectas (OWASP LLM01, MITRE ATLAS AML.T0054), aislamiento por mínimo privilegio y defensa contra envenenamiento de memoria RAG.

---

## Características Principales

* **Plataforma Web Interactiva (`guia-web/`):** Sitio web estático (HTML5, CSS3, JavaScript nativo) sin dependencias ni servidores propios, operable al 100 % en el navegador con privacidad garantizada en `localStorage`.
* **Motor de Gamificación Nativo:**
  * Sistema de Puntos de Experiencia (**XP**) acumulativos por lecturas, autoevaluaciones y prácticas.
  * Progresión de 5 Rangos: *Recluta Digital* 🛡️ ➔ *Operador de Red* 💻 ➔ *Analista de Triaje* 🔍 ➔ *Guardián de Agentes* ⚡ ➔ *Comandante de Ciberdefensa* 🏆.
  * HUD interactivo en tiempo real, efectos sonoros sintetizados mediante la **Web Audio API** y animaciones festivas de confeti en lienzo nativo.
  * **Minijuegos en el navegador:** Simulador táctico de filtrado en cortafuegos (M2) y sandbox interactivo de inyección de prompts con modo blindado (M7).
* **Enseñanza Diferenciada en Dos Rutas:**
  * **Ruta Básica (Cetis - 40 horas):** Construcción conceptual progresiva, retos interactivos y código preconfigurado.
  * **Ruta Avanzada (ISC - 32 horas):** Enfoque ingenieril, construcción de herramientas, métricas cuantitativas (Precisión, Recall, F1) y defensas en profundidad.
* **Alineación con Estándares Internacionales:**
  * CSEC2017 (ACM/IEEE)
  * NICE Framework (NIST SP 800-181r1)
  * NIST Cybersecurity Framework 2.0 (CSF)
  * NIST AI Risk Management Framework (AI RMF)
  * OWASP Top 10 for LLM Applications 2025
* **Revisión Sistemática PRISMA 2020:**
  * Búsqueda y cribado sobre **1,228 registros** académicos (OpenAlex y arXiv) entre 2022 y 2026.
  * **250 estudios incluidos** y caracterizados exhaustivamente en [`Revision sistematica PRISMA - datos.xlsx`](Revision%20sistematica%20PRISMA%20-%20datos.xlsx).
  * Auditoría de muestra del 10 % con concordancia inter-evaluador casi perfecta ($\kappa = 0.9215$ en cribado y $\kappa = 0.7797$ en elegibilidad).

---

## 7 Laboratorios Prácticos Reproducibles (`guia-web/laboratorios/`)

Los laboratorios se ejecutan localmente en entornos aislados con datos sintéticos y permisos controlados:

| Laboratorio | Módulo | Entorno | Propósito y Habilidades Desarrolladas |
|---|:---:|---|---|
| **Lab 1: Mi primer modelo local** | M4 | Python / Ollama | Variación de temperatura (0.0 vs 1.0), ventana de contexto y registro de trampas de alucinación. |
| **Lab 2: Del asistente al agente** | M5 | Python | Implementación del ciclo ReAct conectando el LLM a una herramienta de consulta de bitácoras de solo lectura. |
| **Lab 3: Triaje de alertas** | M6 | Python | Evaluación comparativa entre un motor de reglas estáticas y un agente contextual (Precisión, Recall y F1-score). |
| **Lab 4: Instrucciones ocultas** | M7 | Python / Ollama | Demostración de inyección indirecta oculta en alertas y mitigación mediante validación de esquema y lista cerrada. |
| **Lab 5: Credenciales y mínimo privilegio** | M7 | Python | Demostración empírica de cómo la mediación de herramientas reduce la fuga de claves API de 100 % a 0 % (Jin et al., 2026). |
| **Lab 6: Memoria envenenada** | M7 | Python / RAG | Simulación de inyección de documentos falsos en bases vectoriales y defensa mediante verificación de hashes SHA-256. |
| **Lab 7: Reto integrador CTF** | Reto | Python | Escenario defensivo de respuesta a incidentes en 4 fases, descubriendo banderas (`FLAG{...}`) bajo el marco NIST CSF. |

---

## Estructura del Repositorio

```text
├── Avance de tesis.docx                    # Documento formal de tesis de licenciatura
├── Revision sistematica PRISMA - datos.xlsx# Base de datos de la revisión sistemática (250 estudios)
├── guia-web/                               # Prototipo del sitio web estático interactivo
│   ├── index.html                          # Punto de entrada de la aplicación
│   ├── vercel.json                         # Configuración de despliegue para Vercel
│   ├── css/estilos.css                     # Sistema de estilos y animaciones de gamificación
│   ├── js/
│   │   ├── almacen.js                      # Motor de persistencia (localStorage) y estado de XP
│   │   ├── juego.js                        # Motor de audio Web Audio API, confeti y minijuegos
│   │   ├── asistente.js                    # Conexión multimodal (Ollama, Gemini, FAQ local)
│   │   ├── markdown.js                     # Renderizador seguro de Markdown (sanitizado contra XSS)
│   │   └── app.js                          # Enrutador por hash, HUD, autoevaluaciones y lógica
│   ├── contenido/                          # Módulos M0-M8 y Reto en Markdown + Bancos JSON
│   └── laboratorios/                       # Código fuente y datasets de los 7 laboratorios
└── _material_de_trabajo/
    ├── juicio_expertos/                    # Instrumento de evaluación (Anexo 1, SUS) y script de cálculo CVR
    ├── revision_prisma/                    # Scripts de cosecha (OpenAlex), cribado y auditoría Kappa
    └── generador_docx/                     # Automatización de compilación y actualización de Word COM
```

---

## Puesta en Marcha Local

### 1. Explorar la Guía Web en tu computadora

Al ser una aplicación web estática, solo requiere un servidor HTTP local para servir los archivos JSON y Markdown:

```bash
# Navega a la carpeta de la web
cd guia-web

# Inicia un servidor seguro en localhost
python -m http.server 8000 --bind 127.0.0.1
```

Abre tu navegador en `http://127.0.0.1:8000`.

### 2. Ejecutar los Laboratorios

Cada laboratorio en `guia-web/laboratorios/` contiene su propio archivo instructivo `LEEME.md` y scripts reproducibles en Python estándar:

```bash
# Ejemplo: Ejecutar el Laboratorio 3 de Triaje de Alertas
cd guia-web/laboratorios/lab3
python evaluar_triaje.py

# Ejemplo: Ejecutar el Laboratorio 7 (Reto CTF Defensivo)
cd guia-web/laboratorios/lab7
python analizar_incidente.py
```

---

## Despliegue en la Nube (Vercel)

El proyecto incluye [`guia-web/vercel.json`](guia-web/vercel.json) preconfigurado con políticas de seguridad y URLs limpias.  
Para desplegarlo en tu propio dominio:

1. Importa este repositorio en [Vercel](https://vercel.com).
2. En la configuración de proyecto, establece **Root Directory** como `guia-web`.
3. En **Settings ➔ Domains**, asigna tu dominio o subdominio personalizado (ej. `tesis.rodrigosolbes.com`).

---

## Licencia

Este proyecto se distribuye bajo la licencia **MIT**. Consulta el archivo `LICENSE` para más detalles.
