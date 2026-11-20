#!/usr/bin/env python3
"""Keep Midnight tasklist buttons compact on any MATE panel edge."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "themes/Equinox-Evolution-Midnight/gtk-3.0/gtk.css"


def rule(css, selector):
    start = css.find(selector + " {")
    if start < 0:
        raise ValueError(f"missing tasklist selector: {selector}")
    body_start = start + len(selector) + 2
    end = css.find("}", body_start)
    if end < 0:
        raise ValueError(f"unterminated tasklist rule: {selector}")
    return css[body_start:end]


def main():
    css = CSS.read_text()
    base = rule(css, "PanelToplevel button#tasklist-button,\n#PanelPlug button#tasklist-button")
    checks = {
        "one-pixel button frame": "border: 1px solid alpha(@eqx_panelButtonBorder, 0.78);",
        "orientation-neutral corners": "border-radius: 2px;",
        "original dark-to-light gradient stops": "@eqx_panelButtonTop,\n    @eqx_panelButtonBottom",
        "subtle bevel": "box-shadow: inset 0 1px alpha(@eqx_panelFg, 0.07)",
    }
    failures = []
    for label, snippet in checks.items():
        if snippet not in base:
            failures.append(label)
    for forbidden in ("margin:", "padding:", "min-height:", "min-width:", "border: 2px", "0 0 0 1px"):
        if forbidden in base:
            failures.append(f"unwanted tasklist geometry or heavy box: {forbidden}")
    for state in (":hover", ":active", ":checked", ":disabled"):
        if f"PanelToplevel button#tasklist-button{state}" not in css:
            failures.append(f"missing panel {state} state")
        if f"#PanelPlug button#tasklist-button{state}" not in css:
            failures.append(f"missing plug {state} state")
    if failures:
        for failure in failures:
            print(f"FAIL Midnight tasklist: {failure}")
        return 1
    print("PASS Midnight tasklist: slim borders, states, and orientation-neutral geometry")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
