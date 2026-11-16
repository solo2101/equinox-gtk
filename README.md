# Equinox GTK

Modernization of the classic Equinox 1.50 GTK2 theme engine for Fedora Linux and MATE.

## Status

- GTK2 engine builds and loads successfully on Fedora 43 x86_64.
- Original 1.50 source preserved on the `legacy` branch.
- GTK2 controls theme configurations: `Equinox-Light` and `Equinox-Dark`.
- GTK3/GTK4 styles and Marco window border themes are not yet implemented.

## Compile GTK2 engine on Fedora 43

```bash
sudo dnf install gcc make gtk2-devel pkgconf-pkg-config autoconf automake libtool
./configure --prefix=/usr --libdir=/usr/lib64 --enable-animation
make -j"$(nproc)"
sudo make install
```

## Install and test GTK2 controls themes

```bash
bash scripts/install-user-themes.sh
GTK2_RC_FILES="$HOME/.themes/Equinox-Light/gtk-2.0/gtkrc" awf-gtk2
GTK2_RC_FILES="$HOME/.themes/Equinox-Dark/gtk-2.0/gtkrc" awf-gtk2
```

Themes are copied to `~/.themes/`, without changing your current MATE settings. More details are in [themes/README.md](themes/README.md).

## Upstream

Original Equinox 1.50 source and its authors, license and change history are preserved in `AUTHORS`, `COPYING`, and `ChangeLog`. The original code uses the GNU Library General Public License v2 or later as stated in its file headers. New theme configuration files follow the repository license terms.

## Next steps

Test light and dark GTK2 rendering, refine colors and states, and develop GTK3 and GTK4 equivalents while preserving the original GTK2 engine.
