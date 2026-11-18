# Equinox Evolution theme collection

Five original Equinox Evolution variants are available for Fedora MATE.

| Appearance name | Folder / GTK_THEME | GTK2 / GTK3 / Marco |
| --- | --- | --- |
| Equinox Evolution | `Equinox-Evolution` | Included |
| Equinox Evolution Dawn | `Equinox-Evolution-Dawn` | Included |
| Equinox Evolution Dusk | `Equinox-Evolution-Dusk` | Included |
| Equinox Light (Evolution Light) | `Equinox-Light` | Included |
| Equinox Evolution Midnight | `Equinox-Evolution-Midnight` | Included |

All five GTK3 CSS files use the same control rules with variant palettes. 
The GTK2 styles use the original Equinox renderer. Marco uses the original-style PNG artwork.

## Verify and install

```bash
python3 scripts/check-release.py
python3 scripts/check-gtk3-css.py
python3 scripts/check-marco-theme.py
bash scripts/install-user-themes.sh
```

Run a single theme preview:

```bash
GTK_THEME=Equinox-Evolution-Midnight awf-gtk3
GTK_THEME=Equinox-Evolution-Midnight python3 scripts/preview-gtk3-caja-focus.py
```

To compare GTK2 and GTK3, run `bash scripts/compare-gtk2-gtk3.sh midnight`.

GTK3 uses native CSS. Some GTK2 drawing behavior and widget geometry cannot be reproduced exactly. The experimental original-Cairo renderer and GTK3 frame-shadow compatibility module are optional. Neither is required for normal installation. Historical porting notes are in `docs/GTK3-PORTING-HISTORY.md`.
