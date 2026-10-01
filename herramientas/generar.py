"""Genera la propuesta (index.html) y el sitio (sitio/**) de Frenoteca.

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
    txt = f"Hola Frenoteca, quiero cotizar {servicio}." if servicio else "Hola Frenoteca, quiero información sobre sus servicios."
    return f"https://wa.me/{WA}?text=" + quote(f"{txt} (Ref: WEB-{code})")


SERVICIOS = [
    dict(slug="pastillas", nombre="Pastillas de freno", msg="pastillas de freno", code="PAS", img="pastillas", icon="pad",
         h1="Pastillas de freno <em>en Medellín</em>",
         title="Pastillas de freno en Medellín: Brembo, Bosch e Incolbestos",
         resumen="Brembo, Bosch, Incolbestos e importadas. Formulaciones para blindados.",
         intro="Somos distribuidores de pastillas de freno Brembo, Incolbestos, Bosch y un amplio portafolio de marcas importadas. Además contamos con formulaciones especiales para vehículos blindados.",
         listas=[("Señales de que debes revisarlas", "alert", [
                     "Chirrido metálico o chillido al frenar",
                     "El carro necesita más distancia para detenerse",
                     "Vibración o ruido en el pedal",
                     "Se encendió el testigo de frenos en el tablero"]),
                 ("Qué incluye", "check", [
                     "Revisión del sistema de frenos antes de cambiar",
                     "Pastillas de marca, originales u homologadas",
                     "Revisión del estado de los discos",
                     "Instalación en nuestro taller de la Carrera 50"])],
         faq=[("¿Cada cuánto se cambian las pastillas?", "Depende del vehículo, de la ruta y de cómo se maneja. En el taller revisamos el desgaste y te decimos cuánto les queda antes de recomendar el cambio."),
              ("¿Tienen pastillas para mi carro?", "Manejamos referencias para vehículos livianos y pesados, nacionales e importados. Escríbenos marca, modelo y año por WhatsApp y te confirmamos disponibilidad."),
              ("¿Puedo comprar solo las pastillas?", "Sí. Puedes llevártelas o dejar que las instalemos en el taller.")]),
    dict(slug="discos", nombre="Discos de freno", msg="discos de freno", code="DIS", img="discos", icon="disc",
         h1="Discos de freno <em>en Medellín</em>",
         title="Discos de freno en Medellín: nacionales, importados y originales",
         resumen="Nacionales, importados y de equipo original, a buen precio.",
         intro="Discos de frenos nacionales, importados y equipo original para todo tipo de vehículos, a un precio asequible para todo público. Fabricados bajo los más altos estándares de calidad.",
         listas=[("Señales de que debes revisarlos", "alert", [
                     "Vibración en el volante o en el pedal al frenar",
                     "Rayas o surcos visibles en el disco",
                     "Ruido constante al frenar",
                     "El carro se va hacia un lado al frenar"]),
                 ("Qué incluye", "check", [
                     "Revisión del disco: si se puede seguir usando o hay que cambiarlo",
                     "Discos nacionales, importados y de equipo original",
                     "Cambio por pares, por seguridad",
                     "Revisión de las pastillas en el mismo servicio"])],
         faq=[("¿Hay que cambiar los discos junto con las pastillas?", "No siempre. Revisamos el grosor y el estado del disco y solo recomendamos el cambio cuando hace falta."),
              ("¿Por qué vibra el carro al frenar?", "Casi siempre es un disco deformado o con desgaste desigual. Tráelo al taller y lo revisamos.")]),
    dict(slug="campanas-y-zapatas", nombre="Campanas y zapatas", msg="campanas o zapatas de freno", code="CAM", img="campanas", icon="drum",
         h1="Campanas y zapatas <em>de freno</em>",
         title="Campanas y zapatas de freno en Medellín para livianos y pesados",
         resumen="Para vehículos livianos y pesados. Zapatas originales.",
         intro="Campanas de frenos para vehículos livianos y pesados, fabricadas bajo los más altos estándares de calidad, y zapatas originales para toda clase de vehículo liviano y pesado.",
         listas=[("Señales de que debes revisarlas", "alert", [
                     "El freno de mano no sostiene o hay que subirlo mucho",
                     "Ruido de roce en las ruedas traseras",
                     "El pedal baja más de lo normal",
                     "Vibración al frenar a baja velocidad"]),
                 ("Qué incluye", "check", [
                     "Campanas para vehículos livianos y pesados",
                     "Zapatas originales",
                     "Revisión de cilindros de rueda y resortes",
                     "Ajuste del sistema después del cambio"])],
         faq=[("¿Mi carro tiene campanas o discos atrás?", "Muchos carros tienen discos adelante y campanas atrás. Escríbenos el modelo y te decimos qué lleva."),
              ("¿Trabajan vehículos pesados?", "Sí, manejamos campanas y zapatas para livianos y pesados.")]),
    dict(slug="cilindros", nombre="Cilindros de freno", msg="un cilindro de freno", code="CIL", img="cilindro-maestro", icon="cylinder",
         h1="Cilindro maestro <em>y cilindros de rueda</em>",
         title="Cilindro maestro (bomba de frenos) y cilindros de rueda en Medellín",
         resumen="Bombas de freno y cilindros de rueda tipo original y homologado.",
         intro="El cilindro maestro (bomba de frenos) es de vital importancia para el buen funcionamiento del sistema; por eso lo ofrecemos en reconocidas marcas. Los cilindros de rueda no se reparan, se reemplazan: tenemos una amplia gama de referencias tipo original y homologado, garantizando seguridad y economía.",
         listas=[("Señales de que debes revisarlos", "alert", [
                     "El pedal se va al fondo o se siente esponjoso",
                     "Manchas de líquido cerca de las ruedas",
                     "El nivel del líquido de frenos baja",
                     "Hay que bombear el pedal para frenar"]),
                 ("Qué incluye", "check", [
                     "Bombas de freno en marcas reconocidas",
                     "Cilindros de rueda tipo original y homologado",
                     "Purga del sistema después del cambio",
                     "Revisión de fugas en todo el circuito"])],
         faq=[("¿Se puede reparar un cilindro de rueda?", "No es recomendable. Por seguridad, el cilindro de rueda se reemplaza; tenemos referencias originales y homologadas para que sea económico."),
              ("¿Qué es la bomba de frenos?", "Es el cilindro maestro: convierte la fuerza del pedal en presión hidráulica. Si falla, el pedal se va al fondo.")]),
    dict(slug="mangueras", nombre="Mangueras de freno", msg="mangueras de freno", code="MAN", img="mangueras", icon="hose",
         h1="Mangueras de freno <em>en Medellín</em>",
         title="Mangueras de freno en Medellín para todo tipo de vehículo",
         resumen="Piezas de seguridad de alta calidad para todos los vehículos.",
         intro="Contamos con mangueras de alta calidad para todos los vehículos. Estas piezas de seguridad del sistema de frenos cumplen un papel fundamental dentro de su funcionamiento.",
         listas=[("Señales de que debes revisarlas", "alert", [
                     "Grietas o resequedad en la manguera",
                     "Humedad o fuga de líquido",
                     "Pedal esponjoso",
                     "La manguera se hincha al frenar"]),
                 ("Qué incluye", "check", [
                     "Mangueras para todos los vehículos",
                     "Revisión de conexiones y abrazaderas",
                     "Purga del sistema después del cambio",
                     "Prueba de frenado antes de entregar"])],
         faq=[("¿Cada cuánto se cambian las mangueras?", "Con el tiempo el caucho se reseca y se agrieta. Las revisamos en cada mantenimiento de frenos y te avisamos si hace falta.")]),
    dict(slug="taller-y-suspension", nombre="Taller y suspensión", msg="una revisión en el taller", code="TAL", img="suspension", icon="wrench",
         h1="Taller de frenos <em>y suspensión</em>",
         title="Taller de frenos y reparación de suspensión en Medellín",
         resumen="Mantenimiento de frenos y reparación de suspensión en un solo lugar.",
         intro="Ofrecemos el mejor servicio y la mejor experiencia a la hora de revisar, monitorear y reparar su vehículo: mantenimiento de frenos y reparación de suspensión, con los repuestos en el mismo lugar.",
         listas=[("Señales de que debes traerlo", "alert", [
                     "El carro se va hacia un lado",
                     "Golpes o ruidos al pasar huecos",
                     "Desgaste irregular de las llantas",
                     "El carro rebota o se inclina en las curvas"]),
                 ("Qué incluye", "check", [
                     "Diagnóstico del sistema de frenos",
                     "Reparación de suspensión",
                     "Mantenimiento preventivo",
                     "Repuestos en el mismo lugar, sin vueltas"])],
         faq=[("¿Necesito cita?", "Puedes llegar en nuestro horario, pero si agendas por WhatsApp te esperamos y el servicio es más rápido."),
              ("¿Dónde queda el taller?", f"En la {DIR}. Tenemos patio amplio para recibir tu vehículo.")]),
]
EXTRAS = [
    dict(slug="marcas", nombre="Marcas", msg="repuestos de una marca específica", code="MAR", img="disco-caliper", icon="award",
         h1="Marcas <em>que manejamos</em>",
         title="Marcas de frenos en Medellín: Brembo, Bosch, Incolbestos e importadas",
         resumen="Brembo, Bosch, Incolbestos e importadas.",
         intro="Brembo, Bosch, Incolbestos y un amplio portafolio de marcas importadas, en referencias de equipo original y homologadas, para vehículos livianos y pesados.",
         marcas=True,
         listas=[("Original u homologado: cuál elegir", "check", [
                     "Equipo original: la misma referencia con la que salió tu vehículo de fábrica",
                     "Homologado: cumple las especificaciones del fabricante a un precio más económico",
                     "Te asesoramos según el uso del vehículo y tu presupuesto"])],
         faq=[("¿Consiguen una referencia que no está en la lista?", "Escríbenos por WhatsApp con la marca, el modelo y el año del vehículo; te confirmamos si la tenemos o cuánto tarda.")]),
    dict(slug="blindados", nombre="Vehículos blindados", msg="frenos para un vehículo blindado", code="BLI", img="caliper-rojo", icon="shield",
         h1="Frenos para <em>vehículos blindados</em>",
         title="Frenos para vehículos blindados en Medellín",
         resumen="Formulaciones especiales de pastillas para el peso extra.",
         intro="Un vehículo blindado pesa más y exige más de sus frenos. Contamos con formulaciones especiales de pastillas para vehículos blindados.",
         listas=[("Por qué necesita frenos especiales", "alert", [
                     "El peso adicional aumenta la distancia de frenado",
                     "Las pastillas convencionales se desgastan y se recalientan más rápido",
                     "Una formulación especial mantiene el frenado estable"]),
                 ("Qué incluye", "check", [
                     "Pastillas con formulación para blindados",
                     "Revisión de discos y del sistema completo",
                     "Asesoría según el vehículo y el nivel de blindaje"])],
         faq=[("¿Sirven las pastillas normales en un blindado?", "Funcionan, pero se desgastan mucho más rápido y pierden eficacia con el calor. La formulación especial está hecha para ese peso.")]),
]
TODOS = SERVICIOS + EXTRAS
MARCAS = ["Brembo", "Bosch", "Incolbestos", "Importadas"]

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
<meta name="theme-color" content="#d41111">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_CO">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://revupag.github.io/frenoteca-propuesta/assets/img/{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{a}assets/img/favicon-32.png" sizes="32x32">
<link rel="icon" href="{a}assets/img/favicon-192.png" sizes="192x192">
<link rel="apple-touch-icon" href="{a}assets/img/apple-touch-icon.png">
<link rel="preload" href="{a}assets/fonts/didact-gothic.woff2" as="font" type="font/woff2" crossorigin>
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


def logo(a, alt="Frenoteca"):
    # Logo original del sitio (366 × 99 px, PNG transparente): se usa tal cual sobre el rojo de marca.
    return f'<img class="logo" src="{a}assets/img/logo-frenoteca.png" width="366" height="99" alt="{alt}">'


# ---------------------------------------------------------------- Sitio: cabecera y pie
def cabecera(s, a, activo=""):
    cur = ' aria-current="page"'
    items = "".join(
        f'<li><a href="{s}{x["slug"]}/"{cur if x["slug"] == activo else ""}>{ic(x["icon"])}<span>{x["nombre"]}</span></a></li>'
        for x in SERVICIOS)
    def link(slug, txt):
        cur = ' aria-current="page"' if slug == activo else ""
        return f'<a href="{s}{slug}/"{cur}>{txt}</a>'
    return f"""<a class="skip" href="#contenido">Saltar al contenido</a>
