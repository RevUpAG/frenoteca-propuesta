# Frenoteca — Propuesta de sitio web

Propuesta comercial y demostración navegable del nuevo sitio web de
**Frenoteca S.A.S.** (Medellín, Colombia), preparada por Rev Up Agency Group.

### ▶ Ver en vivo

**https://revupag.github.io/frenoteca-propuesta/**

Ese es el enlace para enviarle al cliente. Abre en la propuesta; el botón
«Sí, quiero ver mi página» lleva al sitio terminado, y desde el pie del sitio
hay un enlace de vuelta. Pensado para abrirse desde el celular.

---

## Qué contiene

| Ruta | Qué es |
|---|---|
| `index.html` | La **propuesta**: hallazgos, lo que vamos a construir, cómo funciona la medición, antes/después, proceso de 3–4 semanas y cierre con el CTA. |
| `sitio/index.html` | El **sitio terminado**: hero, servicios, por qué Frenoteca, pasos, marcas y blindados, galería del taller, reseñas, agenda, cómo llegar y preguntas frecuentes. |
| `sitio/<servicio>/` | **Una página por servicio** (pastillas, discos, campanas y zapatas, cilindros, mangueras, taller y suspensión) más **marcas** y **blindados**, cada una con título único y WhatsApp con código propio (`WEB-PAS`, `WEB-DIS`…). |
| `herramientas/generar.py` | Genera todas las páginas. **Los textos se editan aquí** y luego: `python3 herramientas/generar.py`. |
| `assets/css/brand.css` | Sistema de marca (color, tipografía, botones). |
| `assets/js/app.js` | Menú, «abierto ahora», agenda → WhatsApp, mapa bajo demanda, carrusel. Sin librerías. |

## Branding

Todo se extrajo de `frenoteca.com`; nada se inventó.

- **Color** — hoja de estilos del tema «frenoteca»: rojo `#d41111` (cabecera, pie y títulos),
  negro `#000`, blanco, `#f3f3f3`, `#6a6a6a`, `#333a4d`, y el verde `#43c358` de su botón de WhatsApp (reservado).
- **Tipografía** — **Didact Gothic** (títulos y texto) y **Abel** (etiquetas), las dos que carga el sitio actual.
  Alojadas en el propio sitio (WOFF2, ≈ 21 KB). Solo existen en peso regular, así que la jerarquía se hace
  con tamaño, mayúsculas y color, como en el sitio original.
- **Logo** — el PNG original del sitio (366 × 99 px, transparente), sin modificar, sobre el mismo rojo que lo usa hoy.
- **Fotos** — las del taller y de productos publicadas en su web, convertidas a WebP.

## Datos a confirmar con el cliente

- Años de experiencia: la web dice 35 y 37 en distintas páginas; aquí se usa «más de 35».
- Razón social: el logo dice «Y CIA LTDA.» y Google/propuesta «S.A.S.»; se conserva el logo tal cual.
- Textos de señales, «qué incluye» y preguntas frecuentes de cada servicio: redactados por nosotros, a validar.
- Las reseñas se enlazan a Google (4,6 ★ · 360); no se muestran textos de reseñas inventados.
- El horario «abierto ahora» no contempla festivos.

## Vista previa local

```bash
python3 -m http.server 4175
```
