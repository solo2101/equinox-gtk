#!/usr/bin/env python3
"""Preview Equinox GTK3 keyboard focus, Caja-like selection, and menu navigation.

Use: GTK_THEME=Equinox-Light python3 scripts/preview-gtk3-caja-focus.py
The actual Caja breadcrumb and Places classes are applied only in Caja.
No files are changed.
"""
import gi

gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gtk


class Preview(Gtk.Window):
    def __init__(self):
        super().__init__(title="Equinox GTK3 Caja / Keyboard Focus")
        self.set_default_size(660, 530)
        self.connect("destroy", Gtk.main_quit)
        panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=9)
        panel.set_border_width(12)
        self.add(panel)

        hint = Gtk.Label(
            label="Press Tab and Shift+Tab to move focus. Use arrows in the "
                  "file list and context menu. Watch the focus indicator."
        )
        hint.set_xalign(0)
        hint.set_line_wrap(True)
        panel.pack_start(hint, False, False, 0)

        grid = Gtk.Grid(column_spacing=12, row_spacing=8)
        panel.pack_start(grid, False, False, 0)

        self.focus_status = Gtk.Label(label="Focus: none")
        self.focus_status.set_xalign(0)

        button = Gtk.Button(label="Normal button")
        self.add_control(grid, button, 0, 0, "Button")

        entry = Gtk.Entry()
        entry.set_text("Editable entry")
        self.add_control(grid, entry, 1, 0, "Entry")

        check = Gtk.CheckButton(label="Show hidden files")
        check.set_active(True)
        self.add_control(grid, check, 0, 1, "Checkbox")

        radio = Gtk.RadioButton.new_with_label(None, "Option A")
        self.add_control(grid, radio, 1, 1, "Radio button")

        toggle = Gtk.Switch()
        toggle.set_active(True)
        self.add_control(grid, toggle, 0, 2, "Switch")

        combo = Gtk.ComboBoxText()
        combo.append_text("Icons")
        combo.append_text("List")
        combo.set_active(0)
        self.add_control(grid, combo, 1, 2, "Combo box")

        scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 1)
        scale.set_value(40)
        self.add_control(grid, scale, 0, 3, "Slider")

        menu_button = Gtk.Button(label="Open context menu, then use arrow keys")
        menu_button.connect("clicked", self.show_menu)
        self.add_control(grid, menu_button, 1, 3, "Context menu")

        panel.pack_start(Gtk.Separator(), False, False, 0)
        panel.pack_start(Gtk.Label(label="File-list selection (Caja-like GTK3 tree view)"),
                         False, False, 0)
        model = Gtk.ListStore(str, str)
        for i in range(1, 26):
            model.append(("Folder %02d" % i, "Example file or folder"))
        tree = Gtk.TreeView(model=model)
        for col_index, heading in enumerate(("Name", "Type")):
            tree.append_column(Gtk.TreeViewColumn(
                heading, Gtk.CellRendererText(), text=col_index
            ))
        self.track_focus(tree, "File list")

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(tree)
        panel.pack_start(scrolled, True, True, 0)

        panel.pack_start(self.focus_status, False, False, 0)
        window_note = Gtk.Label(
            label="Check real Caja separately: caja -q && caja ~"
        )
        window_note.set_xalign(0)
        panel.pack_start(window_note, False, False, 0)

    def add_control(self, grid, widget, column, row, name):
        frame = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        label = Gtk.Label(label=name)
        label.set_xalign(0)
        frame.pack_start(label, False, False, 0)
        frame.pack_start(widget, True, False, 0)
        grid.attach(frame, column, row, 1, 1)
        self.track_focus(widget, name)

    def track_focus(self, widget, name):
        def on_focus_change(w, _pspec):
            if w.has_focus():
                self.focus_status.set_text("Focus: " + name)
        widget.connect("notify::has-focus", on_focus_change)

    def show_menu(self, button):
        menu = Gtk.Menu()
        for text in ("Open", "Open with", "Properties"):
            item = Gtk.MenuItem.new_with_label(text)
            menu.append(item)
        menu.append(Gtk.SeparatorMenuItem())
        disabled = Gtk.MenuItem.new_with_label("Unavailable action")
        disabled.set_sensitive(False)
        menu.append(disabled)
        menu.show_all()
        menu.popup_at_widget(
            button, Gdk.Gravity.SOUTH_WEST, Gdk.Gravity.NORTH_WEST, None
        )


if __name__ == "__main__":
    preview = Preview()
    preview.show_all()
    Gtk.main()
