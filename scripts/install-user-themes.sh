#!/usr/bin/env bash
# Install Equinox GTK2, GTK3 and Marco themes for the current user.
# Never change the active GTK theme or Marco theme settings.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
for theme in Equinox-Light Equinox-Dark Equinox-Evolution-Midnight; do
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
      # The Marco design in this checkout is what users are testing.
      # Never silently skip installing a new iteration. If the optional
      # upstream-artwork importer ran before, preserve it as a reference
      # once, then install the version checked out from GitHub.
      if [[ -f "$destination/UPSTREAM.txt" &&
            ! -f "$root/themes/$theme/$toolkit/UPSTREAM.txt" ]]; then
        backup="$HOME/.local/share/equinox-gtk/upstream-marco-backup/$theme"
        if [[ ! -d "$backup" ]]; then
          mkdir -p "$backup"
          cp -a "$destination/." "$backup/"
          printf 'Saved old imported artwork: %s\n' "$backup"
        fi
        rm -f "$destination/UPSTREAM.txt"
      fi
      for asset in "$root/themes/$theme/$toolkit/"*; do
        [[ -f "$asset" ]] || continue
        install -m 0644 "$asset" "$destination/${asset##*/}"
      done
    else
      install -m 0644 "$source" "$destination/$file"
    fi
    printf 'Installed: %s/%s\n' "$theme" "$toolkit"
  done
  # MATE Appearance Preferences requires metatheme metadata at theme root.
  metadata="$root/themes/$theme/index.theme"
  test -f "$metadata" || { printf 'Missing metatheme: %s\n' "$metadata" >&2; exit 1; }
  install -m 0644 "$metadata" "$HOME/.themes/$theme/index.theme"
  printf 'Installed: %s/index.theme\n' "$theme"
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

printf '\nMidnight theme preview:\n'
printf 'GTK_THEME=Equinox-Evolution-Midnight awf-gtk3\n'
printf 'marco-theme-viewer Equinox-Evolution-Midnight\n'