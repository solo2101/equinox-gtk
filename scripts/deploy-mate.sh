#!/usr/bin/env bash
# Apply the tested Equinox theme to this user's Fedora MATE session.
# Usage: bash scripts/deploy-mate.sh light|dark|midnight|restore
# The optional GTK3 frame compatibility module is not globally enabled.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
state="${XDG_STATE_HOME:-$HOME/.local/state}/equinox-gtk"
previous="$state/previous-mate-appearance"
mode="${1:-}"

usage() {
  printf 'Usage: bash scripts/deploy-mate.sh light|dark|midnight|restore\n' >&2
  exit 2
}

case "$mode" in
  light) theme="Equinox-Light"; other="Equinox-Dark" ;;
  dark)  theme="Equinox-Dark"; other="Equinox-Light" ;;
  midnight) theme="Equinox-Evolution-Midnight"; other="Equinox-Light" ;;
  restore) ;;
  *) usage ;;
esac

if ! command -v gsettings >/dev/null 2>&1; then
  echo "gsettings is missing; this script requires a MATE desktop." >&2
  exit 1
fi
if ! gsettings list-schemas | grep -qx 'org.mate.interface' ||
   ! gsettings list-schemas | grep -qx 'org.mate.Marco.general'; then
  echo "MATE desktop settings are unavailable in this session." >&2
  exit 1
fi

if [[ "$mode" == "restore" ]]; then
  if [[ ! -s "$previous" ]]; then
    echo "No previous MATE appearance snapshot exists at: $previous" >&2
    exit 1
  fi
  mapfile -t settings < "$previous"
  if (( ${#settings[@]} != 2 )); then
    echo "Previous appearance snapshot is incomplete." >&2
    exit 1
  fi
  gsettings set org.mate.interface gtk-theme "${settings[0]}"
  gsettings set org.mate.Marco.general theme "${settings[1]}"
  printf 'Restored GTK: %s\n' "$(gsettings get org.mate.interface gtk-theme)"
  printf 'Restored Marco: %s\n' "$(gsettings get org.mate.Marco.general theme)"
  echo 'Restart open applications to pick up the restored GTK theme.'
  exit 0
fi

# Validate before overwriting the currently installed themes.
python3 "$root/scripts/check-gtk3-css.py"
python3 "$root/scripts/check-marco-theme.py"

# The GTK2 engine is a compiled library, not part of the copied theme.
gtk2_version="$(pkg-config --variable=gtk_binary_version gtk+-2.0 2>/dev/null || true)"
gtk2_libdir="$(pkg-config --variable=libdir gtk+-2.0 2>/dev/null || true)"
if [[ -z "$gtk2_version" || -z "$gtk2_libdir" ||
      ! -f "$gtk2_libdir/gtk-2.0/$gtk2_version/engines/libequinox.so" ]]; then
  cat >&2 <<'HELP'
The Equinox GTK2 engine is not installed.
From the repository root, run:
  sudo dnf install -y gcc make gtk2-devel pkgconf-pkg-config
  ./configure --prefix=/usr --libdir=/usr/lib64 --enable-animation
  make -j"$(nproc)"
  sudo make install
  sudo ldconfig
Then rerun: bash scripts/deploy-mate.sh light
HELP
  exit 1
fi

mkdir -p "$state"
if [[ ! -e "$previous" ]]; then
  {
    gsettings get org.mate.interface gtk-theme
    gsettings get org.mate.Marco.general theme
  } > "$previous"
  printf 'Saved previous appearance: %s\n' "$previous"
fi

# Keep a one-time copy of earlier installed Equinox themes.
backup="$state/pre-deployment-themes"
if [[ ! -d "$backup" ]]; then
  mkdir -p "$backup"
  for name in Equinox-Light Equinox-Dark Equinox-Evolution-Midnight; do
    if [[ -d "$HOME/.themes/$name" ]]; then
      cp -a "$HOME/.themes/$name" "$backup/"
    fi
  done
fi

bash "$root/scripts/install-user-themes.sh"

# Reapply even when already selected so Marco notices updated decoration
# artwork. Reopening GTK applications is still necessary for their CSS.
if [[ "$(gsettings get org.mate.Marco.general theme)" == "'$theme'" ]]; then
  gsettings set org.mate.Marco.general theme "$other"
fi
if [[ "$(gsettings get org.mate.interface gtk-theme)" == "'$theme'" ]]; then
  gsettings set org.mate.interface gtk-theme "$other"
fi
gsettings set org.mate.interface gtk-theme "$theme"
gsettings set org.mate.Marco.general theme "$theme"

printf '\nApplied GTK: %s\n' "$(gsettings get org.mate.interface gtk-theme)"
printf 'Applied Marco: %s\n' "$(gsettings get org.mate.Marco.general theme)"
echo 'Icon theme and MATE panel settings were not changed.'
echo 'Restart existing GTK applications to load the updated theme.'
echo 'Rollback: bash scripts/deploy-mate.sh restore'
echo 'Optional GTK3 frame module remains process-scoped, not enabled globally.'
