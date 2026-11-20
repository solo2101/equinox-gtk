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


# Original GTK2 gtkrc values above stay checked for every variant.
# Midnight's popup reference is a separate visual match to the Fedora 14 VM.
MIDNIGHT_VM_REFERENCE = {
    "eqx_popupReferenceBg": "#323232",
    "eqx_popupReferenceSelectedTop": "#497dae",
    "eqx_popupReferenceSelectedBottom": "#426c9d",
    "eqx_popupReferenceSeparator": "#424242",
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
        # MATE menu popups live outside the PanelToplevel hierarchy.
        # A broad descendant label rule can override popup category colors.
        # Protect every variant, not only the original Midnight repair.
        if re.search(r"menubar\s*>\s*menuitem\s+label\b", css):
            failures += 1
            print(f"FAIL {theme}: broad menubar text selector may hide popup labels")
        if theme in ("Equinox-Evolution-Dawn", "Equinox-Evolution-Dusk"):
            if not re.search(r"menubar\s*>\s*menuitem\s*>\s*label", css):
                failures += 1
                print(f"FAIL {theme}: missing direct-child menubar label selector")
        if theme == "Equinox-Evolution-Midnight":
            # A descendant label selector also matches MATE Applications popup
            # categories, painting their text dark on the charcoal popup.
            # Limit silver application-menubar text to direct children.
            if re.search(r"menubar\s*>\s*menuitem\s+label\b", css):
                failures += 1
                print("FAIL Midnight: broad menubar label selector hides popup categories")
            if not re.search(r"menubar\s*>\s*menuitem\s*>\s*label", css):
                failures += 1
                print("FAIL Midnight: direct-child menubar label rule missing")
            for key, expected in MIDNIGHT_VM_REFERENCE.items():
                current = find_gtk3(css, key)
                if current != expected:
                    failures += 1
                    print(f"FAIL {theme}: Fedora 14 reference {key} {expected} vs {current}")
            for selector_value in (
                "background-color: @eqx_popupReferenceBg;",
                "background-color: @eqx_popupReferenceSelectedBottom;",
                "@eqx_popupReferenceSelectedTop,",
                "@eqx_popupReferenceSeparator 25%,",
                "@eqx_popupReferenceSeparator 75%,",
            ):
                if selector_value not in css:
                    failures += 1
                    print(f"FAIL {theme}: reference popup rule missing {selector_value}")
            # The open File/Edit/View menubar item should match the popup fill.
            active_item = re.search(
                r"menubar\s*>\s*menuitem:hover,\s*"
                r"menubar\s*>\s*menuitem:selected,\s*"
                r"menubar\s*>\s*menuitem:active\s*\{([^}]+)\}",
                css,
            )
            if active_item is None or (
                "background-color: @eqx_popupReferenceBg;" not in active_item.group(1)
                or "background-image: none;" not in active_item.group(1)
            ):
                failures += 1
                print("FAIL Midnight: active File/Edit/View menubar tab not charcoal")
            # GtkMenu separators should not draw the too-bright white GTK3 rim.
            separator = re.search(r"menu separator,\s*\.menu separator\s*\{([^}]+)\}", css)
            if separator is None or (
                "background-color: transparent;" not in separator.group(1)
                or "box-shadow: none;" not in separator.group(1)
                or "linear-gradient(to right" not in separator.group(1)
            ):
                failures += 1
                print("FAIL Midnight: faded charcoal GtkMenu separator rule missing")
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