<header class="site-header on-red" id="top">
  <div class="wrap header-in">
    <a class="brand" href="{s}" aria-label="Frenoteca, ir al inicio">{logo(a, "Frenoteca")}</a>
    <nav class="nav" id="menu" aria-label="Principal">
      <ul class="nav-list">
        <li class="has-sub">
          <button class="nav-sub-btn" type="button" aria-expanded="false" aria-controls="sub-servicios">Servicios {ic("chev")}</button>
          <ul class="sub" id="sub-servicios">{items}</ul>
        </li>
        <li>{link("marcas", "Marcas")}</li>
        <li>{link("blindados", "Blindados")}</li>
        <li><a href="{s}#taller">Taller</a></li>
        <li><a href="{s}#visitanos">Cómo llegar</a></li>
      </ul>
      <div class="nav-cta">
        <a class="btn btn-blanco" href="{s}#agenda">{ic("calendar")} Agendar revisión</a>
        <a class="nav-tel" href="{TEL_HREF}">{ic("phone")} {TEL}</a>
      </div>
    </nav>
    <div class="header-actions">
      <a class="icon-btn" href="{CEL_HREF}" aria-label="Llamar al {CEL}">{ic("phone")}</a>
      <button class="icon-btn menu-btn" type="button" aria-expanded="false" aria-controls="menu" aria-label="Abrir menú">{ic("menu")}{ic("close")}</button>
    </div>
  </div>
