#!/usr/bin/env python3
"""Check Midnight GTK3 bar geometry against the original Equinox 1.50 source."""
from pathlib import Path
import re

root = Path(__file__).resolve().parent.parent
draw = (root / "src/equinox_draw.c").read_text()
rc = (root / "src/equinox_rc_style.c").read_text()
css = (root / "themes/Equinox-Evolution-Midnight/gtk-3.0/gtk.css").read_text()
renderer = (root / "tools/equinox-render-assets.c").read_text()

checks = {
    "original uses 2 * fill height for the stripe step":
        re.search(r"stroke_width\s*=\s*height\s*\*\s*2\s*;", draw),
    "original fill gradient middle stop is 45 percent":
        re.search(r"equinox_pattern_add_color_rgb\s*\(pattern,\s*0\.45,\s*&colors->spot\[1\]\)", draw),
    "original default progressbarstyle is non-glassy 0":
        re.search(r"progressbarstyle\s*=\s*0\s*;", rc),
    "GTK3 stripe tile advances 20 px for 10 px fill":
        "background-size: 20px 20px, 100% 100%;" in css,
    "GTK3 horizontal stripe animation advances 20 px":
        "to { background-position: 20px 0px, 0px 0px; }" in css,
    "GTK3 vertical stripe animation follows the length":
        "to { background-position: 0px 20px, 0px 0px; }" in css,
    "GTK3 vertical progress fill uses the vertical animation":
        "animation-name: eqx-progress-flow-vertical;" in css,
    "original Cairo renderer exports horizontal fill":
        'EXPORT("progress-fill-horizontal.png"' in renderer,
    "original Cairo renderer exports vertical fill":
        'EXPORT("progress-fill-vertical.png"' in renderer,
}

for label, passed in checks.items():
    if not passed:
        raise AssertionError(label)
print("PASS Midnight progress: original Cairo geometry, fill mode and GTK3 translation")
