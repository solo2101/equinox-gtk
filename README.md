# Equinox GTK

Modernization of the classic Equinox 1.50 GTK2 theme engine for Fedora Linux and MATE.

## Status

- Original Equinox GTK2 engine compiled, installed, and confirmed loaded on Fedora 43 x86_64.
- Original imported source preserved on the `legacy` branch.
- GTK2 controls: `Equinox-Light` and `Equinox-Dark`, with improved disabled text contrast.
- GTK3 controls: initial CSS implementations of both variants, pending runtime visual testing.
- GTK4 and Marco window borders are not implemented.

## GTK2 engine build

```bash
sudo dnf install gcc make gtk2-devel pkgconf-pkg-config autoconf automake libtool
./configure --prefix=/usr --libdir=/usr/lib64 --enable-animation
make -j"$(nproc)"
sudo make install
```

## Install GTK2 and GTK3 themes without changing MATE settings

```bash
bash scripts/install-user-themes.sh
```

## Test

```bash
GTK2_RC_FILES="$HOME/.themes/Equinox-Light/gtk-2.0/gtkrc" awf-gtk2
GTK2_RC_FILES="$HOME/.themes/Equinox-Dark/gtk-2.0/gtkrc" awf-gtk2
GTK_THEME=Equinox-Light awf-gtk3
GTK_THEME=Equinox-Dark awf-gtk3
```

See [themes/README.md](themes/README.md) for implementation details. GTK3 uses CSS rather than the original GTK2 engine.

## Upstream

Original Equinox 1.50 source and authors, license and change history are preserved in `AUTHORS`, `COPYING`, and `ChangeLog`. The original source uses the GNU Library General Public License v2 or later as specified by the source headers.
