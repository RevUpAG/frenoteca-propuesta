"""Genera el sitio de Frenoteca: inicio (index.html) y una página por servicio (<servicio>/index.html).

Uso:  python3 herramientas/generar.py
Todo el contenido vive aquí; cabecera, pie e iconos son comunes a todas las páginas.
"""
import json, os, time
from urllib.parse import quote

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = time.strftime("%Y%m%d%H%M")  # versión para romper la caché de CSS/JS

# ---------------------------------------------------------------- Datos del negocio
WA = "573128334755"
CEL = "312 833 4755"
TEL = "(604) 448 2194"
TEL_HREF = "tel:+576044482194"
CEL_HREF = "tel:+573128334755"
EMAIL = "frenoteca@hotmail.com"
DIR = "Carrera 50 # 39-87, Medellín, Antioquia"
MAPS = "https://www.google.com/maps/search/?api=1&query=" + quote("Frenoteca S.A.S Carrera 50 39-87 Medellín")
WAZE = "https://waze.com/ul?ll=6.240469,-75.571513&navigate=yes"
RESENAS = MAPS
MAPA_EMBED = ("https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d1983.0881946436834!2d-75.571513!3d6.240469"
              "!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x447979612f651610!2sFRENOTECA%20S.A.S!5e0!3m2!1ses!2sco!4v1599831261457!5m2!1ses!2sco")


def wa(servicio=None, code="INI"):
    """Enlace de WhatsApp con mensaje según el servicio y código de origen (para medir)."""
    txt = f"Hola Frenoteca, quisiera una cotización de {servicio}." if servicio else "Hola Frenoteca, quisiera información sobre sus servicios."
    return f"https://wa.me/{WA}?text=" + quote(f"{txt} (Ref: WEB-{code})")


