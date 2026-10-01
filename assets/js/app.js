/* Frenoteca · interacciones de la propuesta y del sitio. Sin librerías. */
(() => {
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];

  /* ---------- Revelado al hacer scroll ---------- */
  const reveals = $$('.reveal');
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    reveals.forEach((el) => io.observe(el));
  } else reveals.forEach((el) => el.classList.add('is-in'));

  /* ---------- Cabecera y menú ---------- */
  const header = $('.site-header');
  if (header) addEventListener('scroll', () => header.classList.toggle('is-scrolled', scrollY > 8), { passive: true });

  const menuBtn = $('.menu-btn');
  const setMenu = (open) => {
    document.body.classList.toggle('menu-open', open);
    menuBtn.setAttribute('aria-expanded', open);
    menuBtn.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
  };
  if (menuBtn) {
    menuBtn.addEventListener('click', () => setMenu(!document.body.classList.contains('menu-open')));
    $$('#menu a').forEach((a) => a.addEventListener('click', () => setMenu(false)));
    addEventListener('keydown', (e) => { if (e.key === 'Escape' && document.body.classList.contains('menu-open')) { setMenu(false); menuBtn.focus(); } });
  }
  $$('.nav-sub-btn').forEach((b) => b.addEventListener('click', () => b.setAttribute('aria-expanded', b.getAttribute('aria-expanded') !== 'true')));

  /* ---------- Horario: "abierto ahora" en hora de Medellín ---------- */
  // ponytail: no contempla festivos; si hace falta, añadir una lista de fechas cerradas.
  const HORARIO = { 1: [480, 1035], 2: [480, 1035], 3: [480, 1035], 4: [480, 1035], 5: [480, 1035], 6: [480, 795] };
  const DIAS = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'];
  const hora = (m) => { const h = Math.floor(m / 60), mm = String(m % 60).padStart(2, '0'); return `${h > 12 ? h - 12 : h}:${mm} ${h < 12 ? 'a. m.' : 'p. m.'}`; };
  const ahoraBogota = () => {
    const p = Object.fromEntries(new Intl.DateTimeFormat('en-US', { timeZone: 'America/Bogota', weekday: 'short', hour: 'numeric', minute: 'numeric', hourCycle: 'h23' })
      .formatToParts(new Date()).map((x) => [x.type, x.value]));
    return { dia: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(p.weekday), min: +p.hour * 60 + +p.minute };
  };
  const estado = ({ dia, min }) => {
    const hoy = HORARIO[dia];
    if (hoy && min >= hoy[0] && min < hoy[1]) return { open: true, txt: `Abierto ahora · cierra a las ${hora(hoy[1])}` };
    if (hoy && min < hoy[0]) return { open: false, txt: `Cerrado · abre hoy a las ${hora(hoy[0])}` };
    for (let i = 1; i <= 7; i++) {
      const d = (dia + i) % 7;
      if (HORARIO[d]) return { open: false, txt: `Cerrado · abre ${i === 1 ? 'mañana' : 'el ' + DIAS[d]} a las ${hora(HORARIO[d][0])}` };
    }
  };
  const e = estado(ahoraBogota());
  $$('[data-abierto]').forEach((el) => { el.classList.add(e.open ? 'is-open' : 'is-closed'); $('[data-abierto-txt]', el).textContent = e.txt; });

  /* ---------- Agenda → WhatsApp ---------- */
  $$('[data-agenda]').forEach((form) => {
    const fecha = form.elements.fecha, franja = form.elements.franja, err = $('.form-error', form);
    const hoyISO = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Bogota' }).format(new Date());
    fecha.min = hoyISO;
    const diaDe = (iso) => new Date(iso + 'T12:00:00').getDay();
    const actualizarFranja = () => {
      const sab = fecha.value && diaDe(fecha.value) === 6;
      franja.querySelector('[value="tarde"]').disabled = sab;
      if (sab) franja.value = 'mañana';
    };
    fecha.addEventListener('change', actualizarFranja);

    form.addEventListener('submit', (ev) => {
      ev.preventDefault();
      err.textContent = '';
      $$('[aria-invalid]', form).forEach((el) => el.removeAttribute('aria-invalid'));
      const bad = $$('input, select', form).find((el) => !el.checkValidity());
      if (bad) { bad.setAttribute('aria-invalid', 'true'); err.textContent = 'Completa el campo «' + $(`label[for="${bad.id}"]`, form).firstChild.textContent.trim() + '».'; bad.focus(); return; }
      if (diaDe(fecha.value) === 0) { fecha.setAttribute('aria-invalid', 'true'); err.textContent = 'Los domingos está cerrado. Elige de lunes a sábado.'; fecha.focus(); return; }
      if (fecha.value < hoyISO) { fecha.setAttribute('aria-invalid', 'true'); err.textContent = 'Elige hoy o un día posterior.'; fecha.focus(); return; }
      const f = form.elements;
      const dia = new Intl.DateTimeFormat('es-CO', { weekday: 'long', day: 'numeric', month: 'long' }).format(new Date(fecha.value + 'T12:00:00'));
      const msg = `Hola Frenoteca, quiero agendar una revisión.\n\n• Nombre: ${f.nombre.value.trim()}\n• Vehículo: ${f.vehiculo.value.trim()}\n• Servicio: ${f.servicio.value}\n• Día: ${dia}, en la ${f.franja.value}\n\n(Ref: WEB-AGENDA-${form.dataset.code})`;
      window.open(`https://wa.me/${form.dataset.wa}?text=${encodeURIComponent(msg)}`, '_blank', 'noopener');
    });
  });

  /* ---------- Mapa: se carga solo al pedirlo (la página abre más rápido) ---------- */
  $$('[data-map]').forEach((box) => {
    $('.map-btn', box).addEventListener('click', () => {
      box.innerHTML = `<iframe src="${box.dataset.map}" title="Mapa de Frenoteca en Google Maps" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>`;
    });
  });

  /* ---------- Carrusel de la galería (flechas en escritorio) ---------- */
  const car = $('[data-carousel]');
  $$('[data-car]').forEach((b) => b.addEventListener('click', () => {
    car.scrollBy({ left: (+b.dataset.car) * car.clientWidth * 0.8, behavior: 'smooth' });
  }));

  /* ---------- Galería: ampliar foto ---------- */
  const lb = $('.lightbox');
  if (lb && lb.showModal) {
    const fotos = $$('.gal-item'), img = $('img', lb);
    let i = 0;
    const ver = (n) => { i = (n + fotos.length) % fotos.length; img.src = fotos[i].dataset.full; img.alt = $('img', fotos[i]).alt; };
    fotos.forEach((b, n) => b.addEventListener('click', () => { ver(n); lb.showModal(); }));
    $('.lb-close', lb).addEventListener('click', () => lb.close());
    $('.lb-prev', lb).addEventListener('click', () => ver(i - 1));
    $('.lb-next', lb).addEventListener('click', () => ver(i + 1));
    lb.addEventListener('click', (e) => { if (e.target === lb) lb.close(); });
    lb.addEventListener('keydown', (e) => { if (e.key === 'ArrowLeft') ver(i - 1); if (e.key === 'ArrowRight') ver(i + 1); });
    let x0 = null;
    lb.addEventListener('touchstart', (e) => { x0 = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', (e) => { if (x0 === null) return; const dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 50) ver(i + (dx < 0 ? 1 : -1)); x0 = null; });
  }

  /* ---------- WhatsApp flotante: muestra el mensaje un momento tras unos segundos ---------- */
  const waf = $('.wa-float');
  if (waf) {
    setTimeout(() => { waf.classList.add('is-hint'); setTimeout(() => waf.classList.remove('is-hint'), 6000); }, 4000);
  }

  /* ---------- Carruseles: puntos y flechas sobre el scroll-snap nativo ---------- */
  $$('[data-slider]').forEach((sl) => {
    const track = $('.slides', sl), slides = $$('.slide', sl), dots = $('.dots', sl);
    const prev = $('.sl-prev', sl), next = $('.sl-next', sl);
    const paso = () => slides[0].offsetWidth + parseFloat(getComputedStyle(track).columnGap || 0);
    const btns = slides.map((_, i) => {
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'dot'; b.setAttribute('aria-label', `Ir a ${i + 1} de ${slides.length}`);
      b.addEventListener('click', () => track.scrollTo({ left: i * paso(), behavior: 'smooth' }));
      dots.append(b); return b;
    });
    const upd = () => {
      const max = track.scrollWidth - track.clientWidth;
      sl.classList.toggle('no-scroll', max < 4);
      const i = track.scrollLeft >= max - 4 ? slides.length - 1 : Math.round(track.scrollLeft / paso());
      btns.forEach((b, n) => b.classList.toggle('is-active', n === i));
      prev.disabled = track.scrollLeft < 4; next.disabled = track.scrollLeft >= max - 4;
    };
    prev.addEventListener('click', () => track.scrollBy({ left: -paso(), behavior: 'smooth' }));
    next.addEventListener('click', () => track.scrollBy({ left: paso(), behavior: 'smooth' }));
    track.addEventListener('scroll', () => requestAnimationFrame(upd), { passive: true });
    addEventListener('resize', upd);
    upd();
  });

  /* ---------- Pestañas accesibles ---------- */
  $$('[data-tabs]').forEach((tb) => {
    const tabsEl = $$('[role="tab"]', tb);
    const activar = (t, foco) => {
      tabsEl.forEach((x) => {
        const on = x === t;
        x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1;
        document.getElementById(x.getAttribute('aria-controls')).hidden = !on;
      });
      if (foco) t.focus();
      t.scrollIntoView({ block: 'nearest', inline: 'nearest', behavior: 'smooth' });
      // los carruseles dentro de un panel recién visible necesitan recalcular
      dispatchEvent(new Event('resize'));
    };
    tabsEl.forEach((t, i) => {
      t.addEventListener('click', () => activar(t));
      t.addEventListener('keydown', (e) => {
        const d = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
        if (d) { e.preventDefault(); activar(tabsEl[(i + d + tabsEl.length) % tabsEl.length], true); }
      });
    });
  });

  /* ---------- Propuesta: barra de secciones marca dónde va el lector ---------- */
  const pnav = $('[data-pnav]');
  if (pnav && 'IntersectionObserver' in window) {
    const links = $$('a', pnav);
    const io2 = new IntersectionObserver((es) => es.forEach((e) => {
      if (!e.isIntersecting) return;
      links.forEach((l) => {
        const on = l.hash === '#' + e.target.id;
        l.classList.toggle('is-active', on);
        if (on) pnav.firstElementChild.scrollTo({ left: l.offsetLeft - 16, behavior: 'smooth' });
      });
    }), { rootMargin: '-40% 0px -55% 0px' });
    links.forEach((l) => io2.observe($(l.hash)));
  }

  /* ---------- Propuesta: el sitio en vivo dentro del marco de celular ---------- */
  if ('ResizeObserver' in window) {
    const ro = new ResizeObserver((es) => es.forEach((e) => e.target.style.setProperty('--k', e.contentRect.width / 390)));
    $$('.p-screen').forEach((el) => ro.observe(el));
  }

  /* ---------- Propuesta: CTA fijo tras pasar el hero, oculto en el cierre ---------- */
  const sticky = $('[data-sticky]');
  if (sticky && 'IntersectionObserver' in window) {
    const hero = $('.p-hero'), fin = $('.p-final');
    let heroVisible = true, finVisible = false;
    const upd = () => sticky.classList.toggle('is-on', !heroVisible && !finVisible);
    new IntersectionObserver(([x]) => { heroVisible = x.isIntersecting; upd(); }).observe(hero);
    new IntersectionObserver(([x]) => { finVisible = x.isIntersecting; upd(); }).observe(fin);
  }
})();
