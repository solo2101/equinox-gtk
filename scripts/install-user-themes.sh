#!/usr/bin/env bash
# Install Equinox GTK2, GTK3 and Marco themes for the current user.
# Never change the active GTK theme or Marco theme settings.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
for theme in Equinox-Light Equinox-Dark; do
  for toolkit in gtk-2.0 gtk-3.0 metacity-1; do
    case "$toolkit" in
      gtk-2.0) file=gtkrc ;;
      gtk-3.0) file=gtk.css ;;
      metacity-1) file=metacity-theme-1.xml ;;
    esac
    source="$root/themes/$theme/$toolkit/$file"
    destination="$HOME/.themes/$theme/$toolkit"
    test -f "$source" || { printf 'Missing theme: %s\n' "$source" >&2; exit 1; }
    mkdir -p "$destination"
    if [[ "$toolkit" == "metacity-1" ]]; then
      # Keep authentic original button artwork installed by
      # scripts/install-original-marco.sh, even while the GitHub checkout
      # still has the old generated XML. Previously we overwrote the
      # original theme when users reinstalled GTK2/GTK3.
      if [[ -f "$destination/UPSTREAM.txt" &&
            ! -f "$root/themes/$theme/$toolkit/UPSTREAM.txt" ]]; then
        printf 'Preserved original Marco: %s (not overwriting with provisional XML)\n' "$theme"
        continue
      fi
      # Metacity theme XML references the accompanying original PNG files.
      for asset in "$root/themes/$theme/$toolkit/"*; do
        [[ -f "$asset" ]] || continue
        install -m 0644 "$asset" "$destination/${asset##*/}"
      done
      if [[ ! -f "$root/themes/$theme/$toolkit/UPSTREAM.txt" ]]; then
        printf 'NOTICE: Provisional Marco for %s. Install original button artwork with:\n' "$theme"
        printf '  bash scripts/install-original-marco.sh\n'
      fi
    else
      install -m 0644 "$source" "$destination/$file"
    fi
    printf 'Installed: %s/%s\n' "$theme" "$toolkit"
  done
done

printf '\nGTK2 tests:\n'
printf 'GTK2_RC_FILES="$HOME/.themes/Equinox-Light/gtk-2.0/gtkrc" awf-gtk2\n'
printf 'GTK2_RC_FILES="$HOME/.themes/Equinox-Dark/gtk-2.0/gtkrc" awf-gtk2\n'
printf '\nGTK3 tests:\n'
printf 'GTK_THEME=Equinox-Light awf-gtk3\n'
printf 'GTK_THEME=Equinox-Dark awf-gtk3\n'
printf '\nMarco previews (do not change current window theme):\n'
printf 'marco-theme-viewer Equinox-Light\n'
printf 'marco-theme-viewer Equinox-Dark\n'
printf '\nSet Marco window border only (optional):\n'
printf "gsettings set org.mate.Marco.general theme 'Equinox-Light'\n"
printf "gsettings set org.mate.Marco.general theme 'Equinox-Dark'\n"
