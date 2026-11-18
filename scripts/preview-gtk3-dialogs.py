#!/usr/bin/env python3
"""Preview GTK3 dialogs and the native GTK3 file chooser in any Equinox theme.

Use: GTK_THEME=Equinox-Light python3 scripts/preview-gtk3-dialogs.py
This program does not save or modify any files.
"""
import os
import gi

gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Preview(Gtk.Window):
    def __init__(self):
        super().__init__(title="Equinox GTK3 Dialog Preview")
        self.set_default_size(400, 230)
        self.set_border_width(14)
        self.connect("destroy", Gtk.main_quit)

        panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.add(panel)

        title = Gtk.Label(label="Compare dialogs and file pickers across Equinox themes.")
        title.set_line_wrap(True)
        panel.pack_start(title, False, False, 0)

        for caption, callback in (
            ("Message / confirmation dialog", self.message),
            ("Preferences / form dialog", self.preferences),
            ("Open file picker", self.open_file),
            ("Save file picker (preview only)", self.save_file),
        ):
            button = Gtk.Button(label=caption)
            button.connect("clicked", callback)
            panel.pack_start(button, False, False, 0)

    def message(self, _button):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=Gtk.DialogFlags.MODAL,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            text="Apply the selected theme?",
        )
        dialog.format_secondary_text(
            "Check the dialog background, message text, icon, and action buttons."
        )
        dialog.run()
        dialog.destroy()

    def preferences(self, _button):
        dialog = Gtk.Dialog(
            title="Equinox Preferences Preview",
            transient_for=self,
            flags=Gtk.DialogFlags.MODAL,
        )
        dialog.add_buttons(
            "_Cancel", Gtk.ResponseType.CANCEL,
            "_Apply", Gtk.ResponseType.APPLY,
        )
        dialog.set_default_size(390, 190)

        content = dialog.get_content_area()
        content.set_spacing(10)
        content.set_border_width(12)

        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row.pack_start(Gtk.Label(label="Theme name"), False, False, 0)
        row.pack_start(Gtk.Entry(text="Equinox Evolution"), True, True, 0)
        content.pack_start(row, False, False, 0)

        check = Gtk.CheckButton(label="Show classic button gradients")
        check.set_active(True)
        content.pack_start(check, False, False, 0)

        option = Gtk.ComboBoxText()
        for value in ("Normal", "Compact", "Large"):
            option.append_text(value)
        option.set_active(1)
        content.pack_start(option, False, False, 0)
        content.pack_start(Gtk.Label(label="No settings are changed."), False, False, 0)

        dialog.show_all()
        dialog.run()
        dialog.destroy()

    def chooser(self, action, title, accept_label):
        dialog = Gtk.FileChooserDialog(
            title=title,
            transient_for=self,
            action=action,
        )
        dialog.add_buttons(
            "_Cancel", Gtk.ResponseType.CANCEL,
            accept_label, Gtk.ResponseType.ACCEPT,
        )
        dialog.set_default_size(800, 520)
        dialog.set_current_folder(os.path.expanduser("~"))
        if action == Gtk.FileChooserAction.SAVE:
            dialog.set_current_name("theme-preview.txt")
        # Intentionally don't perform a file operation regardless of response.
        dialog.run()
        dialog.destroy()

    def open_file(self, _button):
        self.chooser(Gtk.FileChooserAction.OPEN, "Equinox Open File Preview", "_Open")

    def save_file(self, _button):
        self.chooser(Gtk.FileChooserAction.SAVE, "Equinox Save File Preview", "_Save")


if __name__ == "__main__":
    preview = Preview()
    preview.show_all()
    Gtk.main()
