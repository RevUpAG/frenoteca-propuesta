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

  /* ---------- Mustang clásico rojo, visto desde arriba, que persigue el cursor (solo con mouse) ---------- */
  // El cursor normal se conserva; el carro gira hacia donde va y lo sigue. Se apaga en pantallas táctiles y con «reducir movimiento».
  if (matchMedia('(hover: hover) and (pointer: fine)').matches && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const car = document.createElement('div');
    car.className = 'mustang'; car.setAttribute('aria-hidden', 'true');
    // Vista cenital mirando a la derecha (viewBox 60 × 30): capó largo adelante, techo fastback atrás, franjas de carrera
    car.innerHTML = `<svg viewBox="0 0 60 30">`
      + `<rect x="3.5" y="5.5" width="55" height="22" rx="7" fill="rgba(0,0,0,.25)"/>`                    // sombra
      + `<rect x="9" y="1.6" width="8" height="3.4" rx="1.2" fill="#151515"/><rect x="41" y="1.6" width="8" height="3.4" rx="1.2" fill="#151515"/>`
      + `<rect x="9" y="25" width="8" height="3.4" rx="1.2" fill="#151515"/><rect x="41" y="25" width="8" height="3.4" rx="1.2" fill="#151515"/>`  // llantas
      + `<path fill="#c52b2d" d="M8 3.6H46Q55 3.6 57.5 9Q58.6 15 57.5 21Q55 26.4 46 26.4H8Q2.4 26.4 2 21V9Q2.4 3.6 8 3.6Z"/>`  // carrocería
      + `<path d="M3 12.6H57.4M3 17.4H57.4" stroke="#fff" stroke-width="2"/>`                              // franjas de carrera
      + `<path fill="#1d1d1f" d="M33 6.4Q36 15 33 23.6L37.6 22.2Q39.4 15 37.6 7.8Z"/>`                         // parabrisas
      + `<path fill="#1d1d1f" d="M11.5 7.6Q9.6 15 11.5 22.4L16.4 21.4Q15.2 15 16.4 8.6Z"/>`                   // vidrio trasero (fastback)
      + `<path fill="#1d1d1f" d="M18 5.4H31.5L30.6 6.6H18.8ZM18 24.6H31.5L30.6 23.4H18.8Z"/>`                 // ventanas laterales
      + `<rect x="55.4" y="5.6" width="2.2" height="3.6" rx="1" fill="#fff3c4"/><rect x="55.4" y="20.8" width="2.2" height="3.6" rx="1" fill="#fff3c4"/>`  // farolas
      + `<rect x="2" y="5.8" width="1.6" height="3.4" rx=".6" fill="#2a0708"/><rect x="2" y="20.8" width="1.6" height="3.4" rx=".6" fill="#2a0708"/>`      // stops
      + `<rect x="30" y="1.8" width="2.6" height="2" rx=".8" fill="#c52b2d"/><rect x="30" y="26.2" width="2.6" height="2" rx=".8" fill="#c52b2d"/>`      // espejos
      + `</svg>`;
    document.body.append(car);
    let mx = 0, my = 0, x = 0, y = 0, vx = 0, vy = 0, rumbo = 0, humo = 0, prev = 0, activo = false;
    addEventListener('mousemove', (e) => {
      mx = e.clientX; my = e.clientY;
      if (!activo) { activo = true; x = mx - 40; y = my; car.classList.add('is-on'); }
    }, { passive: true });
    document.documentElement.addEventListener('mouseleave', () => { activo = false; car.classList.remove('is-on'); });

    // Bocanada de humo que sale por detrás y se disipa en sentido contrario a la marcha
    const humito = (fuerte) => {
      const p = document.createElement('span'); p.className = 'humo';
      const t = 6 + Math.random() * 6, c = Math.cos(rumbo), s = Math.sin(rumbo);
      p.style.cssText = `left:${x - c * 29}px;top:${y - s * 29}px;width:${t}px;height:${t}px`;
      document.body.append(p);
      const d = 14 + Math.random() * 14 + (fuerte ? 18 : 0), lado = (Math.random() - .5) * 14;
      p.animate([
        { transform: 'translate(-50%, -50%) scale(.4)', opacity: fuerte ? .7 : .45 },
        { transform: `translate(calc(-50% + ${-c * d - s * lado}px), calc(-50% + ${-s * d + c * lado}px)) scale(${1.8 + Math.random() * 1.2})`, opacity: 0 },
      ], { duration: 900 + Math.random() * 600, easing: 'cubic-bezier(.22, 1, .36, 1)' }).onfinish = () => p.remove();
    };

    const mover = (t) => {
      const dt = Math.min((t - prev) / 16.67 || 1, 3); prev = t;      // movimiento igual a 60 o 120 Hz
      const dx = mx - x, dy = my - y, dist = Math.hypot(dx, dy);
      // Gira hacia el cursor por el camino más corto (sin dar vueltas de más)
      if (dist > 38) {
        let giro = Math.atan2(dy, dx) - rumbo;
        giro = Math.atan2(Math.sin(giro), Math.cos(giro));
        rumbo += giro * Math.min(1, 0.12 * dt);
      }
      // Resorte amortiguado hacia un punto detrás del cursor: arranca y frena suave
      const tx = mx - Math.cos(rumbo) * 36, ty = my - Math.sin(rumbo) * 36;
      vx += (tx - x) * 0.014 * dt; vy += (ty - y) * 0.014 * dt;
      const roce = Math.pow(0.86, dt); vx *= roce; vy *= roce;
      x += vx * dt; y += vy * dt;
      const vel = Math.hypot(vx, vy);
      humo -= dt;
      if (activo && humo <= 0) { const fuerte = vel > 1.5; humito(fuerte); humo = fuerte ? 4 : 24; }  // más humo al acelerar
      car.style.transform = `translate(${x - 28}px, ${y - 14}px) rotate(${rumbo}rad)`;
      requestAnimationFrame(mover);
    };
    requestAnimationFrame(mover);
  }
})();
