#!/usr/bin/env python3
"""Keep Midnight GTK3 form indicators aligned to original Equinox GTK2."""
from pathlib import Path
import re

root = Path(__file__).resolve().parent.parent
theme = root / "themes/Equinox-Evolution-Midnight"
css = (theme / "gtk-3.0/gtk.css").read_text()
gtkrc = (theme / "gtk-2.0/gtkrc").read_text()
source = (root / "src/equinox_draw.c").read_text()

assert re.search(r"checkradiostyle\s*=\s*0\b", gtkrc)
for symbol in ("equinox_draw_checkbutton", "equinox_draw_radiobutton"):
    function = re.search(r"void\s+" + symbol + r"\s*\([^;]+?\)\s*\{", source, re.S)
    assert function, f"Missing source painter: {symbol}"
    block = source[function.end():function.end() + 1400]
    assert "width = height = 15;" in block, f"{symbol} indicator size changed"
assert "const double ROUNDNESS = 1.75;" in source

def declarations(selector):
    match = re.search(re.escape(selector) + r"\s*\{([^}]+)\}", css)
    assert match, f"Missing GTK3 rule: {selector}"
    return match.group(1)

base = declarations("checkbutton check,\nradiobutton radio")
assert "min-width: 13px;" in base and "min-height: 13px;" in base
assert "border: 1px solid" in base
assert "color: @theme_selected_fg_color;" in base
assert "background-color: @theme_base_color;" in base
assert "border-radius: 2px;" in base
assert "border-radius: 100%;" in declarations("radiobutton radio")

# Hover must never replace a selected mark with the unchecked fill.
assert "check:not(:disabled):not(:checked):not(:indeterminate)" in css
assert "radio:not(:disabled):not(:checked)" in css

checked = declarations("checkbutton check:checked,\ncheckbutton check:indeterminate,\nradiobutton radio:checked")
for state in ("@theme_selected_bg_color", "linear-gradient(to bottom",
              "color: @theme_selected_fg_color;"):
    assert state in checked, f"Missing checked/indeterminate indicator state: {state}"

disabled = declarations(
    "checkbutton check:disabled,\nradiobutton radio:disabled,\n"
    "checkbutton check:checked:disabled,\n"
    "checkbutton check:indeterminate:disabled,\n"
    "radiobutton radio:checked:disabled")
assert "color: @eqx_muted;" in disabled
assert "background-image: none;" in disabled
assert "box-shadow: none;" in disabled
assert "menu menuitem check" in css  # Popup check/radio marks still have their own styling.
print("PASS: Midnight check/radio geometry and GTK2 state-derived styling")
