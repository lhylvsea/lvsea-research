#!/usr/bin/env python3
"""Run local release gates for lvsea-research."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from validate_package import scan_secrets, validate


def run(args: list[str], cwd: Path) -> dict[str, Any]:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    completed = subprocess.run(
        args,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    return {
        "ok": completed.returncode == 0,
        "returncode": completed.returncode,
        "stdout": completed.stdout[-4000:],
        "stderr": completed.stderr[-4000:],
    }


def evaluate(root: Path, phase: str, run_tests: bool) -> dict[str, Any]:
    root = root.resolve()
    gates: list[dict[str, Any]] = []
    package = validate(root)
    gates.append({"gate": "package_validation", "status": "pass" if package["ok"] else "block", "evidence": package})

    route = run(["python", "scripts/route_eval.py", ".", "--cases", "evals/route_cases.json"], root)
    gates.append({"gate": "route_regression", "status": "pass" if route["ok"] else "block", "evidence": route})

    trigger = run(["python", "scripts/trigger_eval.py", ".", "--cases", "evals/trigger_cases.json"], root)
    gates.append({"gate": "trigger_regression", "status": "pass" if trigger["ok"] else "block", "evidence": trigger})

    secrets = scan_secrets(root)
    gates.append({"gate": "secret_scan", "status": "pass" if not secrets else "block", "evidence": {"findings": secrets}})

    if run_tests:
        tests = run(["python", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"], root)
        gates.append({"gate": "unit_tests", "status": "pass" if tests["ok"] else "block", "evidence": tests})
    else:
        gates.append({"gate": "unit_tests", "status": "warn", "evidence": {"missing_evidence": "rerun with --run-tests"}})

    branch = run(["git", "branch", "--show-current"], root)
    branch_name = branch["stdout"].strip() if branch["ok"] else ""
    branch_status = "pass" if branch_name and branch_name not in {"main", "master"} else "block"
    gates.append({"gate": "feature_branch", "status": branch_status, "evidence": {"branch": branch_name}})

    diff = run(["git", "diff", "--check"], root)
    gates.append({"gate": "git_diff_check", "status": "pass" if diff["ok"] else "block", "evidence": diff})

    evidence_path = root / "reports/output-evidence.json"
    evidence = json.loads(evidence_path.read_text(encoding="utf-8")) if evidence_path.is_file() else {}
    evidence_status = "pass" if evidence.get("evidence_kind") in {"provider_backed", "human_blind_review"} and evidence.get("ok") is True else "warn"
    gates.append({"gate": "provider_or_human_output_evidence", "status": evidence_status, "evidence": evidence or {"missing_evidence": True}})

    blocks = [gate for gate in gates if gate["status"] == "block"]
    warnings = [gate for gate in gates if gate["status"] == "warn"]
    return {
        "ok": not blocks,
        "phase": phase,
        "root": root.name,
        "summary": {
            "pass": len(gates) - len(blocks) - len(warnings),
            "warn": len(warnings),
            "block": len(blocks),
        },
        "gates": gates,
    }


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Check lvsea-research release readiness.")
    parser.add_argument("skill_dir", nargs="?", default=".")
    parser.add_argument("--phase", choices=("local", "pr", "published"), default="local")
    parser.add_argument("--run-tests", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    result = evaluate(Path(args.skill_dir), args.phase, args.run_tests)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        output = Path(args.output)
        if not output.is_absolute():
            output = Path(args.skill_dir).resolve() / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    if not result["ok"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
