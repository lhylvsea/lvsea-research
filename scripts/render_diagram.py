#!/usr/bin/env python3
"""Render a reviewed Graphviz DOT artifact without invoking a shell."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


FORMATS = ("pdf", "svg", "png")


def default_output_path(input_path: Path, output_format: str) -> Path:
    return input_path.with_suffix(f".{output_format}")


def render_dot(
    input_path: Path,
    output_path: Path,
    output_format: str,
    *,
    force: bool = False,
    dot_command: str | None = None,
) -> Path:
    if output_format not in FORMATS:
        raise ValueError(f"unsupported output format: {output_format}; choose from {', '.join(FORMATS)}")
    input_path = input_path.expanduser().resolve()
    output_path = output_path.expanduser().resolve()
    if not input_path.is_file():
        raise FileNotFoundError(f"input DOT file not found: {input_path}")
    if input_path == output_path:
        raise ValueError("output path must differ from the input DOT file")
    if output_path.exists() and not force:
        raise FileExistsError(f"output already exists; pass --force to replace it: {output_path}")

    executable = dot_command or shutil.which("dot")
    if not executable:
        raise RuntimeError("Graphviz 'dot' was not found on PATH; install Graphviz before rendering")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            prefix=".lvsea-diagram-",
            suffix=f".{output_format}",
            dir=output_path.parent,
            delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
        environment = os.environ.copy()
        environment["PYTHONUTF8"] = "1"
        environment["PYTHONIOENCODING"] = "utf-8"
        command = [executable, f"-T{output_format}", str(input_path), "-o", str(temporary_path)]
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=environment,
        )
        if completed.returncode != 0:
            detail = (completed.stderr or completed.stdout or "Graphviz returned a non-zero exit code").strip()
            raise RuntimeError(f"Graphviz failed ({completed.returncode}): {detail[:1200]}")
        if not temporary_path.is_file() or temporary_path.stat().st_size == 0:
            raise RuntimeError("Graphviz returned success but produced an empty output")
        os.replace(temporary_path, output_path)
        temporary_path = None
        return output_path
    finally:
        if temporary_path and temporary_path.exists():
            temporary_path.unlink()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a reviewed Graphviz DOT file to PDF, SVG, or PNG.")
    parser.add_argument("input_dot", type=Path, help="input Graphviz DOT file")
    parser.add_argument("--output", type=Path, help="output file; defaults to the input stem")
    parser.add_argument("--format", choices=FORMATS, default="pdf", dest="output_format")
    parser.add_argument("--force", action="store_true", help="replace an existing output file")
    parser.add_argument("--dot-command", help="explicit Graphviz executable path, mainly for controlled hosts")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = args.input_dot.expanduser()
    output_path = args.output.expanduser() if args.output else default_output_path(input_path, args.output_format)
    try:
        result = render_dot(
            input_path,
            output_path,
            args.output_format,
            force=args.force,
            dot_command=args.dot_command,
        )
    except (FileExistsError, FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Rendered {result} ({result.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
