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
