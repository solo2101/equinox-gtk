#!/usr/bin/env bash
# Install Equinox GTK2, GTK3 and Marco themes for the current user.
# Never change the active GTK theme or Marco theme settings.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
for theme in Equinox-Evolution Equinox-Evolution-Dawn Equinox-Evolution-Dusk Equinox-Light Equinox-Evolution-Midnight; do
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
      if [[ "$toolkit" == "gtk-3.0" ]]; then
        install -m 0644 "$root/themes/$theme/gtk-3.0/equinox-grip.svg" "$destination/equinox-grip.svg"
        install -m 0644 "$root/themes/$theme/gtk-3.0/equinox-panel-grip.svg" "$destination/equinox-panel-grip.svg"
      fi
    fi
    printf 'Installed: %s/%s\n' "$theme" "$toolkit"
  done
  # MATE Appearance Preferences requires metatheme metadata at theme root.
  metadata="$root/themes/$theme/index.theme"
  test -f "$metadata" || { printf 'Missing metatheme: %s\n' "$metadata" >&2; exit 1; }
  install -m 0644 "$metadata" "$HOME/.themes/$theme/index.theme"
  printf 'Installed: %s/index.theme\n' "$theme"
done


printf '\nGTK3 previews:\n'
for theme in Equinox-Evolution Equinox-Evolution-Dawn Equinox-Evolution-Dusk Equinox-Light Equinox-Evolution-Midnight; do
  printf 'GTK_THEME=%s awf-gtk3\n' "$theme"
done