# Tono: profesional y claro, trato de «usted». Nunca hablar de precio bajo, «barato» o «económico».
SERVICIOS = [
    dict(slug="pastillas", nombre="Pastillas de freno", msg="pastillas de freno", code="PAS", img="pastillas", icon="pad",
         title="Pastillas de freno en Medellín: Brembo, Bosch, ATE e Incolbestos",
         intro="Pastillas de freno Brembo, Bosch, Incolbestos, ATE e importadas, con formulaciones especiales para vehículos blindados.",
         senales_t="¿Cuándo revisarlas?",
         senales=["Chillido o ruido metálico al frenar", "Mayor distancia para detener el vehículo", "Testigo de frenos encendido en el tablero"],
         faq=[("¿Cada cuánto se deben cambiar?", "Depende del uso y del tipo de vehículo. En nuestro taller revisamos su desgaste y le indicamos el momento adecuado para el cambio.")]),
    dict(slug="discos", nombre="Discos de freno", msg="discos de freno", code="DIS", img="discos", icon="disc",
         title="Discos de freno en Medellín: nacionales, importados y de equipo original",
         intro="Discos de freno nacionales, importados y de equipo original para todo tipo de vehículo, fabricados bajo altos estándares de calidad.",
         senales_t="¿Cuándo revisarlos?",
         senales=["Vibración en el timón o en el pedal al frenar", "Rayas o surcos visibles en el disco", "El vehículo se desvía al frenar"],
         faq=[("¿Siempre se cambian junto con las pastillas?", "No necesariamente. Evaluamos el espesor y el estado del disco y recomendamos el cambio solo cuando es necesario.")]),
    dict(slug="campanas-y-zapatas", nombre="Campanas y zapatas", msg="campanas o zapatas de freno", code="CAM", img="campanas", icon="drum",
         title="Campanas y zapatas de freno en Medellín para livianos y pesados",
         intro="Campanas y zapatas originales para vehículos livianos y pesados, fabricadas bajo altos estándares de calidad.",
         senales_t="¿Cuándo revisarlas?",
         senales=["El freno de mano no sostiene el vehículo", "Ruido de roce en las ruedas traseras", "El pedal baja más de lo habitual"],
         faq=[("¿Mi vehículo usa campanas o discos atrás?", "Muchos vehículos usan discos adelante y campanas atrás. Indíquenos marca, modelo y año, y le confirmamos la referencia.")]),
    dict(slug="cilindros", nombre="Cilindros de freno", msg="un cilindro de freno", code="CIL", img="cilindro-maestro", icon="cylinder",
         title="Cilindro maestro (bomba de frenos) y cilindros de rueda en Medellín",
         intro="Cilindro maestro (bomba de frenos) y cilindros de rueda en referencias originales y homologadas de marcas reconocidas.",
         senales_t="¿Cuándo revisarlos?",
         senales=["El pedal se va hasta el fondo", "Manchas de líquido cerca de las ruedas", "Disminuye el nivel del líquido de frenos"],
         faq=[("¿Se puede reparar un cilindro de rueda?", "Por seguridad recomendamos su reemplazo. Contamos con referencias originales y homologadas para cada vehículo.")]),
    dict(slug="mangueras", nombre="Mangueras de freno", msg="mangueras de freno", code="MAN", img="mangueras", icon="hose",
         title="Mangueras de freno en Medellín para todo tipo de vehículo",
         intro="Contamos con mangueras de alta calidad para todos los vehículos. Estas piezas de seguridad del sistema de frenos cumplen un papel fundamental dentro de su funcionamiento.",
         senales_t="¿Cuándo revisarlas?",
         senales=["Manguera reseca o agrietada", "Humedad o fuga de líquido de frenos", "Pedal de freno blando"],
         faq=[]),
]
EXTRAS = [
    dict(slug="blindados", nombre="Frenos para carros blindados", msg="frenos para un carro blindado", code="BLI", img="caliper-rojo", icon="shield",
         title="Frenos para vehículos blindados en Medellín",
         intro="Pastillas de formulación especial para carros blindados, diseñadas para ofrecer un frenado constante, seguro y de alto desempeño.",
         senales_t="Desempeño y calidad",
         senales=["Mayor resistencia a la temperatura en frenadas exigentes", "Frenado estable y confiable en cada recorrido", "Mayor durabilidad frente a una pastilla convencional"],
         faq=[]),
    dict(slug="marcas", nombre="Marcas", msg="repuestos de una marca específica", code="MAR", img="disco-caliper", icon="award",
         title="Marcas de frenos en Medellín: Brembo, Bosch, ATE, Fremax y más",
         intro="Trabajamos con marcas de alto desempeño, en repuestos originales y homologados.",
         marcas=True, senales_t="Le asesoramos en su elección",
         senales=["Original: la misma referencia con la que salió su vehículo de fábrica", "Homologado: cumple las especificaciones del fabricante con la misma seguridad"],
         faq=[]),
]
TODOS = SERVICIOS + EXTRAS
MARCAS = ["Brembo", "Bosch", "Incolbestos", "ATE", "Fremax", "Icer", "Repuestos originales Toyota", "Importadas"]

