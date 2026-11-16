#!/usr/bin/env python3
"""Parse Equinox GTK3 CSS and report every GTK CSS parsing error.

GTK3 sometimes recovers from CSS problems and reports them through the
GtkCssProvider::parsing-error signal. Checking only the load return value
misses some failures.
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
    paths = ([pathlib.Path(p).resolve() for p in sys.argv[1:]]
             if len(sys.argv) > 1 else [
                 root / "themes" / name / "gtk-3.0" / "gtk.css"
                 for name in ("Equinox-Light", "Equinox-Dark")
             ])
    try:
        gtk = ctypes.CDLL("libgtk-3.so.0")
        gobject = ctypes.CDLL("libgobject-2.0.so.0")
        glib = ctypes.CDLL("libglib-2.0.so.0")
    except OSError as exc:
        print(f"GTK3 runtime unavailable: {exc}", file=sys.stderr)
        return 2

    gtk.gtk_css_provider_new.restype = ctypes.c_void_p
    gtk.gtk_css_provider_load_from_path.argtypes = (
        ctypes.c_void_p, ctypes.c_char_p,
        ctypes.POINTER(ctypes.c_void_p),
    )
    gtk.gtk_css_provider_load_from_path.restype = ctypes.c_int
    gtk.gtk_css_section_get_start_line.argtypes = (ctypes.c_void_p,)
    gtk.gtk_css_section_get_start_line.restype = ctypes.c_uint
    gtk.gtk_css_section_get_start_position.argtypes = (ctypes.c_void_p,)
    gtk.gtk_css_section_get_start_position.restype = ctypes.c_uint
    gobject.g_signal_connect_data.argtypes = (
        ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p,
        ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int,
    )
    gobject.g_signal_connect_data.restype = ctypes.c_ulong
    gobject.g_object_unref.argtypes = (ctypes.c_void_p,)
    glib.g_error_free.argtypes = (ctypes.c_void_p,)

    CALLBACK = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p,
                                ctypes.c_void_p, ctypes.c_void_p)
    failures = 0
    for path in paths:
        if not path.is_file():
            print(f"FAIL: missing {path}")
            failures += 1
            continue
        issues = []

        @CALLBACK
        def parsing_error(_provider, section, error, _user_data):
            detail = ctypes.cast(error, ctypes.POINTER(GError)).contents
            line = gtk.gtk_css_section_get_start_line(section) + 1 if section else 0
            column = (gtk.gtk_css_section_get_start_position(section) + 1
                      if section else 0)
            message = detail.message.decode(errors="replace") if detail.message else "unknown error"
            issues.append((line, column, message))

        provider = gtk.gtk_css_provider_new()
        error = ctypes.c_void_p()
        try:
            gobject.g_signal_connect_data(
                provider, b"parsing-error",
                ctypes.cast(parsing_error, ctypes.c_void_p),
                None, None, 0,
            )
            ok = gtk.gtk_css_provider_load_from_path(
                provider, str(path).encode(), ctypes.byref(error)
            )
            if error.value and not issues:
                detail = ctypes.cast(error, ctypes.POINTER(GError)).contents
                issues.append((0, 0, detail.message.decode(errors="replace")))
            if not ok or issues:
                failures += 1
                if not issues:
                    print(f"FAIL: GTK3 refused {path}")
                for line, column, message in issues:
                    print(f"FAIL: {path}:{line}:{column}: {message}")
            else:
                print(f"PASS: {path}")
        finally:
            if error.value:
                glib.g_error_free(error)
            gobject.g_object_unref(provider)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
