// Aplicación de la guía. Navegación por hash (#/...), sin servidor ni cuentas.
(() => {
  const app = document.getElementById('app');
  const cache = {};

  async function obtener(ruta, json = false) {
    if (cache[ruta]) return cache[ruta];
    const r = await fetch(ruta, { cache: 'no-cache' });
    if (!r.ok) throw new Error(`No se pudo cargar ${ruta}`);
    cache[ruta] = json ? await r.json() : await r.text();
    return cache[ruta];
  }

  const h = (html) => { app.innerHTML = html; app.focus?.(); window.scrollTo(0, 0); };
  const esc = Markdown.esc;

  const EJES = {
    todos: { nombre: 'Punto de partida', clase: 'eje-0' },
    A: { nombre: 'Eje A · Fundamentos de ciberseguridad', clase: 'eje-a' },
    B: { nombre: 'Eje B · Agentes de IA para la defensa', clase: 'eje-b' },
    C: { nombre: 'Eje C · Seguridad y gobernanza de los agentes', clase: 'eje-c' },
  };
  const nombreRuta = (r) => (r === 'avanzada' ? 'Ruta avanzada' : r === 'basica' ? 'Ruta básica' : 'Sin ruta elegida');

  function pintarRutaChip() {
    const chip = document.getElementById('ruta-chip');
    const r = Almacen.ruta();
    chip.hidden = !r;
    chip.textContent = nombreRuta(r);
    chip.className = `ruta-chip ruta-${r || 'ninguna'}`;
  }

  // ---------------- páginas ----------------
  async function inicio() {
    const mods = await obtener('contenido/modulos.json', true);
    const r = Almacen.ruta();
    const hechos = mods.filter((m) => Almacen.modulo(m.id).insignia).length;
    h(`
      <section class="portada">
        <p class="antetitulo">Guía didáctica interactiva</p>
        <h1>Agentes de IA y ciberseguridad</h1>
        <p class="entrada">Aprende qué son los agentes de inteligencia artificial, cómo ayudan a defender sistemas,
          cómo pueden ser usados para atacar y cómo se protegen. La guía tiene dos rutas, una para estudiantes de
          bachillerato tecnológico y otra para estudiantes de ingeniería, y la eliges tú.</p>
        <div class="acciones">
          ${r ? `<a class="boton" href="#/mapa">Continuar con la ${nombreRuta(r).toLowerCase()}</a>
                 <a class="boton secundario" href="#/modulo/m0">Volver al punto de partida</a>`
              : `<a class="boton" href="#/modulo/m0">Empezar en el punto de partida</a>
                 <a class="boton secundario" href="#/mapa">Ver el mapa de la guía</a>`}
        </div>
        ${hechos ? `<p class="progreso-texto">Has obtenido ${hechos} insignia${hechos > 1 ? 's' : ''}. <a href="#/insignias">Ver insignias</a></p>` : ''}
      </section>
      <section class="tarjetas tres">
        <article class="tarjeta"><h2>Dos rutas</h2><p>La ruta básica construye los conceptos desde cero con ejemplos y retos. La avanzada valida rápido lo que ya sabes y profundiza en la construcción y la evaluación de agentes.</p></article>
        <article class="tarjeta"><h2>Laboratorios seguros</h2><p>Las prácticas usan modelos que corren en tu computadora, datos inventados y permisos de solo lectura. Nunca se practica contra sistemas reales.</p></article>
        <article class="tarjeta"><h2>Un asistente que responde</h2><p>En cada módulo puedes preguntarle al asistente. Responde con base en el módulo, te dice dónde profundizar y te avisa que puede equivocarse.</p></article>
      </section>`);
  }

  async function mapa() {
    const mods = await obtener('contenido/modulos.json', true);
    const r = Almacen.ruta();
    const grupos = {};
    mods.forEach((m) => { (grupos[m.eje] = grupos[m.eje] || []).push(m); });
    const total = mods.reduce((s, m) => s + (r ? m.horas[r] : 0), 0);
    h(`
      <h1>Mapa de la guía</h1>
      <p class="entrada">${r ? `Vas en la <strong>${nombreRuta(r).toLowerCase()}</strong>, con una duración sugerida de ${total} horas.`
                            : 'Todavía no eliges ruta. Empieza en el punto de partida para que la guía te recomiende una.'}
        Explora los módulos a continuación para seguir la secuencia formativa o consulta cualquier módulo de tu interés.</p>
      ${Object.entries(grupos).map(([eje, lista]) => `
        <section class="eje ${EJES[eje].clase}">
          <h2>${EJES[eje].nombre}</h2>
          <div class="tarjetas">
            ${lista.map((m) => {
              const p = Almacen.modulo(m.id);
              const disponible = m.estado === 'disponible';
              const estado = p.insignia ? '✓ Completado' : p.leido ? 'En progreso' : disponible ? 'Disponible' : 'Próximamente';
              return `<article class="tarjeta modulo ${disponible ? '' : 'inactivo'}">
                <p class="modulo-clave">${esc(m.clave)}</p>
                <h3>${disponible ? `<a href="#/modulo/${m.id}">${esc(m.titulo)}</a>` : esc(m.titulo)}</h3>
                <p>${esc(m.resumen)}</p>
                <p class="meta"><span>${estado}</span><span>${r ? m.horas[r] + ' h' : m.horas.basica + ' h / ' + m.horas.avanzada + ' h'}</span></p>
              </article>`;
            }).join('')}
          </div>
        </section>`).join('')}`);
  }

  async function modulo(id) {
    const mods = await obtener('contenido/modulos.json', true);
    const m = mods.find((x) => x.id === id);
    if (!m) return noEncontrado();
    if (m.estado !== 'disponible') {
      Asistente.fijarModulo({ id: null, titulo: '', texto: '', faq: [] });
      return h(`<h1>${esc(m.clave)}. ${esc(m.titulo)}</h1><p class="entrada">${esc(m.resumen)}</p>
        <p>Este módulo todavía no está disponible en el prototipo.</p><a class="boton" href="#/mapa">Volver al mapa</a>`);
    }
    const md = await obtener(`contenido/${m.archivo}`);
    const faq = m.faq ? await obtener(`contenido/${m.faq}`, true) : [];
    const r = Almacen.ruta();
    Asistente.fijarModulo({ id: m.id, titulo: `${m.clave}. ${m.titulo}`, texto: Markdown.aTexto(md), faq });

    h(`
      <nav class="migas" aria-label="Ruta de navegación"><a href="#/mapa">Mapa</a> › ${esc(m.clave)}</nav>
      <article class="modulo-cuerpo ${EJES[m.eje].clase}">
        <div class="modulo-barra">
          <span class="etiqueta">${EJES[m.eje].nombre}</span>
          <span class="etiqueta">${r ? m.horas[r] + ' h en tu ruta' : 'Elige una ruta en el punto de partida'}</span>
          ${r ? `<label class="interruptor"><input type="checkbox" id="ver-todo"> Mostrar también el contenido de la otra ruta</label>` : ''}
        </div>
        <div id="md">${Markdown.aHtml(md)}</div>
        <div id="extra"></div>
      </article>`);

    aplicarRuta(false);
    const ver = document.getElementById('ver-todo');
    if (ver) ver.addEventListener('change', () => aplicarRuta(ver.checked));
    protegerLaboratorios();

    // Recompensa de XP por explorar el módulo por primera vez
    if (!Almacen.modulo(m.id).leido) {
      const res = Almacen.sumarXP(30, `Módulo iniciado: ${m.clave}`);
      Juego.mostrarNotificacionXP(res.ganados, res.motivo, res.subioNivel, res.nuevoRango);
    }
    Almacen.actualizarModulo(m.id, { leido: true });

    const extra = document.getElementById('extra');
    if (m.diagnostico) await diagnostico(extra, await obtener(`contenido/${m.diagnostico}`, true));

    // Minijuegos interactivos embebidos
    if (m.id === 'm2' && Almacen.get().aceptoReglas) {
      const secJuego = document.createElement('section');
      secJuego.className = 'caja';
      secJuego.innerHTML = '<h2>Minijuego táctico · Simulador de Cortafuegos</h2><p>Pon a prueba tus reflejos filtrando paquetes de red conforme a la política de seguridad.</p><div id="contenedor-minijuego-fw"></div>';
      extra.appendChild(secJuego);
      Juego.iniciarMinijuegoCortafuegos(document.getElementById('contenedor-minijuego-fw'));
    }
    if (m.id === 'm7' && Almacen.get().aceptoReglas) {
      const secJuego = document.createElement('section');
      secJuego.className = 'caja';
      secJuego.innerHTML = '<h2>Laboratorio interactivo en el navegador · Engaña al Guardián</h2><p>Experimenta con la inyección directa e indirecta contra un agente simulado y prueba el modo blindado con filtros de salida.</p><div id="contenedor-minijuego-pi"></div>';
      extra.appendChild(secJuego);
      Juego.iniciarMinijuegoPromptInjection(document.getElementById('contenedor-minijuego-pi'));
    }

    if (m.autoevaluacion) await autoevaluacion(extra, m, await obtener(`contenido/${m.autoevaluacion}`, true));
  }

  function aplicarRuta(verTodo) {
    const r = Almacen.ruta();
    document.querySelectorAll('#md .bloque[data-ruta]').forEach((b) => {
      const dr = b.dataset.ruta;
      b.hidden = !verTodo && r && dr !== 'ambas' && dr !== r;
    });
  }

  // Los laboratorios solo se muestran después de aceptar las reglas de uso ético (M0).
  function protegerLaboratorios() {
    if (Almacen.get().aceptoReglas) return;
    document.querySelectorAll('#md .bloque-laboratorio').forEach((b) => {
      b.innerHTML = `<p class="bloque-titulo">Laboratorio bloqueado</p>
        <p>Para ver las instrucciones y los archivos de los laboratorios primero debes leer y aceptar las
        <a href="#/modulo/m0">reglas de uso ético</a> en el punto de partida.</p>`;
    });
  }

  // ---------- M0 · autoevaluación de entrada ----------
  async function diagnostico(cont, d) {
    const r = Almacen.ruta();
    cont.insertAdjacentHTML('beforeend', `
      <section class="caja" id="diagnostico">
        <h2>Autoevaluación de entrada</h2>
        <p>${esc(d.indicacion)}</p>
        <form id="forma-diag">
          ${d.preguntas.map((p, i) => `
            <fieldset class="pregunta"><legend>${i + 1}. ${esc(p.texto)}</legend>
              ${p.opciones.map((o, j) => `<label><input type="radio" name="d${i}" value="${j}" required> ${esc(o.texto)}</label>`).join('')}
            </fieldset>`).join('')}
          <button class="boton" type="submit">Ver mi recomendación</button>
        </form>
        <div id="diag-resultado" aria-live="polite"></div>
      </section>
      <section class="caja" id="reglas">
        <h2>Reglas de uso ético</h2>
        <p>Las técnicas de esta guía pueden usarse para defender o para atacar. Por eso, antes de los laboratorios, necesitas aceptar estas reglas.</p>
        <ol>${d.reglas.map((x) => `<li>${esc(x)}</li>`).join('')}</ol>
        ${Almacen.get().aceptoReglas
          ? '<p class="exito">✓ Ya aceptaste las reglas. Los laboratorios están desbloqueados.</p>'
          : `<label class="acepto"><input type="checkbox" id="acepto"> Leí las reglas y me comprometo a cumplirlas</label>
             <button class="boton" id="btn-acepto" disabled>Aceptar y desbloquear los laboratorios</button>`}
      </section>`);

    document.getElementById('forma-diag').addEventListener('submit', (ev) => {
      ev.preventDefault();
      const fd = new FormData(ev.target);
      let puntos = 0;
      const consejos = [];
      d.preguntas.forEach((p, i) => {
        const o = p.opciones[Number(fd.get(`d${i}`))];
        puntos += o.puntos || 0;
        if (o.consejo) consejos.push(o.consejo);
      });
      const rec = puntos >= d.umbral ? 'avanzada' : 'basica';
      document.getElementById('diag-resultado').innerHTML = `
        <div class="resultado">
          <p>Obtuviste <strong>${puntos} de ${d.maximo}</strong> puntos. Te recomendamos la <strong>${nombreRuta(rec).toLowerCase()}</strong>.
          ${rec === 'avanzada' ? 'Podrás acreditar rápido los módulos de fundamentos y dedicar más tiempo a los agentes.' : 'Construirás los conceptos paso a paso, con ejemplos y retos.'}
          Puedes elegir la otra ruta si lo prefieres y cambiarla cuando quieras.</p>
          ${consejos.length ? `<p><strong>Consejos para empezar desde hoy</strong></p><ul>${consejos.map((c) => `<li>${esc(c)}</li>`).join('')}</ul>` : ''}
          <div class="acciones">
            <button class="boton" data-ruta="${rec}">Elegir la ${nombreRuta(rec).toLowerCase()}</button>
            <button class="boton secundario" data-ruta="${rec === 'avanzada' ? 'basica' : 'avanzada'}">Prefiero la ${nombreRuta(rec === 'avanzada' ? 'basica' : 'avanzada').toLowerCase()}</button>
          </div>
        </div>`;
      document.querySelectorAll('#diag-resultado [data-ruta]').forEach((b) => b.addEventListener('click', () => {
        Almacen.fijarRuta(b.dataset.ruta);
        pintarRutaChip();
        document.getElementById('diag-resultado').insertAdjacentHTML('beforeend',
          `<p class="exito">✓ Elegiste la ${nombreRuta(b.dataset.ruta).toLowerCase()}. Acepta las reglas de uso ético y continúa en el <a href="#/mapa">mapa de la guía</a>.</p>`);
      }));
    });

    const chk = document.getElementById('acepto');
    if (chk) {
      const btn = document.getElementById('btn-acepto');
      chk.addEventListener('change', () => { btn.disabled = !chk.checked; });
      btn.addEventListener('click', () => {
        Almacen.aceptarReglas();
        Almacen.actualizarModulo('m0', { insignia: true });
        const res = Almacen.sumarXP(50, 'Compromiso ético aceptado');
        Juego.mostrarNotificacionXP(res.ganados, res.motivo, res.subioNivel, res.nuevoRango);
        Juego.lanzarConfeti();
        Juego.reproducirSonido('victoria');
        document.getElementById('reglas').insertAdjacentHTML('beforeend', '<p class="exito">✓ Reglas aceptadas. Obtuviste la insignia «Compromiso ético» y +50 XP.</p>');
        btn.remove(); chk.parentElement.remove();
      });
    }
    if (r) document.getElementById('diag-resultado').innerHTML = `<p class="nota-suave">Ya elegiste la ${nombreRuta(r).toLowerCase()}. Puedes repetir la autoevaluación si quieres cambiarla.</p>`;
  }

  // ---------- autoevaluación del módulo ----------
  async function autoevaluacion(cont, m, a) {
    const r = Almacen.ruta() || 'basica';
    const preguntas = a.preguntas.filter((p) => p.ruta === 'ambas' || p.ruta === r);
    const previo = Almacen.modulo(m.id);
    cont.insertAdjacentHTML('beforeend', `
      <section class="caja" id="autoevaluacion">
        <h2>Autoevaluación · ${esc(nombreRuta(r))}</h2>
        <p>Responde las ${preguntas.length} preguntas. Con ${Math.round(a.aprobatorio * 100)} % o más obtienes la insignia «${esc(a.insignia.nombre)}».
          Cada respuesta incluye una explicación para que aprendas también de los errores.</p>
        ${previo.puntaje != null ? `<p class="nota-suave">Tu mejor resultado hasta ahora es ${previo.puntaje} %.</p>` : ''}
        <form id="forma-auto">
          ${preguntas.map((p, i) => `
            <fieldset class="pregunta" data-i="${i}"><legend>${i + 1}. ${esc(p.texto)}</legend>
              ${p.opciones.map((o, j) => `<label><input type="radio" name="p${i}" value="${j}" required> ${esc(o)}</label>`).join('')}
              <p class="retro" hidden></p>
            </fieldset>`).join('')}
          <button class="boton" type="submit">Revisar mis respuestas</button>
        </form>
        <div id="auto-resultado" aria-live="polite"></div>
      </section>`);

    document.getElementById('forma-auto').addEventListener('submit', (ev) => {
      ev.preventDefault();
      const fd = new FormData(ev.target);
      let bien = 0;
      preguntas.forEach((p, i) => {
        const elegida = Number(fd.get(`p${i}`));
        const ok = elegida === p.correcta;
        if (ok) bien++;
        const fs = ev.target.querySelector(`fieldset[data-i="${i}"]`);
        fs.classList.toggle('correcta', ok);
        fs.classList.toggle('incorrecta', !ok);
        const retro = fs.querySelector('.retro');
        retro.hidden = false;
        retro.textContent = (ok ? '✓ Correcto. ' : `✗ La respuesta correcta es «${p.opciones[p.correcta]}». `) + p.explicacion;
      });
      const pct = Math.round((bien / preguntas.length) * 100);
      const gano = pct >= a.aprobatorio * 100;
      const mejor = Math.max(pct, previo.puntaje || 0);
      const previoGano = previo.insignia;
      Almacen.actualizarModulo(m.id, { puntaje: mejor, insignia: previo.insignia || gano });

      if (bien > 0) {
        const resAciertos = Almacen.sumarXP(bien * 15, `${bien} aciertos en autoevaluación`);
        Juego.mostrarNotificacionXP(resAciertos.ganados, resAciertos.motivo, resAciertos.subioNivel, resAciertos.nuevoRango);
      }
      if (gano && !previoGano) {
        setTimeout(() => {
          const resIns = Almacen.sumarXP(100, `¡Insignia ${a.insignia.nombre}!`);
          Juego.mostrarNotificacionXP(resIns.ganados, resIns.motivo, resIns.subioNivel, resIns.nuevoRango);
          Juego.lanzarConfeti();
          Juego.reproducirSonido('victoria');
        }, 500);
      }

      document.getElementById('auto-resultado').innerHTML = gano
        ? `<div class="resultado exito-caja"><p class="insignia-grande" aria-hidden="true">${esc(a.insignia.icono)}</p>
            <p><strong>¡Obtuviste la insignia «${esc(a.insignia.nombre)}»!</strong> Acertaste ${bien} de ${preguntas.length} (${pct} %).</p>
            <p>${esc(a.insignia.descripcion)}</p><a class="boton" href="#/insignias">Ver mis logros</a></div>`
        : `<div class="resultado"><p>Acertaste ${bien} de ${preguntas.length} (${pct} %). Revisa las explicaciones, vuelve a las secciones del módulo o pregúntale al asistente, y vuelve a intentarlo.</p></div>`;
      document.getElementById('auto-resultado').scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  }

  async function insignias() {
    const mods = await obtener('contenido/modulos.json', true);
    const lista = [];
    for (const m of mods) {
      if (!m.insignia) continue;
      lista.push({ m, gano: Almacen.modulo(m.id).insignia });
    }
    const r = Almacen.obtenerRango();
    const xp = Almacen.obtenerXP();
    const totalInsignias = lista.filter(x => x.gano).length;

    h(`
      <h1>Mis logros y rango</h1>
      <p class="entrada">Tu experiencia y nivel se calculan a partir de tus lecturas, laboratorios e insignias obtenidas.</p>
      
      <section class="logros-resumen">
        <div class="logros-medalla" aria-hidden="true">${r.icono}</div>
        <div class="logros-detalles">
          <h2>${r.titulo} (Nivel ${r.nivel})</h2>
          <p>Tienes acumulados <strong>${xp} XP</strong>. ${r.nivel === 5 ? '¡Alcanzaste el rango máximo de ciberdefensa!' : `Faltan <strong>${Math.max(0, r.sigNivelXP - xp)} XP</strong> para el siguiente rango.`}</p>
          <div class="logros-barra" aria-label="Progreso hacia el siguiente nivel">
            <div class="logros-fill" style="width: ${r.progresoPct}%"></div>
          </div>
          <small>${totalInsignias} de ${lista.length} insignias desbloqueadas</small>
        </div>
      </section>

      <h2>Insignias de ciberdefensa</h2>
      <div class="tarjetas">${lista.map(({ m, gano }) => `
        <article class="tarjeta insignia ${gano ? 'ganada' : ''}">
          <p class="insignia-icono" aria-hidden="true">${gano ? esc(m.insignia.icono) : '🔒'}</p>
          <h2>${esc(m.insignia.nombre)}</h2>
          <p>${gano ? esc(m.insignia.descripcion) : `Se obtiene en ${esc(m.clave)}. ${esc(m.titulo)}.`}</p>
        </article>`).join('')}</div>
      <div class="acciones" style="margin-top:24px;">
        <button class="boton secundario" id="reiniciar">Reiniciar mi progreso</button>
      </div>`);
    document.getElementById('reiniciar').addEventListener('click', () => {
      if (confirm('¿Seguro que quieres borrar tu ruta, tus insignias, XP y resultados?')) {
        Almacen.reiniciar();
        pintarRutaChip();
        Juego.actualizarHUD();
        insignias();
      }
    });
  }

  // ---------- configuración del asistente ----------
  async function configuracion() {
    const c = Asistente.config();
    Asistente.fijarModulo({ id: null, titulo: '', texto: '', faq: [] });
    h(`
      <h1>Configuración del asistente</h1>
      <p class="entrada">El asistente puede usar un modelo que corre en tu computadora o en el laboratorio (Ollama), o el servicio Gemini.
        Si no hay ningún modelo disponible, responde con las preguntas frecuentes del módulo.</p>
      <form id="forma-cfg" class="caja">
        <fieldset class="pregunta"><legend>Modo de conexión</legend>
          ${[['auto', 'Automático (intenta Ollama, luego Gemini y, si no hay ninguno, preguntas frecuentes)'],
             ['ollama', 'Ollama, modelo local (recomendado para estudiantes)'],
             ['intermediario', 'Gemini mediante intermediario (prototipo publicado)'],
             ['gemini', 'Gemini directo con clave en este navegador (solo pruebas del autor)'],
             ['sin-conexion', 'Sin modelo, solo preguntas frecuentes']]
            .map(([v, t]) => `<label><input type="radio" name="modo" value="${v}" ${c.modo === v ? 'checked' : ''}> ${t}</label>`).join('')}
        </fieldset>
        <div class="campos">
          <label>Dirección de Ollama <input name="ollamaUrl" value="${esc(c.ollamaUrl)}" placeholder="http://localhost:11434"></label>
          <label>Modelo de Ollama <select name="ollamaModelo" id="sel-ollama"><option value="${esc(c.ollamaModelo)}">${esc(c.ollamaModelo || 'Primero busca los modelos')}</option></select></label>
          <button class="boton secundario" type="button" id="buscar-ollama">Buscar modelos de Ollama</button>
          <label>Dirección del intermediario <input name="intermediarioUrl" value="${esc(c.intermediarioUrl)}" placeholder="https://tu-intermediario.workers.dev"></label>
          <label>Clave de la API de Gemini <input name="geminiClave" type="password" autocomplete="off" value="${esc(c.geminiClave)}" placeholder="Solo para pruebas en tu propia computadora"></label>
          <label>Modelo de Gemini <select name="geminiModelo" id="sel-gemini"><option value="${esc(c.geminiModelo)}">${esc(c.geminiModelo || 'Primero busca los modelos')}</option></select></label>
          <button class="boton secundario" type="button" id="buscar-gemini">Buscar modelos de Gemini</button>
        </div>
        <p class="aviso">La clave de Gemini se guarda solo en este navegador. No la uses en computadoras compartidas ni la publiques en el código del sitio;
          para un sitio publicado usa el intermediario. Los términos de Gemini prohíben su uso en aplicaciones dirigidas a menores de 18 años,
          por lo que con estudiantes de bachillerato debe usarse Ollama.</p>
        <div class="acciones"><button class="boton" type="submit">Guardar</button><button class="boton secundario" type="button" id="probar">Probar conexión</button></div>
        <p id="cfg-estado" aria-live="polite"></p>
      </form>`);

    const forma = document.getElementById('forma-cfg');
    const estado = document.getElementById('cfg-estado');
    const leerForma = () => Object.fromEntries(new FormData(forma).entries());
    const llenar = (sel, modelos, actual) => {
      sel.innerHTML = modelos.map((n) => `<option value="${esc(n)}" ${n === actual ? 'selected' : ''}>${esc(n)}</option>`).join('');
    };

    document.getElementById('buscar-ollama').addEventListener('click', async () => {
      estado.textContent = 'Buscando modelos en Ollama…';
      try {
        const cfg = leerForma();
        const modelos = await Asistente.proveedores.ollamaModelos(cfg);
        if (!modelos.length) { estado.textContent = 'Ollama respondió, pero no tiene modelos. Descarga uno ligero (consulta la Ayuda).'; return; }
        llenar(document.getElementById('sel-ollama'), modelos, cfg.ollamaModelo);
        estado.textContent = `Se encontraron ${modelos.length} modelos en Ollama.`;
      } catch (e) { estado.textContent = 'No se encontró Ollama en esa dirección. Revisa que esté abierto y que permita conexiones de este sitio (consulta la Ayuda).'; }
    });
    document.getElementById('buscar-gemini').addEventListener('click', async () => {
      estado.textContent = 'Consultando los modelos de Gemini…';
      try {
        const cfg = leerForma();
        const modelos = await Asistente.proveedores.geminiModelos(cfg);
        const pref = modelos.find((n) => /flash-lite/i.test(n)) || modelos[0];
        llenar(document.getElementById('sel-gemini'), modelos, cfg.geminiModelo || pref);
        estado.textContent = `Se encontraron ${modelos.length} modelos Flash. Se recomienda uno «flash-lite».`;
      } catch (e) { estado.textContent = `No se pudo consultar Gemini (${e.message}). Revisa la clave.`; }
    });
    forma.addEventListener('submit', (ev) => {
      ev.preventDefault();
      Almacen.fijarAsistente(Object.assign({}, Asistente.config(), leerForma()));
      estado.textContent = '✓ Configuración guardada.';
      Asistente.actualizarEstado();
    });
    document.getElementById('probar').addEventListener('click', async () => {
      Almacen.fijarAsistente(Object.assign({}, Asistente.config(), leerForma()));
      const est = await Asistente.actualizarEstado();
      estado.textContent = `Modo en uso: ${est.etiqueta}.`;
    });
  }

  async function ayuda() {
    Asistente.fijarModulo({ id: null, titulo: '', texto: '', faq: [] });
    h(`<article class="modulo-cuerpo">${Markdown.aHtml(await obtener('contenido/ayuda.md'))}</article>`);
  }

  function noEncontrado() { h('<h1>Página no encontrada</h1><p><a href="#/">Volver al inicio</a></p>'); }

  // ---------------- enrutador ----------------
  async function enrutar() {
    const partes = (location.hash.replace(/^#\/?/, '') || '').split('/');
    document.getElementById('menu').classList.remove('abierto');
    try {
      if (!partes[0]) await inicio();
      else if (partes[0] === 'mapa') await mapa();
      else if (partes[0] === 'modulo') await modulo(partes[1]);
      else if (partes[0] === 'insignias') await insignias();
      else if (partes[0] === 'configuracion') await configuracion();
      else if (partes[0] === 'ayuda') await ayuda();
      else noEncontrado();
    } catch (e) {
      h(`<h1>No se pudo cargar la página</h1><p>${esc(e.message)}.</p>
         <p>Si abriste el archivo directamente, necesitas servir la carpeta con un servidor local. Consulta el archivo LEEME.md.</p>`);
    }
    document.querySelectorAll('#menu a').forEach((a) => a.classList.toggle('actual', a.getAttribute('href') === `#/${partes[0] || ''}`));
    Juego.actualizarHUD();
  }

  document.getElementById('menu-boton').addEventListener('click', (ev) => {
    const menu = document.getElementById('menu');
    menu.classList.toggle('abierto');
    ev.currentTarget.setAttribute('aria-expanded', String(menu.classList.contains('abierto')));
  });
  window.addEventListener('hashchange', enrutar);
  Asistente.iniciar();
  Asistente.fijarModulo({ id: null, titulo: '', texto: '', faq: [] });
  pintarRutaChip();
  Juego.actualizarHUD();
  enrutar();
})();
