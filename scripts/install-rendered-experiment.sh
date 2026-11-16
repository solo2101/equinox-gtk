#!/usr/bin/env bash
# Build standalone Cairo PNG assets from original Equinox drawing code.
# Install ONLY experimental GTK3 themes under ~/.themes/.
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! pkg-config --exists gtk+-2.0 cairo; then
  echo 'Missing GTK2/Cairo development libraries. Run: sudo dnf install gcc gtk2-devel cairo-devel pkgconf-pkg-config' >&2
  exit 1
fi

build_dir="$(mktemp -d)"
trap 'rm -rf "$build_dir"' EXIT

gcc -std=gnu99 -O2 -Wno-deprecated-declarations \
  -I"$root/src" \
  $(pkg-config --cflags gtk+-2.0 cairo) \
  "$root/tools/equinox-render-assets.c" \
  "$root/src/equinox_draw.c" \
  "$root/src/support.c" \
  -o "$build_dir/equinox-render-assets" \
  $(pkg-config --libs gtk+-2.0 cairo) -lm

for variant in Light Dark; do
  name="Equinox-Rendered-$variant"
  dest="$HOME/.themes/$name/gtk-3.0"
  mkdir -p "$dest/assets"
  cp "$root/themes/Equinox-$variant/gtk-3.0/gtk.css" "$dest/gtk.css"
  printf '\n' >> "$dest/gtk.css"
  cat "$root/experiments/gtk3-rendered/overrides.css" >> "$dest/gtk.css"
  "$build_dir/equinox-render-assets" "${variant,,}" "$dest/assets"
  printf 'Installed experiment: %s\n' "$name"
done

if command -v python3 >/dev/null && [ -f "$root/scripts/check-gtk3-css.py" ]; then
  python3 "$root/scripts/check-gtk3-css.py" \
    "$HOME/.themes/Equinox-Rendered-Light/gtk-3.0/gtk.css" \
    "$HOME/.themes/Equinox-Rendered-Dark/gtk-3.0/gtk.css"
fi

printf '\nTry:\n'
printf 'GTK_THEME=Equinox-Rendered-Light awf-gtk3\n'
printf 'GTK_THEME=Equinox-Rendered-Dark awf-gtk3\n'
