#!/usr/bin/env bash
# Install only GTK2 controls themes into the current user's theme directory.
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
for theme in Equinox-Light Equinox-Dark; do
  source="$root/themes/$theme/gtk-2.0/gtkrc"
  destination="$HOME/.themes/$theme/gtk-2.0"
  test -f "$source" || { printf 'Missing theme: %s\n' "$source" >&2; exit 1; }
  mkdir -p "$destination"
  install -m 0644 "$source" "$destination/gtkrc"
  printf 'Installed GTK2 controls theme: %s\n' "$theme"
done
printf '\nTest either variant without changing your desktop theme:\n'
printf 'GTK2_RC_FILES="$HOME/.themes/Equinox-Light/gtk-2.0/gtkrc" awf-gtk2\n'
printf 'GTK2_RC_FILES="$HOME/.themes/Equinox-Dark/gtk-2.0/gtkrc" awf-gtk2\n'
