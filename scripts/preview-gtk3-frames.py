#!/usr/bin/env python3
"""Compare the four original Equinox frame shades with GTK3.

Run from the repository:
  GTK_THEME=Equinox-Light python3 scripts/preview-gtk3-frames.py

GTK3 does not expose GtkFrame IN/OUT/ETCHED shadow types as separate CSS
classes. This preview explicitly supplies the optional Equinox classes.
It does not modify GTK, your desktop theme, or A Widget Factory.
"""
import sys

try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
except (ImportError, ValueError) as exc:
    raise SystemExit(
        "GTK3 Python bindings unavailable. Install: "
        "sudo dnf install python3-gobject gtk3\n" + str(exc)
    )

FRAMES = (
    ("Shadow in", Gtk.ShadowType.IN, "eqx-shadow-in"),
    ("Shadow out", Gtk.ShadowType.OUT, "eqx-shadow-out"),
    ("Shadow etched in", Gtk.ShadowType.ETCHED_IN, "eqx-shadow-etched-in"),
    ("Shadow etched out", Gtk.ShadowType.ETCHED_OUT, "eqx-shadow-etched-out"),
)


def make_row(title, use_classes):
    group = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
    heading = Gtk.Label(label=title)
    heading.set_xalign(0)
    group.pack_start(heading, False, False, 0)

    row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    for label, shadow_type, css_class in FRAMES:
        frame = Gtk.Frame.new(label)
        frame.set_shadow_type(shadow_type)
        frame.set_size_request(160, 70)
        frame.set_label_align(0.04, 0.5)
        if use_classes:
            frame.get_style_context().add_class(css_class)
        frame.add(Gtk.Box())
        row.pack_start(frame, True, True, 0)
    group.pack_start(row, False, False, 0)
    return group


def main():
    window = Gtk.Window(title="Equinox GTK3 frame comparison")
    window.set_default_size(760, 255)
    window.connect("destroy", Gtk.main_quit)

    content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=18)
    content.set_border_width(12)
    content.pack_start(make_row("Original shadow tones (explicit Equinox classes)",
                                True), False, False, 0)
    content.pack_start(make_row("Standard GTK3 GtkFrame (no extra classes)",
                                False), False, False, 0)
    window.add(content)
    window.show_all()
    Gtk.main()


if __name__ == "__main__":
    sys.exit(main())
