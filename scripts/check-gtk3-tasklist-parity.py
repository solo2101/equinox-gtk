#!/usr/bin/env python3
"""Guard Fedora 14 Equinox Midnight tasklist styling without touching panel layout."""
import pathlib
import re

CSS = (pathlib.Path(__file__).resolve().parent.parent
       / "themes/Equinox-Evolution-Midnight/gtk-3.0/gtk.css").read_text()

COLORS = {
    "eqx_panelTaskRim": "#696969",
    "eqx_panelTaskPressedRim": "#3f3f3f",
    "eqx_panelTaskPressedTop": "#4b4b4b",
    "eqx_panelTaskPressedBottom": "#414141",
}


def rule(selectors):
    pattern = r"\s*,\s*".join(re.escape(selector) for selector in selectors)
    match = re.search(pattern + r"\s*\{([^}]+)\}", CSS)
    if not match:
        raise AssertionError(f"Missing CSS rule: {selectors}")
    return match.group(1)


for key, color in COLORS.items():
    expected = f"@define-color {key} {color};"
    assert expected in CSS, f"Incorrect Fedora 14 tasklist color: {key}"

normal = rule(["PanelToplevel button#tasklist-button",
               "#PanelPlug button#tasklist-button"])
pressed = rule(["PanelToplevel button#tasklist-button:active",
                "PanelToplevel button#tasklist-button:checked",
                "#PanelPlug button#tasklist-button:active",
                "#PanelPlug button#tasklist-button:checked"])
vertical = rule(["PanelToplevel.vertical button#tasklist-button",
                 "#PanelPlug.vertical button#tasklist-button"])
vertical_pressed = rule(["PanelToplevel.vertical button#tasklist-button:active",
                         "PanelToplevel.vertical button#tasklist-button:checked",
                         "#PanelPlug.vertical button#tasklist-button:active",
                         "#PanelPlug.vertical button#tasklist-button:checked"])

assert "border: 1px" in normal, "Tasklist rim must stay 1px"
assert "border-top-color: @eqx_panelTaskRim;" in normal
assert "@eqx_panelButtonTop, @eqx_panelButtonBottom" in normal
assert "@eqx_panelTaskPressedTop, @eqx_panelTaskPressedBottom" in pressed
assert "border-top-color: @eqx_panelTaskPressedRim;" in pressed
assert "linear-gradient(to right" in vertical
assert "@eqx_panelTaskPressedTop, @eqx_panelTaskPressedBottom" in vertical_pressed
for item in (normal, pressed, vertical, vertical_pressed):
    for prop in ("padding:", "margin:", "min-width:", "min-height:", "width:", "height:"):
        assert not re.search(r"^\s*" + re.escape(prop), item, re.MULTILINE), (
            f"Unexpected tasklist geometry override: {prop}")

print("PASS: Midnight GTK3 tasklist bevel, pressed state, and panel orientations")
