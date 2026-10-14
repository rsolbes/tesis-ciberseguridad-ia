// Progreso del estudiante y motor de gamificación.
// Todo se guarda en el navegador (localStorage) y nunca sale de él.
// Si el navegador bloquea el almacenamiento, el sitio sigue funcionando en memoria.
const Almacen = (() => {
  const CLAVE = 'guia-agentes-ia-v2';
  
  const RANGOS = [
    { nivel: 1, minXP: 0, maxXP: 150, titulo: 'Recluta Digital', icono: '🛡️' },
    { nivel: 2, minXP: 151, maxXP: 400, titulo: 'Operador de Red', icono: '💻' },
    { nivel: 3, minXP: 401, maxXP: 800, titulo: 'Analista de Triaje', icono: '🔍' },
    { nivel: 4, minXP: 801, maxXP: 1300, titulo: 'Guardián de Agentes', icono: '⚡' },
    { nivel: 5, minXP: 1301, maxXP: 99999, titulo: 'Comandante de Ciberdefensa', icono: '🏆' },
  ];

  const inicial = () => ({
    ruta: null,
    aceptoReglas: false,
    modulos: {},
    asistente: {},
    xp: 0,
    sonido: true,
    minijuegos: {}
  });

  let memoria = inicial();

  function leer() {
    try {
      const txt = localStorage.getItem(CLAVE);
      if (txt) memoria = Object.assign(inicial(), JSON.parse(txt));
    } catch (e) { /* almacenamiento no disponible */ }
    return memoria;
  }

  function guardar() {
    try { localStorage.setItem(CLAVE, JSON.stringify(memoria)); } catch (e) { /* sin persistencia */ }
  }

  function modulo(id) {
    if (!memoria.modulos[id]) memoria.modulos[id] = { leido: false, puntaje: null, insignia: false, xpGanado: 0 };
    return memoria.modulos[id];
  }

  function rangoActual(xp) {
    const r = RANGOS.find((x) => xp >= x.minXP && xp <= x.maxXP) || RANGOS[RANGOS.length - 1];
    const prevMin = r.minXP;
    const nextMax = r.maxXP === 99999 ? r.minXP + 500 : r.maxXP;
    const progreso = Math.min(100, Math.max(0, Math.round(((xp - prevMin) / (nextMax - prevMin)) * 100)));
    return {
      nivel: r.nivel,
      titulo: r.titulo,
      icono: r.icono,
      xpActual: xp,
      sigNivelXP: nextMax,
      progresoPct: progreso
    };
  }

  return {
    get: () => memoria,
    cargar: leer,
    ruta: () => memoria.ruta,
    fijarRuta(r) { memoria.ruta = r; guardar(); },
    aceptarReglas() { memoria.aceptoReglas = true; guardar(); },
    modulo,
    actualizarModulo(id, cambios) { Object.assign(modulo(id), cambios); guardar(); },
    asistente: () => memoria.asistente,
    fijarAsistente(cfg) { memoria.asistente = cfg; guardar(); },
    codigoAcceso: () => (memoria.asistente && memoria.asistente.codigoAcceso) || '',
    fijarCodigoAcceso(codigo) {
      memoria.asistente = memoria.asistente || {};
      memoria.asistente.codigoAcceso = (codigo || '').trim();
      guardar();
    },
    sonidoHabilitado: () => memoria.sonido !== false,
    conmutarSonido() { memoria.sonido = !memoria.sonido; guardar(); return memoria.sonido; },
    obtenerXP: () => memoria.xp || 0,
    obtenerRango: () => rangoActual(memoria.xp || 0),
    sumarXP(puntos, motivo) {
      const anterior = rangoActual(memoria.xp || 0);
      memoria.xp = (memoria.xp || 0) + puntos;
      const nuevo = rangoActual(memoria.xp);
      guardar();
      const subioNivel = nuevo.nivel > anterior.nivel;
      return { total: memoria.xp, ganados: puntos, motivo, subioNivel, nuevoRango: nuevo };
    },
    haCompletadoMinijuego: (id) => !!(memoria.minijuegos && memoria.minijuegos[id]),
    marcarMinijuego: (id) => {
      memoria.minijuegos = memoria.minijuegos || {};
      memoria.minijuegos[id] = true;
      guardar();
    },
    reiniciar() { memoria = inicial(); guardar(); },
  };
})();
Almacen.cargar();
