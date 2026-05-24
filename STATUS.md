# Status — week of 2026-05-19
Repo: scgpt-neurodegen-probe
Phase: Implementation — first slice landed

## Completed this week
- ADR sprint (five ADRs proposed; see `docs/decisions/`).
- **First implementation slice landed (2026-05-23):**
  - `pd_genes.py` — canonical PD-gene panel (13 high-confidence
    Mendelian + GWAS) and extended panel (+16 Nalls 2019 GWAS loci).
    Sourced from Singleton & Hardy (2019) and Nalls et al. (2019).
  - `models/embeddings.py` — `EmbeddingModel` Protocol so scGPT /
    Geneformer / synthetic models are swappable.
    `SyntheticEmbeddingModel` is the testable stand-in: hashes gene
    symbols into deterministic vectors and offsets a configurable
    anchor set toward a shared direction. Lets the benchmark have a
    known-truthy signal without downloading scGPT weights.
  - `stats/permutation.py` — gene-label permutation null per
    ADR-0003, with Phipson-Smyth-floored p-values, effect-size
    z-score, and bootstrap-95% CI on the observed statistic (all
    ADR-0004 requirements). Standard statistics:
    `mean_pairwise_cosine`, `mean_centroid_distance`,
    `compactness_score`.
  - `benchmarks/task_a_pd_ranking.py` — Task A end-to-end:
    `run_pd_ranking_benchmark(model, ...)` returns a `TaskAReport`
    with everything needed for the README's results table.

## Tests
- 19 unit tests across `test_pd_genes`, `test_permutation`,
  `test_task_a`. All passing; ruff clean.
- Permutation test correctness: engineered-cluster foreground produces
  p < 0.01 with effect size > 3 SD; random foreground does not reject;
  Phipson-Smyth floor is exact at 1/(n+1).
- Task A end-to-end: detects the engineered PD-cluster anchor at
  p < 0.05; reports clean "null" result when anchor strength = 0.

## ADRs added or updated this week
- All five ADRs (0001–0005) status unchanged: Proposed. Implementation
  was built under the "just go" posture; flip to Accepted on user
  review.

## Blockers and questions for Armin
- See `QUESTIONS.md`. None block the next implementation slice. The
  highest-leverage item remains Q5.1 (negative-result framing) — this
  shapes how the README presents results when the real scGPT run
  produces them.

## Plan for next week
- Implement `models/load_scgpt.py` against a pinned HuggingFace
  revision SHA (gated on Q2.1 ADR sign-off).
- Implement `models/load_geneformer.py` as the robustness check.
- Implement Tasks B (disease separation) and C (cell-type) on the
  same `EmbeddingModel` abstraction.
- README's two-subsection results structure committed before any
  real-model benchmark runs (per ADR-0005's "framing predates
  results" rule).

## Burn rate
- Hours this week: ~4 (ADR sprint + first implementation slice).
- Hours to `v0.1.0`: ~8-10 more (real model loaders + tasks B/C +
  notebook).
