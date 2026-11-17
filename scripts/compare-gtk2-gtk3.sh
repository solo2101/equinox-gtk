#!/usr/bin/env bash
# Open two independent A Widget Factory windows, GTK2 and GTK3.
# Usage: bash scripts/compare-gtk2-gtk3.sh [light|dark|midnight]
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
variant="${1:-${GTK_THEME:-light}}"
case "${variant,,}" in
  light|equinox-light) theme="Equinox-Light" ;;
  dark|equinox-dark) theme="Equinox-Dark" ;;
  midnight|equinox-evolution-midnight) theme="Equinox-Evolution-Midnight" ;;
  *) echo "Usage: $0 [light|dark|midnight]" >&2; exit 2 ;;
esac

for app in awf-gtk2 awf-gtk3; do
  if ! command -v "$app" >/dev/null 2>&1; then
    echo "Missing $app. Install with: sudo dnf install -y awf-gtk2 awf-gtk3" >&2
    exit 1
  fi
done

bash "$root/scripts/install-user-themes.sh"
rc="$HOME/.themes/$theme/gtk-2.0/gtkrc"

echo "Opening independent GTK2 and GTK3 windows with $theme..."
GTK2_RC_FILES="$rc" awf-gtk2 &
gtk2_pid=$!
GTK_THEME="$theme" awf-gtk3 &
gtk3_pid=$!
echo "GTK2 PID: $gtk2_pid | GTK3 PID: $gtk3_pid"
echo "Both windows are independent. Move or resize either one as you like."
