# Frenoteca — Sitio web

Nuevo sitio web de **Frenoteca S.A.S.** (Medellín, Colombia), por Rev Up Agency Group.

### ▶ Ver en vivo

**https://revupag.github.io/frenoteca-propuesta/**

Pensado primero para el celular y para público mayor: trato de «usted», letra de 18 px,
botones grandes con texto, pocas secciones.

---

## Qué contiene

| Ruta | Qué es |
|---|---|
| `index.html` | **Inicio**: logo grande, Llamar y WhatsApp, «¿Qué necesita?», por qué Frenoteca, pedir cita, fotos del taller, opiniones, preguntas frecuentes y cómo llegar. |
| `<servicio>/` | **Una página por servicio** (pastillas, discos, campanas y zapatas, cilindros, mangueras, taller y suspensión) más **marcas** y **blindados**, cada una con título único y WhatsApp con código propio (`WEB-PAS`, `WEB-DIS`…). |
| `herramientas/generar.py` | Genera todas las páginas. **Los textos se editan aquí** y luego: `python3 herramientas/generar.py`. |
| `assets/css/brand.css` · `sitio.css` | Sistema de marca y estilos del sitio. |
| `assets/js/app.js` | Menú, «abierto ahora», cita → WhatsApp, mapa bajo demanda, fotos ampliables. Sin librerías. |

## Branding

Todo se extrajo de `frenoteca.com`; nada se inventó.

- **Color** — hoja de estilos del tema «frenoteca»: rojo `#d41111` (cabecera, pie y títulos),
  negro `#000`, blanco, `#f3f3f3`, `#6a6a6a`, `#333a4d`, y el verde `#43c358` de su botón de WhatsApp (reservado).
- **Tipografía** — **Didact Gothic** (títulos y texto) y **Abel** (etiquetas), las dos que carga el sitio actual.
  Alojadas en el propio sitio (WOFF2, ≈ 21 KB). Solo existen en peso regular, así que la jerarquía se hace
  con tamaño, mayúsculas y color, como en el sitio original.
- **Logo** — el sitio solo lo publica en PNG de 366 × 99 px. Se vectorizó trazando ese mismo archivo (sin redibujarlo): `assets/img/logo-frenoteca.svg`, con el negro de la F y la A y el blanco de RENOTEC y las líneas, superpuesto al original para comprobar que calza. Se usa sobre el mismo rojo de su web.
- **Fotos** — las del taller y de productos publicadas en su web, convertidas a WebP.

## Datos a confirmar con el cliente

- Años de experiencia: la web dice 35 y 37 en distintas páginas; aquí se usa «más de 35».
- Razón social: el logo dice «Y CIA LTDA.» y Google «S.A.S.»; se conserva el logo tal cual.
- Textos de señales, «qué incluye» y preguntas frecuentes de cada servicio: redactados por nosotros, a validar.
- Las reseñas se enlazan a Google (4,6 ★ · 360); no se muestran textos de reseñas inventados.
- El horario «abierto ahora» no contempla festivos.
