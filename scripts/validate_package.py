#!/usr/bin/env python3
"""Validate the governed package contract for lvsea-research."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


REQUIRED_FILES = (
    "SKILL.md",
    "README.md",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "agents/interface.yaml",
    "manifest.json",
    "evals/trigger_cases.json",
    "evals/route_cases.json",
    "reports/prior-art-research.md",
    "reports/synthesis-ledger.md",
    "reports/creation-handoff.md",
    "reports/output-evidence.json",
)
SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"""(?i)(?:api[_-]?key|secret|password|token)\s*[:=]\s*["'][^"']{8,}["']"""),
)


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"(?s)\A---\s*\n(.*?)\n---", text)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def local_links(text: str) -> list[str]:
    links = re.findall(r"\]\(([^)]+)\)", text)
    return [
        link.split("#", 1)[0].strip()
        for link in links
        if link.endswith(".md") and not link.startswith(("http://", "https://"))
    ]


def scan_secrets(root: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".json", ".yaml", ".yml", ".py", ".toml"}:
            continue
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            for pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    findings.append({"file": path.relative_to(root).as_posix(), "line": line_number, "kind": pattern.pattern})
    return findings


def validate(root: Path) -> dict[str, Any]:
    root = root.resolve()
    failures: list[str] = []
    warnings: list[str] = []
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            failures.append(f"missing required file: {relative}")

    skill_path = root / "SKILL.md"
    skill_text = skill_path.read_text(encoding="utf-8") if skill_path.is_file() else ""
    frontmatter = parse_frontmatter(skill_text)
    if frontmatter.get("name") != "lvsea-research":
        failures.append("SKILL.md frontmatter name must be lvsea-research")
    if not frontmatter.get("description"):
        failures.append("SKILL.md frontmatter description is missing")
    if len(skill_text.encode("utf-8")) > 14000:
        failures.append("SKILL.md exceeds 14000 UTF-8 bytes")
    for link in local_links(skill_text):
        if not (root / link).exists():
            failures.append(f"SKILL.md links to missing local file: {link}")
    discovered = sorted(
        path.relative_to(root).as_posix()
        for path in root.rglob("SKILL.md")
        if path.relative_to(root).as_posix() != "SKILL.md" and ".git" not in path.parts
    )
    if discovered:
        failures.append("nested discoverable SKILL.md files found: " + ", ".join(discovered))
    if re.search(r"(?:C:\\Users\\|/Users/|/home/|BEGIN .*PRIVATE KEY)", skill_text, re.I):
        failures.append("SKILL.md contains private path or private-key marker")

    manifest: dict[str, Any] = {}
    manifest_path = root / "manifest.json"
    if manifest_path.is_file():
        try:
            manifest = load_json(manifest_path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            failures.append(f"manifest.json is invalid: {exc}")
        if manifest.get("name") != frontmatter.get("name"):
            failures.append("manifest.json name does not match SKILL.md")
        if not re.fullmatch(r"\d+\.\d+\.\d+", str(manifest.get("version", ""))):
            failures.append("manifest.json version must be semantic X.Y.Z")
        for field in ("owner", "updated_at", "status", "maturity_tier", "review_due", "review_cadence", "release_gates"):
            if not manifest.get(field):
                failures.append(f"manifest.json missing governed field: {field}")

    interface_path = root / "agents/interface.yaml"
    interface_text = interface_path.read_text(encoding="utf-8") if interface_path.is_file() else ""
    for field in ("display_name:", "short_description:", "default_prompt:", "adapter_targets:"):
        if field not in interface_text:
            failures.append(f"agents/interface.yaml missing {field}")

    readme = (root / "README.md").read_text(encoding="utf-8") if (root / "README.md").is_file() else ""
    for marker in ("npx skills add", "你可以这样说", "validate_package.py", "注意事项", "许可证"):
        if marker not in readme:
            warnings.append(f"README may be missing {marker}")

    cases_path = root / "evals/trigger_cases.json"
    if cases_path.is_file():
        cases = load_json(cases_path)
        for bucket in ("should_trigger", "should_not_trigger", "near_neighbor", "adversarial"):
            if not cases.get(bucket):
                warnings.append(f"trigger cases have no {bucket} cases")
    route_path = root / "evals/route_cases.json"
    if route_path.is_file() and not load_json(route_path).get("cases"):
        failures.append("route cases are empty")

    ir_path = root / "reports/skill-ir.json"
    if ir_path.is_file() and manifest:
        try:
            package = load_json(ir_path).get("package", {})
            if package.get("name") != manifest.get("name") or package.get("version") != manifest.get("version"):
                failures.append("reports/skill-ir.json package identity does not match manifest")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            failures.append(f"reports/skill-ir.json is invalid: {exc}")
    else:
        warnings.append("reports/skill-ir.json missing; run export_skill_ir.py")

    trigger_report = root / "reports/trigger-eval.json"
    if trigger_report.is_file():
        try:
            trigger = load_json(trigger_report)
            if trigger.get("ok") is not True:
                failures.append("reports/trigger-eval.json is not passing")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            failures.append(f"reports/trigger-eval.json is invalid: {exc}")
    else:
        warnings.append("reports/trigger-eval.json missing; run trigger_eval.py")

    route_report = root / "reports/route-eval.json"
    if route_report.is_file():
        try:
            route = load_json(route_report)
            if route.get("ok") is not True:
                failures.append("reports/route-eval.json is not passing")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            failures.append(f"reports/route-eval.json is invalid: {exc}")
    else:
        warnings.append("reports/route-eval.json missing; run route_eval.py")

    secrets = scan_secrets(root)
    if secrets:
        failures.append("secret scan found " + str(len(secrets)) + " finding(s)")

    return {
        "ok": not failures,
        "root": root.name,
        "failures": failures,
        "warnings": warnings,
        "secret_findings": secrets,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the governed lvsea-research package.")
    parser.add_argument("skill_dir", nargs="?", default=".")
    args = parser.parse_args()
    result = validate(Path(args.skill_dir))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["ok"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
