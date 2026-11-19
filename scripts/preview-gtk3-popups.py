#!/usr/bin/env python3
"""Test the GTK3 menu widgets used by Caja and MATE plus Shutter selection."""
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

window = Gtk.Window(title="Equinox GTK3 Caja and MATE menu preview")
window.set_default_size(620, 390)
window.connect("destroy", Gtk.main_quit)
layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
layout.set_border_width(12)
window.add(layout)

def build_menu():
    menu = Gtk.Menu()
    normal = Gtk.MenuItem(label="Open")
    menu.append(normal)
    menu.append(Gtk.MenuItem(label="Open in New Window"))
    menu.append(Gtk.SeparatorMenuItem())
    menu.append(Gtk.CheckMenuItem(label="Show Hidden Files"))
    recent = Gtk.MenuItem(label="Open Recent")
    sub = Gtk.Menu()
    sub.append(Gtk.MenuItem(label="Recent Document"))
    recent.set_submenu(sub)
    menu.append(recent)
    disabled = Gtk.MenuItem(label="Unavailable Action")
    disabled.set_sensitive(False)
    menu.append(disabled)
    menu.show_all()
    return menu

layout.pack_start(Gtk.Label(label="Caja-style GtkMenuBar: File, Edit, View"), False, False, 0)
caja = Gtk.MenuBar()
for name in ("File", "Edit", "View"):
    item = Gtk.MenuItem(label=name)
    item.set_submenu(build_menu())
    caja.append(item)
layout.pack_start(caja, False, False, 0)

layout.pack_start(Gtk.Label(label="MATE-style GtkMenuBar: Applications, Places, System"), False, False, 0)
panel = Gtk.MenuBar()
for name in ("Applications", "Places", "System"):
    item = Gtk.MenuItem(label=name)
    item.set_submenu(build_menu())
    panel.append(item)
layout.pack_start(panel, False, False, 0)

contextButton = Gtk.Button(label="Show Caja-style right-click context menu")
contextButton.connect("clicked", lambda widget: build_menu().popup_at_widget(
    widget, Gdk.Gravity.SOUTH_WEST, Gdk.Gravity.NORTH_WEST, None))
layout.pack_start(contextButton, False, False, 0)

layout.pack_start(Gtk.Label(label="Shutter's blue selection rectangle:"), False, False, 0)
area = Gtk.DrawingArea()
area.set_size_request(270, 130)
area.get_style_context().add_class("imageview")
def draw(widget, cr):
    ctx = widget.get_style_context()
    ctx.save()
    ctx.add_class("rubberband")
    Gtk.render_background(ctx, cr, 22, 12, 230, 100)
    Gtk.render_frame(ctx, cr, 22, 12, 230, 100)
    ctx.restore()
    return False
area.connect("draw", draw)
layout.pack_start(area, True, True, 0)

window.show_all()
Gtk.main()
