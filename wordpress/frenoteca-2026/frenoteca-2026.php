<?php
/**
 * Plugin Name: Frenoteca 2026
 * Description: Sitio nuevo de Frenoteca (inicio + páginas de servicio). Se enciende en Ajustes → Frenoteca 2026. Desactivar el plugin devuelve el sitio anterior.
 * Version: 1.2.0
 * Author: Rev Up Agency Group
 * Requires PHP: 7.4
 */

defined('ABSPATH') || exit;

const F26_PAGINAS = ['', 'pastillas', 'discos', 'campanas-y-zapatas', 'cilindros', 'mangueras', 'blindados', 'marcas'];
// Direcciones del sitio anterior → página nueva (301, solo con el sitio nuevo encendido)
const F26_REDIRECCIONES = [
    'campanas' => 'campanas-y-zapatas/', 'zapatas-de-frenos' => 'campanas-y-zapatas/',
    'cilindro-maestro' => 'cilindros/', 'cilindro-de-rueda' => 'cilindros/',
    'taller' => '#taller', 'quienes-somos' => '', 'contactenos' => '#cotizar', 'inicio' => '',
];

function f26_activo() {
    return (bool) get_option('f26_activo');
}

// Vista previa para administradores: ?f26=1 la enciende (cookie), ?f26=0 la apaga
function f26_vista_previa() {
    if (!is_user_logged_in() || !current_user_can('manage_options')) return false;
    if (isset($_GET['f26'])) {
        $on = $_GET['f26'] === '1';
        setcookie('f26', $on ? '1' : '', $on ? 0 : 1, COOKIEPATH, COOKIE_DOMAIN, is_ssl(), true);
        return $on;
    }
    return !empty($_COOKIE['f26']);
}

const F26_HOST = 'www.frenoteca.com';
// Parámetros de campañas que no cambian la página (se puede servir rápido aunque vengan en la URL)
const F26_PARAMS_OK = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'gbraid', 'wbraid', 'gad_source', 'gad_campaignid', 'fbclid', 'srsltid'];

/** Ruta pedida, sin la carpeta de WordPress ni barras: '' (inicio), 'pastillas', 'guias/…'. */
function f26_ruta() {
    $home = trim((string) parse_url(home_url('/'), PHP_URL_PATH), '/');
    $ruta = trim((string) parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH), '/');
    if ($home !== '' && strpos($ruta, $home) === 0) $ruta = trim(substr($ruta, strlen($home)), '/');
    return $ruta;
}

/** Archivo de /paginas que corresponde a la ruta, o null si la ruta es de WordPress. */
function f26_archivo($ruta) {
    if (in_array($ruta, F26_PAGINAS, true)) $nombre = $ruta === '' ? 'index' : $ruta;
    elseif ($ruta === 'guias') $nombre = 'guias';
    elseif (preg_match('#^guias/([a-z0-9-]+)$#', $ruta, $m)) $nombre = 'guias--' . $m[1];
    else return null;
    $archivo = __DIR__ . '/paginas/' . $nombre . '.html';
    return is_readable($archivo) ? $archivo : null;
}

/** Atiende la ruta si es del sitio nuevo (redirecciones, sitemap o página) y termina; si no, vuelve. */
function f26_servir($ruta, $previa = false) {
    if ($ruta === 'frenoteca-sitemap.xml') {
        status_header(200);
        header('Content-Type: application/xml; charset=utf-8');
        readfile(__DIR__ . '/paginas/sitemap.xml');
        exit;
    }
    if (array_key_exists($ruta, F26_REDIRECCIONES)) {
        wp_redirect('https://' . F26_HOST . '/' . F26_REDIRECCIONES[$ruta], 301);
        exit;
    }
    $archivo = f26_archivo($ruta);
    if (!$archivo) return;
    status_header(200);
    header('Content-Type: text/html; charset=utf-8');
    if ($previa && !f26_activo()) {
        header('X-Robots-Tag: noindex');
        header('Cache-Control: no-store');
    } else {
        // Páginas estáticas: el navegador las guarda 10 min y el caché de LiteSpeed (si está activo en el servidor) 1 h
        header('Cache-Control: public, max-age=600');
        header('X-LiteSpeed-Cache-Control: public,max-age=3600');
    }
    readfile($archivo);
    exit;
}