# ---------------------------------------------------------------- Iconos (SVG en línea)
ICONOS = {
    "wa": '<path class="icon-fill" d="M12 2a10 10 0 0 0-8.66 15l-1.3 4.76 4.87-1.28A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.18-1.14l-.3-.18-2.9.76.78-2.83-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.14c-.25-.12-1.46-.72-1.69-.8-.23-.08-.39-.12-.55.12-.17.25-.64.8-.78.97-.14.16-.29.18-.54.06a6.7 6.7 0 0 1-3.34-2.92c-.25-.43.25-.4.72-1.34.08-.16.04-.3-.02-.43-.06-.12-.55-1.33-.76-1.82-.2-.48-.4-.41-.55-.42h-.47a.9.9 0 0 0-.65.3 2.74 2.74 0 0 0-.86 2.04 4.76 4.76 0 0 0 1 2.53 10.9 10.9 0 0 0 4.18 3.7c1.55.67 2.16.73 2.94.61.47-.07 1.46-.6 1.66-1.18.21-.58.21-1.07.15-1.18-.06-.1-.22-.16-.47-.28Z"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92Z"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="9.5"/><path d="M12 7v5l3 2"/>',
    "star": '<path class="icon-fill" d="m12 2.5 2.94 5.96 6.56.95-4.75 4.63 1.12 6.54L12 17.5l-5.87 3.08 1.12-6.54L2.5 9.41l6.56-.95L12 2.5Z"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "alert": '<circle cx="12" cy="12" r="9.5"/><path d="M12 7.5v5.5M12 16.5h.01"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "arrow-l": '<path d="M19 12H5M11 6l-6 6 6 6"/>',
    "chev": '<path d="m6 9 6 6 6-6"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M18 6 6 18M6 6l12 12"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "disc": '<circle cx="12" cy="12" r="9.5"/><circle cx="12" cy="12" r="3"/><circle cx="12" cy="6.5" r=".6"/><circle cx="17.5" cy="12" r=".6"/><circle cx="12" cy="17.5" r=".6"/><circle cx="6.5" cy="12" r=".6"/>',
    "pad": '<path d="M3.5 8.5c0-1.7 1.3-3 3-3h11c1.7 0 3 1.3 3 3v2c0 4.4-3.6 8-8 8h-1c-4.4 0-8-3.6-8-8v-2Z"/><path d="M7 10.5h10"/>',
    "drum": '<circle cx="12" cy="12" r="9.5"/><circle cx="12" cy="12" r="6"/><path d="M12 9.5v5M9.5 12h5"/>',
    "cylinder": '<rect x="2.5" y="8" width="14" height="8" rx="2"/><path d="M16.5 10.5h5v3h-5M6.5 8V5.5M11.5 8V5.5"/>',
    "hose": '<path d="M3 5v4M3 7c7 0 5 10 12 10h3M18 15v4M21 15v4"/>',
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76Z"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/>',
    "award": '<circle cx="12" cy="8.5" r="6"/><path d="M8.2 13.9 7 22l5-3 5 3-1.2-8.1"/>',
    "gauge": '<path d="M3.3 17a10 10 0 1 1 17.4 0"/><path d="m12 14 4.5-4.5"/>',
    "search": '<circle cx="11" cy="11" r="7.5"/><path d="m21 21-4.35-4.35"/>',
    "chart": '<path d="M3 3v18h18"/><path d="m7 15 4-4 3 3 6-7"/>',
    "calendar": '<rect x="3" y="4.5" width="18" height="17" rx="2"/><path d="M16 2.5v4M8 2.5v4M3 10h18"/>',
    "msg": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2Z"/>',
    "mobile": '<rect x="5.5" y="2" width="13" height="20" rx="2.5"/><path d="M11 18.5h2"/>',
    "layers": '<path d="m12 2 10 5-10 5L2 7l10-5Z"/><path d="m2 17 10 5 10-5M2 12l10 5 10-5"/>',
    "text": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6M16 13H8M16 17H8"/>',
    "redirect": '<path d="m17 1 4 4-4 4"/><path d="M3 11V9a4 4 0 0 1 4-4h14M7 23l-4-4 4-4"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/>',
    "image": '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-5-5L5 21"/>',
    "car": '<path d="M3 17v-4.5L5.2 7h13.6l2.2 5.5V17"/><path d="M3 12.5h18M2 17h20"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    "bolt": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8Z"/>',
    "tag": '<path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L2 12V2h10l8.6 8.6a2 2 0 0 1 0 2.8Z"/><circle cx="7" cy="7" r="1.5"/>',
    "nav": '<path d="m3 11 19-9-9 19-2-8-8-2Z"/>',
    "mail": '<rect x="2.5" y="4.5" width="19" height="15" rx="2"/><path d="m3 6 9 7 9-7"/>',
}


def ic(nombre, clase="icon"):
    if nombre == "wa":
        clase += " icon-wa"  # el logo de WhatsApp va en su verde original (ver brand.css)
    return f'<svg class="{clase}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{ICONOS[nombre]}</svg>'


