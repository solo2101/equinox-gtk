# GTK3 rendering experiment: conservative pass 2

Status: experimental, and not yet visually validated on Fedora 43.

The first version looked worse than the GTK3 CSS baseline. Why:

- The Equinox GTK2 entry drawing routine paints its parent background into the
  surface. Nine-slice scaling made that background look like a thick inset.
- The GTK2 notebook tab drawing routine deliberately draws outside the tab
  rectangle. Extracting the graphic loses the notebook edge relationship.
- Wide 8px image slices visually inflated widget borders in GTK3.

## What pass 2 changes

- Only ordinary `button.text-button` controls use the original Cairo PNG art.
- Button nine-slice widths are reduced from 8px to 5px.
- Entries, tabs, comboboxes, toolbar icons, and switches use the existing
  GTK3 baseline CSS instead of the generated PNG assets.
- The asset generator still produces all 16 PNGs for future research.

## Test on Fedora 43

    cd ~/Downloads/equinox-gtk
    git pull
    bash scripts/install-rendered-experiment.sh
    GTK_THEME=Equinox-Rendered-Light awf-gtk3

Compare against the stable theme in a separate process:

    GTK_THEME=Equinox-Light awf-gtk3

To test dark instead, use `Equinox-Rendered-Dark` and `Equinox-Dark`.

The experiment installs only to ~/.themes/Equinox-Rendered-*.
It does not change MATE settings or replace your stable themes.

## Goal

See if narrow nine-slice graphics are genuinely better for simple buttons.
If they still look worse than CSS, remove the PNG overrides and continue
with source-guided GTK3 CSS. Matching GTK2 pixel-for-pixel would require
GTK3-specific layout integration, not just exported images.