</header>"""


def estado_horario():
    return '<p class="abierto" data-abierto><span class="dot"></span><span data-abierto-txt>Lunes a viernes 8:00 a. m. – 5:15 p. m.</span></p>'


def horario_lista():
    return """<dl class="horario">
  <div><dt>Lunes a viernes</dt><dd>8:00 a. m. – 5:15 p. m.</dd></div>
  <div><dt>Sábado</dt><dd>8:00 a. m. – 1:15 p. m.</dd></div>
  <div><dt>Domingo y festivos</dt><dd>Cerrado</dd></div>
</dl>"""


def visitanos(s, a, code="INI", msg=None):
    return f"""<section class="section visit" id="visitanos" aria-labelledby="visit-t">
  <div class="wrap visit-grid">
    <div class="visit-info reveal">
      <p class="eyebrow">Visítanos</p>
      <h2 class="title" id="visit-t">Carrera 50, <em>Medellín</em></h2>
      {estado_horario()}
      <ul class="contact-list">
        <li>{ic("pin")}<div><strong>Dirección</strong><span>{DIR}</span></div></li>
        <li>{ic("clock")}<div><strong>Horario · jornada continua</strong>{horario_lista()}</div></li>
        <li>{ic("wa")}<div><strong>WhatsApp y celular</strong><a href="{wa(msg, code)}">{CEL}</a></div></li>
        <li>{ic("phone")}<div><strong>Teléfono fijo</strong><a href="{TEL_HREF}">{TEL}</a></div></li>
      </ul>
      <div class="btn-row">
        <a class="btn btn-rojo" href="{MAPS}" target="_blank" rel="noopener">{ic("pin")} Google Maps</a>
        <a class="btn btn-borde" href="{WAZE}" target="_blank" rel="noopener">{ic("nav")} Waze</a>
      </div>
    </div>
    <div class="map reveal" data-map="{MAPA_EMBED}">
      <img src="{a}assets/img/aerea-taller.webp" alt="Vista aérea de la sede de Frenoteca con su patio interior" width="1024" height="682" loading="lazy" decoding="async">
      <button class="btn btn-blanco map-btn" type="button">{ic("pin")} Ver mapa interactivo</button>
    </div>
  </div>
</section>"""


def agenda(preseleccion=""):
    opciones = "".join(
        f'<option value="{x["nombre"]}"{" selected" if x["slug"] == preseleccion else ""}>{x["nombre"]}</option>'
        for x in TODOS)
    code = next((x["code"] for x in TODOS if x["slug"] == preseleccion), "INI")
    return f"""<section class="section agenda bg-negro on-dark" id="agenda" aria-labelledby="agenda-t">
  <div class="wrap agenda-grid">
    <div class="agenda-copy reveal">
      <p class="eyebrow">Agenda en un minuto</p>
      <h2 class="title" id="agenda-t">Reserva tu <em>revisión de frenos</em></h2>
      <p class="lead">Elige el servicio y el día. Te llega todo listo a WhatsApp y te confirmamos la hora.</p>
      <ul class="ticks">
        <li>{ic("check")} Sin llamadas ni esperas</li>
        <li>{ic("check")} Confirmación por WhatsApp</li>
        <li>{ic("check")} Jornada continua, sábados hasta la 1:15 p. m.</li>
      </ul>
    </div>
    <form class="form reveal" data-agenda data-wa="{WA}" data-code="{code}" novalidate>
      <div class="field">
        <label for="f-nombre">Tu nombre</label>
        <input id="f-nombre" name="nombre" autocomplete="name" required placeholder="Ej.: Laura Gómez">
      </div>
      <div class="field">
        <label for="f-vehiculo">Vehículo <span class="opt">marca, modelo y año</span></label>
        <input id="f-vehiculo" name="vehiculo" required placeholder="Ej.: Mazda 3, 2019">
      </div>
      <div class="field">
        <label for="f-servicio">Servicio</label>
        <div class="select"><select id="f-servicio" name="servicio" required>{"" if preseleccion else '<option value="" selected disabled>Elige una opción</option>'}{opciones}<option value="No estoy seguro, quiero un diagnóstico">No estoy seguro</option></select>{ic("chev")}</div>
      </div>
      <div class="field-row">
        <div class="field">
          <label for="f-fecha">Día</label>
          <input id="f-fecha" name="fecha" type="date" required>
        </div>
        <div class="field">
          <label for="f-franja">Franja</label>
          <div class="select"><select id="f-franja" name="franja" required><option value="mañana">Mañana</option><option value="tarde">Tarde</option></select>{ic("chev")}</div>
        </div>
      </div>
      <p class="form-error" role="alert" aria-live="polite"></p>
      <button class="btn btn-rojo btn-lg btn-block" type="submit">{ic("wa")} Enviar por WhatsApp</button>
      <p class="form-note">Abrimos WhatsApp con tu mensaje listo. Nada se envía sin que tú lo confirmes.</p>
    </form>
  </div>
