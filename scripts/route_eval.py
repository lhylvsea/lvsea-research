#!/usr/bin/env python3
"""Run deterministic route regression for lvsea-research."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from route_request import choose_route  # noqa: E402


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def evaluate(cases_path: Path, extra_roots: list[str] | None = None) -> dict[str, Any]:
    cases = load_json(cases_path)
    rows: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for raw in cases.get("cases", []):
        if not isinstance(raw, dict) or not raw.get("text"):
            continue
        result = choose_route(str(raw["text"]), extra_roots)
        expected = str(raw.get("expected_route", ""))
        expected_depth = raw.get("expected_depth")
        passed = result["route"] == expected
        if expected_depth:
            passed = passed and result["depth"] == expected_depth
        row = {
            "id": raw.get("id"),
            "text": raw["text"],
            "expected_route": expected,
            "actual_route": result["route"],
            "expected_depth": expected_depth,
            "actual_depth": result["depth"],
            "primary_provider": result["primary_provider"],
            "collaborators": result["collaborator_candidates"],
            "passed": passed,
        }
        rows.append(row)
        if not passed:
            failures.append(row)
    return {
        "ok": bool(rows) and not failures,
        "summary": {
            "total": len(rows),
            "passed": sum(1 for row in rows if row["passed"]),
            "failed": len(failures),
        },
        "failures": failures,
        "results": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate lvsea-research route boundaries.")
    parser.add_argument("skill_dir", nargs="?", default=".")
    parser.add_argument("--cases", default="evals/route_cases.json")
    parser.add_argument("--skills-root", action="append", default=[])
    parser.add_argument("--output", "-o")
    args = parser.parse_args()
    root = Path(args.skill_dir).resolve()
    cases_path = Path(args.cases)
    if not cases_path.is_absolute():
        cases_path = root / cases_path
    result = evaluate(cases_path, args.skills_root)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        output = Path(args.output)
        if not output.is_absolute():
            output = root / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    if not result["ok"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
