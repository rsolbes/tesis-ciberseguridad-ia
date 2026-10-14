// Serverless Function de Vercel para el Asistente de IA (Google Gemini).
// Protege la API Key de Gemini en el servidor y valida el código de acceso del evaluador.
// No requiere bases de datos.

const crypto = require('crypto');

// Límites de protección
const LIMITE_POR_MINUTO = 20;
const registroIps = new Map();

function limpiarRegistroIps() {
  const ahora = Date.now();
  for (const [ip, datos] of registroIps.entries()) {
    if (ahora - datos.inicio > 60000) {
      registroIps.delete(ip);
    }
  }
}

function esRateLimited(ip) {
  limpiarRegistroIps();
  const ahora = Date.now();
  const reg = registroIps.get(ip) || { inicio: ahora, count: 0 };
  if (ahora - reg.inicio > 60000) {
    reg.inicio = ahora;
    reg.count = 0;
  }
  reg.count += 1;
  registroIps.set(ip, reg);
  return reg.count > LIMITE_POR_MINUTO;
}

module.exports = async (req, res) => {
  // Encabezados CORS y seguridad
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,POST');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, x-codigo-acceso');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // Health check por GET
  if (req.method === 'GET') {
    const configurado = Boolean(process.env.GEMINI_API_KEY && process.env.CODIGO_ACCESO);
    return res.status(200).json({
      estado: 'activo',
      configurado,
      mensaje: configurado
        ? 'Servicio de agente seguro listo en Vercel.'
        : 'Variables de entorno GEMINI_API_KEY o CODIGO_ACCESO pendientes en Vercel.'
    });
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Método no permitido. Utiliza POST.' });
  }

  // 1. Verificar variables de entorno en Vercel
  const apiKey = process.env.GEMINI_API_KEY;
  const codigoEsperado = process.env.CODIGO_ACCESO;
  const modelo = process.env.GEMINI_MODEL || 'gemini-1.5-flash';

  if (!apiKey || !codigoEsperado) {
    return res.status(503).json({
      error: 'El backend aún no tiene configuradas las variables GEMINI_API_KEY o CODIGO_ACCESO en Vercel.'
    });
  }

  // 2. Control de saturación (Rate limiting)
  const ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress || '127.0.0.1';
  if (esRateLimited(ip)) {
    return res.status(429).json({
      error: 'Se alcanzó el límite de preguntas por minuto. Por favor espera un momento.'
    });
  }

  // 3. Validar código de acceso del evaluador (en encabezado x-codigo-acceso o en el body)
  const codigoRecibido = req.headers['x-codigo-acceso'] || (req.body && req.body.codigoAcceso);
  if (!codigoRecibido) {
    return res.status(401).json({
      error: 'Se requiere el código de acceso de evaluador para consultar al agente de IA.'
    });
  }

  // Comparación segura en tiempo constante para mitigar timing attacks
  const bufEsperado = Buffer.from(String(codigoEsperado).trim());
  const bufRecibido = Buffer.from(String(codigoRecibido).trim());

  let coincide = false;
  if (bufEsperado.length === bufRecibido.length) {
    coincide = crypto.timingSafeEqual(bufEsperado, bufRecibido);
  }

  if (!coincide) {
    return res.status(401).json({
      error: 'Código de acceso de evaluador inválido.'
    });
  }

  // 4. Validar cuerpo de la solicitud
  const cuerpo = req.body;
  if (!cuerpo || !cuerpo.contents) {
    return res.status(400).json({ error: 'Formato de solicitud inválido.' });
  }

  // Limitar turnos de historial y tokens
  const payloadGemini = {
    systemInstruction: cuerpo.systemInstruction,
    contents: Array.isArray(cuerpo.contents) ? cuerpo.contents.slice(-14) : [],
    generationConfig: cuerpo.generationConfig || {
      temperature: 0.3,
      maxOutputTokens: 700
    }
  };

  try {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(modelo)}:generateContent?key=${apiKey}`;
    const respuestaGemini = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payloadGemini)
    });

    const datos = await respuestaGemini.json();
    if (!respuestaGemini.ok) {
      const mensaje = (datos.error && datos.error.message) || 'Error al comunicarse con Google Gemini';
      return res.status(respuestaGemini.status).json({ error: mensaje });
    }

    return res.status(200).json(datos);
  } catch (err) {
    return res.status(502).json({
      error: 'Fallo de conexión con la API de Google Gemini: ' + err.message
    });
  }
};
