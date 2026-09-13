#!/usr/bin/env python3
"""Build a locally installable Anki add-on package."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "AnkiConnect.py"
MANIFEST = ROOT / "manifest.json"
CONFIG = ROOT / "config.json"
CONFIG_DOCUMENTATION = ROOT / "config.md"
OUTPUT = ROOT / "dist" / "AnkiConnectLocal.ankiaddon"
REQUIRED_MEMBERS = {"__init__.py", "manifest.json", "config.json", "config.md"}


def main():
    if not SOURCE.is_file():
        raise FileNotFoundError("Missing add-on entry point: {}".format(SOURCE))
    if not MANIFEST.is_file():
        raise FileNotFoundError("Missing add-on manifest: {}".format(MANIFEST))
    if not CONFIG.is_file():
        raise FileNotFoundError("Missing add-on configuration: {}".format(CONFIG))
    if not CONFIG_DOCUMENTATION.is_file():
        raise FileNotFoundError("Missing configuration documentation: {}".format(CONFIG_DOCUMENTATION))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUTPUT, "w", ZIP_DEFLATED) as archive:
        archive.write(SOURCE, "__init__.py")
        archive.write(MANIFEST, "manifest.json")
        archive.write(CONFIG, "config.json")
        archive.write(CONFIG_DOCUMENTATION, "config.md")

    with ZipFile(OUTPUT) as archive:
        members = set(archive.namelist())
        if members != REQUIRED_MEMBERS:
            raise RuntimeError("Invalid package contents: {}".format(sorted(members)))

    print("Created {}".format(OUTPUT))


if __name__ == "__main__":
    main()
