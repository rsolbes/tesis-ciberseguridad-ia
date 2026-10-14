// Conversor de Markdown mínimo y seguro.
// Todo el texto se escapa antes de darle formato, de modo que ningún contenido
// (ni el de los módulos ni el que genera el asistente) puede inyectar HTML o scripts.
const Markdown = (() => {
  const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
                      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');

  function enLinea(texto) {
    let t = esc(texto);
    t = t.replace(/`([^`]+)`/g, '<code>$1</code>');
    t = t.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    t = t.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    // Enlaces: solo se permiten https, rutas internas (#/) y archivos del propio sitio.
    t = t.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (m, txt, url) => {
      const u = url.replace(/&amp;/g, '&');
      const externo = /^https:\/\//i.test(u);
      const interno = /^#\//.test(u) || /^[\w./-]+$/.test(u);
      if (!externo && !interno) return txt;
      const attrs = externo ? ' target="_blank" rel="noopener noreferrer"'
                            : /^laboratorios\//.test(u) ? ' download' : '';
      return `<a href="${esc(u)}"${attrs}>${txt}</a>`;
    });
    return t;
  }

  // Bloques especiales: :::avanzada, :::basica, :::nota, :::alerta, :::laboratorio
  const ETIQUETAS = {
    avanzada: 'Profundización · ruta avanzada',
    basica: 'Para la ruta básica',
    nota: 'Nota',
    alerta: 'Cuidado',
    laboratorio: 'Laboratorio',
    ejemplo: 'Ejemplo',
  };

  function aHtml(md) {
    const lineas = md.replace(/\r/g, '').split('\n');
    const out = [];
    let i = 0;
    let lista = null;
    const cerrarLista = () => { if (lista) { out.push(`</${lista}>`); lista = null; } };

    while (i < lineas.length) {
      const l = lineas[i];

      if (/^```/.test(l)) {                       // bloque de código
        cerrarLista();
        const buf = [];
        i++;
        while (i < lineas.length && !/^```/.test(lineas[i])) buf.push(lineas[i++]);
        out.push(`<pre><code>${esc(buf.join('\n'))}</code></pre>`);
        i++; continue;
      }
      // :::tipo[ruta] Título opcional   (ruta = basica | avanzada)
      const bloque = l.match(/^:::(\w+)(?:\[(basica|avanzada)\])?\s*(.*)$/);
      if (bloque) {                               // bloque especial
        cerrarLista();
        const tipo = bloque[1];
        const rutaBloque = bloque[2] || (tipo === 'avanzada' || tipo === 'basica' ? tipo : 'ambas');
        const titulo = bloque[3] || ETIQUETAS[tipo] || '';
        const buf = [];
        i++;
        while (i < lineas.length && !/^:::\s*$/.test(lineas[i])) buf.push(lineas[i++]);
        i++;
        out.push(`<section class="bloque bloque-${esc(tipo)}" data-ruta="${rutaBloque}">` +
                 (titulo ? `<p class="bloque-titulo">${enLinea(titulo)}</p>` : '') + aHtml(buf.join('\n')) + '</section>');
        continue;
      }
      if (/^\|.*\|\s*$/.test(l)) {                // tabla
        cerrarLista();
        const filas = [];
        while (i < lineas.length && /^\|.*\|\s*$/.test(lineas[i])) filas.push(lineas[i++]);
        const celdas = (f) => f.trim().slice(1, -1).split('|').map((c) => c.trim());
        const cab = celdas(filas[0]);
        const cuerpo = filas.slice(2).map(celdas);
        out.push('<div class="tabla-envoltura"><table><thead><tr>' + cab.map((c) => `<th>${enLinea(c)}</th>`).join('') +
                 '</tr></thead><tbody>' + cuerpo.map((r) => '<tr>' + r.map((c) => `<td>${enLinea(c)}</td>`).join('') + '</tr>').join('') +
                 '</tbody></table></div>');
        continue;
      }
      const h = l.match(/^(#{1,4})\s+(.*)$/);
      if (h) {
        cerrarLista();
        const n = h[1].length;
        const id = h[2].toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^\w]+/g, '-').replace(/^-|-$/g, '');
        out.push(`<h${n} id="${id}">${enLinea(h[2])}</h${n}>`);
        i++; continue;
      }
      const li = l.match(/^\s*(-|\d+\.)\s+(.*)$/);
      if (li) {
        const tipo = li[1] === '-' ? 'ul' : 'ol';
        if (lista !== tipo) { cerrarLista(); out.push(`<${tipo}>`); lista = tipo; }
        out.push(`<li>${enLinea(li[2])}</li>`);
        i++; continue;
      }
      if (/^>\s?/.test(l)) {
        cerrarLista();
        const buf = [];
        while (i < lineas.length && /^>\s?/.test(lineas[i])) buf.push(lineas[i++].replace(/^>\s?/, ''));
        out.push(`<blockquote>${aHtml(buf.join('\n'))}</blockquote>`);
        continue;
      }
      if (!l.trim()) { cerrarLista(); i++; continue; }
      cerrarLista();
      const buf = [l];
      i++;
      while (i < lineas.length && lineas[i].trim() && !/^(#|```|:::|\||\s*-\s|\s*\d+\.\s|>)/.test(lineas[i])) buf.push(lineas[i++]);
      out.push(`<p>${enLinea(buf.join(' '))}</p>`);
    }
    cerrarLista();
    return out.join('\n');
  }

  // Versión en texto plano del módulo, para dársela como contexto al asistente.
  function aTexto(md) {
    return md.replace(/```[\s\S]*?```/g, ' ')
             .replace(/^:::(\w+)(?:\[\w+\])?\s*(.*)$/gm, (m, t, tit) => `[${ETIQUETAS[t] || t}${tit ? ' · ' + tit : ''}]`)
             .replace(/^:::\s*$/gm, '')
             .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
             .replace(/[*`#>|]/g, '')
             .replace(/\n{3,}/g, '\n\n').trim();
  }

  return { aHtml, aTexto, esc, enLinea };
})();
