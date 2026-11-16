#!/usr/bin/env python3
"""Validate Equinox Marco (Metacity v1) XML and internal theme references.

No graphical session needed. This checks structure and references, not the
Marco renderer. Preview the themes with marco-theme-viewer on Fedora 43.
"""
import pathlib
import sys
import xml.etree.ElementTree as ET

REQUIRED_BUTTONS = {"menu", "minimize", "maximize", "close"}
REQUIRED_WINDOWS = {"normal", "dialog", "modal_dialog", "menu", "utility", "border"}
REQUIRED_FRAME_STATES = {
    "normal", "maximized", "shaded", "maximized_and_shaded"
}


def verify(path):
    issues = []
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        return [f"XML error: {exc}"]

    if root.tag != "metacity_theme":
        issues.append("incorrect root element")
    geometries = {e.get("name") for e in root.findall("frame_geometry")}
    frame_styles = {e.get("name"): e for e in root.findall("frame_style")}
    frame_sets = {e.get("name"): e for e in root.findall("frame_style_set")}
    operations = {e.get("name") for e in root.findall("draw_ops")}
    if len(operations) != len(root.findall("draw_ops")):
        issues.append("duplicate draw_ops name")
    if len(frame_styles) != len(root.findall("frame_style")):
        issues.append("duplicate frame_style name")

    for e in root.iter("include"):
        if e.get("name") not in operations:
            issues.append(f"undefined include: {e.get('name')}")
    for e in root.findall("frame_style"):
        parent = e.get("parent")
        if parent and parent not in frame_styles:
            issues.append(f"undefined parent frame style: {parent}")
        if e.get("geometry") and e.get("geometry") not in geometries:
            issues.append(f"undefined frame geometry: {e.get('geometry')}")
        for child in e.findall("piece") + e.findall("button"):
            ref = child.get("draw_ops")
            if ref and ref not in operations:
                issues.append(f"undefined drawing operation: {ref}")

    for e in root.findall("frame_style_set"):
        parent = e.get("parent")
        if parent and parent not in frame_sets:
            issues.append(f"undefined parent frame set: {parent}")
        for child in e.findall("frame"):
            if child.get("style") not in frame_styles:
                issues.append(f"undefined frame style: {child.get('style')}")

    windows = {e.get("type"): e.get("style_set")
               for e in root.findall("window")}
    for kind in sorted(REQUIRED_WINDOWS):
        if kind not in windows:
            issues.append(f"missing window type: {kind}")
        elif windows[kind] not in frame_sets:
            issues.append(f"undefined window style_set: {windows[kind]}")

    # Marco checks EVERY frame_style before loading its frame_style_sets.
    # A border-only frame still needs button slots, even when has_title=false.
    # The previous test checked the four titled styles but missed border_only.
    for name, style in frame_styles.items():
        buttons = {}
        seen = set()
        chain = set()
        current = style
        while current is not None:
            current_name = current.get("name")
            if current_name in chain:
                issues.append(f"{name}: cyclic frame_style parent chain")
                break
            chain.add(current_name)
            for button in current.findall("button"):
                function, state = button.get("function"), button.get("state")
                if (function, state) in seen:
                    continue
                seen.add((function, state))
                buttons.setdefault(function, set()).add(state)
            current = frame_styles.get(current.get("parent"))
        for function in sorted(REQUIRED_BUTTONS):
            # prelight is an optional fallback in Metacity v1; original
            # Equinox supplies it explicitly for consistent hover visuals.
            missing = {"normal", "pressed"} - buttons.get(function, set())
            if missing:
                issues.append(
                    f"{name}: {function} lacks {','.join(sorted(missing))}"
                )

    for name, frame_set in frame_sets.items():
        for focus in ("yes", "no"):
            for state in REQUIRED_FRAME_STATES:
                if not any(
                    x.get("focus") == focus and x.get("state") == state
                    for x in frame_set.findall("frame")
                ):
                    issues.append(f"{name}: missing {focus}/{state} frame")

    return issues


def main():
    root = pathlib.Path(__file__).resolve().parent.parent
    files = [
        root / "themes" / f"Equinox-{variant}" / "metacity-1" / "metacity-theme-1.xml"
        for variant in ("Light", "Dark")
    ]
    failed = False
    for path in files:
        issues = verify(path)
        if issues:
            failed = True
            print(f"FAIL: {path}")
            for issue in issues:
                print(f"  {issue}")
        else:
            print(f"PASS: {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