</section>"""


def pie(s, a, code="INI", msg=None, proposal="../"):
    serv = "".join(f'<li><a href="{s}{x["slug"]}/">{x["nombre"]}</a></li>' for x in TODOS)
    return f"""<footer class="site-footer on-red">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <a href="{s}" aria-label="Frenoteca, inicio">{logo(a)}</a>
      <p>Repuestos y taller de frenos en Medellín desde hace más de 35 años.</p>
      <div class="rating-mini">{ic("star")} <span>4,6 en Google · 360 reseñas</span></div>
    </div>
    <div>
      <h2 class="footer-t">Servicios</h2>
      <ul class="footer-links">{serv}</ul>
    </div>
    <div>
      <h2 class="footer-t">Contacto</h2>
      <ul class="footer-links">
        <li><a href="{wa(msg, code)}">WhatsApp {CEL}</a></li>
        <li><a href="{TEL_HREF}">Fijo {TEL}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="{MAPS}" target="_blank" rel="noopener">{DIR}</a></li>
      </ul>
    </div>
    <div>
      <h2 class="footer-t">Horario</h2>
      {horario_lista()}
    </div>
  </div>
  <div class="wrap footer-bottom">
    <p>© 2026 Frenoteca S.A.S. · Medellín, Colombia</p>
    <a class="back-proposal" href="{proposal}">{ic("arrow-l")} Volver a la propuesta</a>
  </div>
</footer>
<nav class="action-bar" aria-label="Contacto rápido">
  <a class="btn btn-rojo" href="{CEL_HREF}">{ic("phone")} Llamar</a>
  <a class="btn btn-negro" href="#agenda">{ic("calendar")} Agendar</a>
</nav>
<a class="wa-float" href="{wa(msg, code)}" aria-label="Escríbenos por WhatsApp">
  <span class="wa-float-label">¿Cotizamos? <strong>Escríbenos</strong></span>
  <span class="wa-float-btn">{ic("wa")}</span>
</a>"""


def llamar_cta(titulo="¿Tu carro frena raro?", texto="No esperes a que empeore. Llámanos y te decimos qué revisar."):
    return f"""<section class="call-band on-red" aria-label="Llámanos">
  <div class="wrap call-in reveal">
    <div class="call-copy">
      <span class="call-ico">{ic("phone")}</span>
      <div>
        <h2 class="call-t">{titulo}</h2>
        <p>{texto}</p>
      </div>
    </div>
    <div class="call-actions">
      <a class="btn btn-negro btn-lg" href="{CEL_HREF}">{ic("phone")} Llamar al {CEL}</a>
      <a class="call-fijo" href="{TEL_HREF}">o al fijo {TEL}</a>
    </div>
  </div>
</section>"""


def faq_html(items, titulo="Preguntas frecuentes", id_="faq"):
    qs = "".join(f"""<details class="faq-item"><summary><span>{q}</span>{ic("chev")}</summary><div class="faq-a"><p>{r}</p></div></details>""" for q, r in items)
    return f"""<section class="section" id="{id_}" aria-labelledby="{id_}-t">
  <div class="wrap faq-wrap">
    <div class="section-head reveal"><p class="eyebrow">Resolvemos tus dudas</p><h2 class="title" id="{id_}-t">{titulo}</h2></div>
    <div class="faq reveal">{qs}</div>
  </div>
</section>"""


def card_servicio(x, s, a):
    return f"""<a class="svc-card reveal" href="{s}{x["slug"]}/">
  <div class="svc-img"><img src="{a}assets/img/productos/{x["img"]}.webp" alt="" loading="lazy" decoding="async"></div>
  <div class="svc-body">
    <span class="svc-ico">{ic(x["icon"])}</span>
    <h3>{x["nombre"]}</h3>
    <p>{x["resumen"]}</p>
    <span class="svc-more">Ver servicio {ic("arrow")}</span>
  </div>
</a>"""


GALERIA = [
    ("taller-01", "Entrada a la sede de Frenoteca vista desde arriba"),
    ("taller-02", "Entrada principal con el aviso de Frenoteca"),
    ("taller-03", "Camioneta en el elevador del taller"),
    ("taller-04", "Vehículo comercial en revisión"),
    ("taller-05", "Disco de freno Brembo en exhibición"),
    ("taller-06", "Automóvil en el patio del taller"),
    ("taller-07", "Camioneta con el capó abierto en revisión"),
    ("taller-08", "Carro clásico en el patio de Frenoteca"),
    ("taller-09", "Barril de Brembo en el patio"),
    ("taller-10", "El taller de noche, con vehículos listos para entregar"),
]


def jsonld():
    data = {
        "@context": "https://schema.org", "@type": "AutoRepair", "name": "Frenoteca S.A.S.",
        "description": "Repuestos y taller de frenos y suspensión en Medellín.",
        "telephone": "+57 312 833 4755", "email": EMAIL,
        "address": {"@type": "PostalAddress", "streetAddress": "Carrera 50 # 39-87", "addressLocality": "Medellín",
                    "addressRegion": "Antioquia", "addressCountry": "CO"},
        "geo": {"@type": "GeoCoordinates", "latitude": 6.240469, "longitude": -75.571513},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "17:15"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "08:00", "closes": "13:15"}],
        "brand": [{"@type": "Brand", "name": m} for m in MARCAS[:3]],
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>\n'


# ---------------------------------------------------------------- Sitio: inicio
def inicio():
    s, a = "./", "../"
    tarjetas = "".join(card_servicio(x, s, a) for x in SERVICIOS)
    galeria = "".join(
        f'<button class="gal-item" type="button" data-full="{a}assets/img/galeria/{f}.webp" aria-label="Ampliar foto: {alt}"><img src="{a}assets/img/galeria/{f}.webp" alt="{alt}" loading="lazy" decoding="async"></button>'
        for f, alt in GALERIA)
    marcas = "".join(f"<li>{m}</li>" for m in MARCAS)
    body = f"""{cabecera(s, a)}
