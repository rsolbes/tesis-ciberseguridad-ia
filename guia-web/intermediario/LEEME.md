# Intermediario del asistente

Este intermediario solo se necesita si la guía se publica en internet y el asistente usa Gemini. Su función es guardar la clave de la API en un servidor, para que nunca aparezca en el código de la página, y limitar quién y cuánto puede preguntar.

## Publicarlo en Cloudflare Workers (plan gratuito)

1. Crea una cuenta en https://dash.cloudflare.com y entra a Workers.
2. Crea un Worker nuevo y pega el contenido de `worker.js`.
3. En la configuración del Worker agrega tres variables. `GEMINI_API_KEY` como secreto, con tu clave de Google AI Studio. `ORIGEN_PERMITIDO` con la dirección de tu sitio, por ejemplo `https://usuario.github.io`. `MODELO` con el nombre del modelo Flash-Lite vigente, que puedes consultar en la sección Asistente de la guía con el botón «Buscar modelos de Gemini».
4. Publica el Worker y copia su dirección, que tendrá la forma `https://nombre.usuario.workers.dev`.
5. En la sección Asistente de la guía elige el modo «Gemini mediante intermediario» y pega esa dirección.

## Recomendaciones

Fija un tope de uso en Google AI Studio, no compartas la clave y revoca la clave cuando termine la validación de la tesis. Recuerda que los términos de Gemini prohíben usarlo en aplicaciones dirigidas a menores de 18 años, por lo que esta opción es solo para las demostraciones con el comité y los expertos.
