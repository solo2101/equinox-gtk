# Equinox Evolution Midnight: release freeze checklist

Target: Fedora 44 MATE. Fedora 43 is the development comparison system.
Source of truth: Fedora 14 Equinox 1.50 GTK2 engine and original rendered appearance.
Development PR: https://github.com/solo2101/equinox-gtk/pull/4

## Freeze rule

The currently approved Midnight appearance is the baseline. No changes to
`themes/Equinox-Evolution-Midnight/gtk-3.0/gtk.css` or its Marco assets
without a reproduced issue and a Fedora 14 comparison. Keep the remaining
four Equinox variants stable. Avoid a wholesale CSS cleanup; removing
apparently duplicated selectors can silently change GTK3 specificity.
Do not merge to the stable `production` branch without visual approval.

## Automated gates

- [ ] GTK3 CSS parses on Fedora 43 and Fedora 44 for all five variants.
- [ ] Original-source parity checks pass: progress, notebook, indicators, Caja
      headers and separators, and Midnight MATE panel tasklist styling.
- [ ] Real X11 GtkNotebook mouse-click tests pass on every tab orientation.
- [ ] Original GTK2 engine builds and rendered-reference assets are verified.
- [ ] Marco theme XML, button-art assets and release metadata validate.

## Fedora 44 MATE visual and functional gates

- [ ] Midnight matches Fedora 14 reference for top chrome (Marco titlebar
      blending into menubar), popup menus, buttons, tabs and progress stripes.
- [ ] Caja in icon/list views: toolbar, breadcrumbs, column headers, Places
      sidebar, file selections, status bar, popup menus, folder navigation.
- [ ] MATE panels on top, bottom, left and right: tasklist buttons, menu
      launchers, applets, active/hover/disabled states, compact spacing.
- [ ] Confirm tab clicks, checkbox/radio activation, menu selections,
      keyboard focus, Caja navigation and window-manager buttons still work.
- [ ] Switch through Evolution, Dawn, Dusk, Light and Midnight; check no
      previously working variant has changed unexpectedly.
- [ ] Capture comparable screenshots at 100% scaling for any mismatch.

## Test without replacing the stable release

```bash
cd ~/Downloads/equinox-midnight-test
git pull
bash scripts/install-user-themes.sh
GTK_THEME=Equinox-Evolution-Midnight awf-gtk3
caja -q && caja ~
```

Select Midnight again in MATE Appearance Preferences after updating the
Marco theme. The script installs user themes but does not switch the active
theme. Keep the production branch unchanged pending the checklist.
