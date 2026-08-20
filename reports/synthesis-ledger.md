# Keep / Adapt / Reject / Invent Ledger

## Keep

| Capability | Source inspiration | Why it generalizes |
| --- | --- | --- |
| Vertical-domain discovery before specialized search | anysearch | Domain-specific queries have different identifiers and required fields; discovering the schema reduces invalid or shallow searches |
| Batch search and full-page extraction | anysearch | Research needs coverage and primary-page reading, not a single snippet |
| Region/language/time/operator diversity | user-specified multi-search-engine lead and current research practice | Different query surfaces reduce blind spots; diversity is a coverage tactic, not a quality guarantee |
| Longitudinal and cross-sectional views | hv-analysis | History explains path dependence; current comparison explains present position |
| Intersection insight and conditional scenarios | hv-analysis | The value of research is the mechanism connecting evidence, not a second summary |
| Reference class, evidence grades and weak priors | yao-bayesian | Uncertainty becomes visible and numeric claims are less likely to outrun their evidence |
| Sensitivity, action thresholds and information value | yao-bayesian | A research answer should say what to do and what would change the decision |
| Staged premise challenge | dbs-diagnosis, reworded independently | Many requests fail because the question, not the answer, is under-specified |
| Consistent value-chain comparison | dbs-benchmark, reworded independently | Benchmarking needs mechanism and execution detail, not surface resemblance |
| Structure fingerprint and success/failure/counterexample roles | dbs-standard-answer, reworded independently | Historical analogies need structural similarity and boundary checks |

## Adapt

| Source pattern | Adaptation in lvsea-research |
| --- | --- |
| Any one provider as the recommended search tool | Provider-neutral selection: AnySearch, a verified multi-engine tool, host Web/browser, or local files; record actual invocation and downgrade |
| Fixed deep-report length and PDF output | Three depths: quick, standard and deep; format follows user need |
| Bayesian probability as default | Use numbers only with a defensible reference class and update assumptions; otherwise use qualitative confidence, intervals or a test |
| Diagnosis as a harsh, doctrine-driven funnel | Ask the smallest high-value question, challenge premises directly but respectfully, and never invent psychology or population rates |
| Benchmarking by profit or imitation alone | Compare cost, quality, safety, compliance, sustainability and transfer conditions in addition to economics; learn mechanisms without copying protected assets |
| History as a long narrative | Use stages and source-backed nodes; expand only when history changes the current decision |
| Parallel subagents as a requirement | Parallel lanes are optional host capabilities; a single agent can run the same query matrix sequentially |

## Reject

- Copying upstream SKILL.md prose, example cases, scripts, templates, images or provider code.
- Treating search snippets, Stars, downloads, catalog scores or a provider's own privacy claim as evidence of factual correctness.
- A forced 10,000–30,000 word report for every request.
- Precise posterior probabilities without a base rate, likelihood model or sensitivity check.
- Absolute axioms, arbitrary thresholds, psychological labels or claims such as “always”, “only”, “most” without evidence.
- Asking the user to choose internal routes when the route can be inferred safely.
- Calling all routes or all search engines on every request.
- Treating an installed/configured provider as actually called.
- Publishing upstream CC BY-NC content or silently changing its license boundary.

## Invent

1. A single evidence ledger shared by retrieval, fact-check, decision, timeline, benchmark and history routes.
2. A deterministic route interface with primary route, collaborators, source lanes, depth, risk flags and provider fallback.
3. A two-layer contract: short conclusion first, auditable evidence appendix second.
4. A claim-strength rule that couples wording to source grade, independence, uncertainty and counterevidence.
5. A generalization gate: a method enters the core only when it helps at least three request families and has a trigger/near-neighbor test.
6. A provider state vocabulary: configured, discoverable, actually called, output captured, human reviewed, or missing evidence.
7. A maintenance boundary: references carry judgment; scripts carry deterministic checks; reports carry provenance and limitations.
8. A Chinese-first operating style shaped for manufacturing management, policy, safety, operations, AI tools and reusable local artifacts.

## Generalization gate result

The combined design supports at least these independent families:

- current fact retrieval and URL extraction;
- fact and number verification;
- product/company/technology/policy research;
- timeline plus current comparison;
- business or engineering decision;
- premise and problem diagnosis;
- benchmark and competitor comparison;
- historical analogy and conditional standard answers.

The methods are therefore implemented as a router with modules, not as one inseparable mega-prompt.
