#!/usr/bin/env python3
"""Export the platform-neutral IR for lvsea-research."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def export_ir(root: Path) -> dict[str, Any]:
    root = root.resolve()
    manifest = load_json(root / "manifest.json")
    cases = load_json(root / "evals/trigger_cases.json")
    route_cases = load_json(root / "evals/route_cases.json")
    try:
        from route_request import ROUTES
    except ImportError:
        import sys
        sys.path.insert(0, str(root / "scripts"))
        from route_request import ROUTES

    return {
        "schema_version": "1.0",
        "package": {
            "name": manifest.get("name"),
            "version": manifest.get("version"),
            "owner": manifest.get("owner"),
            "status": manifest.get("status"),
            "maturity_tier": manifest.get("maturity_tier"),
        },
        "intent": manifest.get("intent", {}),
        "triggers": {
            "positive": cases.get("should_trigger", []),
            "negative": cases.get("should_not_trigger", []),
            "near_neighbor": cases.get("near_neighbor", []),
            "adversarial": cases.get("adversarial", []),
            "description_required_concepts": cases.get("description_required_concepts", []),
        },
        "workflow": {
            "primary_routes": {
                name: {
                    "role": value["role"],
                    "source_lanes": value["source_lanes"],
                    "primary_candidates": value["primary_candidates"],
                    "collaborators": value["collaborators"],
                }
                for name, value in ROUTES.items()
            },
            "route_cases": route_cases.get("cases", []),
            "stages": ["intent", "source_plan", "retrieve", "evidence_ledger", "analysis", "challenge", "synthesis", "qa"],
        },
        "resources": {
            "references": sorted(path.relative_to(root).as_posix() for path in (root / "references").glob("*.md")),
            "scripts": sorted(path.relative_to(root).as_posix() for path in (root / "scripts").glob("*.py")),
            "evals": sorted(path.relative_to(root).as_posix() for path in (root / "evals").glob("*")),
            "reports": sorted(path.relative_to(root).as_posix() for path in (root / "reports").glob("*") if path.is_file()),
        },
        "risk": manifest.get("risk", {}),
        "governance": {
            "review_due": manifest.get("review_due"),
            "review_cadence": manifest.get("review_cadence"),
            "release_gates": manifest.get("release_gates", []),
            "publication": "feature branch -> pull request -> versioned release -> discovery -> clean install",
        },
        "portability": {
            "platforms": manifest.get("target_platforms", []),
            "runtime": "agent-skills canonical source; Python scripts are optional deterministic QA helpers",
            "degradation": "provider fallback and evidence-state reporting are required",
        },
        "evidence_boundary": {
            "static_tests_prove": ["package shape", "trigger boundary fixtures", "route regression", "script behavior"],
            "static_tests_do_not_prove": ["current-world factual correctness", "provider availability", "human usefulness", "professional advice"],
            "output_evidence_file": "reports/output-evidence.json",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Export lvsea-research Skill IR.")
    parser.add_argument("skill_dir", nargs="?", default=".")
    parser.add_argument("--output", "-o")
    args = parser.parse_args()
    root = Path(args.skill_dir)
    result = export_ir(root)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        output = Path(args.output)
        if not output.is_absolute():
            output = root.resolve() / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
