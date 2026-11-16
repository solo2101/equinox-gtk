#!/usr/bin/env python3
"""Check Equinox GTK3 CSS with GTK's own parser, without launching a window.

Requires the GTK3 runtime library. Usage:
    python3 scripts/check-gtk3-css.py
    python3 scripts/check-gtk3-css.py themes/Equinox-Light/gtk-3.0/gtk.css
"""
import ctypes
import pathlib
import sys


class GError(ctypes.Structure):
    _fields_ = [
        ("domain", ctypes.c_uint),
        ("code", ctypes.c_int),
        ("message", ctypes.c_char_p),
    ]


def main() -> int:
    root = pathlib.Path(__file__).resolve().parent.parent
    if len(sys.argv) > 1:
        paths = [pathlib.Path(p).resolve() for p in sys.argv[1:]]
    else:
        paths = [
            root / "themes" / name / "gtk-3.0" / "gtk.css"
            for name in ("Equinox-Light", "Equinox-Dark")
        ]

    try:
        gtk = ctypes.CDLL("libgtk-3.so.0")
        gobject = ctypes.CDLL("libgobject-2.0.so.0")
        glib = ctypes.CDLL("libglib-2.0.so.0")
    except OSError as exc:
        print(f"Missing GTK3 runtime: {exc}", file=sys.stderr)
        return 2

    gtk.gtk_css_provider_new.restype = ctypes.c_void_p
    gtk.gtk_css_provider_load_from_path.argtypes = (
        ctypes.c_void_p,
        ctypes.c_char_p,
        ctypes.POINTER(ctypes.c_void_p),
    )
    gtk.gtk_css_provider_load_from_path.restype = ctypes.c_int
    gobject.g_object_unref.argtypes = (ctypes.c_void_p,)
    glib.g_error_free.argtypes = (ctypes.c_void_p,)

    errors = 0
    for path in paths:
        if not path.is_file():
            print(f"FAIL: missing {path}")
            errors += 1
            continue
        provider = gtk.gtk_css_provider_new()
        err = ctypes.c_void_p()
        try:
            success = gtk.gtk_css_provider_load_from_path(
                provider,
                str(path).encode(),
                ctypes.byref(err),
            )
            if success and not err.value:
                print(f"PASS: {path}")
            else:
                errors += 1
                if err.value:
                    detail = ctypes.cast(err, ctypes.POINTER(GError)).contents
                    print(f"FAIL: {path}: {detail.message.decode(errors='replace')}")
                else:
                    print(f"FAIL: {path}: GTK rejected the stylesheet")
        finally:
            if err.value:
                glib.g_error_free(err)
            gobject.g_object_unref(provider)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
