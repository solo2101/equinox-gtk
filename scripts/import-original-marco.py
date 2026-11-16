#!/usr/bin/env python3
"""Import the unmodified Equinox 1.50 Metacity artwork into our Marco themes.

Source: 140449-equinox-themes-1.50.tar.gz (GPL-2.0-or-later).
No code generation or replacement artwork. Extract only whitelisted files
from the original archive and keep the filename layout required by Marco.
"""
import argparse
import hashlib
import pathlib
import re
import sys
import tarfile
import xml.etree.ElementTree as ET

EXPECTED_SHA256 = "32b3cedfbc27e466289aa8a0b6d1f3f964a553956d94bf267bd42c749691823c"
SOURCES = {
    "Equinox Light": "Equinox-Light",
    "Equinox Evolution Dusk": "Equinox-Dark",
}
EXTENSIONS = {".xml", ".png", ".svg", ".xpm"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=pathlib.Path)
    parser.add_argument("--destination", type=pathlib.Path, default=pathlib.Path("themes"))
    args = parser.parse_args()

    actual = hashlib.sha256(args.archive.read_bytes()).hexdigest()
    if actual != EXPECTED_SHA256:
        parser.error(
            f"Wrong upstream archive SHA256: {actual}. Expected {EXPECTED_SHA256}."
        )

    for upstream_name, target_name in SOURCES.items():
        found = {}
        with tarfile.open(args.archive, "r:gz") as archive:
            for member in archive:
                if not member.isfile() or member.size > 5 * 1024 * 1024:
                    continue
                parts = pathlib.PurePosixPath(member.name).parts
                if len(parts) < 3:
                    continue
                # Accept either direct theme/ or wrapped release/theme/ layout.
                if parts[-3] != upstream_name or parts[-2] != "metacity-1":
                    continue
                filename = parts[-1]
                if filename in ("", ".", ".."):
                    continue
                if pathlib.PurePosixPath(filename).suffix.lower() not in EXTENSIONS:
                    continue
                stream = archive.extractfile(member)
                if stream is not None:
                    found[filename] = stream.read()

        if "metacity-theme-1.xml" not in found:
            raise SystemExit(f"Upstream theme missing: {upstream_name}")
        xml = ET.fromstring(found["metacity-theme-1.xml"])
        if xml.tag != "metacity_theme":
            raise SystemExit(f"Invalid Metacity theme root: {upstream_name}")
        missing = []
        images = set()
        for node in xml.iter("image"):
            filename = node.attrib.get("filename", "")
            if filename and not filename.startswith("theme:"):
                images.add(filename)
                if filename not in found:
                    missing.append(filename)
        if missing:
            raise SystemExit(
                f"Missing artwork in {upstream_name}: {', '.join(sorted(set(missing)))}"
            )
        png_count = sum(name.lower().endswith(".png") for name in found)
        if png_count < 4 or not images:
            raise SystemExit(
                f"Theme {upstream_name} has only {png_count} PNGs "
                f"and {len(images)} image references. Refusing a "
                "non-original or incomplete window-button theme."
            )

        dest = args.destination / target_name / "metacity-1"
        dest.mkdir(parents=True, exist_ok=True)
        # Remove obsolete generated XML-era assets, but only filetypes
        # specifically owned by this importer, not the GTK directories.
        for item in dest.iterdir():
            if item.is_file() and item.suffix.lower() in EXTENSIONS and item.name not in found:
                item.unlink()
        for filename, data in found.items():
            (dest / filename).write_bytes(data)

        note = (
            f"Original Equinox 1.50 Metacity theme: {upstream_name}\n"
            "Source archive: 140449-equinox-themes-1.50.tar.gz\n"
            f"Archive SHA256: {EXPECTED_SHA256}\n"
            "This directory preserves the upstream window-frame XML and original artwork.\n"
            "Original theme license: GPL-2.0-or-later.\n"
        )
        (dest / "UPSTREAM.txt").write_text(note, encoding="utf-8")
        print(
            f"IMPORTED {upstream_name} -> {target_name}: {len(found)} files, "
            f"{png_count} original PNGs, {len(images)} image references"
        )


if __name__ == "__main__":
    main()
