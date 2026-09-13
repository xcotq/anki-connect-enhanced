import json
import py_compile
import subprocess
import sys
import unittest
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "dist" / "AnkiConnectLocal.ankiaddon"
EXPECTED_MEMBERS = {"__init__.py", "manifest.json", "config.json", "config.md"}


def build_package():
    subprocess.run([sys.executable, "build_addon.py"], cwd=ROOT, check=True)


class TestAddonPackage(unittest.TestCase):
    def test_addon_source_compiles(self):
        py_compile.compile(ROOT / "AnkiConnect.py", doraise=True)

    def test_addon_uses_modern_qt_and_collection_apis(self):
        source = (ROOT / "AnkiConnect.py").read_text(encoding="utf-8")

        self.assertIn("from aqt.qt import QMessageBox, QTimer", source)
        self.assertNotIn("from PyQt5", source)
        self.assertIn("collection.add_notes(requests)", source)
        self.assertIn("collection.update_notes(updatedNotes)", source)

    def test_build_creates_a_valid_installable_package(self):
        build_package()

        with ZipFile(PACKAGE) as archive:
            self.assertEqual(EXPECTED_MEMBERS, set(archive.namelist()))
            self.assertIsNone(archive.testzip())

            manifest = json.loads(archive.read("manifest.json"))
            config = json.loads(archive.read("config.json"))

        self.assertEqual("ankiconnectlocal", manifest["package"])
        self.assertEqual("AnkiConnect Local", manifest["name"])
        self.assertEqual("127.0.0.1", config["webBindAddress"])
        self.assertEqual(8765, config["webBindPort"])
        self.assertIsInstance(config["webCorsOriginList"], list)
