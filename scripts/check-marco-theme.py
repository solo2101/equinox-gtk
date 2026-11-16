#!/usr/bin/env python3
"""Validate Equinox Marco theme XML and local image assets.

Accepts both hand-authored Metacity themes and the original Equinox 1.50
Metacity XML. Use marco-theme-viewer for full renderer validation.
"""
import pathlib
import struct
import sys
import xml.etree.ElementTree as ET

REQUIRED_BUTTONS = {"close", "maximize", "minimize", "menu"}
REQUIRED_STATES = {"normal", "prelight", "pressed"}
WINDOW_TYPES = {"normal", "dialog", "modal_dialog", "menu", "utility", "border"}


def validate(path):
    errors = []
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        return [f"XML error: {exc}"]
    if root.tag != "metacity_theme":
        return ["Incorrect XML root: expected metacity_theme"]

    def by_name(tag):
        found = {}
        for element in root.findall(tag):
            key = element.get("name")
            if not key or key in found:
                errors.append(f"Missing or duplicate {tag} name: {key}")
            found[key] = element
        return found

    geometries = by_name("frame_geometry")
    drawing = by_name("draw_ops")
    styles = by_name("frame_style")
    sets = by_name("frame_style_set")

    for element in root.iter("include"):
        name = element.get("name")
        if name not in drawing:
            errors.append(f"Undefined include operation: {name}")

    seen_images = set()
    for element in root.iter("image"):
        filename = element.get("filename", "")
        if not filename or filename.startswith("theme:"):
            continue
        # Images must be local artwork, never an absolute path or a
        # parent traversal. This also checks the original PNG bytes.
        if pathlib.PurePath(filename).name != filename:
            errors.append(f"Unsafe image path: {filename}")
            continue
        image = path.parent / filename
        if not image.is_file():
            errors.append(f"Missing image asset: {filename}")
        elif filename not in seen_images and filename.lower().endswith(".png"):
            seen_images.add(filename)
            with image.open("rb") as stream:
                header = stream.read(24)
            if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
                errors.append(f"Invalid PNG asset: {filename}")
                continue
            width, height = struct.unpack(">II", header[16:24])
            if not (1 <= width <= 512 and 1 <= height <= 512):
                errors.append(f"Unexpected PNG size: {filename} ({width}x{height})")

    # All authored titlebar buttons must use the original image sprites.
    # The previous hand-drawn circles passed XML validation but did not
    # reproduce the original artwork.
    for name, ops in drawing.items():
        if name.startswith("button_") and name != "button_blank":
            if len(ops.findall("image")) < 2:
                errors.append(f"{name}: expected PNG background and icon")

    for name, style in styles.items():
        geometry = style.get("geometry")
        parent = style.get("parent")
        if geometry and geometry not in geometries:
            errors.append(f"{name}: missing frame geometry {geometry}")
        if parent and parent not in styles:
            errors.append(f"{name}: missing parent frame style {parent}")
        for item in style.findall("piece") + style.findall("button"):
            ref = item.get("draw_ops")
            if ref and ref not in drawing:
                errors.append(f"{name}: missing drawing operation {ref}")

        # Marco v1 demands button slots even for border-only frames.
        slots = set()
        current = style
        visited = set()
        while current is not None:
            key = current.get("name")
            if key in visited:
                errors.append(f"{name}: cyclic frame_style inheritance")
                break
            visited.add(key)
            slots.update(
                (b.get("function"), b.get("state"))
                for b in current.findall("button")
            )
            current = styles.get(current.get("parent"))
        for func in REQUIRED_BUTTONS:
            for state in REQUIRED_STATES:
                if (func, state) not in slots:
                    errors.append(f"{name}: missing {func}/{state} button slot")

    for name, style_set in sets.items():
        parent = style_set.get("parent")
        if parent and parent not in sets:
            errors.append(f"{name}: missing frame_style_set parent {parent}")
        for frame in style_set.findall("frame"):
            ref = frame.get("style")
            if ref not in styles:
                errors.append(f"{name}: missing frame style {ref}")

    windows = {w.get("type"): w.get("style_set") for w in root.findall("window")}
    for kind in WINDOW_TYPES:
        if kind not in windows:
            errors.append(f"Missing window type: {kind}")
        elif windows[kind] not in sets:
            errors.append(f"{kind}: undefined frame style set {windows[kind]}")
    return errors


def main():
    root = pathlib.Path(__file__).resolve().parent.parent
    variants = ("Equinox-Light", "Equinox-Dark")
    failed = False
    for variant in variants:
        path = root / "themes" / variant / "metacity-1" / "metacity-theme-1.xml"
        errors = validate(path)
        if errors:
            failed = True
            print(f"FAIL: {path}")
            for msg in errors:
                print(f"  {msg}")
        else:
            print(f"PASS: {path}")
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
