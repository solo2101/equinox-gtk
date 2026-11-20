#!/usr/bin/env python3
"""Guard Midnight GTK3 notebook colors and edge directions against Equinox GTK2."""
from pathlib import Path
import re

root = Path(__file__).resolve().parent.parent
theme = root / "themes" / "Equinox-Evolution-Midnight"
gtkrc = (theme / "gtk-2.0" / "gtkrc").read_text()
css = (theme / "gtk-3.0" / "gtk.css").read_text()
source = (root / "src/equinox_draw.c").read_text()

assert re.search(r'bg\[NORMAL\]\s*=\s*"#4e4e4e"', gtkrc)
assert re.search(r'bg\[ACTIVE\]\s*=\s*"#3b3b3b"', gtkrc)
assert "equinox_draw_tab (" in source
for factor in ("0.925", "0.90", "1.06"):
    assert factor in source, f"Equinox tab shade {factor} is missing in C source"
assert "@define-color eqx_tabGtk2Inactive #3b3b3b;" in css
assert "shade(@eqx_tabGtk2Inactive, 0.925)" in css
assert "shade(@eqx_tabGtk2Inactive, 0.90) 50%" in css
assert "shade(@theme_bg_color, 1.06) 0%" in css

# Verify all four tab edges rotate the same GTK2 source gradient.
for side, direction in (("bottom", "top"), ("left", "right"), ("right", "left")):
    for state in ("", ":checked"):
        selector = f"notebook > header.{side} > tabs > tab{state}"
        pattern = re.escape(selector) + r"(?:\s*,\s*[^{}]+)?\s*\{([^}]+)\}"
        hit = re.search(pattern, css)
        assert hit, f"Missing {selector}"
        assert f"linear-gradient(to {direction}" in hit.group(1), selector

# Avoid event/click handling changes: this is a paint-only port.
selected = re.search(
    r"notebook\s*>\s*header\s*>\s*tabs\s*>\s*tab:checked,\s*"
    r"notebook\s*>\s*header\s*>\s*tabs\s*>\s*tab:checked:hover\s*\{([^}]+)\}",
    css,
)
assert selected and "background-image: linear-gradient" in selected.group(1)
for unsafe in ("pointer-events:", "min-height:", "min-width:", "margin:", "padding:"):
    assert unsafe not in selected.group(1), f"Selected tab geometry changed: {unsafe}"

print("PASS Midnight notebook: original GTK2 shades, four edge directions, native GTK3 state")
