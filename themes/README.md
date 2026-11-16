# Equinox GTK2 control themes

These are new theme configurations for the original Equinox 1.50 engine. They do not modify the original C source.

- `Equinox-Light`: neutral gray surfaces, blue selections.
- `Equinox-Dark`: charcoal surfaces, blue selections.

Install locally:

```bash
bash scripts/install-user-themes.sh
```

Launch A Widget Factory separately with either theme (do not change MATE's active theme):

```bash
GTK2_RC_FILES="$HOME/.themes/Equinox-Light/gtk-2.0/gtkrc" awf-gtk2
GTK2_RC_FILES="$HOME/.themes/Equinox-Dark/gtk-2.0/gtkrc" awf-gtk2
```

GTK2 requires the previously compiled `libequinox.so` engine in its GTK2 engine directory. This stage implements **GTK2 controls only**, not a GTK3/GTK4 theme, icon theme, or Marco window borders. In MATE Appearance Preferences, use Customize > Controls to select an available GTK2 controls theme; modern applications will continue to use their respective toolkit themes. AWF can override the test selection using its own theme menus.

The `legacy` branch preserves the original imported source.
