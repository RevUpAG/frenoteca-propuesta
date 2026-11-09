#!/usr/bin/env bash
# Sube una carpeta local al hosting por la API de cPanel (HTTPS, puerto 2083), sin FTP.
# Uso: CPANEL_HOST=frenoteca.com CPANEL_USUARIO=frenoteca CPANEL_TOKEN=… \
#      herramientas/subir_cpanel.sh wordpress/frenoteca-2026 public_html/wp-content/plugins/frenoteca-2026
# El token se crea en cPanel → Seguridad → Administrar tokens de API (se puede revocar cuando quieras).
set -euo pipefail

ORIGEN=${1:?carpeta local}
DESTINO=${2:?carpeta en el hosting, relativa al home}
: "${CPANEL_HOST:?}" "${CPANEL_USUARIO:?}" "${CPANEL_TOKEN:?}"
HOME_REMOTO=${CPANEL_HOME:-/home/$CPANEL_USUARIO}
API="https://$CPANEL_HOST:2083"
AUTH="Authorization: cpanel $CPANEL_USUARIO:$CPANEL_TOKEN"

# Crea una carpeta (si ya existe, cPanel responde error y se ignora)
crear_carpeta() {
  local padre=${1%/*} nombre=${1##*/}
  curl -sS -o /dev/null -H "$AUTH" -G "$API/json-api/cpanel" \
    --data-urlencode cpanel_jsonapi_apiversion=2 --data-urlencode cpanel_jsonapi_module=Fileman \
    --data-urlencode cpanel_jsonapi_func=mkdir --data-urlencode "path=$HOME_REMOTO/$padre" \
    --data-urlencode "name=$nombre"
}

# Crea el destino y todas las subcarpetas, de la más corta a la más larga
ruta=""
IFS=/ read -ra partes <<< "$DESTINO"
for p in "${partes[@]}"; do ruta=${ruta:+$ruta/}$p; crear_carpeta "$ruta"; done
(cd "$ORIGEN" && find . -mindepth 1 -type d | sed 's#^\./##' | sort) | while read -r d; do
  crear_carpeta "$DESTINO/$d"
done

# Sube los archivos de cada carpeta en una sola petición, sobrescribiendo
total=0
while read -r d; do
  args=()
  i=0
  while read -r f; do i=$((i+1)); args+=(-F "file-$i=@$ORIGEN/$f"); done < <(cd "$ORIGEN" && find "./$d" -maxdepth 1 -type f | sed 's#^\./##' | sort)
  [ "$i" -eq 0 ] && continue
  dir_remoto="$HOME_REMOTO/$DESTINO${d:+/$d}"
  dir_remoto=${dir_remoto%/.}
  resp=$(curl -sS -H "$AUTH" -F "dir=$dir_remoto" -F overwrite=1 "${args[@]}" "$API/execute/Fileman/upload_files")
  echo "$resp" | python3 -c 'import json,sys; r=json.load(sys.stdin); sys.exit(0 if r.get("status")==1 else (print(r.get("errors")) or 1))' \
    || { echo "::error::Falló la subida a $dir_remoto"; exit 1; }
  total=$((total+i)); echo "Subidos $i archivos a $dir_remoto"
done < <(cd "$ORIGEN" && { echo .; find . -mindepth 1 -type d | sed 's#^\./##'; } | sort)
echo "Total: $total archivos"
