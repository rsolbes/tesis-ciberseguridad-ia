// Intermediario para el asistente de la guía (Cloudflare Workers, plan gratuito).
// Guarda la clave de Gemini como secreto del servidor para que nunca llegue al navegador,
// acepta solicitudes solo desde el sitio de la guía y limita el tamaño y la frecuencia de las preguntas.
//
// Variables de configuración del Worker:
//   GEMINI_API_KEY   (secreto)  clave de la API de Gemini
//   ORIGEN_PERMITIDO            dirección del sitio, por ejemplo https://usuario.github.io
//   MODELO                      modelo a usar, por ejemplo el Flash-Lite vigente

const LIMITE_POR_MINUTO = 10;        // preguntas por dirección IP y por minuto (aproximado, por instancia)
const MAX_BYTES = 40000;             // tamaño máximo de cada solicitud
const contador = new Map();

function cors(origen, env) {
  return {
    'Access-Control-Allow-Origin': origen === env.ORIGEN_PERMITIDO ? origen : 'null',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Vary': 'Origin',
  };
}

function limitar(ip) {
  const ahora = Date.now();
  const r = contador.get(ip) || { inicio: ahora, n: 0 };
  if (ahora - r.inicio > 60000) { r.inicio = ahora; r.n = 0; }
  r.n += 1;
  contador.set(ip, r);
  return r.n > LIMITE_POR_MINUTO;
}

export default {
  async fetch(request, env) {
    const origen = request.headers.get('Origin') || '';
    const encabezados = cors(origen, env);

    if (request.method === 'OPTIONS') return new Response(null, { headers: encabezados });
    if (request.method !== 'POST') return new Response('Método no permitido', { status: 405, headers: encabezados });
    if (origen !== env.ORIGEN_PERMITIDO) return new Response('Origen no permitido', { status: 403, headers: encabezados });

    const ip = request.headers.get('CF-Connecting-IP') || 'desconocida';
    if (limitar(ip)) return new Response('Demasiadas solicitudes', { status: 429, headers: encabezados });

    const texto = await request.text();
    if (texto.length > MAX_BYTES) return new Response('Solicitud demasiado grande', { status: 413, headers: encabezados });

    let cuerpo;
    try { cuerpo = JSON.parse(texto); } catch { return new Response('JSON inválido', { status: 400, headers: encabezados }); }

    // Solo se reenvían los campos esperados; el modelo lo fija el servidor, no el navegador.
    const limpio = {
      systemInstruction: cuerpo.systemInstruction,
      contents: Array.isArray(cuerpo.contents) ? cuerpo.contents.slice(-13) : [],
      generationConfig: { temperature: 0.3, maxOutputTokens: 700 },
    };

    const url = `https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(env.MODELO)}:generateContent`;
    const r = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-goog-api-key': env.GEMINI_API_KEY },
      body: JSON.stringify(limpio),
    });

    return new Response(await r.text(), {
      status: r.status,
      headers: Object.assign({ 'Content-Type': 'application/json' }, encabezados),
    });
  },
};
