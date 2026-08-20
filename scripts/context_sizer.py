#!/usr/bin/env python3
"""Measure the context footprint of lvsea-research."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def measure(root: Path) -> dict[str, Any]:
    root = root.resolve()
    groups = {
        "entrypoint": [root / "SKILL.md"],
        "interface": [root / "agents/interface.yaml", root / "manifest.json"],
        "references": sorted((root / "references").glob("*.md")),
        "scripts": sorted((root / "scripts").glob("*.py")),
        "evals": sorted((root / "evals").glob("*")),
    }
    group_stats: dict[str, Any] = {}
    all_files: list[dict[str, Any]] = []
    for group, paths in groups.items():
        total = 0
        for path in paths:
            if not path.is_file():
                continue
            size = path.stat().st_size
            total += size
            all_files.append({"path": path.relative_to(root).as_posix(), "bytes": size, "group": group})
        group_stats[group] = {"bytes": total, "files": sum(1 for row in all_files if row["group"] == group)}
    entry_bytes = group_stats["entrypoint"]["bytes"]
    reference_bytes = group_stats["references"]["bytes"]
    status = "pass"
    warnings: list[str] = []
    if entry_bytes > 14000:
        status = "block"
        warnings.append("SKILL.md exceeds the production entrypoint budget of 14000 UTF-8 bytes")
    if reference_bytes > 100000:
        status = "warn" if status != "block" else status
        warnings.append("references exceed 100000 UTF-8 bytes; load only the module needed by the route")
    all_files.sort(key=lambda row: row["bytes"], reverse=True)
    return {
        "status": status,
        "root": root.name,
        "entrypoint_bytes": entry_bytes,
        "reference_bytes": reference_bytes,
        "total_package_bytes": sum(row["bytes"] for row in all_files),
        "groups": group_stats,
        "largest_files": all_files[:10],
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure lvsea-research context budget.")
    parser.add_argument("skill_dir", nargs="?", default=".")
    parser.add_argument("--output", "-o")
    args = parser.parse_args()
    result = measure(Path(args.skill_dir))
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        output = Path(args.output)
        if not output.is_absolute():
            output = Path(args.skill_dir).resolve() / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    if result["status"] == "block":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