<main id="contenido">
  <section class="hero on-dark">
    <picture class="hero-bg">
      <source media="(min-width: 800px)" srcset="{a}assets/img/hero.webp" width="1024" height="576">
      <img src="{a}assets/img/hero-movil.webp" width="768" height="1024" alt="Patio de Frenoteca de noche con vehículos listos para entregar" fetchpriority="high">
    </picture>
    <div class="wrap hero-in">
      <p class="eyebrow">Taller y repuestos de frenos</p>
      <h1 class="hero-t">Frenos en Medellín, <em>con más de 35 años</em> de respaldo</h1>
      <p class="lead">Repuestos y taller en un solo lugar: pastillas, discos, campanas, cilindros y mangueras con marcas como Brembo, Bosch e Incolbestos.</p>
      <div class="btn-row">
        <a class="btn btn-rojo btn-lg" href="{wa()}">{ic("wa")} Cotizar por WhatsApp</a>
        <a class="btn btn-borde btn-lg" href="#agenda">{ic("calendar")} Agendar revisión</a>
      </div>
      <p class="hero-call">¿Prefieres hablar? <a href="{CEL_HREF}">{ic("phone")} Llama al {CEL}</a></p>
      <div class="hero-meta">
        <a class="hero-rating" href="{RESENAS}" target="_blank" rel="noopener">
          <span class="stars">{ic("star")}{ic("star")}{ic("star")}{ic("star")}{ic("star")}</span>
          <span><strong>4,6</strong> en Google · 360 reseñas</span>
        </a>
        {estado_horario()}
      </div>
    </div>
  </section>

  <section class="trust" aria-label="Por qué confiar en Frenoteca">
    <ul class="wrap trust-list">
      <li>{ic("award")}<span><strong>+35 años</strong> en frenos</span></li>
      <li>{ic("star")}<span><strong>4,6 ★</strong> 360 reseñas</span></li>
      <li>{ic("tag")}<span><strong>Brembo, Bosch</strong> e Incolbestos</span></li>
      <li>{ic("pin")}<span><strong>Carrera 50</strong> Medellín</span></li>
    </ul>
  </section>

  <section class="section" id="servicios" aria-labelledby="serv-t">
    <div class="wrap">
      <div class="section-head reveal">
        <p class="eyebrow">Nuestros servicios</p>
        <h2 class="title" id="serv-t">Todo el sistema de frenos, <em>en un solo lugar</em></h2>
        <p class="lead">Elige lo que necesitas y te enviamos cotización por WhatsApp con el repuesto correcto para tu vehículo.</p>
      </div>
      <div class="svc-grid">{tarjetas}</div>
    </div>
  </section>

  {llamar_cta()}

  <section class="section why bg-negro on-dark" aria-labelledby="why-t">
    <div class="wrap why-grid">
      <div class="why-media reveal">
        <img src="{a}assets/img/galeria/taller-01.webp" alt="Entrada a la sede de Frenoteca en la Carrera 50 de Medellín" width="800" height="450" loading="lazy" decoding="async">
      </div>
      <div class="reveal">
        <p class="eyebrow">Por qué Frenoteca</p>
        <h2 class="title" id="why-t">El repuesto correcto <em>y quien lo instala</em></h2>
        <ul class="why-list">
          <li>{ic("award")}<div><h3>Más de 35 años en frenos</h3><p>Nos dedicamos a una sola cosa y la conocemos a fondo.</p></div></li>
          <li>{ic("tag")}<div><h3>Marcas que responden</h3><p>Brembo, Bosch, Incolbestos e importadas, originales y homologadas.</p></div></li>
          <li>{ic("wrench")}<div><h3>Repuesto y taller juntos</h3><p>Compras e instalas en el mismo lugar, sin vueltas.</p></div></li>
          <li>{ic("shield")}<div><h3>Expertos en blindados</h3><p>Formulaciones especiales para vehículos que pesan más.</p></div></li>
        </ul>
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="pasos-t">
    <div class="wrap">
      <div class="section-head reveal">
        <p class="eyebrow">Así de fácil</p>
        <h2 class="title" id="pasos-t">De la cotización <em>a frenar tranquilo</em></h2>
      </div>
      <ol class="steps">
        <li class="reveal"><span class="step-n">1</span><h3>Escríbenos</h3><p>Por WhatsApp o llamada, con la marca, el modelo y el año de tu vehículo.</p></li>
        <li class="reveal"><span class="step-n">2</span><h3>Cotizamos</h3><p>Te decimos qué referencia necesitas y cuánto cuesta.</p></li>
        <li class="reveal"><span class="step-n">3</span><h3>Revisamos</h3><p>Traes el vehículo a la Carrera 50 y lo revisamos en el taller.</p></li>
        <li class="reveal"><span class="step-n">4</span><h3>Entregamos</h3><p>Instalamos, probamos los frenos y te lo entregamos listo.</p></li>
      </ol>
    </div>
  </section>

  <section class="section bg-gris" aria-labelledby="marcas-t">
    <div class="wrap duo">
      <a class="duo-card reveal" href="{s}marcas/">
        <p class="eyebrow">Marcas</p>
        <h2 class="duo-t" id="marcas-t">Distribuidores de las marcas que conoces</h2>
        <ul class="brands">{marcas}</ul>
        <span class="svc-more">Ver marcas {ic("arrow")}</span>
      </a>
      <a class="duo-card duo-dark on-dark reveal" href="{s}blindados/">
        <img class="duo-bg" src="{a}assets/img/galeria/taller-07.webp" alt="" loading="lazy" decoding="async">
        <p class="eyebrow">Vehículos blindados</p>
        <h2 class="duo-t">Frenos hechos para el peso extra</h2>
        <p>Formulaciones especiales de pastillas para vehículos blindados.</p>
        <span class="svc-more">Conocer más {ic("arrow")}</span>
      </a>
    </div>
  </section>

  <section class="section" id="taller" aria-labelledby="taller-t">
    <div class="wrap">
      <div class="section-head head-row reveal">
        <div>
          <p class="eyebrow">Nuestro taller</p>
          <h2 class="title" id="taller-t">Así se ve <em>por dentro</em></h2>
        </div>
        <div class="car-nav" aria-hidden="true">
          <button class="car-btn" type="button" data-car="-1" tabindex="-1">{ic("arrow-l")}</button>
          <button class="car-btn" type="button" data-car="1" tabindex="-1">{ic("arrow")}</button>
        </div>
      </div>
    </div>
    <div class="gallery reveal" data-carousel aria-label="Fotos del taller, desliza para ver más">{galeria}</div>
    <dialog class="lightbox" aria-label="Foto del taller">
      <img alt="">
      <button class="lb-btn lb-close" type="button" aria-label="Cerrar">{ic("close")}</button>
      <button class="lb-btn lb-prev" type="button" aria-label="Foto anterior">{ic("arrow-l")}</button>
      <button class="lb-btn lb-next" type="button" aria-label="Foto siguiente">{ic("arrow")}</button>
    </dialog>
  </section>

  <section class="section reviews bg-rojo on-red" aria-labelledby="rev-t">
    <div class="wrap reviews-in reveal">
      <div class="rev-score">
        <span class="rev-num">4,6</span>
        <span class="stars">{ic("star")}{ic("star")}{ic("star")}{ic("star")}{ic("star")}</span>
        <span class="rev-count">360 reseñas en Google</span>
      </div>
      <div>
        <h2 class="title" id="rev-t">Lo que dicen <em>quienes ya vinieron</em></h2>
        <p class="lead">Una de las mejores calificaciones entre los talleres de frenos de Medellín. Léelas tú mismo, o cuéntanos cómo te fue.</p>
        <div class="btn-row">
          <a class="btn btn-blanco" href="{RESENAS}" target="_blank" rel="noopener">Leer reseñas en Google {ic("arrow")}</a>
        </div>
      </div>
    </div>
  </section>

  {agenda()}
  {visitanos(s, a)}
  {faq_html([
      ("¿Necesito cita?", "Puedes llegar en nuestro horario, pero si agendas por WhatsApp te esperamos y el servicio es más rápido."),
      ("¿Venden solo el repuesto?", "Sí. Puedes comprar el repuesto y llevártelo, o dejar que lo instalemos en el taller."),
      ("¿Trabajan con vehículos blindados?", "Sí. Tenemos formulaciones especiales de pastillas para blindados."),
      ("¿Qué marcas manejan?", "Brembo, Bosch, Incolbestos y un amplio portafolio de marcas importadas, en referencias originales y homologadas."),
      ("¿Cuál es el horario?", "Lunes a viernes de 8:00 a. m. a 5:15 p. m. y sábados de 8:00 a. m. a 1:15 p. m., en jornada continua."),
  ])}
