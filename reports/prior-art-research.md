# Prior-Art Research

- Reviewed at: 2026-08-20
- Scope: the seven user-specified sources plus the local lvsea-zao-skill authoring tool
- Policy: read public source and metadata only; do not execute unreviewed upstream scripts or bundle upstream private material
- Result: five repositories were cloned read-only at shallow snapshots, the specified OpenClaw path was independently checked and unavailable, and the local lvsea-zao prior-art script was run as an additional discovery pass

## Source inventory

| Source | Snapshot/evidence | Strongest reusable idea | Main limitation observed | Decision |
| --- | --- | --- | --- | --- |
| anysearch-ai/anysearch-skill | Git commit 69b3088fd36f20e3501951ec3826a208d0b085a4; root SKILL.md, README, CLI/security docs; Apache-2.0 | One search surface with vertical-domain discovery, required-parameter discipline, batch search, full-page extraction, runtime detection and fallback | Provider account, rate limits, privacy claims and API availability remain external; a recommended provider must not become a single-source policy | Keep the decision rules; adapt as an optional provider |
| yaojingang/yao-open-skills/skills/yao-bayesian-skill | Git commit ab04ef5caa57edb5493b2764c636cdb6ceb0a1fa; SKILL.md, seven references, scripts, schema, evals; MIT | Decision brief, reference class, evidence grades, weak prior, multi-turn log, action thresholds, sensitivity and information value | Numeric updates are unsafe without defensible base rates/likelihood assumptions; it is intentionally narrower than broad research | Keep as decision-analysis module; block fake precision |
| KKKKhazix/khazix-skills/hv-analysis | Git commit 7a5c4934be4106ac740ffdb95280bb81b3f4b83c; SKILL.md, schema and PDF renderer; MIT | Longitudinal story, current cross-section, intersection insight, three future scenarios, source priority | Fixed 10,000–30,000 word/PDF expectation is too heavy for quick questions; prose style and hard-coded provider assumptions do not generalize | Adapt as an optional timeline-cross-section route |
| openclaw/skills/.../gpyangyoujun/multi-search-engine | Git clone and raw path checked on 2026-08-20; both returned repository/file not found (404) | Secondary catalogs consistently describe engine diversity, region/language/time filters and operator-based query construction | The user-specified source could not be read directly; third-party catalogs are not authoritative and do not prove ranking, deduplication or engine availability | Do not copy; retain only a clearly labeled, generic source-diversity principle |
| dontbesilent2025/dbskill/dbs-diagnosis | Git commit 7e770e54aaaa8f43cac344b536d3adce095ead8f; SKILL.md and agent metadata; CC BY-NC 4.0 | Automatically challenge ambiguous terms, assumptions, causal leaps, fact premises and information gaps; use staged dialogue | Contains strong unverified axioms, arbitrary population claims, forced harsh voice and psychological overreach; noncommercial license forbids casual reuse | Adapt only the abstract questioning problem; no prose, cases or code copied |
| dontbesilent2025/dbskill/dbs-benchmark | Same dbskill snapshot; SKILL.md; CC BY-NC 4.0 | Compare candidates through a consistent filter and business value chain; inspect execution granularity rather than surface similarity | “Profit is the only standard”, fixed thresholds and dismissing user constraints are too dogmatic; copying can create ethical/legal risk | Adapt into multi-criteria mechanism/benchmark comparison |
| dontbesilent2025/dbskill/dbs-standard-answer | Same dbskill snapshot; SKILL.md, evals and agent metadata; CC BY-NC 4.0 | Structure fingerprint, closest/success/failure/counterexample roles, analogy matrix, conditional answer and failure boundary | Historical analogy can become biography or survivor bias unless source independence and differences are explicit | Keep the structure-fingerprint and conditional-answer pattern, with evidence gates |

## What was actually checked

The following files were read from the local snapshots:

- anysearch: root SKILL.md, README.md/README_zh.md, LICENSE, NOTICE and security/runtime notes
- yao-bayesian: SKILL.md, manifest, interface, trigger cases, intake, evidence/prior, multi-turn, prior hygiene, decision contract and sensitivity references
- hv-analysis: SKILL.md, schema and PDF script metadata
- dbskill: dbs-diagnosis, dbs-benchmark and dbs-standard-answer SKILL.md files, agent metadata, eval metadata and repository license
- OpenClaw source: the exact user URL, Git clone URL, raw SKILL.md and raw README.md path

No upstream executable, installer, hook or provider script was run. Public method descriptions were paraphrased rather than copied into this package.

## Additional lvsea-zao discovery pass

The installed lvsea-zao-skill prior-art script was invoked with four intent queries:

- deep research evidence synthesis
- Bayesian decision analysis
- web research source verification
- competitive historical analysis

The run returned 54 candidate families in its catalog. Three skills.sh query runs completed; the Bayesian query timed out at the configured 15-second limit. SkillsMP was intentionally skipped in this pass. This catalog is discovery evidence only, not proof that a candidate is usable or high quality.

## Evidence and license boundary

- anysearch, yao and hv-analysis use Apache-2.0 or MIT licenses, but this package does not copy their code.
- dbskill is CC BY-NC 4.0. This package does not bundle its prose, examples, scripts, data or cases. The reusable content here is independently worded and limited to generic research questions and comparison structures, with attribution retained.
- The missing OpenClaw source is not treated as confirmed prior art. Secondary directory pages may be used as leads for future review, not as a source of copied implementation or authoritative claims.
