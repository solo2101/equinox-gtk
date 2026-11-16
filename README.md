# Equinox GTK

Modernizing the classic Equinox 1.50 theme engine for Fedora and MATE.

## Current status

- **GTK2:** Original C engine compiles and loads on Fedora 43. The original source is preserved on the `legacy` branch.
- **GTK3:** Light and dark themes use source-guided CSS. The GTK3 stylesheets have been consolidated to match the original button shading, entry bevels, notebook tabs, icons, and widget proportions. Runtime testing of the latest pass is still needed.
- **GTK4 and Marco:** Not implemented.

GTK3 does not load the original GTK2 engine. The optional early PNG experiment is archived under `experiments/gtk3-rendered/` for reference, and is not installed by the standard theme installer.

## Build and install the GTK2 engine

```bash
sudo dnf install gcc make gtk2-devel pkgconf-pkg-config autoconf automake libtool
./configure --prefix=/usr --libdir=/usr/lib64 --enable-animation
make -j"$(nproc)"
sudo make install
```

## Install the GTK2 and GTK3 themes

```bash
bash scripts/install-user-themes.sh
python3 scripts/check-gtk3-css.py
```

This copies GTK2 and GTK3 theme files to `~/.themes/` for your user. It does not change the active desktop theme.

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
