#!/usr/bin/env python3
"""Verify Midnight Caja's 1px grooves follow original Equinox GTK2 separators."""
from pathlib import Path
import re

root = Path(__file__).resolve().parent.parent
css = (root / "themes/Equinox-Evolution-Midnight/gtk-3.0/gtk.css").read_text()
source = (root / "src/equinox_draw.c").read_text()

start = source.index("equinox_draw_separator (")
end = source.index("equinox_draw_list_view_header (", start)
painter = source[start:end]
assert "equinox_shade (&dark, &light, separatorstyle >= 2 ? 1.5 : 1.15)" in painter
assert "equinox_shade (&dark, &dark, 0.68)" in painter
assert "0.6" in painter
assert "@define-color eqx_separatorDark shade(@theme_bg_color, 0.68);" in css
assert "@define-color eqx_separatorLight shade(@theme_bg_color, 1.15);" in css

for selector in (
    ".caja-navigation-window .caja-side-pane > notebook scrolledwindow.frame",
    ".caja-navigation-window .caja-notebook > stack",
    ".caja-navigation-window statusbar",
):
    m = re.search(re.escape(selector) + r"\s*\{([^}]+)\}", css)
    assert m, f"Missing Caja groove: {selector}"
    body = m.group(1)
    assert "border-top: 1px solid @eqx_separatorDark;" in body, selector
    assert "box-shadow: inset 0 1px alpha(@eqx_separatorLight, 0.60);" in body, selector
    for forbidden in ("min-height:", "min-width:", "padding:", "margin:"):
        assert forbidden not in body, f"Do not change Caja geometry: {selector}"

assert ".caja-navigation-window .caja-pathbar button" in css
print("PASS Midnight Caja GTK2 two-stroke separators, untouched layout")
