<?php
/**
 * Plugin Name: Frenoteca 2026
 * Description: Sitio nuevo de Frenoteca (inicio + páginas de servicio). Se enciende en Ajustes → Frenoteca 2026. Desactivar el plugin devuelve el sitio anterior.
 * Version: 1.0.0
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

add_action('template_redirect', function () {
    $previa = f26_vista_previa();
    if (!f26_activo() && !$previa) return;

    $home = trim((string) parse_url(home_url('/'), PHP_URL_PATH), '/');
    $ruta = trim((string) parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH), '/');
    if ($home !== '' && strpos($ruta, $home) === 0) $ruta = trim(substr($ruta, strlen($home)), '/');

    if ($ruta === 'frenoteca-sitemap.xml') {
        header('Content-Type: application/xml; charset=utf-8');
        readfile(__DIR__ . '/paginas/sitemap.xml');
        exit;
    }
    if (array_key_exists($ruta, F26_REDIRECCIONES)) {
        wp_redirect(home_url('/' . F26_REDIRECCIONES[$ruta]), 301);
        exit;
    }
    if (!in_array($ruta, F26_PAGINAS, true)) return; // el resto del WordPress sigue igual
    if ($ruta === '' && (!is_front_page() || is_search() || is_preview())) return; // /?s=, /?p=… siguen siendo de WordPress

    $archivo = __DIR__ . '/paginas/' . ($ruta === '' ? 'index' : $ruta) . '.html';
    if (!is_readable($archivo)) return;
    status_header(200);
    header('Content-Type: text/html; charset=utf-8');
    if ($previa && !f26_activo()) header('X-Robots-Tag: noindex');
    readfile($archivo);
    exit;
}, 0);

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
