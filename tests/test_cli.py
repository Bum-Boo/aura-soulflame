import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CLI = Path(__file__).resolve().parents[1] / "aura.py"


class InstallerTest(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.home = Path(scratch.name)
        self.config = self.home / "app config"
        self.data = self.home / "app data"
        self.state = self.home / "app state"
        self.codex = self.home / "codex"
        self.env = {
            **os.environ,
            "HOME": str(self.home),
            "USERPROFILE": str(self.home),
            "XDG_CONFIG_HOME": str(self.config),
            "XDG_DATA_HOME": str(self.data),
            "XDG_STATE_HOME": str(self.state),
            "CODEX_HOME": str(self.codex),
        }
        self.env.pop("KITTY_CONFIG_DIRECTORY", None)

    def run_cli(self, *args, expect=0):
        completed = subprocess.run([sys.executable, str(CLI), *args], env=self.env, capture_output=True, text=True)
        self.assertEqual(completed.returncode, expect, completed.stdout + completed.stderr)
        return json.loads(completed.stdout)

    @unittest.skipUnless(sys.platform in {"linux", "darwin"}, "Kitty preset targets Linux and macOS")
    def test_plan_reads_custom_kitty_root_without_writing_it(self):
        custom = self.home / "custom kitty"
        self.env["KITTY_CONFIG_DIRECTORY"] = str(custom)
        result = self.run_cli("plan", "--modules", "kitty")
        self.assertEqual(result["modules"]["kitty"]["target"], str(custom / "aura-soulflame.conf"))
        self.assertEqual(list(self.home.iterdir()), [])

    @unittest.skipUnless(sys.platform == "linux", "Plasma package targets Linux")
    def test_core_install_repeat_and_remove_with_existing_settings(self):
        current = self.config / "kitty/kitty.conf"
        current.parent.mkdir(parents=True)
        current.write_text("font_size 16\n")
        skin = self.data / "plasma/look-and-feel/io.github.bum_boo.soulflame.splash"
        modules = ("--modules", "kitty", "plasma-colors", "plasma-splash")
        result = self.run_cli("install", *modules)
        self.assertTrue(all(item["status"] == "installed" for item in result["modules"].values()))
        self.assertTrue((skin / "contents/splash/AuraFlame.qml").is_file())
        self.assertIn("portraitPack: false", (skin / "contents/splash/AuraScene.qml").read_text())
        self.assertEqual(self.run_cli("install", *modules), result)
        self.run_cli("uninstall", *modules)
        self.assertEqual(current.read_text(), "font_size 16\n")
        self.assertFalse(skin.exists())
        self.assertFalse((current.parent / "aura-soulflame.conf").exists())

    @unittest.skipUnless(sys.platform == "linux", "Plasma package targets Linux")
    def test_conflict_stops_selected_install_and_preserves_modified_file(self):
        kitty = self.config / "kitty/aura-soulflame.conf"
        self.run_cli("install", "--modules", "kitty")
        kitty.write_text("# My edited palette\n")
        outputs = self.run_cli("install", "--modules", "kitty", "plasma-colors", expect=2)
        self.assertEqual(outputs["modules"]["kitty"]["status"], "conflict")
        self.assertFalse(self.data.exists())
        result = self.run_cli("uninstall", "--modules", "kitty", expect=2)
        self.assertEqual(result["modules"]["kitty"]["status"], "modified")
        self.assertEqual(kitty.read_text(), "# My edited palette\n")

    @unittest.skipUnless(sys.platform in {"linux", "darwin"}, "Kitty preset targets Linux and macOS")
    def test_existing_identical_file_is_unmanaged(self):
        source = CLI.parent / "themes/kitty/aura-soulflame.conf"
        target = self.config / "kitty/aura-soulflame.conf"
        target.parent.mkdir(parents=True)
        target.write_bytes(source.read_bytes())
        self.assertEqual(self.run_cli("install", "--modules", "kitty")["modules"]["kitty"]["status"], "present-unmanaged")
        self.run_cli("uninstall", "--modules", "kitty")
        self.assertEqual(target.read_bytes(), source.read_bytes())

    @unittest.skipUnless(sys.platform == "linux", "Xcursor targets Linux")
    def test_cursor_accepts_internal_alias_and_rejects_external_link(self):
        pack = self.home / "assets/cursor"
        files = pack / "cursors"
        files.mkdir(parents=True)
        (pack / "index.theme").write_text("[Icon Theme]\nName=Test\n")
        (files / "left_ptr").write_bytes(b"Xcur")
        (files / "default").symlink_to("left_ptr")
        (files / "outside").symlink_to(self.home)
        args = ("--assets", str(pack.parent), "--modules", "cursor")
        response = self.run_cli("plan", *args, expect=2)
        self.assertIn("Asset link leaves", response["modules"]["cursor"]["reason"])
        (files / "outside").unlink()
        self.run_cli("install", *args)
        installed = self.data / "icons/AuraSoulflameCursor/cursors/default"
        self.assertEqual(str(installed.readlink()), "left_ptr")
        self.run_cli("uninstall", "--modules", "cursor")
        self.assertFalse(installed.exists())

    def test_pet_rejects_manifest_traversal_and_wrong_dimensions(self):
        pack = self.home / "assets/pet"
        pack.mkdir(parents=True)
        manifest = pack / "pet.json"
        args = ("--assets", str(pack.parent), "--modules", "codex-pet")
        manifest.write_text(json.dumps({"id": "demo", "spritesheetPath": "../outside.png"}))
        item = self.run_cli("plan", *args, expect=2)["modules"]["codex-pet"]
        self.assertIn("plain PNG or WebP filename", item["reason"])
        manifest.write_text(json.dumps({"id": "demo", "spritesheetPath": "sheet.png"}))
        (pack / "sheet.png").write_bytes(bytes.fromhex("89504e470d0a1a0a0000000d494844520000000100000001"))
        item = self.run_cli("plan", *args, expect=2)["modules"]["codex-pet"]
        self.assertIn("dimensions do not match", item["reason"])
        self.assertFalse(self.codex.exists())


if __name__ == "__main__":
    unittest.main()