# ---------------------------------------------------------------- Plantilla base
def documento(*, title, desc, css, body, a, og, body_class="", extra_head=""):
    """a = prefijo relativo hasta /assets (p. ej. '../')."""
    return f"""<!doctype html>
<html lang="es-CO" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#c52b2d">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_CO">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://revupag.github.io/frenoteca-propuesta/assets/img/{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{a}assets/img/favicon-32.png" sizes="32x32">
<link rel="icon" href="{a}assets/img/favicon-192.png" sizes="192x192">
<link rel="apple-touch-icon" href="{a}assets/img/apple-touch-icon.png">
<link rel="preload" href="{a}assets/fonts/bitter.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{a}assets/css/brand.css?v={V}">
<link rel="stylesheet" href="{a}assets/css/{css}?v={V}">
<script>document.documentElement.classList.replace('no-js','js')</script>
{extra_head}</head>
<body class="{body_class}">
{body}
<script src="{a}assets/js/app.js?v={V}" defer></script>
</body>
</html>
"""


def logo(a, alt="Frenoteca", clase="logo"):
    # Logo nuevo de Frenoteca, vectorial, convertido del archivo original LOGO FRENOTECA.ai (ver README).
    return f'<img class="{clase}" src="{a}assets/img/logo-frenoteca.svg?v={V}" width="864" height="155" alt="{alt}">'


# ---------------------------------------------------------------- Sitio: cabecera y pie
# Público mayor: letra grande, frases cortas, trato de «usted» y botones con texto (no solo íconos).
# Todas las llamadas van al teléfono fijo; el celular se usa solo para WhatsApp.
def cabecera(s, a, activo=""):
    cur = ' aria-current="page"'
    items = "".join(
        f'<li><a href="{s}{x["slug"]}/"{cur if x["slug"] == activo else ""}>{ic(x["icon"])}<span>{x["nombre"]}</span></a></li>'
        for x in TODOS)
    return f"""<a class="skip" href="#contenido">Saltar al contenido</a>
<header class="site-header on-red" id="top">
  <div class="wrap header-in">
    <a class="brand" href="{s}" aria-label="Frenoteca, ir al inicio">{logo(a, "Frenoteca")}</a>
    <nav class="nav" id="menu" aria-label="Principal">
      <ul class="nav-list">
        <li class="has-sub">
          <a class="nav-sub-btn" href="{s}#servicios" aria-haspopup="true">Servicios {ic("chev")}</a>
          <ul class="sub" id="sub-servicios">{items}</ul>
        </li>
        <li><a href="{s}#cotizar">Cotizar</a></li>
        <li><a href="{s}#preguntas">Preguntas</a></li>
        <li><a href="{s}#visitenos">Cómo llegar</a></li>
      </ul>
      <div class="nav-cta">
        <a class="btn btn-blanco" href="{TEL_HREF}">{ic("phone")} {TEL}</a>
        <a class="btn btn-blanco nav-wa" href="{wa()}">{ic("wa")} WhatsApp</a>
      </div>
    </nav>
    <button class="hdr-btn menu-btn" type="button" aria-expanded="false" aria-controls="menu">{ic("menu")}{ic("close")}<span>Menú</span></button>
  </div>
  <a class="hdr-phone" href="{TEL_HREF}">{ic("phone")} <span>Llámenos:</span> <strong>{TEL}</strong></a>
</header>"""


def estado_horario():
    return '<p class="abierto" data-abierto><span class="dot"></span><span data-abierto-txt>Lunes a viernes 8:00 a. m. – 5:00 p. m.</span></p>'


def horario_lista():
    return """<dl class="horario">
  <div><dt>Lunes a viernes</dt><dd>8:00 a. m. – 5:00 p. m.</dd></div>
  <div><dt>Sábado</dt><dd>8:00 a. m. – 1:00 p. m.</dd></div>
  <div><dt>Domingo</dt><dd>Cerrado</dd></div>
</dl>"""


def cabeza(eyebrow, titulo, id_, lead=""):
    """Encabezado de sección: rótulo, título y una frase de apoyo."""
    l = f'<p class="lead">{lead}</p>' if lead else ""
    return f'<div class="section-head reveal"><p class="eyebrow">{eyebrow}</p><h2 class="title" id="{id_}">{titulo}</h2>{l}</div>'


