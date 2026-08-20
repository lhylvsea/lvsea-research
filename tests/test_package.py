import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_required_entrypoints_exist(self) -> None:
        for relative in ("SKILL.md", "README.md", "manifest.json", "agents/interface.yaml"):
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_manifest_identity(self) -> None:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "lvsea-research")
        self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+$")

    def test_single_root_skill_entrypoint(self) -> None:
        entries = [
            path.relative_to(ROOT).as_posix()
            for path in ROOT.rglob("SKILL.md")
            if ".git" not in path.parts
        ]
        self.assertEqual(entries, ["SKILL.md"])


if __name__ == "__main__":
    unittest.main()
