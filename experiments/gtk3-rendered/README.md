# GTK3 experiment using the original Equinox renderer

This experiment compiles the original src/equinox_draw.c and src/support.c
with a standalone Cairo asset generator, tools/equinox-render-assets.c.
It calls upstream equinox_draw_button(), equinox_draw_entry(), and
equinox_draw_tab() rather than recreating their drawing formulas in CSS.

It exports 16 PNG surfaces per variant for normal, hover, pressed, focused,
disabled, selected, and orientation states. Shade and spot values follow
equinox_style_realize(), with colors from the new GTK2 Equinox themes.
GTK3 uses border-image-slice: 8 fill for nine-slice scaling.

## Build and install on Fedora 43

From the cloned repository:

    sudo dnf install -y gcc gtk2-devel cairo-devel pkgconf-pkg-config
    git pull
    bash scripts/install-rendered-experiment.sh

Installation paths:

- ~/.themes/Equinox-Rendered-Light/gtk-3.0/
- ~/.themes/Equinox-Rendered-Dark/gtk-3.0/

The script does not change your active MATE theme or overwrite the
stable Equinox-Light, Equinox-Dark, or GTK2 engine.

## Test with AWF

    GTK_THEME=Equinox-Rendered-Light awf-gtk3
    GTK_THEME=Equinox-Rendered-Dark awf-gtk3

Compare against GTK2 screenshots. Focus on button bevels, disabled
buttons, entries, and notebook tabs.

## Limitations

- Experimental prototype. Build and CSS parser checks still need to
  run on Fedora 43.
- GTK3 layout geometry differs from GTK2. Nine-slice scaling might
  distort gradients, tab edges, and corners.
- Only buttons, entries, and tabs use original drawing functions yet.
- PNG assets are generated on the Fedora computer, not committed.
- HiDPI scaling requires follow-up work.
