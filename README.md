# Equinox GTK

Equinox GTK v2.0 revives the classic Equinox 1.50 theme collection for Fedora MATE. It includes **Equinox Evolution**, **Dawn**, **Dusk**, **Light**, and **Midnight**, with GTK2, GTK3, and Marco window borders.

Developed and tested primarily on **Fedora 43 MATE**.

## Install

Install the build dependencies:

```bash
sudo dnf install -y git gcc make gtk2-devel pkgconf-pkg-config autoconf automake libtool python3
```

Clone the stable release and build the original GTK2 engine:

```bash
git clone --branch production https://github.com/solo2101/equinox-gtk.git
cd equinox-gtk
./configure --prefix=/usr --libdir=/usr/lib64 --enable-animation
make -j"$(nproc)"
sudo make install
sudo ldconfig
```

Install and activate the Light theme:

```bash
bash scripts/deploy-mate.sh light
```

For another variant, run `bash scripts/deploy-mate.sh evolution`, `dawn`, `dusk`, or `midnight`. The script validates the themes, installs all five versions in `~/.themes`, and applies the chosen GTK and Marco appearance. Restart open applications to reload the styling.

Alternatively, install without changing your current theme:

```bash
bash scripts/install-user-themes.sh
```

Then select **Equinox Evolution**, **Equinox Evolution Dawn**, **Equinox Evolution Dusk**, **Equinox Light** (Evolution Light), or **Equinox Evolution Midnight** in MATE **Appearance Preferences**.

## Recommended icons

Equinox looks best with the [**Delft icon family**](https://github.com/madmaxms/iconpack-delft):

- **Equinox Light:** Delft
- **Equinox Evolution:** Delft
- **Equinox Evolution Dawn:** Delft
- **Equinox Evolution Dusk:** Delft-Darkest
- **Equinox Evolution Midnight:** Delft-Darkest

The icons are optional and installed separately. The MATE Appearance Preferences theme entries include these icon selections; the command-line deployment script leaves your existing icons unchanged.

## Project status

| Component | Status |
| --- | --- |
| GTK2 | Original Equinox engine supported |
| GTK3 | All five stylesheets included and CSS-validated |
| Marco | Matching window decorations included |
| GTK4 | Not implemented |

GTK3 uses CSS rather than the original GTK2 drawing engine, so some controls and application-specific layouts differ. The release has automated checks and Fedora 43 MATE visual testing. See [theme documentation](themes/README.md) for previews and component details.

The `production` branch holds the stable release. The `main` branch contains ongoing development. Validate a checkout with `python3 scripts/check-release.py`, `python3 scripts/check-gtk3-css.py`, and `python3 scripts/check-marco-theme.py`.

## Credits

Based on the original Equinox 1.50 project. Original authorship and license details are preserved in [AUTHORS](AUTHORS), [COPYING](COPYING), and [ChangeLog](ChangeLog).
