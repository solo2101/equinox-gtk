#!/usr/bin/env python3
"""Preview Equinox GTK3 popup menus, including check/radio and disabled items."""
import gi

gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gtk


def make_menu():
    menu = Gtk.Menu()
    for name in ("Open", "Open in New Window"):
        menu.append(Gtk.MenuItem.new_with_label(name))
    menu.append(Gtk.SeparatorMenuItem())

    hidden = Gtk.CheckMenuItem.new_with_label("Show Hidden Files")
    hidden.set_active(True)
    menu.append(hidden)
    first = Gtk.RadioMenuItem.new_with_label(None, "Icon View")
    first.set_active(True)
    menu.append(first)
    menu.append(Gtk.RadioMenuItem.new_with_label_from_widget(first, "List View"))
    menu.append(Gtk.SeparatorMenuItem())

    submenu = Gtk.Menu()
    for name in ("Text Editor", "Other Application..."):
        submenu.append(Gtk.MenuItem.new_with_label(name))
    other = Gtk.MenuItem.new_with_label("Open With")
    other.set_submenu(submenu)
    menu.append(other)

    disabled = Gtk.MenuItem.new_with_label("Unavailable Action")
    disabled.set_sensitive(False)
    menu.append(disabled)
    menu.show_all()
    return menu


class Preview(Gtk.Window):
    def __init__(self):
        super().__init__(title="Equinox GTK3 Popup Menu Preview")
        self.set_default_size(370, 190)
        self.set_border_width(14)
        self.connect("destroy", Gtk.main_quit)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(box)
        box.pack_start(
            Gtk.Label(label="Right-click below to open the context menu."),
            False, False, 0
        )

        target = Gtk.EventBox()
        target.set_size_request(-1, 80)
        target.add(Gtk.Label(label="Right-click here"))
        target.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        target.connect("button-press-event", self.on_right_click)
        box.pack_start(target, True, True, 0)

        button = Gtk.Button(label="Open Popup Menu")
        button.connect("clicked", self.on_button_click)
        box.pack_start(button, False, False, 0)

    def on_right_click(self, _widget, event):
        if event.button != 3:
            return False
        menu = make_menu()
        menu.popup_at_pointer(event)
        return True

    def on_button_click(self, button):
        menu = make_menu()
        menu.popup_at_widget(
            button, Gdk.Gravity.SOUTH_WEST, Gdk.Gravity.NORTH_WEST, None
        )


if __name__ == "__main__":
    window = Preview()
    window.show_all()
    Gtk.main()
