#!/usr/bin/env bash
# Install GTK2 and GTK3 controls themes without changing MATE appearance settings.
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
for theme in Equinox-Light Equinox-Dark; do
  for toolkit in gtk-2.0 gtk-3.0; do
    case "$toolkit" in
      gtk-2.0) file=gtkrc ;;
      gtk-3.0) file=gtk.css ;;
    esac
    source="$root/themes/$theme/$toolkit/$file"
    destination="$HOME/.themes/$theme/$toolkit"
    test -f "$source" || { printf 'Missing theme: %s\n' "$source" >&2; exit 1; }
    mkdir -p "$destination"
    install -m 0644 "$source" "$destination/$file"
    printf 'Installed: %s/%s\n' "$theme" "$toolkit"
  done
done
printf '\nGTK2 tests:\n'
printf 'GTK2_RC_FILES="$HOME/.themes/Equinox-Light/gtk-2.0/gtkrc" awf-gtk2\n'
printf 'GTK2_RC_FILES="$HOME/.themes/Equinox-Dark/gtk-2.0/gtkrc" awf-gtk2\n'
printf '\nGTK3 tests:\n'
printf 'GTK_THEME=Equinox-Light awf-gtk3\n'
printf 'GTK_THEME=Equinox-Dark awf-gtk3\n'
