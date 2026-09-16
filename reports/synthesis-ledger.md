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
| Research-to-diagram separation of research, structure and rendering | wshuyi/research-to-diagram | A visual artifact is more trustworthy when its nodes and edges come from an explicit evidence process rather than decorative layout |
| Visual grammar matched to the object | wshuyi/research-to-diagram | People, concepts, processes, architectures and timelines need different node, edge and layout choices |
| Editable source plus rendered artifact plus sources | wshuyi/research-to-diagram | DOT can be reviewed and revised; the rendered file serves communication; the source ledger preserves auditability |

## Adapt

| Source pattern | Adaptation in lvsea-research |
| --- | --- |
| Any one provider as the recommended search tool | Provider-neutral selection: AnySearch, a verified multi-engine tool, host Web/browser, or local files; record actual invocation and downgrade |
| Fixed deep-report length and PDF output | Three depths: quick, standard and deep; format follows user need |
| Bayesian probability as default | Use numbers only with a defensible reference class and update assumptions; otherwise use qualitative confidence, intervals or a test |
| Diagnosis as a harsh, doctrine-driven funnel | Ask the smallest high-value question, challenge premises directly but respectfully, and never invent psychology or population rates |
| Benchmarking by profit or imitation alone | Compare cost, quality, safety, compliance, sustainability and transfer conditions in addition to economics; learn mechanisms without copying protected assets |
| History as a long narrative | Use stages and source-backed nodes; expand only when history changes the current decision |
| Claude Code WebSearch and macOS-specific installation | Provider-neutral source plan; host Web/browser, AnySearch, multi-engine or local material; package-owned cross-platform renderer |
| Fixed “10x faster”, 2–5 minute, 50+ node and PDF-size claims | Keep only the bounded readability heuristic; record time, node count and file size as run evidence when actually measured |
| PlantUML/Mermaid as if already available | Treat as optional adapters; only claim them after the host has the renderer and a successful invocation |
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
- Treating a graph’s visual neatness as evidence for an unsupported node or relationship.
- Adding a second root Skill or mirroring the upstream plugin tree into a vertical router.

## Invent

1. A single evidence ledger shared by retrieval, fact-check, decision, timeline, benchmark and history routes.
2. A deterministic route interface with primary route, collaborators, source lanes, depth, risk flags and provider fallback.
3. A two-layer contract: short conclusion first, auditable evidence appendix second.
4. A claim-strength rule that couples wording to source grade, independence, uncertainty and counterevidence.
5. A generalization gate: a method enters the core only when it helps at least three request families and has a trigger/near-neighbor test.
6. A provider state vocabulary: configured, discoverable, actually called, output captured, human reviewed, or missing evidence.
7. A maintenance boundary: references carry judgment; scripts carry deterministic checks; reports carry provenance and limitations.
8. A Chinese-first operating style shaped for manufacturing management, policy, safety, operations, AI tools and reusable local artifacts.
9. A research-to-visualization route that keeps evidence mapping, editable DOT, rendered output and visual QA as separate checkpoints.

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
- research-driven relationship, concept, process, technical architecture and knowledge-graph visualization.

The methods are therefore implemented as a router with modules, not as one inseparable mega-prompt. Pure conversion of user-provided structured data remains a renderer action, not a research claim.
