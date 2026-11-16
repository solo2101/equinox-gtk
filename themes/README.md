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

## GTK3 parity pass 5: measured button states

Compared with the GTK2 baseline screenshots from Fedora 43, the GTK2 light
button face transitions approximately from `#e1e1e1` at the upper edge to
`#c4c4c4` at the lower edge. The pressed state transitions from roughly
`#c0c0c0` to `#a8a8a8`. The GTK3 stylesheet now models those slopes in
the correct direction for both variants.

This pass also:
- Adds separate gradients for disabled and pressed-disabled buttons.
- Adds an icon-theme-independent triangle to GTK3 combo-box arrows.
- Aligns active notebook tabs across all four orientations using a 1px
  overlap instead of detached outlines.
- Keeps GTK2 C code and the original GTK3 PNG experiment untouched.

GTK3 changes widget layout and sizing independently of theme CSS. The goal
is to match the controls' paint and states, not the full GTK2 AWF window
geometry. Validate both styles with `python3 scripts/check-gtk3-css.py`,
then compare equal-sized screenshots at the same display scale.

## Independent GTK2/GTK3 comparison windows

The helper launches two separate A Widget Factory processes with the
same variant. It does not tile, resize, or position them. Move each
window to the desired monitor.

```bash
bash scripts/compare-gtk2-gtk3.sh light
bash scripts/compare-gtk2-gtk3.sh dark
```

The first window uses the original GTK2 Equinox engine and the second
uses the GTK3 CSS theme. The script installs the local theme files for
the current user without changing the active MATE theme.


## GTK3 parity pass 6: shared gradients, gray inactive tabs, striped progress

The Fedora AWF side-by-side screenshot revealed that the original GTK2
inactive tabs were noticeably darker than the GTK3 version. The light
variant now uses an inactive tab gradient from `#c3c3c3` to
`#aaaaaa`; selected tabs still join the window background. The dark
variant also uses darker inactive tab shades. Bottom, left, and right
tab gradients follow their respective orientation.

The menu and icon toolbar now use distinct but connected gradients,
with a subtle shadow dividing the toolbar from the application controls.

Progress bars now use full-height beveled troughs, a blue 3-stop
gradient, repeating diagonal bands and a stripe-position animation.
These match the paint layers in the original C functions
`equinox_draw_progressbar_trough()` and
`equinox_draw_progressbar_fill()`, while remaining pure GTK3 CSS.

To compare:

```bash
python3 scripts/check-gtk3-css.py
bash scripts/install-user-themes.sh
GTK2_RC_FILES="$HOME/.themes/Equinox-Light/gtk-2.0/gtkrc" awf-gtk2 & GTK_THEME=Equinox-Light awf-gtk3
```

Visual comparison on the actual Fedora 43 desktop is still required.


## GTK3 parity pass 7: GTK2 toolbar groove, tab bevel, tree progress cells

This pass uses pixel samples from the side-by-side AWF light-theme screenshot:

| Surface | Original GTK2 | Previous GTK3 |
| --- | --- | --- |
| Menubar top | RGB 214 | RGB 230 |
| Menubar lower edge | RGB 202 | RGB 218 |
| Toolbar upper content | RGB 201 | RGB 221 |
| Toolbar lower content | RGB 182 | RGB 189 |
| Groove line | RGB 173 | RGB 164 |
| Highlight line | RGB 226 | RGB 229 |

The light CSS now targets these GTK2 values through shared menu/toolbar
gradient endpoints and a dark groove followed by a light ridge. The dark
variant follows the same ratios from its GTK2 palette.

Inactive notebook tabs use a four-stop orientation-aware gradient with
a subtle upper highlight. Selected tabs retain the page background.

GTK3 treeview progress cells use GtkCellRendererProgress, which supplies
the `.progressbar` and `.trough` style classes rather than the
`progressbar > progress` node layout used by stand-alone progress
widgets. This pass adds separate cell-renderer CSS with blue diagonal
stripes and an inset trough. The tree view's rightmost Progress column
may be clipped when the widget preview is narrow; scroll the table
horizontally to inspect the rendered cells.

As before, the GTK2 engine and original C drawing functions remain
untouched. GTK3's actual cell layout, animation timing, and tab join
geometry are not identical to GTK2 and require runtime verification.


## GTK3 top-edge blending pass 8

The GTK2 engine stays unchanged and remains the appearance reference.
Both GTK3 themes now paint their menubar and toolbar from the outer edge
of each widget allocation, with no left or right frame lines and no extra
container border. The menubar ends at the exact shade where the toolbar
starts, giving a continuous color transition.

The menubar keeps the thin dark bottom groove drawn by original
`equinox_draw_menubar()`. The toolbar keeps its single-pixel top ridge
and subtle bottom shadow from `equinox_draw_toolbar()`. GTK3 client-side
headerbars remain a separate case.

```bash
git pull
python3 scripts/check-gtk3-css.py
bash scripts/install-user-themes.sh
GTK2_RC_FILES="$HOME/.themes/Equinox-Light/gtk-2.0/gtkrc" awf-gtk2 & GTK_THEME=Equinox-Light awf-gtk3
```

Check the menubar directly below the Marco titlebar, especially at the
left/right edges, and the join between the menubar and icon toolbar.
