import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
SKILL = REPOSITORY / ".agents/skills/aura-theme-design"


class SkillBundleTest(unittest.TestCase):
    def test_skill_uses_the_same_palette_and_license_as_the_theme(self):
        files = {
            "references/palette.json": "resources/palette.json",
            "assets/aura-soulflame.conf": "themes/kitty/aura-soulflame.conf",
            "LICENSE": "LICENSE",
        }
        for bundled, canonical in files.items():
            with self.subTest(bundled=bundled):
                self.assertEqual((SKILL / bundled).read_bytes(), (REPOSITORY / canonical).read_bytes())

    def test_palette_exports_css_when_skill_is_outside_checkout(self):
        with tempfile.TemporaryDirectory() as directory:
            skill_copy = Path(directory) / SKILL.name
            shutil.copytree(SKILL, skill_copy)
            result = subprocess.run([sys.executable, str(skill_copy / "scripts/palette.py"), "css"],
                                    cwd=directory, capture_output=True, text=True, check=True)
        self.assertIn("--aura-background: #2B2235;", result.stdout)
        self.assertIn("--aura-ansi-15: #FFF2E5;", result.stdout)

    def test_contrast_report_detects_unreadable_adapted_text(self):
        helper = SKILL / "scripts/palette.py"
        command = [sys.executable, str(helper), "contrast"]
        default = subprocess.run(command, capture_output=True, text=True, check=True)
        self.assertTrue(json.loads(default.stdout)["ok"])
        with tempfile.TemporaryDirectory() as directory:
            palette = json.loads((SKILL / "references/palette.json").read_text(encoding="utf-8"))
            palette["colors"]["foreground"] = palette["colors"]["background"]
            override = Path(directory) / "adapted.json"
            override.write_text(json.dumps(palette), encoding="utf-8")
            result = subprocess.run([*command, "--palette", str(override)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stderr)
        checks = json.loads(result.stdout)["pairs"]
        normal = next(pair for pair in checks if pair["background"] == "background" and pair["foreground"] == "foreground")
        self.assertFalse(normal["passes"])
        self.assertEqual(normal["ratio"], 1)
