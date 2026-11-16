# Equinox GTK

Modernizing the classic Equinox 1.50 theme engine for Fedora and MATE.

## Current status

- **GTK2:** Original C engine compiles and loads on Fedora 43. The original source is preserved on the `legacy` branch.
- **GTK3:** Light and dark themes use source-guided CSS. The GTK3 stylesheets have been consolidated to match the original button shading, entry bevels, notebook tabs, icons, and widget proportions. Runtime testing of the latest pass is still needed.
- **Marco:** Initial light and dark window-decoration themes added. Fedora 43 preview testing is pending.
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

Marco is being switched to the actual **Equinox 1.50 Metacity artwork**
instead of our earlier hand-drawn approximation. Source archive:
`140449-equinox-themes-1.50.tar.gz`, SHA256
`32b3cedfbc27e466289aa8a0b6d1f3f964a553956d94bf267bd42c749691823c`.
The original `Equinox Light` provides the Light window frame, and
`Equinox Evolution Dusk` provides the Dark frame. Original filenames
and button graphics are preserved; GTK2 and GTK3 control themes are untouched.
The blue field shown in `marco-theme-viewer` is the preview background,
not the Marco theme.

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

## Restore the original upstream Marco artwork

For an immediate preview on Fedora 43, use the direct installer. It downloads
and checks the upstream archive before replacing only the two Marco window
border themes in `~/.themes`:

```bash
bash scripts/install-original-marco.sh
marco-theme-viewer Equinox-Light
```

This does not change the selected Marco theme or the GTK controls. The GitHub
import workflow also commits the original assets into the project. Until those
assets appear in your local Git checkout, running the normal
`install-user-themes.sh` afterwards may restore the older provisional XML.


The source's original Metacity decorations are imported into
`themes/Equinox-{Light,Dark}/metacity-1`. The repository workflow
`.github/workflows/import-original-marco.yml` retrieves the upstream
theme archive, checks its SHA256, and commits the original XML/PNG files.

If the assets have not arrived in your checkout yet, you can import them
on Fedora without changing your active Marco theme:

```bash
curl -fL --retry 3 -o /tmp/equinox-themes-1.50.tar.gz \
  https://distcache.freebsd.org/ports-distfiles/140449-equinox-themes-1.50.tar.gz
python3 scripts/import-original-marco.py /tmp/equinox-themes-1.50.tar.gz
bash scripts/install-user-themes.sh
marco-theme-viewer Equinox-Light
```

The importer rejects archives with the wrong SHA256 and checks that
all original XML-referenced images are present. The window theme only
changes if you explicitly set the Marco theme using gsettings.

### Confirm the original Marco buttons, not the placeholder buttons

The first Marco implementation used simplified hand-drawn XML buttons.
The source repository still contains that provisional XML until the original
upstream archive has been successfully imported. An Equinox titlebar gradient
does not prove original button artwork has loaded.

```bash
git pull
bash scripts/install-original-marco.sh
python3 scripts/verify-original-marco.py
marco-theme-viewer Equinox-Light
```

The verification script reports the PNG button count, referenced image count,
and archive provenance. Only a PASS for both variants confirms authentic
Metacity window artwork. A normal GTK theme reinstall now preserves imported
original Marco artwork instead of silently replacing it with synthetic XML.

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
