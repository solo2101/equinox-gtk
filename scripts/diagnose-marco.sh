#!/usr/bin/env bash
# Read-only Equinox / Marco diagnostics for Fedora MATE.
# Usage: bash scripts/diagnose-marco.sh [light|dark] [--preview]
# Does not change or restart window-manager settings.
set -uo pipefail

variant="${1:-light}"
case "${variant,,}" in
  light|equinox-light) theme="Equinox-Light" ;;
  dark|equinox-dark) theme="Equinox-Dark" ;;
  *) echo "Usage: $0 [light|dark] [--preview]" >&2; exit 2 ;;
esac
preview="${2:-}"
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

printf '\n== Window manager ==\n'
if command -v wmctrl >/dev/null 2>&1; then
  wmctrl -m 2>&1 | sed -n '1,5p'
elif command -v xprop >/dev/null 2>&1; then
  xprop -root _NET_SUPPORTING_WM_CHECK 2>&1
else
  echo 'Neither wmctrl nor xprop is installed. Install wmctrl to identify the active WM.'
fi

printf '\n== Active theme settings ==\n'
if command -v gsettings >/dev/null 2>&1; then
  if gsettings list-schemas | grep -qx 'org.mate.Marco.general'; then
    printf 'Marco window theme: '
    gsettings get org.mate.Marco.general theme
  else
    echo 'Marco settings schema is unavailable.'
  fi
  if gsettings list-schemas | grep -qx 'org.mate.interface'; then
    printf 'GTK controls theme: '
    gsettings get org.mate.interface gtk-theme
  fi
else
  echo 'gsettings unavailable.'
fi

printf '\n== Theme files ==\n'
for f in \
  "$root/themes/$theme/metacity-1/metacity-theme-1.xml" \
  "$HOME/.themes/$theme/metacity-1/metacity-theme-1.xml"; do
  if [[ -s "$f" ]]; then
    printf 'FOUND: %s (%s bytes)\n' "$f" "$(wc -c < "$f")"
    if command -v sha256sum >/dev/null 2>&1; then
      sha256sum "$f"
    fi
  else
    echo "MISSING: $f"
  fi
done

printf '\n== Structural validation ==\n'
if command -v python3 >/dev/null 2>&1; then
  python3 "$root/scripts/check-marco-theme.py"
fi

printf '\n== Live viewer ==\n'
if command -v marco-theme-viewer >/dev/null 2>&1; then
  if [[ "$preview" == "--preview" ]]; then
    echo "Opening preview for $theme; close the preview window when done."
    G_MESSAGES_DEBUG=all marco-theme-viewer "$theme"
  else
    echo "Installed: marco-theme-viewer $theme"
    echo "Run: bash scripts/diagnose-marco.sh ${variant,,} --preview"
  fi
else
  echo 'marco-theme-viewer is unavailable. Fedora: sudo dnf install marco'
fi

printf '\nIf the window manager is not Marco, changing org.mate.Marco.general theme will not affect existing window borders.\n'