def visitenos(a, compacto=False):
    mapa = "" if compacto else f"""<div class="map reveal" data-map="{MAPA_EMBED}">
      <img src="{a}assets/img/aerea-taller.webp" alt="Vista aérea de la sede de Frenoteca" width="1024" height="682" loading="lazy" decoding="async">
      <button class="btn btn-blanco map-btn" type="button">{ic("pin")} Ver mapa</button>
    </div>"""
    return f"""<section class="section visit" id="visitenos" aria-labelledby="visit-t">
  <div class="wrap visit-grid{" visit-compact" if compacto else ""}">
    <div class="visit-info">
      {cabeza("Ubicación", "Cómo llegar a Frenoteca", "visit-t")}
      {estado_horario()}
      <p class="visit-dir">{ic("pin")}<span>Carrera 50 # 39-87<br>Medellín, Antioquia</span></p>
      {horario_lista()}
      <div class="btn-col">
        <a class="btn btn-rojo btn-lg" href="{MAPS}" target="_blank" rel="noopener">{ic("nav")} Abrir en Google Maps</a>
        <a class="btn btn-borde btn-lg" href="{WAZE}" target="_blank" rel="noopener">{ic("nav")} Abrir en Waze</a>
      </div>
    </div>
    {mapa}
  </div>
</section>"""


def cotizar(preseleccion=""):
    """En Frenoteca no se reservan citas (se atiende en orden de llegada): el formulario pide cotización y disponibilidad."""
    opciones = "".join(
        f'<option value="{x["nombre"]}"{" selected" if x["slug"] == preseleccion else ""}>{x["nombre"]}</option>'
        for x in TODOS if x["slug"] != "marcas")
    code = next((x["code"] for x in TODOS if x["slug"] == preseleccion), "INI")
    vacia = "" if preseleccion else '<option value="" selected disabled>Escoja una opción</option>'
    return f"""<section class="section cita bg-negro on-dark" id="cotizar" aria-labelledby="cita-t">
  <div class="wrap cita-grid">
    {cabeza("Cotizaciones", "Cotice y consulte disponibilidad", "cita-t",
            "Atendemos en orden de llegada. Cuéntenos qué necesita y cuándo piensa venir; le respondemos por WhatsApp con la cotización y la disponibilidad.")}
    <form class="form reveal" data-agenda data-wa="{WA}" data-code="{code}" novalidate>
      <div class="field">
        <label for="f-nombre">Su nombre</label>
        <input id="f-nombre" name="nombre" autocomplete="name" required>
      </div>
      <div class="field">
        <label for="f-servicio">¿Qué necesita?</label>
        <div class="select"><select id="f-servicio" name="servicio" required>{vacia}{opciones}<option value="Una revisión del sistema de frenos">No estoy seguro</option></select>{ic("chev")}</div>
      </div>
      <div class="field">
        <label for="f-fecha">¿Qué día piensa venir?</label>
        <input id="f-fecha" name="fecha" type="date" required>
      </div>
      <fieldset class="field franja">
        <legend>¿En qué jornada?</legend>
        <label><input type="radio" name="franja" value="mañana" checked> Mañana</label>
        <label><input type="radio" name="franja" value="tarde"> Tarde</label>
      </fieldset>
      <p class="form-error" role="alert" aria-live="polite"></p>
      <button class="btn btn-rojo btn-lg btn-block" type="submit">{ic("wa")} Enviar por WhatsApp</button>
    </form>
  </div>
</section>"""


def pie(s, a, code="INI", msg=None):
    return f"""<footer class="site-footer on-red">
  <div class="wrap footer-grid">
    <div>
      <a href="{s}" aria-label="Frenoteca, inicio">{logo(a)}</a>
      <p>Especialistas en frenos en Medellín. Más de 40 años en el mercado.</p>
    </div>
    <div class="footer-contact">
      <a href="{TEL_HREF}">{ic("phone")} {TEL}</a>
      <a href="{wa(msg, code)}">{ic("wa")} WhatsApp {CEL}</a>
      <a href="{MAPS}" target="_blank" rel="noopener">{ic("pin")} Carrera 50 # 39-87</a>
    </div>
    <div>{horario_lista()}</div>
  </div>
  <div class="wrap footer-bottom">
    <p>© 2026 Frenoteca S.A.S.</p>
  </div>
</footer>
<nav class="action-bar" aria-label="Contacto rápido">
  <a class="btn btn-rojo" href="{TEL_HREF}">{ic("phone")} Llamar</a>
  <a class="btn btn-negro" href="#cotizar">{ic("calendar")} Cotizar</a>
</nav>
<a class="wa-float" href="{wa(msg, code)}" aria-label="Escríbanos por WhatsApp">
  <span class="wa-float-label">¿Le ayudamos? <strong>Escríbanos</strong></span>
  <span class="wa-float-btn">{ic("wa")}</span>
</a>"""


