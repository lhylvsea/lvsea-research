#!/usr/bin/env python3
"""Deterministic, availability-aware router for lvsea-research."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any


ROUTES: dict[str, dict[str, Any]] = {
    "fast-retrieval": {
        "role": "single-fact, definition, URL, or current-state retrieval",
        "primary_candidates": ["anysearch", "multi-search-engine", "host-web"],
        "collaborators": [],
        "source_lanes": ["direct page", "primary source"],
    },
    "fact-check": {
        "role": "claim, number, date, causality, regulation, or authenticity verification",
        "primary_candidates": ["anysearch", "multi-search-engine", "host-web"],
        "collaborators": ["problem-diagnosis"],
        "source_lanes": ["primary source", "independent check", "counterevidence"],
    },
    "deep-research": {
        "role": "systematic research of a product, company, technology, policy, or concept",
        "primary_candidates": ["anysearch", "multi-search-engine", "host-web"],
        "collaborators": ["fact-check"],
        "source_lanes": ["definition", "mechanism", "current state", "alternatives", "counterevidence", "primary sources"],
    },
    "timeline-cross-section": {
        "role": "longitudinal development plus current cross-sectional comparison",
        "primary_candidates": ["anysearch", "multi-search-engine", "host-web"],
        "collaborators": ["fact-check", "benchmark-comparison"],
        "source_lanes": ["origin", "timeline", "current position", "comparators", "counterevidence"],
    },
    "decision-analysis": {
        "role": "choice, investment, adoption, prioritization, or experiment design",
        "primary_candidates": ["anysearch", "multi-search-engine", "host-web"],
        "collaborators": ["fact-check"],
        "source_lanes": ["reference class", "current evidence", "alternative actions", "disconfirming evidence"],
    },
    "problem-diagnosis": {
        "role": "ambiguous business, management, engineering, or operational problem",
        "primary_candidates": ["host-web", "anysearch", "multi-search-engine"],
        "collaborators": ["decision-analysis"],
        "source_lanes": ["term definitions", "assumption check", "causal evidence", "fact premises", "constraints"],
    },
    "benchmark-comparison": {
        "role": "benchmark, competitor, option, mechanism, or value-chain comparison",
        "primary_candidates": ["anysearch", "multi-search-engine", "host-web"],
        "collaborators": ["fact-check"],
        "source_lanes": ["candidate set", "value chain", "cost and quality", "risk and compliance", "failure evidence"],
    },
    "historical-analogy": {
        "role": "historical analogy, standard-answer research, or reusable mechanism",
        "primary_candidates": ["anysearch", "multi-search-engine", "host-web"],
        "collaborators": ["fact-check"],
        "source_lanes": ["closest success", "cross-domain mechanism", "failure case", "boundary or counterexample"],
    },
}

PROVIDERS: dict[str, dict[str, Any]] = {
    "anysearch": {
        "skills": ["anysearch"],
        "role": "managed realtime search, vertical discovery, batch search, and extraction",
    },
    "multi-search-engine": {
        "skills": ["multi-search-engine"],
        "role": "no-key search URL diversification and comparison",
    },
    "host-web": {
        "skills": [],
        "role": "host-managed web or browser capability; availability must be reported by the host",
    },
}

EXPLICIT_ALIASES = {
    "fast-retrieval": ["fast-retrieval", "fast retrieval", "快速查", "查一个事实"],
    "fact-check": ["fact-check", "fact check", "事实核验", "查证"],
    "deep-research": ["deep-research", "deep research", "深度研究", "系统研究"],
    "timeline-cross-section": ["timeline-cross-section", "横纵分析", "时间线与横截面"],
    "decision-analysis": ["decision-analysis", "bayesian", "贝叶斯", "决策分析"],
    "problem-diagnosis": ["problem-diagnosis", "商业诊断", "问题诊断", "前提挑战"],
    "benchmark-comparison": ["benchmark-comparison", "竞品分析", "对标分析", "方案比较"],
    "historical-analogy": ["historical-analogy", "历史同构", "标准答案", "历史类比"],
}


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def _has(text: str, *terms: str) -> bool:
    return any(term.lower() in text for term in terms)


def _skill_roots(extra: list[str] | None = None) -> list[Path]:
    roots: list[Path] = []
    raw = os.environ.get("LVSEA_SKILLS_ROOTS", "")
    if raw:
        roots.extend(Path(item) for item in raw.split(os.pathsep) if item)
    home = Path(os.environ.get("USERPROFILE", Path.home()))
    codex_home = Path(os.environ.get("CODEX_HOME", home / ".codex"))
    roots.extend([codex_home / "skills", home / ".agents" / "skills"])
    if extra:
        roots.extend(Path(item) for item in extra)
    unique: list[Path] = []
    for root in roots:
        root = root.expanduser()
        if root not in unique:
            unique.append(root)
    return unique


def _find_provider(provider: str, roots: list[Path]) -> dict[str, Any]:
    meta = PROVIDERS[provider]
    if provider == "host-web":
        return {
            "provider": provider,
            "available": True,
            "mode": "host-managed",
            "paths": [],
            "role": meta["role"],
        }
    hits: list[str] = []
    for root in roots:
        for name in meta["skills"]:
            candidate = root / name
            if (candidate / "SKILL.md").is_file():
                hits.append(str(candidate))
    return {
        "provider": provider,
        "available": bool(hits),
        "mode": "local-skill" if hits else "not-found",
        "paths": hits,
        "role": meta["role"],
    }


def _explicit_route(text: str) -> str | None:
    for route, aliases in EXPLICIT_ALIASES.items():
        if any(alias in text for alias in aliases):
            return route
    return None


def _depth(text: str) -> str:
    if _has(text, "快查", "一句话", "只查", "quick"):
        return "quick"
    if _has(text, "深度", "系统性", "完整研究", "研究报告", "deep research"):
        return "deep"
    if _has(text, "研究", "调研", "分析", "比较", "查证"):
        return "standard"
    return "quick"


def _risk_flags(text: str) -> list[str]:
    flags: list[str] = []
    if _has(text, "医疗", "疾病", "诊断", "用药", "medical", "health"):
        flags.append("medical")
    if _has(text, "法律", "法规适用", "诉讼", "合同", "legal"):
        flags.append("legal")
    if _has(text, "投资建议", "买股票", "证券", "理财", "financial", "investment"):
        flags.append("financial")
    if _has(text, "安全生产", "人身安全", "重大设备", "危险化学品", "production safety"):
        flags.append("safety-critical")
    return flags


def _choose_route(text: str) -> tuple[str, str]:
    explicit = _explicit_route(text)
    if explicit:
        return explicit, "user explicitly named a stable research route or method"

    if _has(text, "是否", "要不要", "选哪个", "选哪种", "值得做", "投入", "投资", "采用", "改造方案", "先试什么", "should we", "which option"):
        return "decision-analysis", "the request contains an explicit choice, commitment, or experiment"

    if _has(text, "时间线", "发展历程", "从诞生", "历史与现状", "历史和竞品", "timeline"):
        return "timeline-cross-section", "the request asks for both development over time and current comparison"

    if _has(text, "历史案例", "历史上怎么", "标准答案", "同构", "成功案例和失败", "历史类比"):
        return "historical-analogy", "the request asks for reusable mechanisms from historical cases"

    if _has(text, "竞品", "对标", "比较方案", "竞争对手", "替代方案", "benchmark", "competitor"):
        return "benchmark-comparison", "the request asks for a structured comparison or benchmark"

    if _has(text, "为什么不", "问题出在哪", "前提", "假设", "因果", "商业困境", "瓶颈", "诊断", "复盘"):
        return "problem-diagnosis", "the request asks to locate a problem, premise, or causal gap"

    if _has(text, "查证", "核实", "真假", "是否属实", "数字对不对", "法规依据", "fact check", "verify"):
        return "fact-check", "the request asks to verify claims or source-backed facts"

    if _has(text, "是什么", "最新情况", "网页内容", "链接内容", "查一下", "lookup", "extract") and _depth(text) == "quick":
        return "fast-retrieval", "the request is a bounded retrieval task"

    return "deep-research", "the request asks for research without a narrower route signal"


def _collaborators(route: str, text: str) -> list[str]:
    candidates = list(ROUTES[route]["collaborators"])
    if route == "deep-research" and _has(text, "竞品", "对标", "比较", "替代"):
        candidates.insert(0, "benchmark-comparison")
    if route == "decision-analysis" and _has(text, "竞品", "方案", "替代"):
        candidates.insert(0, "benchmark-comparison")
    if route == "fact-check" and _has(text, "因果", "为什么", "原因"):
        candidates.insert(0, "problem-diagnosis")
    unique: list[str] = []
    for item in candidates:
        if item != route and item not in unique:
            unique.append(item)
    return unique[:2]


def choose_route(request: str, extra_roots: list[str] | None = None) -> dict[str, Any]:
    original = request.strip()
    text = _normalize(original)
    route, reason = _choose_route(text)
    depth = _depth(text)
    risk_flags = _risk_flags(text)
    roots = _skill_roots(extra_roots)

    candidate_names = list(ROUTES[route]["primary_candidates"])
    provider_status = {
        name: _find_provider(name, roots)
        for name in sorted(set(candidate_names + _collaborators(route, text)))
        if name in PROVIDERS
    }
    primary_provider = next(
        (
            name
            for name in candidate_names
            if provider_status.get(name, {}).get("available")
        ),
        None,
    )
    collaborator_names = _collaborators(route, text)
    return {
        "request": original,
        "route": route,
        "reason": reason,
        "depth": depth,
        "risk_flags": risk_flags,
        "primary_candidates": candidate_names,
        "primary_provider": primary_provider,
        "method_status": "available",
        "collaborator_candidates": collaborator_names,
        "source_lanes": ROUTES[route]["source_lanes"],
        "provider_status": provider_status,
        "assumptions": {
            "language": "zh-CN",
            "max_clarifying_questions": 3,
            "source_plan": "user_materials_first_then_live_sources",
            "probability_rule": "numeric_only_when_reference_class_and_update_assumptions_are defensible",
            "output_rule": "conclusion_first_evidence_bound",
        },
        "status": "available" if primary_provider else "method-available-provider-fallback",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Route a research request for lvsea-research.")
    parser.add_argument("--text", required=True, help="Natural-language research request")
    parser.add_argument("--skills-root", action="append", default=[], help="Additional skill root; repeatable")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()
    result = choose_route(args.text, args.skills_root)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"route={result['route']}")
        print(f"depth={result['depth']}")
        print(f"primary={result['primary_provider'] or 'host-or-manual-fallback'}")
        print(f"status={result['status']}")
        print(f"reason={result['reason']}")


if __name__ == "__main__":
    main()
