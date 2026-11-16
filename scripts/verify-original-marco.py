#!/usr/bin/env python3
"""Verify the user-installed Marco themes use original Equinox 1.50 PNG buttons.

Unlike a generic XML parser, this distinguishes authentic upstream artwork
from the earlier hand-drawn Equinox Marco prototype.
"""
import pathlib
import sys
import xml.etree.ElementTree as ET

EXPECTED_ARCHIVE = "32b3cedfbc27e466289aa8a0b6d1f3f964a553956d94bf267bd42c749691823c"


def inspect(theme, root):
    folder = root / theme / "metacity-1"
    xml_path = folder / "metacity-theme-1.xml"
    provenance = folder / "UPSTREAM.txt"
    print(f"\n{theme}: {folder}")
    if not xml_path.is_file():
        print("FAIL: No installed Marco XML.")
        return False
    if not provenance.is_file():
        print("FAIL: This is still the hand-built prototype, not original Equinox 1.50 artwork.")
        print("      Run: bash scripts/install-original-marco.sh")
        return False
    if EXPECTED_ARCHIVE not in provenance.read_text(encoding="utf-8"):
        print("FAIL: Missing expected source archive checksum in UPSTREAM.txt.")
        return False

    try:
        xml = ET.parse(xml_path)
    except ET.ParseError as exc:
        print(f"FAIL: Invalid theme XML: {exc}")
        return False

    pngs = sorted(folder.glob("*.png"))
    refs = set()
    for node in xml.iter("image"):
        value = node.get("filename")
        if value and not value.startswith("theme:"):
            refs.add(value)
    missing = [name for name in refs if not (folder / name).is_file()]
    print(f"Original artwork PNGs: {len(pngs)}")
    print(f"Artwork file references: {len(refs)}")
    if missing:
        print(f"FAIL: Missing button artwork: {', '.join(sorted(missing))}")
        return False
    if len(pngs) < 4 or not refs:
        print("FAIL: Original button PNGs are absent or not referenced by the XML.")
        return False
    print("PASS: Installed theme uses original Equinox 1.50 window-button artwork.")
    return True


def main():
    destination = pathlib.Path.home() / ".themes"
    ok = True
    for variant in ("Equinox-Light", "Equinox-Dark"):
        ok &= inspect(variant, destination)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
