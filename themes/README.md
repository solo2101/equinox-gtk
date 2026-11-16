# Equinox light and dark controls themes

The original Equinox 1.50 engine is GTK2-only. The two GTK3 stylesheets use native GTK3 CSS and do not load `libequinox.so`.

| Variant | GTK2 | GTK3 |
| --- | --- | --- |
| Equinox-Light | Original rendering engine, `gtkrc` | Consolidated `gtk.css` |
| Equinox-Dark | Original rendering engine, `gtkrc` | Consolidated `gtk.css` |

## Install

```bash
bash scripts/install-user-themes.sh
python3 scripts/check-gtk3-css.py
```

The installer copies files under `~/.themes/`, without altering MATE settings or replacing the original engine.

## Compare

```bash
GTK2_RC_FILES="$HOME/.themes/Equinox-Light/gtk-2.0/gtkrc" awf-gtk2
GTK_THEME=Equinox-Light awf-gtk3

GTK2_RC_FILES="$HOME/.themes/Equinox-Dark/gtk-2.0/gtkrc" awf-gtk2
GTK_THEME=Equinox-Dark awf-gtk3
```

Keep the application window size and display scaling consistent between tests.

## GTK3 parity pass 4

The previous stylesheet accumulated several conflicting override layers. Both GTK3 variants now use the same consolidated rules, with different palette values. The changes target:

- Button gradients and edge highlights from the original `equinox_draw_button()` with the default `buttonstyle=0`.
- Inset entry strokes based on `equinox_draw_entry()`.
- Notebook tabs across all four edge orientations, using the GTK3 `notebook > header > tabs > tab` CSS node structure.
- Explicit GTK3 combo-box arrow icons.
- Compact scales, scrollbars, tree-view headers, frame edges, and disabled states.

The target is the original Equinox GTK2 **appearance**, not identical application layouts. GTK3 exposes controls and layout behavior that differ from GTK2. Pixel-perfect replication is not feasible through theme CSS alone.

The earlier nine-slice PNG prototype remains in `experiments/gtk3-rendered/` for reference. The stable light and dark stylesheets do not import its overrides or depend on the exported images.

## Validation

`scripts/check-gtk3-css.py` uses the GTK3 CSS provider parser and reports errors. The repository also includes a Fedora 43 workflow in `.github/workflows/gtk3-css.yml`.

Visual appearance and interaction still need A Widget Factory testing on Fedora 43. Neither test changes your active MATE desktop theme.