</main>
{pie(s, a)}"""
    return documento(
        title="Frenoteca | Frenos en Medellín: repuestos y taller desde hace más de 35 años",
        desc="Pastillas, discos, campanas, cilindros y mangueras de freno con Brembo, Bosch e Incolbestos. Taller de frenos y suspensión en la Carrera 50, Medellín. 4,6 ★ en Google.",
        css="sitio.css", body=body, a=a, og="og-sitio.jpg", body_class="sitio", extra_head=jsonld())


# ---------------------------------------------------------------- Sitio: páginas de servicio
def servicio(x):
    s, a = "../", "../../"
    listas = "".join(
        f"""<div class="list-card reveal"><h2 class="list-t">{t}</h2><ul class="svc-list svc-list-{ico}">{"".join(f"<li>{ic(ico)}<span>{i}</span></li>" for i in items)}</ul></div>"""
        for t, ico, items in x["listas"])
    marcas = ""
    if x.get("marcas"):
        marcas = f"""<ul class="brands brands-lg reveal">{"".join(f"<li>{m}</li>" for m in MARCAS)}</ul>"""
    otros = "".join(card_servicio(o, s, a) for o in TODOS if o["slug"] != x["slug"])
    body = f"""{cabecera(s, a, x["slug"])}
<main id="contenido">
  <section class="svc-hero">
    <div class="wrap">
      <nav class="crumbs" aria-label="Ruta"><a href="{s}">Inicio</a> <span aria-hidden="true">/</span> <span aria-current="page">{x["nombre"]}</span></nav>
      <div class="svc-hero-grid">
        <div>
          <p class="eyebrow">{ic(x["icon"])} Frenoteca · Medellín</p>
          <h1 class="svc-h1">{x["h1"]}</h1>
          <p class="lead">{x["intro"]}</p>
          <div class="btn-row">
            <a class="btn btn-rojo btn-lg" href="{wa(x["msg"], x["code"])}">{ic("wa")} Cotizar por WhatsApp</a>
            <a class="btn btn-borde btn-lg" href="{CEL_HREF}">{ic("phone")} Llamar</a>
          </div>
          <ul class="mini-trust">
            <li>{ic("star")} 4,6 en Google</li>
            <li>{ic("award")} +35 años</li>
            <li>{ic("pin")} Carrera 50</li>
          </ul>
        </div>
        <figure class="svc-hero-img"><img src="{a}assets/img/productos/{x["img"]}.webp" alt="{x["nombre"]}" fetchpriority="high"></figure>
      </div>
    </div>
  </section>
  <section class="section section-tight bg-gris">
    <div class="wrap">
      {marcas}
      <div class="lists">{listas}</div>
    </div>
  </section>
  {llamar_cta(f"¿Necesitas {x['msg']}?", "Llámanos y te confirmamos la referencia y el precio para tu vehículo.")}
  {agenda(x["slug"])}
  {faq_html(x["faq"])}
  <section class="section section-tight bg-gris" aria-labelledby="otros-t">
    <div class="wrap">
      <div class="section-head reveal"><p class="eyebrow">También te ayudamos con</p><h2 class="title" id="otros-t">Otros <em>servicios</em></h2></div>
    </div>
    <div class="svc-rail" data-rail>{otros}</div>
  </section>
  {visitanos(s, a, x["code"], x["msg"])}
