#!/usr/bin/env python3
"""Check Midnight GTK3 bar geometry against the original Equinox 1.50 source."""
from pathlib import Path
import re
from xml.etree import ElementTree as ET

root = Path(__file__).resolve().parent.parent
draw = (root / "src/equinox_draw.c").read_text()
rc = (root / "src/equinox_rc_style.c").read_text()
css = (root / "themes/Equinox-Evolution-Midnight/gtk-3.0/gtk.css").read_text()
renderer = (root / "tools/equinox-render-assets.c").read_text()

assets = root / "themes/Equinox-Evolution-Midnight/gtk-3.0"
def tile(name, width, height, path):
    img = ET.parse(assets / name).getroot()
    assert img.attrib["viewBox"] == f"0 0 {width} {height}"
    shape = img.find("{http://www.w3.org/2000/svg}path")
    assert shape is not None and shape.attrib["d"] == path
    return True

checks = {
    "original uses 2 * fill height for the stripe step":
        re.search(r"stroke_width\s*=\s*height\s*\*\s*2\s*;", draw),
    "original fill gradient middle stop is 45 percent":
        re.search(r"equinox_pattern_add_color_rgb\s*\(pattern,\s*0\.45,\s*&colors->spot\[1\]\)", draw),
    "original default progressbarstyle is non-glassy 0":
        re.search(r"progressbarstyle\s*=\s*0\s*;", rc),
    "GTK3 stripe tile is 2 * fill height and repeats horizontally":
        "background-size: 20px 10px, 100% 100%;" in css
        and "background-repeat: repeat-x, no-repeat;" in css,
    "horizontal tile matches original four-point Cairo polygon":
        tile("equinox-progress-stripes-h.svg", 20, 10, "M10 0 H20 L10 10 H0 Z"),
    "vertical tile rotates original polygon by 90 degrees":
        tile("equinox-progress-stripes-v.svg", 10, 20, "M0 10 V0 L10 10 V20 Z"),
    "GTK3 uses source polygon tiles instead of triangular CSS stripes":
        css.count('url("equinox-progress-stripes-h.svg")') == 2
        and css.count('url("equinox-progress-stripes-v.svg")') == 1
        and "repeating-linear-gradient(135deg" not in css
        and "repeating-linear-gradient(45deg" not in css,
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
print("PASS Midnight progress: original Cairo parallelogram tiles, gradient, and animation")
