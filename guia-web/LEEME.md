# Guía de iniciación · Agentes de IA y ciberseguridad (prototipo)

Prototipo del sitio web interactivo que acompaña la tesis *Diseño de una guía didáctica para la iniciación en ciberseguridad con agentes de inteligencia artificial en bachillerato tecnológico y universidad*.

## Qué incluye este prototipo

La portada, el mapa completo de la guía, el módulo M0 (autoevaluación de entrada, elección de ruta y reglas de uso ético), el módulo M7 completo (seguridad de los agentes) con su autoevaluación e insignia, el laboratorio 4 y el asistente conversacional. Los demás módulos aparecen en el mapa como «próximamente».

## Cómo abrirlo en tu computadora

El sitio necesita un servidor local porque carga sus contenidos desde archivos. Abre una terminal **dentro de la carpeta `guia-web`** y ejecuta

```
python -m http.server 8000 --bind 127.0.0.1
```

Después abre `http://localhost:8000` en el navegador. Para detener el servidor, presiona Ctrl+C en la terminal.

Dos cuidados importantes. El servidor publica la carpeta desde la que lo ejecutas, así que si lo inicias en otra carpeta mostrará todos sus archivos. Y sin la opción `--bind 127.0.0.1`, cualquier equipo de tu red podría abrirlo, por lo que siempre conviene incluirla.

## Estructura

```
guia-web/
  index.html              página única del sitio
  css/estilos.css         estilos (modo claro y oscuro, adaptable a celular)
  js/almacen.js           progreso del estudiante en el navegador (localStorage)
  js/markdown.js          conversor de Markdown que escapa todo el HTML
  js/asistente.js         asistente y conexión intercambiable con el modelo
  js/app.js               navegación, módulos, autoevaluaciones e insignias
  contenido/              textos de los módulos (Markdown) y datos (JSON)
  laboratorios/lab4/      archivos del laboratorio 4
  intermediario/          intermediario opcional para publicar con Gemini
```

## Cómo agregar o editar un módulo

1. Escribe el contenido en `contenido/mX.md`. Puedes usar los bloques `:::avanzada`, `:::basica`, `:::nota`, `:::alerta`, `:::ejemplo` y `:::laboratorio`, que se cierran con `:::`. Para que un bloque aparezca solo en una ruta, agrega la ruta entre corchetes, por ejemplo `:::laboratorio[avanzada] Título`.
2. Si tiene autoevaluación, créala en `contenido/mX-autoevaluacion.json` siguiendo el formato de `m7-autoevaluacion.json`. Cada pregunta indica si es para la ruta `basica`, `avanzada` o `ambas`.
3. Agrega preguntas frecuentes en `contenido/mX-faq.json`; el asistente las usa cuando no hay modelo disponible.
4. En `contenido/modulos.json` cambia el `estado` del módulo a `disponible` y agrega los nombres de sus archivos.

## Seguridad del propio sitio

El sitio no tiene servidor ni cuentas y no recolecta datos personales. Todo el texto, incluido el que genera el asistente, se escapa antes de mostrarse, por lo que una respuesta manipulada no puede inyectar código en la página. La política de seguridad de contenido solo permite ejecutar los scripts propios del sitio. La clave de Gemini nunca debe escribirse en el código; para un sitio publicado se usa el intermediario.

## Publicarlo

Al ser un sitio estático, puede publicarse gratis en GitHub Pages subiendo la carpeta `guia-web` a un repositorio y activando Pages. Si el asistente usará Gemini, publica también el intermediario (consulta `intermediario/LEEME.md`).
