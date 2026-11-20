#!/usr/bin/env python3
"""Check GTK3 Midnight Caja/list headers against the original Equinox GTK2 C painter."""
from pathlib import Path
import re

root = Path(__file__).resolve().parent.parent
theme = root / "themes/Equinox-Evolution-Midnight"
css = (theme / "gtk-3.0/gtk.css").read_text()
gtkrc = (theme / "gtk-2.0/gtkrc").read_text()
rc_source = (root / "src/equinox_rc_style.c").read_text()
draw = (root / "src/equinox_draw.c").read_text()

assert re.search(r"listviewheaderstyle\s*=\s*0\s*;", rc_source)
assert "listviewheaderstyle" not in gtkrc, "Original Midnight overrides the header style"
assert "equinox_draw_list_view_header" in draw
for fragment in (
    "equinox_shade_shift (&fill, &highlight, 1.05)",
    "equinox_shade_shift (&fill, &fill_darker, 0.92)",
    "equinox_pattern_add_color_rgb (pattern, 0.56, &fill)",
    "fill = colors->bg[GTK_STATE_ACTIVE]",
):
    assert fragment in draw, f"GTK2 reference changed: {fragment}"
for name, value in (("NORMAL", "#4e4e4e"), ("PRELIGHT", "#606060"), ("ACTIVE", "#3b3b3b")):
    assert re.search(rf'bg\[{name}\]\s*=\s*"{value}"', gtkrc)

def block(selector):
    hit = re.search(re.escape(selector) + r"\s*\{([^}]+)\}", css)
    assert hit, f"Missing GTK3 rule: {selector}"
    return hit.group(1)

normal = block("treeview header button")
# This is an existing geometry rule earlier in the file. Find the painting rule.
normal = next((b for b in re.findall(r"treeview header button\s*\{([^}]+)\}", css)
               if "background-image:" in b), None)
assert normal is not None
for term in ("@theme_bg_color", "1.05", "56%", "0.92", "@eqx_columnHeaderText"):
    assert term in normal, f"Incorrect GTK2 header shade: {term}"
assert "@define-color eqx_columnHeaderText #dddddd;" in css
hover = block("treeview header button:hover:not(:checked)")
assert "#606060" in hover
sorted_header = block("treeview header button:checked,\ntreeview header button:checked:hover,\ntreeview header button:active")
assert "#3b3b3b" in sorted_header
disabled = block("treeview header button:disabled")
assert "background-image: none;" in disabled
assert "@eqx_muted" in disabled
for geometry in ("padding:", "min-height:", "min-width:", "margin:"):
    assert geometry not in normal and geometry not in hover and geometry not in sorted_header
print("PASS Midnight Caja headers: source-derived colors, sorted/hover states, native geometry")
