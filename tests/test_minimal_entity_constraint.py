import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class MinimalEntityConstraintTests(unittest.TestCase):
    def test_reference_defines_necessity_and_relationship_gates(self) -> None:
        reference = (ROOT / "references/minimal-entity-constraint.md").read_text(encoding="utf-8")
        for marker in ("如无必需，勿增实体", "实体进入闸门", "关系进入闸门", "停止条件"):
            self.assertIn(marker, reference)

    def test_entrypoint_links_constraint_reference(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("references/minimal-entity-constraint.md", skill)


if __name__ == "__main__":
    unittest.main()
