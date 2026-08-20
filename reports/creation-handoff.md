# Creation Handoff

## Result

Created the original governed package lvsea-research as a Chinese-first vertical research router. It uses one root SKILL.md, modular references, deterministic route/trigger/context/IR scripts, evaluation fixtures, provenance reports and a clear provider/evidence boundary.

## Integrated strengths

- realtime and domain-aware source retrieval;
- source diversity and full-page reading;
- timeline/cross-section intersection;
- evidence grading and Bayesian decision support;
- premise, causal and fact challenge;
- mechanism/value-chain benchmarking;
- historical structure fingerprints with success, failure and counterexample roles;
- evidence-bound conclusions and reversible next actions.

## Deliberate limits

- no upstream source code or restricted prose is bundled;
- no search API key, MCP registration or browser session is created;
- no real user research request was run through the new package during packaging;
- OpenClaw's exact user-specified source could not be directly retrieved on 2026-08-20;
- static package and route tests do not prove current-world factual accuracy or human usefulness.

## Files

- SKILL.md: discoverable entrypoint and routing contract
- README.md: Chinese installation, usage, examples, verification, limitations and troubleshooting
- agents/interface.yaml: platform-neutral interface and trust metadata
- manifest.json: intent, permissions, maturity and release gates
- references/: research method modules
- scripts/: deterministic route, trigger, context, IR, package and release checks
- evals/: trigger and route regression cases
- reports/: research ledger, synthesis ledger, evidence boundary and generated QA reports
- tests/: Python unit tests

## Verification status

Generated reports should be read together with this handoff:

- package structure: run python scripts/validate_package.py .
- route boundaries: run python scripts/route_eval.py . --cases evals/route_cases.json --output reports/route-eval.json
- trigger boundaries: run python scripts/trigger_eval.py . --cases evals/trigger_cases.json --output reports/trigger-eval.json
- platform-neutral IR: run python scripts/export_skill_ir.py . --output reports/skill-ir.json
- context budget: run python scripts/context_sizer.py . --output reports/context-budget.json
- local release gates: run python scripts/release_check.py . --phase local --run-tests

## Publication boundary

The intended release chain is feature branch, pull request, versioned Release, public skill discovery and clean installation. Direct default-branch pushes are not part of the accepted process.
