# Ayuda

## Cómo se usa la guía

Empieza en el [punto de partida](#/modulo/m0), responde la autoevaluación de entrada, elige tu ruta y acepta las reglas de uso ético. Después avanza por el [mapa de la guía](#/mapa). Al final de cada módulo hay una autoevaluación, y si la apruebas obtienes una insignia.

## Privacidad

El sitio no pide registro y no envía tus respuestas a ningún servidor. Tu ruta, tus resultados y tus insignias se guardan solo en este navegador. Si borras los datos de navegación, se pierden.

Las preguntas que haces al asistente sí se envían al modelo de lenguaje que esté configurado. Si usas Ollama, nunca salen de tu computadora o de la red de tu escuela. Si se usa Gemini, se envían a los servidores de Google. Por eso nunca escribas datos personales ni contraseñas en el asistente.

## Cómo conectar el asistente con Ollama

1. Instala Ollama desde https://ollama.com y ábrelo.
2. Descarga un modelo ligero. En una terminal escribe `ollama pull llama3.2:3b` o cualquier otro modelo de tamaño similar.
3. Si abres la guía desde tu propia computadora (por ejemplo en `http://localhost:8000`, con el servidor iniciado dentro de la carpeta `guia-web` mediante `python -m http.server 8000 --bind 127.0.0.1`), Ollama la acepta sin configuración adicional.
4. Si abres la guía desde internet, debes autorizar su dirección en Ollama. En Windows, crea la variable de entorno `OLLAMA_ORIGINS` con la dirección del sitio, por ejemplo `https://usuario.github.io`, y reinicia Ollama. Algunos navegadores también pedirán permiso para que la página acceda a la red local; acéptalo.
5. En la sección [Asistente](#/configuracion) elige el modo Ollama y pulsa «Buscar modelos de Ollama».

## Servidor de laboratorio

En un salón de cómputo, una sola computadora puede atender a las demás. En esa computadora se configura la variable `OLLAMA_HOST` con el valor `0.0.0.0` para que acepte conexiones de la red local, se agrega la dirección del sitio en `OLLAMA_ORIGINS` y se restringe el firewall a la red del plantel. En las demás computadoras basta con escribir su dirección, por ejemplo `http://192.168.1.20:11434`, en la sección [Asistente](#/configuracion).

## Sobre Gemini

El prototipo puede usar el nivel gratuito de la API de Gemini para demostraciones con adultos. Sus términos prohíben usarlo en aplicaciones dirigidas a menores de 18 años y, en el nivel gratuito, permiten que Google use el contenido enviado para mejorar sus productos. Con estudiantes de bachillerato debe usarse Ollama.
