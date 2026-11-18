#!/usr/bin/env python3
"""Validate the complete five-theme Equinox v2 release tree, without a display."""
import configparser
import pathlib
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
THEMES = ROOT / "themes"
VARIANTS = {
    "Equinox-Evolution": "Equinox Evolution",
    "Equinox-Evolution-Dawn": "Equinox Evolution Dawn",
    "Equinox-Evolution-Dusk": "Equinox Evolution Dusk",
    "Equinox-Light": "Equinox Light",
    "Equinox-Evolution-Midnight": "Equinox Evolution Midnight",
}
IMAGES = (
    "button_inactive.png", "button_normal.png", "button_prelight.png",
    "button_pressed.png", "close.png", "close_inactive.png", "max.png",
    "max_inactive.png", "menu.png", "menu_inactive.png", "min.png",
    "min_inactive.png",
)

def validate_theme(theme, display_name):
    errors = []
    directory = THEMES / theme
    required = {
        "gtk-2.0/gtkrc", "gtk-3.0/gtk.css", "index.theme",
        "metacity-1/metacity-theme-1.xml",
    }
    required.update("metacity-1/" + name for name in IMAGES)
    for name in sorted(required):
        if not (directory / name).is_file():
            errors.append(f"{theme}: missing {name}")
    metadata = directory / "index.theme"
    if metadata.is_file():
        config = configparser.ConfigParser(interpolation=None)
        config.optionxform = str
        try:
            config.read(metadata, encoding="utf-8")
            if config.get("Desktop Entry", "Name") != display_name:
                errors.append(f"{theme}: incorrect display name")
            for key in ("GtkTheme", "MetacityTheme"):
                if config.get("X-GNOME-Metatheme", key) != theme:
                    errors.append(f"{theme}: incorrect {key}")
            if "placeholder" in config.get("Desktop Entry", "Comment", fallback="").lower():
                errors.append(f"{theme}: unfinished placeholder metadata")
        except (configparser.Error, KeyError, ValueError) as exc:
            errors.append(f"{theme}: invalid index.theme: {exc}")
    gtkrc = directory / "gtk-2.0/gtkrc"
    if gtkrc.is_file() and 'engine "equinox"' not in gtkrc.read_text():
        errors.append(f"{theme}: missing original GTK2 engine declaration")
    for name in IMAGES:
        image = directory / "metacity-1" / name
        if not image.is_file():
            continue
        with image.open("rb") as stream:
            header = stream.read(24)
        if len(header) != 24 or header[:8] != b"\x5c\x78\x38\x39PNG\x5c\x72\x5c\x6e\x5c\x78\x31\x61\x5c\x6e":
            errors.append(f"{theme}: invalid PNG {name}")
        else:
            width, height = struct.unpack(">II", header[16:24])
            if not (1 <= width <= 512 and 1 <= height <= 512):
                errors.append(f"{theme}: invalid dimensions {name}")
    return errors

def main():
    actual = {p.name for p in THEMES.iterdir() if p.is_dir()}
    expected = set(VARIANTS)
    errors = [f"unexpected theme folder: {name}" for name in sorted(actual - expected)]
    errors += [f"missing theme folder: {name}" for name in sorted(expected - actual)]
    for name, display in VARIANTS.items():
        if (THEMES / name).is_dir():
            failures = validate_theme(name, display)
            errors.extend(failures)
            print(f"{'FAIL' if failures else 'PASS'}: {name}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return int(bool(errors))

if __name__ == "__main__":
    sys.exit(main())
