#!/usr/bin/env bash
# Import the real Equinox 1.50 Metacity XML and PNG buttons.
# No GTK2/GTK3 files or active Marco theme setting are changed.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
theme_root="$HOME/.themes"

# First inspect what is already installed. This prevents repeated
# downloads and makes it clear whether the preview uses original PNGs.
if python3 "$root/scripts/verify-original-marco.py"; then
  echo "Authentic Equinox Marco themes are already installed. No changes needed."
  exit 0
fi

if [[ -f "$root/themes/Equinox-Light/metacity-1/UPSTREAM.txt" &&
      -f "$root/themes/Equinox-Dark/metacity-1/UPSTREAM.txt" ]]; then
  echo "Installing original artwork from GitHub checkout."
  bash "$root/scripts/install-user-themes.sh"
else
  archive="$(mktemp --suffix=.tar.gz)"
  trap 'rm -f "$archive"' EXIT
  urls=(
    "https://mirrors.nju.edu.cn/freebsd-ports/distfiles/140449-equinox-themes-1.50.tar.gz"
    "https://mirror.nju.edu.cn/freebsd-ports/distfiles/140449-equinox-themes-1.50.tar.gz"
    "https://mirror.ihost.md/openbsd/distfiles/140449-equinox-themes-1.50.tar.gz"
    "https://distcache.freebsd.org/ports-distfiles/140449-equinox-themes-1.50.tar.gz"
    "https://ftp.ec-m.fr/pub/OpenBSD/distfiles/140449-equinox-themes-1.50.tar.gz"
  )

  if ! command -v curl >/dev/null 2>&1; then
    echo "Install curl first: sudo dnf install curl" >&2
    exit 1
  fi

  ok=0
  for url in "${urls[@]}"; do
    echo "Trying source: $url"
    if curl -fL --retry 2 --connect-timeout 10 --max-time 45 \
         -o "$archive" "$url"; then
      if echo "32b3cedfbc27e466289aa8a0b6d1f3f964a553956d94bf267bd42c749691823c  $archive" |
          sha256sum --check --status; then
        echo "Upstream archive checksum verified."
        ok=1
        break
      fi
      echo "Rejected archive: checksum does not match original Equinox 1.50." >&2
    fi
  done
  if [[ "$ok" -ne 1 ]]; then
    echo "FAIL: Cannot retrieve the original archive. Your old Marco theme was not replaced." >&2
    exit 1
  fi

  python3 "$root/scripts/import-original-marco.py" "$archive" \
    --destination "$theme_root"
fi

echo
python3 "$root/scripts/verify-original-marco.py"
echo
echo "Preview the original window buttons:"
echo "  marco-theme-viewer Equinox-Light"
echo "  marco-theme-viewer Equinox-Dark"
