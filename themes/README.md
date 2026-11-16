# Equinox control themes

Equinox 1.50 originally provided a GTK2 engine. The engine source has not been rewritten. These themes add GTK2 control definitions and independent GTK3 CSS implementations using the same visual palette.

| Theme | GTK2 | GTK3 |
| --- | --- | --- |
| Equinox-Light | gtkrc using libequinox.so | gtk.css |
| Equinox-Dark | gtkrc using libequinox.so | gtk.css |

Install both themes for your current user:

```bash
bash scripts/install-user-themes.sh
```

Compare in A Widget Factory:

```bash
GTK2_RC_FILES="$HOME/.themes/Equinox-Light/gtk-2.0/gtkrc" awf-gtk2
GTK2_RC_FILES="$HOME/.themes/Equinox-Dark/gtk-2.0/gtkrc" awf-gtk2
GTK_THEME=Equinox-Light awf-gtk3
GTK_THEME=Equinox-Dark awf-gtk3
```

Each test command launches a separate process. AWF's menus can override its theme at runtime. Close the previous instance before testing a new variant.

The GTK2 themes require the previously built `libequinox.so` in `/usr/lib64/gtk-2.0/2.10.0/engines/`. GTK3 uses CSS and does not load the Equinox GTK2 engine.

The script copies theme files to `~/.themes/`. It does not change the active MATE theme, GTK settings, icon theme, or Marco window decoration. The GTK3 styling is an initial port and still needs visual comparison and runtime testing on Fedora 43. GTK4 and Marco support are not included.

The `legacy` branch preserves the imported original source.

## GTK3 shading parity, refinement 3

The light and dark GTK3 styles now share the same gradient, border, entry, and notebook rules, with variant-specific colors. The button gradient is based on the original `equinox_draw_button()` function. Entry inset shading follows `equinox_draw_entry()`. Selected tabs use the parent surface color as in `equinox_draw_tab()`.

The implementation is an approximation using GTK3 CSS, not a compiled GTK3 version of the GTK2 theme engine. GTK3 adds controls such as switches and uses different widget geometry.

Validate CSS syntax before visual testing:

```bash
python3 scripts/check-gtk3-css.py
```

Run A Widget Factory and compare the states of buttons, text entries, and all four tab orientations. Use the same window size and scaling for the closest comparison.
