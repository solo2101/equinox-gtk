#!/usr/bin/env python3
"""Regression test: GtkNotebook tabs must remain clickable with Equinox GTK3.

Run with a virtual X display and xdotool:
  xvfb-run -a env GTK_THEME=Equinox-Light python3 tests/test-gtk3-notebook-clicks.py

Uses real X11 mouse clicks, not gtk_notebook_set_current_page().
"""
import os
import subprocess
import sys
import time

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gtk


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