</main>
{pie(s, a, x["code"], x["msg"], "../../")}"""
    return documento(title=f'{x["title"]} | Frenoteca', desc=x["intro"][:155],
                     css="sitio.css", body=body, a=a, og="og-sitio.jpg", body_class="sitio")


# ---------------------------------------------------------------- Propuesta
def propuesta():
    a, s = "", "sitio/"
    cta = f'<a class="btn btn-rojo btn-lg" href="{s}">Sí, quiero ver mi página {ic("arrow")}</a>'
    paginas = "".join(f"<li>{ic(x['icon'])}{x['nombre']}</li>" for x in TODOS)
    incluye = [
        ("mobile", "Diseño pensado primero para el celular", "Con la identidad de Frenoteca: su logo, su rojo y su tipografía."),
        ("layers", "Inicio y una página por servicio", "Pastillas, discos, campanas y zapatas, cilindros, mangueras, taller y suspensión."),
        ("award", "Página de marcas y de blindados", "Brembo, Bosch, Incolbestos, importadas y formulaciones para blindados."),
        ("star", "Reseñas, fotos reales, mapa y horario", "Su 4,6 ★ de Google, el taller tal como es y cómo llegar en un toque."),
        ("wa", "WhatsApp y llamada siempre a mano", "Botón fijo con un mensaje distinto según el servicio que la persona está viendo."),
        ("calendar", "Agenda en un minuto", "La persona elige servicio, día y franja, y le llega todo listo a WhatsApp."),
        ("bolt", "Carga en menos de 3 segundos", "Imágenes optimizadas y código liviano. Hoy la web tarda 7,8 s."),
        ("search", "SEO técnico y local", "Títulos únicos, datos estructurados de negocio local y sitemap."),
        ("redirect", "Redirecciones", "Para no perder nada de lo que ya está posicionado en Google."),
        ("chart", "Analytics 4, Tag Manager y conversiones", "Conversiones de Google Ads por servicio: se mide el cliente, no el clic."),
        ("text", "Textos redactados por nosotros", "Claros y orientados a vender, con una ronda de ajustes incluida."),
    ]
    incluye_html = "".join(f'<li class="inc reveal">{ic(i)}<div><h3>{t}</h3><p>{d}</p></div></li>' for i, t, d in incluye)
    filas = [
        ("A dónde llegan los anuncios", "Todos al inicio", "Cada anuncio a la página de su servicio"),
        ("Páginas por servicio", "Imágenes sin texto, sin información para Google", "Una página completa por servicio, con texto, señales y preguntas"),
        ("Títulos para Google", "El mismo título de ~700 caracteres en todas", "Un título único y claro por página"),
        ("Velocidad en celular", "7,8 segundos", "Objetivo: menos de 3 segundos"),
        ("WhatsApp", "El mismo mensaje desde cualquier página", "Mensaje y código según el servicio y el origen"),
        ("Agendar", "No hay forma de agendar", "Agenda en un minuto directo a WhatsApp"),
        ("Reseñas y confianza", "No aparecen en la web", "4,6 ★ y 360 reseñas visibles desde el primer pantallazo"),
        ("Datos de contacto", "4 teléfonos y años distintos según dónde se lea", "Nombre, dirección, teléfono y horario iguales en todos los canales"),
        ("Medición", "Clics en botones", "Conversaciones y clientes reales"),
    ]
    filas_html = "".join(
        f'<div class="cmp-row reveal" role="row"><div class="cmp-k" role="rowheader">{k}</div><div class="cmp-antes" role="cell"><span class="cmp-lbl">Hoy</span>{ic("x")}<span>{h}</span></div><div class="cmp-despues" role="cell"><span class="cmp-lbl">Nuevo sitio</span>{ic("check")}<span>{n}</span></div></div>'
        for k, h, n in filas)
    body = f"""<a class="skip" href="#contenido">Saltar al contenido</a>
<header class="p-header on-red">
  <div class="wrap p-header-in">
    {logo(a)}
    <span class="p-tag">Propuesta de sitio web</span>
  </div>
