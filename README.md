# Equinox GTK

Modernizing the classic Equinox 1.50 theme engine for Fedora and MATE.

## Current status

- **GTK2:** Original C engine compiles and loads on Fedora 43. The original source is preserved on the `legacy` branch.
- **GTK3:** Light and dark themes use source-guided CSS. The GTK3 stylesheets have been consolidated to match the original button shading, entry bevels, notebook tabs, icons, and widget proportions. Runtime testing of the latest pass is still needed.
- **Marco:** Original Equinox-inspired light and dark decorations actively developed in this repository. The current pass replaces square title buttons with rounded, beveled controls and a dedicated red close button. Fedora 43 preview comparison is pending.
- **GTK4:** Not implemented.

GTK3 does not load the original GTK2 engine. The optional early PNG experiment is archived under `experiments/gtk3-rendered/` for reference, and is not installed by the standard theme installer.

## Build and install the GTK2 engine

```bash
sudo dnf install gcc make gtk2-devel pkgconf-pkg-config autoconf automake libtool
./configure --prefix=/usr --libdir=/usr/lib64 --enable-animation
make -j"$(nproc)"
sudo make install
```

## Install the GTK2, GTK3 and Marco themes

```bash
bash scripts/install-user-themes.sh
python3 scripts/check-gtk3-css.py
```

This copies GTK2, GTK3 and Marco theme files to `~/.themes/` for your user. It does not change the active desktop theme.

## Preview Marco window borders

We maintain the Equinox Marco design directly in
`themes/Equinox-{Light,Dark}/metacity-1/metacity-theme-1.xml`.
This version draws rounded glossy title buttons, custom close/minimize/
maximize symbols, a silver/dark title gradient, and a thin lower groove.
It uses Metacity's native drawing commands, not an external art pack.
The blue background inside `marco-theme-viewer` belongs to the
preview application, not to the window decoration.

```bash
python3 scripts/check-marco-theme.py
bash scripts/install-user-themes.sh
marco-theme-viewer Equinox-Light
marco-theme-viewer Equinox-Dark
```

Previewing does **not** switch your window manager theme. To apply only the
window borders, leaving GTK and icon themes alone:

```bash
gsettings get org.mate.Marco.general theme
gsettings set org.mate.Marco.general theme 'Equinox-Light'
# Or: gsettings set org.mate.Marco.general theme 'Equinox-Dark'
```

The preceding `get` command shows the current theme name for restoring
later. The theme uses Marco's compatible v1 Metacity format under
`metacity-1/metacity-theme-1.xml`. The first pass requires visual
verification with `marco-theme-viewer` on Fedora 43.

### Marco preview rejects the theme with a missing button error

Marco requires close, minimize, maximize, and menu button definitions for
every frame style, even border-only frames. The initial Equinox Marco themes
omitted them from `border_only`. Both variants now include no-op slots.

```bash
git pull
bash scripts/install-user-themes.sh
python3 scripts/check-marco-theme.py
marco-theme-viewer Equinox-Light
```

The structural validator now checks every frame style. The
`Validate Marco Themes` GitHub Actions workflow also attempts to load
both themes with `marco-theme-viewer` under Xvfb.

Your current border theme remains unchanged until you explicitly apply
Equinox using `gsettings set org.mate.Marco.general theme 'Equinox-Light'`.
If the viewer shows another error, use the error's exact line and message
to fix the theme before applying it.

## Optional upstream reference

The `scripts/import-original-marco.py` importer and optional
`install-original-marco.sh` remain available for historical research.
They are **not** part of the current Equinox Marco design workflow.

The original-archive GitHub workflow is manual-only, saves its results as
a reference artifact, and does not overwrite our modified theme files.
Running `bash scripts/install-user-themes.sh` installs the latest
authored design from this checkout. If older upstream artwork was installed
before, the installer saves a one-time backup in
`~/.local/share/equinox-gtk/upstream-marco-backup/`.

## Compare in A Widget Factory

Run the GTK2 and GTK3 versions separately at the same window size and scale:

```bash
GTK2_RC_FILES="$HOME/.themes/Equinox-Light/gtk-2.0/gtkrc" awf-gtk2
GTK_THEME=Equinox-Light awf-gtk3

GTK2_RC_FILES="$HOME/.themes/Equinox-Dark/gtk-2.0/gtkrc" awf-gtk2
GTK_THEME=Equinox-Dark awf-gtk3
```

AWF's status line can retain the last theme it selected from its menus. Launch with the environment overrides shown above, and avoid manually changing the theme inside AWF while comparing.

GTK3 CSS is checked by the `Validate GTK3 CSS` GitHub workflow. See [theme details](themes/README.md).

## Upstream

Original Equinox 1.50 source, authors, license, and history are preserved in `AUTHORS`, `COPYING`, and `ChangeLog`. The original source uses the GNU Library General Public License v2 or later as specified in its source headers.
