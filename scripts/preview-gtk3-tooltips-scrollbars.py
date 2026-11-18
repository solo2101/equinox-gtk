#!/usr/bin/env python3
"""Preview GTK3 tooltip and classic scrollbars in all five Equinox themes.

Example: GTK_THEME=Equinox-Light python3 scripts/preview-gtk3-tooltips-scrollbars.py
"""
import gi

gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Preview(Gtk.Window):
    def __init__(self):
        super().__init__(title="Equinox GTK3 Tooltips and Scrollbars")
        self.set_default_size(620, 415)
        self.connect("destroy", Gtk.main_quit)

        panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        panel.set_border_width(12)
        self.add(panel)

        instructions = Gtk.Label(
            label="Hover over the button or list items for tooltips. "
                  "Drag both scrollbars to inspect their gradients."
        )
        instructions.set_line_wrap(True)
        instructions.set_xalign(0)
        panel.pack_start(instructions, False, False, 0)

        button = Gtk.Button(label="Hover here to preview an Equinox tooltip")
        button.set_tooltip_text(
            "Equinox GTK3 tooltip: check the background gradient, "
            "square border, and text contrast."
        )
        panel.pack_start(button, False, False, 0)

        view = Gtk.TreeView()
        view.set_tooltip_column(0)
        model = Gtk.ListStore(str, str, str, str)
        for i in range(1, 81):
            model.append((
                "Item %02d: hover for a tooltip" % i,
                "Color and contrast",
                "Long example column for horizontal scrollbar",
                "Equinox Evolution GTK3",
            ))
        view.set_model(model)

        for index, title in enumerate(("Item", "Appearance", "Details", "Theme")):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(title, renderer, text=index)
            column.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
            column.set_fixed_width(250)
            column.set_resizable(True)
            view.append_column(column)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)
        scrolled.set_overlay_scrolling(False)
        scrolled.add(view)
        panel.pack_start(scrolled, True, True, 0)

        status = Gtk.Label(label="Permanent scrollbars for testing. No files are modified.")
        status.set_xalign(0)
        panel.pack_start(status, False, False, 0)


if __name__ == "__main__":
    preview = Preview()
    preview.show_all()
    Gtk.main()
