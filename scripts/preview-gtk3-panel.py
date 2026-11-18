#!/usr/bin/env python3
"""Visual panel/clock/tasklist test with MATE's real GTK3 style classes.

Run:
  GTK_THEME=Equinox-Light python3 scripts/preview-gtk3-panel.py
No panel settings or files are changed.
"""
import gi

gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Preview(Gtk.Window):
    def __init__(self):
        super().__init__(title="Equinox GTK3 MATE Panel Preview")
        self.set_default_size(750, 260)
        self.set_border_width(12)
        self.connect("destroy", Gtk.main_quit)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.add(box)
        title = Gtk.Label(label="Panel buttons: resting, hover, pressed, active window, and disabled")
        title.set_xalign(0)
        box.pack_start(title, False, False, 0)

        panel = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        panel.get_style_context().add_class("mate-panel-menu-bar")
        box.pack_start(panel, False, False, 0)

        menubar = Gtk.MenuBar()
        for name in ("Applications", "Places", "System"):
            item = Gtk.MenuItem(label=name)
            submenu = Gtk.Menu()
            submenu.append(Gtk.MenuItem(label="Example item"))
            submenu.show_all()
            item.set_submenu(submenu)
            menubar.append(item)
        panel.pack_start(menubar, False, False, 0)

        launcher = Gtk.Button()
        launcher.set_image(Gtk.Image.new_from_icon_name("folder", Gtk.IconSize.MENU))
        launcher.set_tooltip_text("Folder launcher")
        panel.pack_start(launcher, False, False, 0)

        launcher2 = Gtk.Button(label="Launcher")
        panel.pack_start(launcher2, False, False, 0)

        clock = Gtk.ToggleButton(label="Wed Nov 18  1:07 AM")
        clock.set_name("clock-applet-button")
        panel.pack_end(clock, False, False, 0)

        box.pack_start(Gtk.Label(label="Window-list buttons (libwnck tasklist appearance)"), False, False, 0)

        task_panel = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        task_panel.get_style_context().add_class("mate-panel-menu-bar")
        box.pack_start(task_panel, False, False, 0)
        tasklist = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        tasklist.get_style_context().add_class("wnck-tasklist")
        task_panel.pack_start(tasklist, True, True, 0)
        for label, active in (("Caja", True), ("Firefox", False), ("Terminal", False)):
            task = Gtk.ToggleButton(label=label)
            task.set_name("tasklist-button")
            task.set_active(active)
            tasklist.pack_start(task, True, True, 0)

        disabled = Gtk.Button(label="Disabled launcher")
        disabled.set_sensitive(False)
        task_panel.pack_start(disabled, False, False, 0)

        note = Gtk.Label(
            label="Open real MATE Panel to verify applets and clock. "
                  "This preview does not change the desktop."
        )
        note.set_xalign(0)
        note.set_line_wrap(True)
        box.pack_start(note, False, False, 0)


if __name__ == "__main__":
    window = Preview()
    window.show_all()
    Gtk.main()
