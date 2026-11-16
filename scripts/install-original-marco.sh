#!/usr/bin/env bash
# Install authentic Equinox 1.50 Metacity/Marco decorations from upstream.
# Does not change GTK2, GTK3, or the active Marco gsettings theme.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ -f "$root/themes/Equinox-Light/metacity-1/UPSTREAM.txt" ]] &&
   [[ -f "$root/themes/Equinox-Dark/metacity-1/UPSTREAM.txt" ]]; then
  echo "Original Equinox Marco decorations are already in this checkout."
  bash "$root/scripts/install-user-themes.sh"
else
  archive="$(mktemp --suffix=.tar.gz)"
  trap 'rm -f "$archive"' EXIT
  urls=(
    "https://distcache.freebsd.org/ports-distfiles/140449-equinox-themes-1.50.tar.gz"
    "https://ftp.ec-m.fr/pub/OpenBSD/distfiles/140449-equinox-themes-1.50.tar.gz"
    "https://mirror.ihost.md/pub/OpenBSD/distfiles/140449-equinox-themes-1.50.tar.gz"
    "https://mirrors.nju.edu.cn/freebsd-ports/distfiles/140449-equinox-themes-1.50.tar.gz"
  )
  if ! command -v curl >/dev/null 2>&1; then
    echo "Please install curl: sudo dnf install curl" >&2
    exit 1
  fi
  success=0
  for url in "${urls[@]}"; do
    echo "Downloading original Equinox 1.50 themes from $url"
    if curl --fail --silent --show-error --location \
      --connect-timeout 10 --max-time 60 --output "$archive" "$url"; then
      if echo "32b3cedfbc27e466289aa8a0b6d1f3f964a553956d94bf267bd42c749691823c  $archive" |
          sha256sum --check --status; then
        success=1
        break
      fi
      echo "Archive checksum mismatch, trying next mirror." >&2
    fi
  done
  if [[ "$success" -ne 1 ]]; then
    echo "Unable to retrieve the checksum-verified original theme archive." >&2
    exit 1
  fi
  python3 "$root/scripts/import-original-marco.py" "$archive" \
    --destination "$HOME/.themes"
fi

echo
echo "Original Marco window borders installed under ~/.themes."
echo "Preview without changing your current window theme:"
echo "  marco-theme-viewer Equinox-Light"
echo "  marco-theme-viewer Equinox-Dark"