def tile(x, s, a):
    return f"""<a class="tile reveal" href="{s}{x["slug"]}/">
  <span class="tile-img"><img src="{a}assets/img/productos/{x["img"]}.webp" alt="" loading="lazy" decoding="async"></span>
  <span class="tile-name">{x["nombre"]}</span>
  {ic("arrow")}
</a>"""


FAQ = [
    ("¿Necesito cita para ser atendido?", "No. Atendemos en orden de llegada dentro de nuestro horario. Si desea confirmar disponibilidad antes de venir, escríbanos por WhatsApp."),
    ("¿Cómo saber si mis frenos necesitan revisión?", "Ruidos al frenar, vibración en el pedal o en el timón, un pedal blando o una mayor distancia de frenado son señales para revisar el sistema cuanto antes."),
    ("¿Cómo puedo solicitar una cotización?", f"Llámenos al {TEL} o escríbanos por WhatsApp indicando la marca, el modelo y el año de su vehículo."),
    ("¿Con qué marcas trabajan?", "Brembo, Bosch, Incolbestos, ATE, Fremax, Icer, repuestos originales Toyota y marcas importadas, en referencias originales y homologadas."),
    ("¿Cuál es el horario de atención?", "Lunes a viernes de 8:00 a. m. a 5:00 p. m. y sábados de 8:00 a. m. a 1:00 p. m., en jornada continua."),
    ("¿Dónde están ubicados?", "En la Carrera 50 # 39-87, Medellín. Contamos con patio para recibir su vehículo."),
]


def faq_html(items, titulo=None):
    if not items:
        return ""
    qs = "".join(f"""<details class="faq-item"><summary><span>{q}</span>{ic("chev")}</summary><p>{r}</p></details>""" for q, r in items)
    head = cabeza("Preguntas frecuentes", titulo, "preguntas-t") if titulo else ""
    attrs = ' id="preguntas" aria-labelledby="preguntas-t"' if titulo else ' aria-label="Preguntas"'
    return f"""<section class="section section-tight"{attrs}>
  <div class="wrap faq-wrap">{head}<div class="faq reveal">{qs}</div></div>
</section>"""


GALERIA = [
    ("taller-01", "Entrada a la sede de Frenoteca vista desde arriba"),
    ("taller-03", "Camioneta en el elevador del taller"),
    ("taller-05", "Disco de freno Brembo en exhibición"),
    ("taller-02", "Entrada principal con el aviso de Frenoteca"),
    ("taller-04", "Vehículo comercial en revisión"),
    ("taller-06", "Automóvil en el patio del taller"),
    ("taller-07", "Camioneta con el capó abierto en revisión"),
    ("taller-08", "Carro clásico en el patio de Frenoteca"),
    ("taller-09", "Barril de Brembo en el patio"),
    ("taller-10", "El taller de noche, con carros listos para entregar"),
]


