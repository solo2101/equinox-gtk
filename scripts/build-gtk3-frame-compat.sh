#!/usr/bin/env bash
# Build the optional GTK3 frame-shadow compatibility module for this user.
# Does NOT change the active desktop theme or globally enable GTK modules.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if ! pkg-config --exists gtk+-3.0; then
  echo 'GTK3 development headers missing. Install: sudo dnf install gtk3-devel gcc pkgconf-pkg-config' >&2
  exit 1
fi

out="$HOME/.local/lib/equinox-gtk"
mkdir -p "$out"
gcc -std=c11 -Wall -Wextra -O2 -fPIC -shared \
  $(pkg-config --cflags gtk+-3.0) \
  "$root/src/gtk3/equinox-frame-compat.c" \
  -o "$out/libequinox-frame-compat.so" \
  $(pkg-config --libs gtk+-3.0)

printf 'Built: %s\n' "$out/libequinox-frame-compat.so"
printf '\nTest original GTK3 frame types with:\n'
printf "  GTK_THEME=Equinox-Light GTK3_MODULES='%s/libequinox-frame-compat.so' awf-gtk3\n" "$out"
printf "  GTK_THEME=Equinox-Dark GTK3_MODULES='%s/libequinox-frame-compat.so' awf-gtk3\n" "$out"
printf '\nThis module is opt-in and does not modify normal application startup.\n'
