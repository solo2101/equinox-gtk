#!/usr/bin/env python3
"""Inspect Equinox GTK3 popups and Shutter-style blue rubberband painting."""
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

window = Gtk.Window(title="Equinox popup and selection preview")
window.set_default_size(540, 330)
window.connect("destroy", Gtk.main_quit)
box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
box.set_border_width(12)
window.add(box)

menubar = Gtk.MenuBar()
item = Gtk.MenuItem(label="Applications")
popup = Gtk.Menu()
for title in ("Open", "Settings", "Preferences", "Close"):
    choice = Gtk.MenuItem(label=title)
    popup.append(choice)
item.set_submenu(popup)
menubar.append(item)
box.pack_start(menubar, False, False, 0)

controls = Gtk.Box(spacing=8)
btn = Gtk.Button(label="Open popover")
controls.pack_start(btn, False, False, 0)
box.pack_start(controls, False, False, 0)

popover = Gtk.Popover.new(btn)
contents = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
contents.set_border_width(6)
for title in ("New window", "Preferences"):
    contents.pack_start(Gtk.ModelButton.new(), False, False, 0)
    model = contents.get_children()[-1]
    model.set_property("text", title)
popover.add(contents)
btn.connect("clicked", lambda *_: (popover.show_all(), popover.popup()))

box.pack_start(Gtk.Label(label="Shutter-style selection, blue overlay and outline:"), False, False, 0)
area = Gtk.DrawingArea()
area.set_size_request(250, 125)
area.get_style_context().add_class("imageview")

def draw_selection(widget, cr):
    context = widget.get_style_context()
    context.save()
    context.add_class("rubberband")
    Gtk.render_background(context, cr, 22, 15, 230, 95)
    Gtk.render_frame(context, cr, 22, 15, 230, 95)
    context.restore()
    return False

area.connect("draw", draw_selection)
box.pack_start(area, True, True, 0)
window.show_all()
Gtk.main()
