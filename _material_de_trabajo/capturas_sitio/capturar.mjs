// Recorre el sitio con el protocolo de depuración de Edge (CDP) y toma capturas en modo claro.
import { spawn } from 'node:child_process';
import { writeFileSync, mkdirSync, rmSync } from 'node:fs';
import { join } from 'node:path';

const OUT = process.argv[2];
const BASE = 'http://localhost:8001/';
const EDGE = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const PERFIL = join(OUT, 'perfil-cdp');
mkdirSync(OUT, { recursive: true });
rmSync(PERFIL, { recursive: true, force: true });

const edge = spawn(EDGE, ['--headless=new', '--disable-gpu', '--hide-scrollbars', '--remote-debugging-port=9333',
  `--user-data-dir=${PERFIL}`, 'about:blank'], { stdio: 'ignore' });
const dormir = (ms) => new Promise((r) => setTimeout(r, ms));

let lista;
for (let i = 0; i < 40; i++) {
  try { lista = await (await fetch('http://127.0.0.1:9333/json/list')).json(); if (lista.length) break; } catch {}
  await dormir(250);
}
const pagina = lista.find((t) => t.type === 'page');
const ws = new WebSocket(pagina.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener('open', r));
let id = 0; let nav = 0; const pend = new Map();
ws.addEventListener('message', (ev) => { const m = JSON.parse(ev.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); } });
const cdp = (method, params = {}) => new Promise((res) => { const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
const js = async (expr) => {
  const r = await cdp('Runtime.evaluate', { expression: `(async()=>{${expr}})()`, awaitPromise: true, returnByValue: true });
  if (r.result?.exceptionDetails) throw new Error(JSON.stringify(r.result.exceptionDetails).slice(0, 400));
  return r.result?.result?.value;
};

await cdp('Page.enable');
await cdp('Runtime.enable');
await cdp('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: 'light' }] });

async function tam(width, height, mobile = false) {
  await cdp('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 2, mobile });
}
async function ir(hash) {
  await cdp('Page.navigate', { url: BASE + '?c=' + (++nav) + hash });
  await dormir(1500);
}
async function foto(nombre) {
  const r = await cdp('Page.captureScreenshot', { format: 'png' });
  writeFileSync(join(OUT, nombre + '.png'), Buffer.from(r.result.data, 'base64'));
  console.log('captura', nombre);
}
const estado = (obj) => `localStorage.setItem('guia-agentes-ia-v1', ${JSON.stringify(JSON.stringify(obj))});`;
const BASICA = { ruta: 'basica', aceptoReglas: true, modulos: { m0: { leido: true, puntaje: null, insignia: true } }, asistente: { modo: 'sin-conexion' } };
const AVANZADA = Object.assign({}, BASICA, { ruta: 'avanzada' });

// 1. Portada sin progreso
await tam(1280, 800);
await ir('#/');
await js(`localStorage.clear(); return 1;`);
await ir('#/');
await foto('01_portada');

// 2. Mapa con la ruta básica elegida
await js(estado(BASICA) + 'return 1;');
await tam(1280, 1180);
await ir('#/mapa');
await foto('02_mapa');

// 3. M0, resultado de la autoevaluación de entrada y reglas
await js(`localStorage.clear(); return 1;`);
await tam(1280, 1000);
await ir('#/modulo/m0');
await js(`
  const fs=[...document.querySelectorAll('#forma-diag fieldset')];
  fs.forEach((f,i)=>{const o=f.querySelectorAll('input'); o[i%3===0?0:o.length-1].click();});
  document.querySelector('#forma-diag button[type=submit]').click();
  await new Promise(r=>setTimeout(r,300));
  document.getElementById('diag-resultado').scrollIntoView({block:'start'});
  window.scrollBy(0,-90);
  return 1;`);
await dormir(400);
await foto('03_m0_resultado');

// 4. M7, contenido diferenciado en la ruta avanzada mostrando ambas rutas
await js(estado(AVANZADA) + 'return 1;');
await tam(1280, 1000);
await ir('#/modulo/m7');
await js(`
  const v=document.getElementById('ver-todo'); v.click();
  document.querySelector('.bloque-basica').scrollIntoView({block:'start'}); window.scrollBy(0,-330);
  return 1;`);
await dormir(400);
await foto('04_m7_contenido');

// 5. Autoevaluación con retroalimentación e insignia (ruta básica)
await js(estado(BASICA) + 'return 1;');
await tam(1280, 1000);
await ir('#/modulo/m7');
await js(`
  const a=await (await fetch('contenido/m7-autoevaluacion.json')).json();
  const pq=a.preguntas.filter(p=>p.ruta!=='avanzada');
  document.querySelectorAll('#forma-auto fieldset').forEach((f,i)=>{const k=i===6?(pq[i].correcta+1)%4:pq[i].correcta; f.querySelectorAll('input')[k].click();});
  document.querySelector('#forma-auto button[type=submit]').click();
  await new Promise(r=>setTimeout(r,500));
  const fs=document.querySelectorAll('#forma-auto fieldset'); fs[5].scrollIntoView({block:'start'}); window.scrollBy(0,-20);
  return 1;`);
await dormir(500);
await foto('05_autoevaluacion');

// 6. Asistente abierto en modo de preguntas frecuentes
await tam(1280, 860);
await ir('#/modulo/m7');
await js(`
  document.querySelector('#md h2:nth-of-type(3)').scrollIntoView({block:'start'});
  document.getElementById('asistente-boton').click();
  await new Promise(r=>setTimeout(r,1200));
  document.getElementById('asistente-entrada').value='¿Por qué no debo darle mi clave de API al agente?';
  document.getElementById('asistente-forma').requestSubmit();
  await new Promise(r=>setTimeout(r,900));
  return 1;`);
await foto('06_asistente');

// 7. Vista en celular
await tam(390, 844, true);
await ir('#/modulo/m7');
await foto('07_movil');

ws.close();
edge.kill();
await dormir(500);
rmSync(PERFIL, { recursive: true, force: true });
console.log('listo');

