#!/usr/bin/env python3
"""Regression test: GtkNotebook tabs must remain clickable with Equinox GTK3.

Run with a virtual X display and xdotool:
  xvfb-run -a env GTK_THEME=Equinox-Light python3 tests/test-gtk3-notebook-clicks.py

Uses real X11 mouse clicks, not gtk_notebook_set_current_page().
"""
import os
import base64
import subprocess
import sys
import time

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gtk, GLib


def dispatch_events():
    while Gtk.events_pending():
        Gtk.main_iteration_do(False)


def wait_for_page(notebook, expected, timeout=2.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        dispatch_events()
        if notebook.get_current_page() == expected:
            return True
        time.sleep(0.025)
    return False


def click_tab(label):
    # GtkLabel is a no-window widget, so the label allocation is relative
    # to its backing GdkWindow. Add that window's root-screen origin.
    backing = label.get_window()
    if backing is None:
        raise RuntimeError("Tab label has no mapped window")
    origin = backing.get_origin()
    allocation = label.get_allocation()
    x = origin[0] + allocation.x + allocation.width // 2
    y = origin[1] + allocation.y + allocation.height // 2
    subprocess.run(
        ["xdotool", "mousemove", "--sync", str(x), str(y), "click", "1"],
        check=True,
    )



def check_page_surface(window, notebook, orientation):
    """Check the visible page fill as well as functional tab switching."""
    dispatch_events()
    time.sleep(0.05)
    dispatch_events()
    width = window.get_allocated_width()
    height = window.get_allocated_height()
    pixels = Gdk.pixbuf_get_from_window(window.get_window(), 0, 0,
                                        width, height)
    if pixels is None:
        raise RuntimeError("Unable to capture GTK3 window")
    page = notebook.get_nth_page(notebook.get_current_page())
    rect = page.get_allocation()
    x = min(width - 2, max(1, rect.x + 22))
    y = min(height - 2, max(1, rect.y + 22))
    stride = pixels.get_rowstride()
    channels = pixels.get_n_channels()
    raw = pixels.get_pixels()
    offset = y * stride + x * channels
    rgb = tuple(raw[offset:offset + 3])
    theme = os.environ.get("GTK_THEME", "")
    if theme == "Equinox-Light":
        # Original GTK2 notebook page in the screenshot is #e8e8e8,
        # versus #d7d7d7 normal theme background. The page must not
        # disappear into the window background again.
        if not 222 <= rgb[0] <= 246:
            raise AssertionError(
                f"{orientation.value_nick}: lost light notebook page surface: "
                f"sample at ({x},{y})={rgb}; expected approx #e8e8e8")
    elif theme == "Equinox-Dark":
        if not 48 <= rgb[0] <= 95:
            raise AssertionError(
                f"{orientation.value_nick}: unexpected dark notebook "
                f"page surface: {rgb}")
    print(f"Visible {orientation.value_nick} page surface: {rgb}")



def tab_background_rgb(window, tab_label):
    """Sample the tab face to the left of its label, avoiding text and top border."""
    backing = tab_label.get_window()
    origin = backing.get_origin()
    rect = tab_label.get_allocation()
    screen_x = origin[0] + rect.x - 4
    screen_y = origin[1] + rect.y + rect.height // 2
    win_origin = window.get_window().get_origin()
    x = screen_x - win_origin[0]
    y = screen_y - win_origin[1]
    pb = Gdk.pixbuf_get_from_window(window.get_window(), x, y, 1, 1)
    if pb is None:
        raise RuntimeError(f"Unable to sample notebook tab at {x},{y}")
    raw = pb.get_pixels()
    return tuple(raw[:3])


def trace_tab_selection(window, notebook, labels, orientation):
    """Trace selected-tab face colors before adding a visual assertion."""
    if orientation != Gtk.PositionType.TOP:
        return
    # Remove hover from all tabs before measuring their checked style.
    # The preceding mouse-click test ends with the pointer on tab 1.
    subprocess.run(["xdotool", "mousemove", "--sync", "690", "380"],
                   check=True)
    dispatch_events()
    for page in (0, 1, 2, 3):
        notebook.set_current_page(page)
        notebook.queue_resize()
        notebook.queue_draw()
        window.queue_draw()
        window.get_window().invalidate_rect(None, True)
        window.get_window().process_updates(True)
        dispatch_events()
        # A real GLib main loop is needed for GTK's frame clock to draw.
        loop = GLib.MainLoop()
        GLib.timeout_add(130, loop.quit)
        loop.run()
        dispatch_events()
        colors = [tab_background_rgb(window, label) for label in labels]
        print(f"TAB COLORS selected={page + 1}: {colors}", flush=True)
        if (os.environ.get("GTK_THEME") in ("Equinox-Light", "Adwaita", "Equinox-Notebook-Baseline")
                and page in (0, 1)):
            capture = Gdk.pixbuf_get_from_window(
                window.get_window(), 0, 0, 260, 86)
            target = f"/tmp/equinox-tab-state-{page + 1}.png"
            capture.savev(target, "png", [], [])
            with open(target, "rb") as screenshot_file:
                encoded = base64.b64encode(screenshot_file.read()).decode("ascii")
            print(f"TAB_SCREENSHOT page={page + 1} base64={encoded}", flush=True)
        if page in (0, 1):
            pix = Gdk.pixbuf_get_from_window(window.get_window(), 0, 0,
                                             window.get_allocated_width(),
                                             window.get_allocated_height())
            raw = pix.get_pixels()
            origin = window.get_window().get_origin()
            for i, label in enumerate(labels):
                origin_tab = label.get_window().get_origin()
                a = label.get_allocation()
                bx = origin_tab[0] + a.x - origin[0]
                by = origin_tab[1] + a.y - origin[1]
                probes = []
                for dx, dy in ((-4, 2), (a.width + 3, 2),
                               (-4, a.height//2), (a.width//2, -4),
                               (a.width//2, a.height+3)):
                    px, py = bx+dx, by+dy
                    offset = py * pix.get_rowstride() + px * pix.get_n_channels()
                    probes.append((px, py, tuple(raw[offset:offset+3])))
                print(f"TAB PROBES selected={page+1} tab={i+1} "
                      f"alloc={(bx,by,a.width,a.height)}: {probes}", flush=True)
        if page in (0, 1):
            print(f"CSS TREE selected={page + 1}:\\n" +
                  notebook.get_style_context().to_string(
                      Gtk.StyleContextPrintFlags.RECURSE |
                      Gtk.StyleContextPrintFlags.SHOW_STYLE)[:14000], flush=True)



def main():
    if not Gtk.init_check():
        raise SystemExit("GTK3 display unavailable")
    win = Gtk.Window(title="Equinox notebook click test")
    win.set_default_size(700, 400)
    notebook = Gtk.Notebook()
    notebook.set_scrollable(False)
    labels = []
    for i in range(4):
        page = Gtk.Label(label=f"Contents of page {i + 1}")
        tab = Gtk.Label(label=f"Tab {i + 1}")
        notebook.append_page(page, tab)
        labels.append(tab)
    win.add(notebook)
    win.show_all()
    dispatch_events()

    if os.environ.get("EQUINOX_DIAGNOSTIC") == "high-contrast":
        # Diagnostic-only override. Never written to the production CSS.
        # An extreme color difference reveals whether GTK redraws the
        # :checked node, independent of our gradients and page borders.
        provider = Gtk.CssProvider()
        provider.load_from_data(
            b"notebook > header > tabs > tab { "
            b"background-image: none; background-color: #00aa00; "
            b"border: 3px solid #005500; box-shadow: none; } "
            b"notebook > header > tabs > tab:checked { "
            b"background-image: none; background-color: #ff2222; "
            b"border: 3px solid #ff2222; "
            b"box-shadow: inset 0 -4px #ff2222; }")
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER)
        dispatch_events()

    failures = []
    for orientation in (Gtk.PositionType.TOP, Gtk.PositionType.BOTTOM,
                        Gtk.PositionType.LEFT, Gtk.PositionType.RIGHT):
        notebook.set_tab_pos(orientation)
        dispatch_events()
        for selected in (1, 2, 3, 0):
            click_tab(labels[selected])
            if not wait_for_page(notebook, selected):
                failures.append(f"{orientation.value_nick}: click Tab {selected + 1} "
                                f"left selected page {notebook.get_current_page() + 1}")
        trace_tab_selection(win, notebook, labels, orientation)
        if os.environ.get("EQUINOX_DIAGNOSTIC") != "high-contrast":
            check_page_surface(win, notebook, orientation)
        print(f"Checked {orientation.value_nick} tab orientation")
    win.destroy()
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print("PASS: 16 real mouse clicks switched GTK3 notebook pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
