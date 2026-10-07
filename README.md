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

- **Color** — rojo `#c52b2d`, tomado del logo nuevo (`LOGO FRENOTECA.ai`); antes se usaba el `#d41111` de la web vieja. Además negro `#000`, blanco, `#f3f3f3`, `#6a6a6a`, `#333a4d`, y el verde `#43c358` de su botón de WhatsApp.
- **Tipografía** — **Didact Gothic** (títulos y texto) y **Abel** (etiquetas), las dos que carga el sitio actual.
  Alojadas en el propio sitio (WOFF2, ≈ 21 KB). Solo existen en peso regular, así que la jerarquía se hace
  con tamaño, mayúsculas y color, como en el sitio original.
- **Logo** — el logo nuevo de Frenoteca (`LOGO FRENOTECA.ai`, entregado por el cliente). Los trazos vectoriales del archivo se convirtieron a SVG sin redibujar (`assets/img/logo-frenoteca.svg`, blanco para fondos rojos) y se comprobó superponiéndolos al original. El ícono de la pestaña y la imagen para compartir salen de las mesas de trabajo del mismo archivo.
- **Fotos** — las del taller y de productos publicadas en su web, convertidas a WebP.

## Datos a confirmar con el cliente

- Años de experiencia: la web dice 35 y 37 en distintas páginas; aquí se usa «más de 35».
- Textos de señales, «qué incluye» y preguntas frecuentes de cada servicio: redactados por nosotros, a validar.
- Las reseñas se enlazan a Google (4,6 ★ · 360); no se muestran textos de reseñas inventados.
- El horario «abierto ahora» no contempla festivos.
