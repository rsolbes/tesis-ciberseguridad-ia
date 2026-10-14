// Serverless Function de Vercel para el Asistente de IA (Google Gemini).
// Protege la API Key de Gemini en el servidor, valida el código de acceso del evaluador
// y auto-detecta dinámicamente los modelos compatibles disponibles en la cuenta del usuario.
// No requiere bases de datos.

const crypto = require('crypto');

// Límites de protección
const LIMITE_POR_MINUTO = 20;
const registroIps = new Map();
let modeloCacheado = null;

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

// Descubre dinámicamente qué modelos soportan generateContent en la cuenta de la API Key
async function descubrirModelo(apiKey) {
  if (modeloCacheado) return modeloCacheado;
  try {
    const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${apiKey}`);
    if (res.ok) {
      const data = await res.json();
      const validos = (data.models || [])
        .filter(m => (m.supportedGenerationMethods || []).includes('generateContent'))
        .map(m => m.name.replace(/^models\//, ''));

      // Priorizar variantes Flash (rápidas, económicas y de buen razonamiento)
      const seleccionado =
        validos.find(n => /flash-lite/i.test(n)) ||
        validos.find(n => /gemini-2/i.test(n) && /flash/i.test(n)) ||
        validos.find(n => /gemini-1\.5-flash/i.test(n)) ||
        validos.find(n => /flash/i.test(n)) ||
        validos.find(n => /gemini/i.test(n)) ||
        validos[0];

      if (seleccionado) {
        modeloCacheado = seleccionado;
        return seleccionado;
      }
    }
  } catch (e) {
    // Si la llamada falla, se recurre a la lista de respaldo
  }
  return null;
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
      modeloActivo: modeloCacheado || 'auto-detección activa',
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

  // 3. Validar código de acceso del evaluador
  const codigoRecibido = req.headers['x-codigo-acceso'] || (req.body && req.body.codigoAcceso);
  if (!codigoRecibido) {
    return res.status(401).json({
      error: 'Se requiere el código de acceso de evaluador para consultar al agente de IA.'
    });
  }

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

  const payloadGemini = {
    systemInstruction: cuerpo.systemInstruction,
    contents: Array.isArray(cuerpo.contents) ? cuerpo.contents.slice(-14) : [],
    generationConfig: cuerpo.generationConfig || {
      temperature: 0.3,
      maxOutputTokens: 700
    }
  };

  // 5. Construir lista de modelos a intentar de forma resiliente
  const modelosAIntentar = [];
  if (process.env.GEMINI_MODEL) {
    modelosAIntentar.push(process.env.GEMINI_MODEL.trim());
  }

  const modeloDescubierto = await descubrirModelo(apiKey);
  if (modeloDescubierto && !modelosAIntentar.includes(modeloDescubierto)) {
    modelosAIntentar.push(modeloDescubierto);
  }

  const respaldos = [
    'gemini-1.5-flash-latest',
    'gemini-1.5-flash-002',
    'gemini-1.5-flash-001',
    'gemini-2.0-flash',
    'gemini-2.5-flash',
    'gemini-pro'
  ];
  for (const r of respaldos) {
    if (!modelosAIntentar.includes(r)) {
      modelosAIntentar.push(r);
    }
  }

  // 6. Probar secuencialmente hasta que uno responda con éxito
  let ultimoError = 'Modelo no disponible';
  let datos = null;
  let exito = false;

  for (const mod of modelosAIntentar) {
    try {
      const url = `https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(mod)}:generateContent?key=${apiKey}`;
      const respuestaGemini = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payloadGemini)
      });

      datos = await respuestaGemini.json();

      if (respuestaGemini.ok) {
        modeloCacheado = mod;
        exito = true;
        break;
      }

      // Si Google dice que no existe el modelo (404), pasamos silenciosamente al siguiente
      if (respuestaGemini.status === 404 || (datos.error && /not found/i.test(datos.error.message || ''))) {
        ultimoError = datos.error ? datos.error.message : `Modelo ${mod} no encontrado`;
        continue;
      } else {
        // Si es un error de credenciales, bloqueo o cuota, lo retornamos de inmediato
        const msg = (datos.error && datos.error.message) || 'Error al comunicarse con Google Gemini';
        return res.status(respuestaGemini.status).json({ error: msg });
      }
    } catch (err) {
      ultimoError = err.message;
    }
  }

  if (!exito) {
    return res.status(502).json({
      error: `No fue posible conectar con ningún modelo disponible en tu cuenta (${ultimoError}).`
    });
  }

  return res.status(200).json(datos);
};