def jsonld():
    data = {
        "@context": "https://schema.org", "@type": "AutoRepair", "name": "Frenoteca S.A.S.",
        "description": "Especialistas en frenos en Medellín: repuestos y taller.",
        "telephone": "+57 604 448 2194", "email": EMAIL,
        "address": {"@type": "PostalAddress", "streetAddress": "Carrera 50 # 39-87", "addressLocality": "Medellín",
                    "addressRegion": "Antioquia", "addressCountry": "CO"},
        "geo": {"@type": "GeoCoordinates", "latitude": 6.240469, "longitude": -75.571513},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "17:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "08:00", "closes": "13:00"}],
        "brand": [{"@type": "Brand", "name": m} for m in ["Brembo", "Bosch", "Incolbestos", "ATE", "Fremax", "Icer", "Toyota"]],
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>\n'


# ---------------------------------------------------------------- Sitio: inicio
def inicio():
    s, a = "./", ""
    # 6 tarjetas (servicios + blindados): filas completas; «Marcas» queda en el menú y en «Por qué Frenoteca»
    tiles = "".join(tile(x, s, a) for x in TODOS if x["slug"] != "marcas")
    galeria = "".join(
        f'<button class="gal-item" type="button" data-full="{a}assets/img/galeria/{f}.webp" aria-label="Ampliar foto: {alt}"><img src="{a}assets/img/galeria/{f}.webp" alt="{alt}" loading="lazy" decoding="async"></button>'
        for f, alt in GALERIA)
    estrellas = ic("star") * 5
    body = f"""{cabecera(s, a)}
<main id="contenido">
  <section class="hero on-dark">
    <picture class="hero-bg">
      <source media="(min-width: 800px)" srcset="{a}assets/img/hero.webp" width="1024" height="576">
      <img src="{a}assets/img/hero-movil.webp" width="768" height="1024" alt="Patio de Frenoteca con carros listos para entregar" fetchpriority="high">
    </picture>
    <div class="wrap hero-in">
      <p class="eyebrow">Especialistas en frenos</p>
      <h1 class="hero-t">Frenos para su carro en Medellín</h1>
      <p class="lead">Repuestos de alto desempeño y taller especializado en un solo lugar. Más de 40 años brindando seguridad y tranquilidad en cada recorrido.</p>
      <div class="btn-col hero-btns">
        <a class="btn btn-rojo btn-xl" href="{TEL_HREF}">{ic("phone")} Llamar al {TEL}</a>
        <a class="btn btn-blanco btn-xl" href="{wa()}">{ic("wa")} Escribir por WhatsApp</a>
      </div>
      <div class="hero-meta">
        {estado_horario()}
        <a class="hero-rating" href="{RESENAS}" target="_blank" rel="noopener"><span class="stars">{estrellas}</span><span><strong>4,6</strong> · 360 opiniones en Google</span></a>
      </div>
    </div>
  </section>

  <section class="section" id="servicios" aria-labelledby="serv-t">
    <div class="wrap">
      {cabeza("Nuestros servicios", "¿Qué necesita?", "serv-t", "Repuestos y servicio especializado para cada componente del sistema de frenos.")}
      <div class="tiles tiles-3">{tiles}</div>
    </div>
  </section>

  <section class="section section-tight bg-gris" aria-labelledby="why-t">
    <div class="wrap">
      {cabeza("Por qué elegirnos", "¿Por qué Frenoteca?", "why-t")}
      <ul class="why reveal">
        <li>{ic("award")}<span><strong>Más de 40 años en el mercado</strong> Especialistas en sistemas de frenos</span></li>
        <li>{ic("tag")}<span><strong>Marcas de alto desempeño</strong> <a href="{s}marcas/">Brembo, Bosch, ATE, Fremax y más</a></span></li>
        <li>{ic("wrench")}<span><strong>Todo en un solo lugar</strong> El repuesto y el taller que lo instala</span></li>
      </ul>
    </div>
  </section>

  {cotizar()}

  <section class="section" id="taller" aria-labelledby="taller-t">
    <div class="wrap">
      {cabeza("Nuestra sede", "Nuestro taller", "taller-t", "Carrera 50 # 39-87, con patio para recibir su vehículo.")}
      <div class="gallery reveal">{galeria}</div>
      <button class="btn btn-borde btn-lg gal-all" type="button" data-gal-open>{ic("image")} Ver las {len(GALERIA)} fotos</button>
    </div>
    <dialog class="lightbox" aria-label="Fotos del taller">
      <img alt="">
      <button class="lb-btn lb-close" type="button" aria-label="Cerrar">{ic("close")}</button>
      <button class="lb-btn lb-prev" type="button" aria-label="Foto anterior">{ic("arrow-l")}</button>
      <button class="lb-btn lb-next" type="button" aria-label="Foto siguiente">{ic("arrow")}</button>
    </dialog>
  </section>

  <section class="section section-tight reviews bg-rojo on-red" aria-labelledby="rev-t">
    <div class="wrap reviews-in reveal">
      <p class="rev-num" id="rev-t">4,6 <span class="stars">{estrellas}</span></p>
      <p class="rev-txt">360 clientes opinan sobre Frenoteca en Google</p>
      <a class="btn btn-blanco btn-lg" href="{RESENAS}" target="_blank" rel="noopener">Leer opiniones {ic("arrow")}</a>
    </div>
  </section>

  {faq_html(FAQ, "Resolvemos sus dudas")}

  {visitenos(a)}
</main>
{pie(s, a)}"""
    return documento(
        title="Frenoteca | Especialistas en frenos en Medellín, más de 40 años en el mercado",
        desc="Pastillas, discos, campanas, cilindros y mangueras de freno con Brembo, Bosch, ATE e Incolbestos. Taller especializado en la Carrera 50, Medellín.",
        css="sitio.css", body=body, a=a, og="og-sitio.jpg", body_class="sitio", extra_head=jsonld())


# ---------------------------------------------------------------- Sitio: páginas de servicio
def servicio(x):
    s, a = "../", "../"
    senales = "".join(f"<li>{ic('alert' if not x.get('marcas') and x['slug'] != 'blindados' else 'check')}<span>{i}</span></li>" for i in x["senales"])
    marcas = f'<ul class="brands reveal">{"".join(f"<li>{m}</li>" for m in MARCAS)}</ul>' if x.get("marcas") else ""
    # 6 tarjetas: llenan filas completas (2 columnas en celular, 3 en computador)
    otros = "".join(tile(o, s, a) for o in [t for t in TODOS if t["slug"] != x["slug"]][:6])
    body = f"""{cabecera(s, a, x["slug"])}
<main id="contenido">
  <section class="svc-hero">
    <div class="wrap">
      <a class="back" href="{s}">{ic("arrow-l")} Volver al inicio</a>
      <div class="svc-hero-grid">
        <div>
          <p class="eyebrow">Frenoteca · Medellín</p>
          <h1 class="svc-h1">{x["nombre"]}</h1>
          <p class="lead">{x["intro"]}</p>
          <div class="btn-col">
            <a class="btn btn-rojo btn-xl" href="{TEL_HREF}">{ic("phone")} Llamar al {TEL}</a>
            <a class="btn btn-borde btn-xl" href="{wa(x["msg"], x["code"])}">{ic("wa")} Escribir por WhatsApp</a>
          </div>
        </div>
        <figure class="svc-hero-img"><img src="{a}assets/img/productos/{x["img"]}.webp" alt="{x["nombre"]}" fetchpriority="high"></figure>
      </div>
    </div>
  </section>
  <section class="section section-tight bg-gris">
    <div class="wrap">
      {marcas}
      <div class="signs reveal">
        <h2 class="signs-t">{x["senales_t"]}</h2>
        <ul class="signs-list">{senales}</ul>
      </div>
    </div>
  </section>
  {faq_html(x["faq"])}
  {cotizar(x["slug"])}
  <section class="section" aria-labelledby="otros-t">
    <div class="wrap">
      {cabeza("Nuestros servicios", "Otros servicios", "otros-t")}
      <div class="tiles tiles-3">{otros}</div>
    </div>
  </section>
  {visitenos(a, compacto=True)}
</main>
{pie(s, a, x["code"], x["msg"])}"""
    return documento(title=f'{x["title"]} | Frenoteca', desc=x["intro"][:155],
                     css="sitio.css", body=body, a=a, og="og-sitio.jpg", body_class="sitio")


def escribir(ruta, html):
    ruta = os.path.join(RAIZ, ruta)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(html)
    print("✓", os.path.relpath(ruta, RAIZ))


if __name__ == "__main__":
    escribir("index.html", inicio())
    for x in TODOS:
        escribir(f"{x['slug']}/index.html", servicio(x))
