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
| `index.html` | **Inicio**: llamar al fijo y WhatsApp, «¿Qué necesita?», por qué Frenoteca, cotización por WhatsApp, fotos del taller, opiniones, preguntas frecuentes y cómo llegar. |
| `<servicio>/` | **Una página por servicio** (pastillas, discos, campanas y zapatas, cilindros, mangueras) más **frenos para carros blindados** y **marcas**, cada una con título único y WhatsApp con código propio (`WEB-PAS`, `WEB-DIS`…). |
| `herramientas/generar.py` | Genera todas las páginas. **Los textos se editan aquí** y luego: `python3 herramientas/generar.py`. |
| `assets/css/brand.css` · `sitio.css` | Sistema de marca y estilos del sitio. |
| `assets/js/app.js` | Menú, «abierto ahora», cotización → WhatsApp, mapa bajo demanda, fotos ampliables y el Mustang que sigue el cursor (solo con mouse). Sin librerías. |

## Branding

Logo, color y fotos del cliente; nada se inventó.

- **Color** — rojo `#c52b2d`, tomado del logo nuevo (`LOGO FRENOTECA.ai`); antes se usaba el `#d41111` de la web vieja. Además negro `#000`, blanco, `#f3f3f3`, `#6a6a6a`, `#333a4d`, y el verde oficial de WhatsApp `#25d366` en sus botones. El rojo no varía en ningún estado (tampoco al pasar el mouse).
- **Tipografía** — **Bitter** en todo el sitio: serif de remate clásico, afín al logo y muy legible en pantalla. Alojada en el propio sitio (WOFF2 variable, ≈ 34 KB).
- **Logo** — el logo nuevo de Frenoteca (`LOGO FRENOTECA.ai`, entregado por el cliente). Los trazos vectoriales del archivo se convirtieron a SVG sin redibujar (`assets/img/logo-frenoteca.svg`, blanco para fondos rojos) y se comprobó superponiéndolos al original. El ícono de la pestaña y la imagen para compartir salen de las mesas de trabajo del mismo archivo.
- **Fotos** — las del taller son las publicadas en su web. Las de cada servicio (`assets/img/servicios/`) son fotos de estudio generadas con IA (Seedream 5 Pro, sin logos de marcas), aprobadas por Rev Up el 7 de octubre de 2026.

## Datos a confirmar con el cliente

- Años de experiencia: «más de 40 años en el mercado», según el cliente.
- Textos de señales, «qué incluye» y preguntas frecuentes de cada servicio: redactados por nosotros, a validar.
- Las reseñas se enlazan a Google (4,6 ★ · 360); no se muestran textos de reseñas inventados.
- El horario «abierto ahora» no contempla festivos.
- Contacto: todas las llamadas van al fijo (604) 448 2194; el celular 312 833 4755 se usa solo para WhatsApp.
- Horario: lunes a viernes 8:00 a. m. – 5:00 p. m. y sábados 8:00 a. m. – 1:00 p. m., jornada continua. No se reservan citas: se atiende en orden de llegada.
- Tono: profesional y claro; nunca hablar de precio bajo, «barato» o «económico».
