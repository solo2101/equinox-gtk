#!/usr/bin/env python3
"""Check Equinox's GTK3 inset-circle splitter grips without changing MATE."""
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

window = Gtk.Window(title="Equinox GTK3 grip preview")
window.set_default_size(620, 420)
window.set_border_width(12)
window.connect("destroy", Gtk.main_quit)
outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
window.add(outer)
outer.pack_start(Gtk.Label(label="Drag the recessed dot between the panes."), False, False, 0)

horizontal = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)
left = Gtk.Frame(label="Sidebar")
left.add(Gtk.Label(label="Left pane"))
right = Gtk.Frame(label="Main window")
right.add(Gtk.Label(label="Right pane"))
horizontal.pack1(left, True, False)
horizontal.pack2(right, True, False)
horizontal.set_position(190)
outer.pack_start(horizontal, True, True, 0)

vertical = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
top = Gtk.Frame(label="Upper area")
top.add(Gtk.Label(label="Top pane"))
bottom = Gtk.Frame(label="Lower area")
bottom.add(Gtk.Label(label="Bottom pane"))
vertical.pack1(top, True, False)
vertical.pack2(bottom, True, False)
vertical.set_position(80)
outer.pack_start(vertical, True, True, 0)

window.show_all()
Gtk.main()
