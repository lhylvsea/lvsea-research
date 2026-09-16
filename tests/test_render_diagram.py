import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from render_diagram import default_output_path, render_dot


class RenderDiagramTests(unittest.TestCase):
    def test_default_output_uses_requested_format(self) -> None:
        self.assertEqual(default_output_path(Path("topic.dot"), "svg"), Path("topic.svg"))

    def test_missing_input_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing.dot"
            with self.assertRaises(FileNotFoundError):
                render_dot(missing, Path(directory) / "out.pdf", "pdf", dot_command="dot")

    def test_successful_render_replaces_temp_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            input_path = root / "topic.dot"
            output_path = root / "nested" / "topic.pdf"
            input_path.write_text("digraph G { a -> b }\n", encoding="utf-8")

            def fake_run(command, **kwargs):
                Path(command[-1]).write_bytes(b"fake-pdf")
                return SimpleNamespace(returncode=0, stdout="", stderr="")

            with patch("render_diagram.subprocess.run", side_effect=fake_run):
                result = render_dot(input_path, output_path, "pdf", dot_command="dot")

            self.assertEqual(result, output_path.resolve())
            self.assertEqual(output_path.read_bytes(), b"fake-pdf")
            self.assertFalse(any(root.rglob(".lvsea-diagram-*")))

    def test_existing_output_requires_force(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            input_path = root / "topic.dot"
            output_path = root / "topic.pdf"
            input_path.write_text("digraph G { a -> b }\n", encoding="utf-8")
            output_path.write_bytes(b"keep-me")
            with self.assertRaises(FileExistsError):
                render_dot(input_path, output_path, "pdf", dot_command="dot")
            self.assertEqual(output_path.read_bytes(), b"keep-me")


if __name__ == "__main__":
    unittest.main()
