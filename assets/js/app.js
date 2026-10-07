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

  /* ---------- Horario: "abierto ahora" en hora de Medellín ---------- */
  // ponytail: no contempla festivos; si hace falta, añadir una lista de fechas cerradas.
  const HORARIO = { 1: [480, 1020], 2: [480, 1020], 3: [480, 1020], 4: [480, 1020], 5: [480, 1020], 6: [480, 780] }; // L-V 8:00-17:00, sáb 8:00-13:00
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
      $('[value="tarde"]', form).disabled = sab;
      if (sab) franja.value = 'mañana';
    };
    fecha.addEventListener('change', actualizarFranja);

    form.addEventListener('submit', (ev) => {
      ev.preventDefault();
      err.textContent = '';
      $$('[aria-invalid]', form).forEach((el) => el.removeAttribute('aria-invalid'));
      const bad = $$('input:not([type="radio"]), select', form).find((el) => !el.checkValidity());
      if (bad) { bad.setAttribute('aria-invalid', 'true'); err.textContent = 'Por favor complete: ' + $(`label[for="${bad.id}"]`, form).textContent.trim(); bad.focus(); return; }
      if (diaDe(fecha.value) === 0) { fecha.setAttribute('aria-invalid', 'true'); err.textContent = 'Los domingos está cerrado. Escoja de lunes a sábado.'; fecha.focus(); return; }
      if (fecha.value < hoyISO) { fecha.setAttribute('aria-invalid', 'true'); err.textContent = 'Escoja hoy o un día después.'; fecha.focus(); return; }
      const f = form.elements;
      const dia = new Intl.DateTimeFormat('es-CO', { weekday: 'long', day: 'numeric', month: 'long' }).format(new Date(fecha.value + 'T12:00:00'));
      const msg = `Hola Frenoteca, quisiera una cotización y saber su disponibilidad.\n\n• Nombre: ${f.nombre.value.trim()}\n• Servicio: ${f.servicio.value}\n• Pienso ir: ${dia}, en la ${f.franja.value}\n\n(Ref: WEB-COT-${form.dataset.code})`;
      window.open(`https://wa.me/${form.dataset.wa}?text=${encodeURIComponent(msg)}`, '_blank', 'noopener');
    });
  });

  /* ---------- Mapa: se carga solo al pedirlo (la página abre más rápido) ---------- */
  $$('[data-map]').forEach((box) => {
    $('.map-btn', box).addEventListener('click', () => {
      box.innerHTML = `<iframe src="${box.dataset.map}" title="Mapa de Frenoteca en Google Maps" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>`;
    });
  });

  /* ---------- Galería: ampliar foto ---------- */
  const lb = $('.lightbox');
  if (lb && lb.showModal) {
    const fotos = $$('.gal-item'), img = $('img', lb);
    let i = 0;
    const ver = (n) => { i = (n + fotos.length) % fotos.length; img.src = fotos[i].dataset.full; img.alt = $('img', fotos[i]).alt; };
    fotos.forEach((b, n) => b.addEventListener('click', () => { ver(n); lb.showModal(); }));
    $$('[data-gal-open]').forEach((b) => b.addEventListener('click', () => { ver(0); lb.showModal(); }));
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

  /* ---------- Mustang clásico rojo que persigue el cursor (solo con mouse) ---------- */
  // El cursor normal se conserva; el carro corre detrás. Se apaga en pantallas táctiles y con «reducir movimiento».
  if (matchMedia('(hover: hover) and (pointer: fine)').matches && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    // Mustang fastback 1967 de perfil, mirando a la derecha (viewBox 120 × 46)
    const rueda = (cx) => {
      const rayos = [0, 72, 144, 216, 288].map((g) => { const r = g * Math.PI / 180; return `M${cx} 32L${(cx + 4.6 * Math.sin(r)).toFixed(2)} ${(32 - 4.6 * Math.cos(r)).toFixed(2)}`; }).join('');
      return `<g class="rueda" style="transform-origin:${cx}px 32px"><circle cx="${cx}" cy="32" r="8.6" fill="#111"/><circle cx="${cx}" cy="32" r="5.4" fill="#d9d9d9"/><path d="${rayos}" stroke="#8a8a8a" stroke-width="1.5" stroke-linecap="round"/><circle cx="${cx}" cy="32" r="1.5" fill="#444"/></g>`;
    };
    const car = document.createElement('div');
    car.className = 'mustang'; car.setAttribute('aria-hidden', 'true');
    car.innerHTML = `<svg viewBox="0 0 120 46"><ellipse cx="61" cy="42.6" rx="51" ry="2.4" fill="rgba(0,0,0,.22)"/>`
      // carrocería: cola corta con alerón, techo fastback, capó largo y nariz de tiburón
      + `<path fill="#c52b2d" d="M7 32.5L5 27L5.5 22Q6 20 9 19.5L13 19L40 9Q43 7.8 47 7.8L58 7.8Q61 8 63 9.5L73 17.5L104 18.6Q110 19 114 20.5L117.5 22L116.3 25.2L117.4 29.5Q117.4 32.5 114 32.5L101 32.5A11 11 0 0 0 79 32.5L40 32.5A11 11 0 0 0 18 32.5L9 32.5Z"/>`
      // ventanas con pilar central y rejillas en el pilar trasero
      + `<path fill="#1d1d1f" d="M33 13.3L40.5 10.1Q43 9.3 46.5 9.3L48.4 9.3L48.4 17.4L33 17.4ZM50.2 9.3L57.5 9.3Q60 9.4 61.5 10.6L69 17.4L50.2 17.4Z"/>`
      + `<path d="M24.5 16.6L26.5 15.8M27.6 16.6L29.6 15.1M30.7 16.6L32.4 14.3" stroke="#1d1d1f" stroke-width="1.1" stroke-linecap="round"/>`
      // toma de aire lateral, franja GT, parrilla con faro, calavera y bompers cromados
      + `<path fill="#1d1d1f" d="M40.5 22.4L48.5 21.2L48.5 24.6L42.5 24.6Z"/>`
      + `<path d="M8 29.4H115" stroke="#fff" stroke-width="1.4"/>`
      + `<path fill="#1d1d1f" d="M113.6 21.6L117.3 22.1L116.2 25.2L117.2 28.2L113.6 28.2Z"/><circle cx="115.2" cy="24.6" r="1.5" fill="#fff3c4"/>`
      + `<rect x="5.2" y="21.6" width="2.8" height="3" rx=".7" fill="#2a0708"/><rect x="3.2" y="28.6" width="6.2" height="2" rx="1" fill="#e2e2e2"/><rect x="112.6" y="28.8" width="6.4" height="2" rx="1" fill="#e2e2e2"/>`
      + `<rect x="1.4" y="30.6" width="6" height="1.6" rx=".8" fill="#8d8d8d"/>`  // tubo de escape
      + rueda(29) + rueda(90) + `</svg>`;
    document.body.append(car);
    const ruedas = car.querySelectorAll('.rueda');
    let mx = 0, my = 0, x = 0, y = 0, vx = 0, vy = 0, dir = 1, sx = 1, ang = 0, giro = 0, humo = 0, prev = 0, activo = false;
    addEventListener('mousemove', (e) => {
      mx = e.clientX; my = e.clientY;
      if (!activo) { activo = true; x = mx - 46; y = my + 22; car.classList.add('is-on'); }
    }, { passive: true });
    document.documentElement.addEventListener('mouseleave', () => { activo = false; car.classList.remove('is-on'); });

    // Bocanada de humo que sale del exhosto y se disipa hacia atrás y hacia arriba
    const humito = (fuerte) => {
      const p = document.createElement('span'); p.className = 'humo';
      const t = 7 + Math.random() * 6;
      p.style.cssText = `left:${x - sx * 40}px;top:${y + 6}px;width:${t}px;height:${t}px`;
      document.body.append(p);
      const atras = -dir * (12 + Math.random() * 14 + (fuerte ? 22 : 0)), sube = 8 + Math.random() * 14;
      p.animate([
        { transform: 'translate(-50%, -50%) scale(.4)', opacity: fuerte ? .7 : .45 },
        { transform: `translate(calc(-50% + ${atras}px), calc(-50% - ${sube}px)) scale(${1.8 + Math.random() * 1.2})`, opacity: 0 },
      ], { duration: 900 + Math.random() * 600, easing: 'cubic-bezier(.22, 1, .36, 1)' }).onfinish = () => p.remove();
    };

    const mover = (t) => {
      const dt = Math.min((t - prev) / 16.67 || 1, 3); prev = t;      // movimiento igual a 60 o 120 Hz
      // Da la vuelta cuando el cursor cruza al otro lado del carro (con margen para que no titubee)
      if (dir === 1 && mx < x - 24) dir = -1; else if (dir === -1 && mx > x + 24) dir = 1;
      // Resorte amortiguado: arranca y frena suave, siempre detrás del cursor y un poco más abajo
      vx += (mx - dir * 46 - x) * 0.014 * dt; vy += (my + 22 - y) * 0.014 * dt;
      const roce = Math.pow(0.86, dt); vx *= roce; vy *= roce;
      x += vx * dt; y += vy * dt;
      sx += (dir - sx) * Math.min(1, 0.16 * dt);                         // el giro se ve como una vuelta, no un salto
      ang += (Math.max(-12, Math.min(12, Math.atan2(vy, Math.abs(vx) + .6) * 57.3)) - ang) * Math.min(1, 0.1 * dt);
      const vel = Math.hypot(vx, vy);
      giro += vel * 7 * dt;                                               // las ruedas giran con la distancia recorrida
      humo -= dt;
      if (activo && humo <= 0) { const fuerte = vel > 1.5; humito(fuerte); humo = fuerte ? 4 : 24; }  // más humo al acelerar
      car.style.transform = `translate(${x - 42}px, ${y - 16}px) scaleX(${sx}) rotate(${ang}deg)`;
      ruedas.forEach((r) => { r.style.transform = `rotate(${giro}deg)`; });
      requestAnimationFrame(mover);
    };
    requestAnimationFrame(mover);
  }
})();