</header>
<main id="contenido">
  <section class="p-hero on-dark">
    <picture class="p-hero-bg">
      <source media="(min-width: 800px)" srcset="assets/img/aerea-1600.webp">
      <img src="assets/img/hero-movil.webp" alt="" width="768" height="1024" fetchpriority="high">
    </picture>
    <div class="wrap p-hero-grid"><div class="p-hero-in">
      <p class="eyebrow">Propuesta para Frenoteca S.A.S.</p>
      <h1 class="p-title">Tienen la reputación. <em>Les falta una web que la convierta en clientes.</em></h1>
      <p class="lead">Más de tres décadas, 4,6 ★ en Google y marcas como Brembo y Bosch. Les proponemos un sitio nuevo, rápido y pensado para el celular, donde cada anuncio lleva a su servicio y cada contacto se mide.</p>
      <div class="btn-row">
        {cta}
        <a class="btn btn-borde btn-lg" href="#incluye">Qué incluye</a>
      </div>
      <p class="p-hero-note">La página ya está hecha: es navegable y usa su marca, sus fotos y sus datos reales. · Rev Up Agency Group, 30 de septiembre de 2026</p>
    </div>
    <a class="p-phone p-phone-hero" href="{s}" tabindex="-1" aria-hidden="true"><span class="p-screen"><iframe src="{s}" title="Vista previa" tabindex="-1" scrolling="no"></iframe></span></a>
    </div>
  </section>

  <section class="section" aria-labelledby="enc-t">
    <div class="wrap">
      <div class="section-head reveal">
        <p class="eyebrow">01 · Lo que encontramos</p>
        <h2 class="title" id="enc-t">Un gran taller <em>con una web que lo frena</em></h2>
        <p class="lead">Revisamos su pauta, su sitio y su perfil de Google. El activo está; no se está aprovechando.</p>
      </div>
      <ul class="stats">
        <li class="stat reveal"><span class="stat-n">4,6 ★</span><p>360 reseñas, mejor que la mayoría de la competencia</p></li>
        <li class="stat stat-bad reveal"><span class="stat-n">7,8 s</span><p>de carga de la web; lo recomendado es menos de 3</p></li>
        <li class="stat stat-bad reveal"><span class="stat-n">1</span><p>sola página de destino: todos los anuncios llevan al inicio</p></li>
        <li class="stat stat-bad reveal"><span class="stat-n">217</span><p>«conversiones» que en realidad son clics en botones</p></li>
      </ul>
      <div class="findings">
        <article class="finding reveal"><span class="finding-n">1</span><div><h3>Casi no aparecen cuando buscan frenos</h3><p>En «frenos Medellín», «taller de frenos» o «discos de frenos» salen otros. Frenoteca aparece cuando la buscan por su nombre: gente que ya la conoce.</p></div></article>
        <article class="finding reveal"><span class="finding-n">2</span><div><h3>La web frena a los anuncios</h3><p>No hay páginas por servicio, todas tienen el mismo título y el WhatsApp manda el mismo mensaje desde cualquier lugar.</p></div></article>
        <article class="finding reveal"><span class="finding-n">3</span><div><h3>Se mide el clic, no el cliente</h3><p>Nadie sabe cuántos carros entraron al taller por la pauta. Google optimiza con una señal equivocada.</p></div></article>
      </div>
    </div>
  </section>

  <section class="section bg-negro on-dark" id="incluye" aria-labelledby="inc-t">
    <div class="wrap">
      <div class="section-head reveal">
        <p class="eyebrow">02 · Lo que vamos a construir</p>
        <h2 class="title" id="inc-t">Un sitio nuevo, <em>diseñado para vender frenos</em></h2>
        <p class="lead">Todo esto está incluido y ya lo pueden probar en la versión navegable.</p>
      </div>
      <ul class="inc-grid">{incluye_html}</ul>
      <div class="pages reveal">
        <h3>Páginas incluidas</h3>
        <ul class="pages-list"><li>{ic("layers")}Inicio</li>{paginas}</ul>
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="flow-t">
    <div class="wrap">
      <div class="section-head reveal">
        <p class="eyebrow">03 · Cómo funciona</p>
        <h2 class="title" id="flow-t">De la búsqueda <em>al carro en el taller</em></h2>
        <p class="lead">Cada anuncio lleva a su página, y cada página abre WhatsApp con un mensaje y un código propios. Así sabemos qué servicio y qué anuncio trajo a cada cliente.</p>
      </div>
      <ol class="flow">
        <li class="reveal">{ic("search")}<div><span class="flow-k">Busca en Google</span><p>«pastillas de freno Medellín»</p></div></li>
        <li class="reveal">{ic("tag")}<div><span class="flow-k">Ve el anuncio</span><p>Con horario, llamada, ubicación y reseñas</p></div></li>
        <li class="reveal">{ic("layers")}<div><span class="flow-k">Llega a su página</span><p>/pastillas: marcas, señales y cotización a un toque</p></div></li>
        <li class="reveal">{ic("wa")}<div><span class="flow-k">Escribe por WhatsApp</span><p>«Quiero cotizar pastillas» + código WEB-PAS</p></div></li>
        <li class="reveal">{ic("car")}<div><span class="flow-k">Entra al taller</span><p>Se registra el servicio y el valor facturado</p></div></li>
      </ol>
      <div class="funnel reveal" aria-label="Lo que muestra cada reporte">
        <span>Clics</span>{ic("arrow")}<span>Conversaciones</span>{ic("arrow")}<span>Carros en el taller</span>{ic("arrow")}<span>Facturado</span>{ic("arrow")}<span class="funnel-end">Costo por cliente</span>
      </div>
    </div>
  </section>

  <section class="section bg-gris" aria-labelledby="cmp-t">
    <div class="wrap">
      <div class="section-head reveal">
        <p class="eyebrow">04 · Antes y después</p>
        <h2 class="title" id="cmp-t">Lo que cambia <em>con el sitio nuevo</em></h2>
      </div>
      <div class="cmp" role="table" aria-label="Comparación entre el sitio actual y el nuevo">
        <div class="cmp-row cmp-head" role="row"><div role="columnheader"><span class="sr-only">Aspecto</span></div><div role="columnheader">Hoy</div><div role="columnheader">Nuevo sitio</div></div>
        {filas_html}
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="proc-t">
    <div class="wrap">
      <div class="section-head reveal">
        <p class="eyebrow">05 · Proceso</p>
        <h2 class="title" id="proc-t">Publicado en <em>3 a 4 semanas</em></h2>
        <p class="lead">Contadas desde que recibamos accesos, fotos y contenido.</p>
      </div>
      <ol class="timeline">
        <li class="reveal"><span class="tl-w">Semana 1</span><h3>Orden</h3><p>Accesos, medición real, datos unificados y estructura de páginas por servicio.</p></li>
        <li class="reveal"><span class="tl-w">Semana 2</span><h3>Diseño y textos</h3><p>Diseño final para celular y computador, textos de cada servicio y fotos del taller.</p></li>
        <li class="reveal"><span class="tl-w">Semana 3</span><h3>Desarrollo</h3><p>Sitio rápido, SEO técnico, WhatsApp por servicio, Analytics y conversiones.</p></li>
        <li class="reveal"><span class="tl-w">Semana 4</span><h3>Ajustes y publicación</h3><p>Una ronda de ajustes, redirecciones y los anuncios apuntando a cada página.</p></li>
      </ol>
      <div class="need reveal">
        <h3>Para empezar necesitamos</h3>
        <ul class="ticks ticks-dark">
          <li>{ic("check")} Acceso al hosting y al dominio</li>
          <li>{ic("check")} Lectura de Google Ads y Analytics, y administración del perfil de Google</li>
          <li>{ic("check")} El WhatsApp que atienden</li>
          <li>{ic("check")} Fotos del taller y de los servicios</li>
        </ul>
        <p class="need-note">La inversión y las condiciones están en el documento de propuesta que les enviamos.</p>
      </div>
    </div>
  </section>

  <section class="p-final bg-rojo on-red" aria-labelledby="fin-t">
    <div class="wrap p-final-in reveal">
      <p class="eyebrow">Ya está lista</p>
      <h2 class="title" id="fin-t">Así se vería <em>Frenoteca en internet</em></h2>
      <p class="lead">Ábrala desde el celular, como la verán sus clientes. Pruebe los botones de WhatsApp, la agenda y las páginas de cada servicio.</p>
      <div class="phones" aria-hidden="true">
        <a class="p-phone" href="{s}pastillas/" tabindex="-1" aria-hidden="true"><span class="p-screen"><iframe src="{s}pastillas/" title="Vista previa" tabindex="-1" scrolling="no" loading="lazy"></iframe></span></a>
        <a class="p-phone p-phone-front" href="{s}" tabindex="-1" aria-hidden="true"><span class="p-screen"><iframe src="{s}" title="Vista previa" tabindex="-1" scrolling="no" loading="lazy"></iframe></span></a>
        <a class="p-phone" href="{s}blindados/" tabindex="-1" aria-hidden="true"><span class="p-screen"><iframe src="{s}blindados/" title="Vista previa" tabindex="-1" scrolling="no" loading="lazy"></iframe></span></a>
      </div>
      <a class="btn btn-negro btn-lg" href="{s}">Sí, quiero ver mi página {ic("arrow")}</a>
      <p class="p-sign">Felipe Restrepo · CEO, Rev Up Agency Group<br><a href="mailto:info@revupagencygroup.com">info@revupagencygroup.com</a> · <a href="https://revupagencygroup.com" target="_blank" rel="noopener">revupagencygroup.com</a><br><span>Propuesta válida por 30 días desde su fecha.</span></p>
    </div>
  </section>
</main>
<footer class="p-footer">
  <div class="wrap"><p>Rev Up Agency Group · Driven by data. Powered by growth.</p></div>
</footer>
<div class="p-sticky" data-sticky>
  <a class="btn btn-rojo btn-block" href="{s}">Sí, quiero ver mi página {ic("arrow")}</a>
</div>"""
    return documento(title="Frenoteca · Propuesta de sitio web | Rev Up Agency Group",
                     desc="Propuesta de Rev Up Agency Group para el nuevo sitio web de Frenoteca: rápido, pensado para el celular y con una página por servicio.",
                     css="propuesta.css", body=body, a=a, og="og-propuesta.jpg", body_class="propuesta")


def escribir(ruta, html):
    ruta = os.path.join(RAIZ, ruta)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(html)
    print("✓", os.path.relpath(ruta, RAIZ))


if __name__ == "__main__":
    escribir("index.html", propuesta())
    escribir("sitio/index.html", inicio())
    for x in TODOS:
        escribir(f"sitio/{x['slug']}/index.html", servicio(x))
