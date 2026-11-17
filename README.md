# Equinox GTK

A work-in-progress revival of the classic Equinox theme for MATE, with Light and Dark variants. Includes GTK2, GTK3, and Marco window decorations. GTK4 is not supported.

## Install

Dependencies (Fedora):

```bash
sudo dnf install -y git gcc make gtk2-devel pkgconf-pkg-config autoconf automake libtool python3
```

```bash
git clone --branch production https://github.com/solo2101/equinox-gtk.git
cd equinox-gtk
./configure --prefix=/usr --libdir=/usr/lib64 --enable-animation
make -j"$(nproc)"
sudo make install
sudo ldconfig
bash scripts/install-user-themes.sh
```

Select **Equinox Light** or **Equinox Dark** in MATE Appearance Preferences.

Recommended icons: **Delft** (Light) and **Delft-Darkest** (Dark).

## Status

GTK2 and GTK3 themes are usable. Visual refinements are ongoing. The `production` branch is the stable version; `main` is for development.

Original credits and licensing: [AUTHORS](AUTHORS), [COPYING](COPYING).