// Camino rápido para visitantes: responde antes de cargar el tema y el resto de WordPress (baja el TTFB).
add_action('plugins_loaded', function () {
    if (!f26_activo() || is_admin() || wp_doing_ajax() || wp_doing_cron() || (defined('REST_REQUEST') && REST_REQUEST)) return;
    if (!in_array($_SERVER['REQUEST_METHOD'] ?? 'GET', ['GET', 'HEAD'], true)) return;
    foreach (array_keys($_COOKIE) as $c) {
        if (strpos($c, 'wordpress_logged_in_') === 0) return; // administradores: vista previa y barra de WP por template_redirect
    }
    $ruta = f26_ruta();
    if ($ruta !== 'frenoteca-sitemap.xml' && !array_key_exists($ruta, F26_REDIRECCIONES) && !f26_archivo($ruta)) return;
    // Una sola dirección pública, en un solo salto: https://www.frenoteca.com
    if (!is_ssl() || strtolower($_SERVER['HTTP_HOST'] ?? '') !== F26_HOST) {
        wp_redirect('https://' . F26_HOST . ($_SERVER['REQUEST_URI'] ?? '/'), 301);
        exit;
    }
    if (array_diff(array_keys($_GET), F26_PARAMS_OK)) return; // /?s=, /?p=… siguen siendo de WordPress
    f26_servir($ruta);
}, 1);

// Resto de WordPress: misma dirección canónica (https + www)
add_action('template_redirect', function () {
    if (is_ssl() && strtolower($_SERVER['HTTP_HOST'] ?? '') === F26_HOST) return;
    wp_redirect('https://' . F26_HOST . ($_SERVER['REQUEST_URI'] ?? '/'), 301);
    exit;
}, -1);

// Administradores conectados (y vista previa con ?f26=1)
add_action('template_redirect', function () {
    $previa = f26_vista_previa();
    if (!f26_activo() && !$previa) return;
    $ruta = f26_ruta();
    if ($ruta === '' && (!is_front_page() || is_search() || is_preview())) return; // /?s=, /?p=… siguen siendo de WordPress
    f26_servir($ruta, $previa);
}, 0);

// robots.txt anuncia el mapa del sitio nuevo (el sitemap_index.xml de Yoast responde 404)
add_filter('robots_txt', function ($salida) {
    if (!f26_activo()) return $salida;
    $salida = preg_replace('/^Sitemap:.*$/mi', '', $salida);
    return rtrim($salida) . "\nDisallow: /wp/\nSitemap: https://" . F26_HOST . "/frenoteca-sitemap.xml\n";
}, 99);

// Ajustes → Frenoteca 2026: un interruptor
add_action('admin_menu', function () {
    add_options_page('Frenoteca 2026', 'Frenoteca 2026', 'manage_options', 'f26', 'f26_ajustes');
});
add_action('admin_init', function () {
    register_setting('f26', 'f26_activo', ['type' => 'boolean', 'sanitize_callback' => 'rest_sanitize_boolean']);
});
add_action('update_option_f26_activo', function () {
    do_action('litespeed_purge_all'); // que el caché no siga mostrando la versión anterior
});

function f26_ajustes() { ?>
    <div class="wrap">
        <h1>Frenoteca 2026</h1>
        <p><a class="button" href="<?php echo esc_url(home_url('/?f26=1')); ?>" target="_blank">Ver vista previa</a>
           <a class="button" href="<?php echo esc_url(home_url('/?f26=0')); ?>" target="_blank">Salir de la vista previa</a></p>
        <p>La vista previa solo la ven los administradores. Los visitantes siguen viendo el sitio anterior hasta encender el sitio nuevo.</p>
        <form method="post" action="options.php">
            <?php settings_fields('f26'); ?>
            <label><input type="checkbox" name="f26_activo" value="1" <?php checked(f26_activo()); ?>>
                <strong>Sitio nuevo encendido para todos los visitantes</strong></label>
            <p class="description">Al encenderlo, las direcciones anteriores (campanas, cilindro-maestro, taller, contáctenos…) redirigen a las nuevas.</p>
            <?php submit_button('Guardar'); ?>
        </form>
    </div>
<?php }
