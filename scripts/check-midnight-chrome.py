#!/usr/bin/env python3
"""Guard Midnight window chrome against the Fedora 14 AWF screenshot reference.

The original 24px-high titlebar uses a left-aligned title near x=40, while
the modern centered title was a clear visual mismatch. This check is scoped
to Midnight and intentionally leaves other Equinox variants untouched.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
import re

root = Path(__file__).resolve().parent.parent
theme = root / "themes/Equinox-Evolution-Midnight"
marco = ET.parse(theme / "metacity-1/metacity-theme-1.xml").getroot()
css = (theme / "gtk-3.0/gtk.css").read_text()

drawing = {node.get("name"): node for node in marco.findall("draw_ops")}
for state, text_color in (("focus", "#222222"), ("unfocus", "#777777")):
    title = drawing[f"title_{state}"].find("title")
    assert title is not None
    assert title.get("x") == "40", f"{state} title must align to Fedora 14"
    assert title.get("color") == text_color, f"{state} title text changed"

focus = drawing["titlebar_focus"]
gradient = focus.find("gradient")
assert gradient is not None and gradient.get("type") == "vertical"
stops = [node.get("value") for node in gradient.findall("color")]
assert stops == ["#cecece", "#bebebe", "#aeaeae"], stops
assert focus.find("line").get("color") == "#cfcfcf"

matches = list(re.finditer(r"headerbar,\s*\.titlebar\s*\{([^}]+)\}", css))
assert len(matches) >= 2, "Missing GTK3 titlebar override"
csd = next((m.group(1) for m in matches if "#cecece" in m.group(1)), None)
assert csd is not None, "Missing Midnight client-side titlebar gradient"
for stop in ("#cecece 0%", "#bebebe 50%", "#aeaeae 100%"):
    assert stop in csd, f"GTK3 client-side titlebar missing {stop}"

buttons = (theme / "metacity-1")
for filename in ("button_normal.png", "button_prelight.png",
                 "button_pressed.png", "button_inactive.png"):
    assert (buttons / filename).is_file(), filename
print("PASS Midnight Marco/GTK3 titlebar alignment and matched silver gradients")
