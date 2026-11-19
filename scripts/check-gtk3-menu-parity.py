#!/usr/bin/env python3
"""Check GtkMenu palettes match the GTK2 colors for all Equinox variants."""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
THEMES = (
    "Equinox-Evolution",
    "Equinox-Evolution-Dawn",
    "Equinox-Evolution-Dusk",
    "Equinox-Light",
    "Equinox-Evolution-Midnight",
)
VALUES = {
    "bg[NORMAL]": "eqx_popupBg",
    "fg[NORMAL]": "eqx_popupFg",
    "fg[INSENSITIVE]": "eqx_popupDisabled",
    "bg[SELECTED]": "eqx_popupHoverBg",
    "fg[SELECTED]": "eqx_popupHoverFg",
}


def find_gtk2(gtkrc, name):
    pattern = r"^\s*" + re.escape(name) + r'\s*=\s*"(?P<hex>#[0-9a-fA-F]{6})"'
    match = re.search(pattern, gtkrc, re.MULTILINE)
    if match is None:
        raise ValueError(f"missing GTK2 {name}")
    return match.group("hex").lower()


def find_gtk3(css, name):
    pattern = r"^@define-color\s+" + re.escape(name) + r"\s+(#[0-9a-fA-F]{6});"
    matches = re.findall(pattern, css, re.MULTILINE)
    if len(matches) != 1:
        raise ValueError(f"expected one GTK3 {name}, found {len(matches)}")
    return matches[0].lower()


def main():
    failures = 0
    for theme in THEMES:
        gtkrc = (ROOT / "themes" / theme / "gtk-2.0" / "gtkrc").read_text()
        css = (ROOT / "themes" / theme / "gtk-3.0" / "gtk.css").read_text()
        for gtk2_key, gtk3_key in VALUES.items():
            original = find_gtk2(gtkrc, gtk2_key)
            current = find_gtk3(css, gtk3_key)
            if original != current:
                failures += 1
                print(f"FAIL {theme}: {gtk2_key} {original} vs {gtk3_key} {current}")
        if "menu menuitem label" not in css or "menu menuitem:hover label" not in css:
            failures += 1
            print(f"FAIL {theme}: GtkMenu label/selected selectors missing")
        if "PanelToplevel menubar > menuitem" not in css:
            failures += 1
            print(f"FAIL {theme}: panel menu protections missing")
        if failures == 0:
            print(f"PASS {theme}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
