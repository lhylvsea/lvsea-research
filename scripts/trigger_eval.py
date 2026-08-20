#!/usr/bin/env python3
"""Run trigger-boundary regression for lvsea-research."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\u4e00-\u9fff]+", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()


def phrase_present(text: str, phrase: str) -> bool:
    phrase = normalize(phrase)
    if not phrase:
        return False
    if re.search(r"[\u4e00-\u9fff]", phrase):
        return phrase in text
    return f" {phrase} " in f" {text} "


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def parse_description(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"(?ms)^description:\s*(?:[\"'](?P<quoted>.*?)[\"']|(?P<plain>.+?))\s*(?:\n[a-zA-Z_]+:|\n---)", text)
    if match:
        return (match.group("quoted") or match.group("plain") or "").strip()
    return text


def concept_hits(text: str, concepts: dict[str, list[str]]) -> set[str]:
    normalized = normalize(text)
    return {
        name
        for name, phrases in concepts.items()
        if any(phrase_present(normalized, phrase) for phrase in phrases)
    }


def negative_hit(text: str, patterns: list[str]) -> str | None:
    normalized = normalize(text)
    for pattern in patterns:
        if phrase_present(normalized, pattern):
            return pattern
    return None


def case_items(cases: dict[str, Any], bucket: str) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for raw in cases.get(bucket, []):
        if isinstance(raw, str):
            output.append({"text": raw, "family": "default"})
        elif isinstance(raw, dict) and raw.get("text"):
            item = dict(raw)
            item.setdefault("family", "default")
            output.append(item)
    return output


def evaluate(root: Path, cases_path: Path) -> dict[str, Any]:
    cases = load_json(cases_path)
    concepts = cases.get("positive_concepts", {})
    required = set(cases.get("description_required_concepts", []))
    threshold = float(cases.get("recommended_threshold", 0.5))
    description = parse_description(root / "SKILL.md")
    description_hits = concept_hits(description, concepts)
    missing = sorted(required - description_hits)
    negative_patterns = list(cases.get("negative_patterns", []))
    buckets = ("should_trigger", "should_not_trigger", "near_neighbor", "adversarial")
    results: dict[str, list[dict[str, Any]]] = {bucket: [] for bucket in buckets}
    failures: list[dict[str, Any]] = []
    total = 0
    passed = 0
    false_positive = 0
    false_negative = 0
    denominator = max(1, len(required))

    for bucket in buckets:
        default_expected = bucket == "should_trigger"
        for item in case_items(cases, bucket):
            prompt = str(item["text"])
            expected = bool(item.get("expected_trigger", default_expected))
            prompt_hits = concept_hits(prompt, concepts)
            matched = sorted(prompt_hits & description_hits)
            negative = negative_hit(prompt, negative_patterns)
            required_matches = int(item.get("min_concept_matches", 2 if expected else denominator))
            score = min(1.0, len(matched) / denominator)
            predicted = len(matched) >= required_matches and score >= threshold and negative is None
            ok = predicted == expected
            row = {
                "prompt": prompt,
                "family": item.get("family", "default"),
                "expected_trigger": expected,
                "predicted_trigger": predicted,
                "passed": ok,
                "score": round(score, 3),
                "matched_concepts": matched,
                "negative_pattern": negative,
            }
            results[bucket].append(row)
            total += 1
            if ok:
                passed += 1
            else:
                failures.append({"bucket": bucket, **row})
                if expected:
                    false_negative += 1
                else:
                    false_positive += 1

    return {
        "ok": not missing and not failures and total > 0,
        "threshold": threshold,
        "description_concepts": sorted(description_hits),
        "missing_description_concepts": missing,
        "summary": {
            "total": total,
            "passed": passed,
            "false_positive": false_positive,
            "false_negative": false_negative,
            "pass_rate": round(passed / total, 3) if total else 0,
        },
        "bucket_summary": {
            bucket: {
                "total": len(rows),
                "passed": sum(1 for row in rows if row["passed"]),
            }
            for bucket, rows in results.items()
        },
        "failures": failures,
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate lvsea-research trigger boundaries.")
    parser.add_argument("skill_dir", nargs="?", default=".")
    parser.add_argument("--cases", default="evals/trigger_cases.json")
    parser.add_argument("--output", "-o")
    args = parser.parse_args()
    root = Path(args.skill_dir).resolve()
    cases_path = Path(args.cases)
    if not cases_path.is_absolute():
        cases_path = root / cases_path
    result = evaluate(root, cases_path)
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
