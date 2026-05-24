# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added — first implementation slice (2026-05-23)
- **`pd_genes.py`** — canonical PD-gene panel (13 high-confidence
  Mendelian + GWAS; Singleton & Hardy 2019) and extended panel (+16
  Nalls 2019 GWAS loci).
- **`models/embeddings.py`** — `EmbeddingModel` Protocol +
  `SyntheticEmbeddingModel` deterministic embedder (anchor-based
  cluster injection so tests can exercise the full pipeline without
  downloading scGPT weights).
- **`stats/permutation.py`** — gene-label permutation null per
  ADR-0003 with Phipson-Smyth-floored p-values, effect-size z-score,
  and bootstrap-95% CI on the observed statistic (all ADR-0004
  requirements). Standard statistics: `mean_pairwise_cosine`,
  `mean_centroid_distance`, `compactness_score`.
- **`benchmarks/task_a_pd_ranking.py`** — Task A end-to-end:
  `run_pd_ranking_benchmark(model, ...)` returns a `TaskAReport` with
  observed statistic + null mean/SD + effect size + floored p +
  bootstrap CI, all in one dict for downstream reporting.
- **19 unit tests** across `test_pd_genes`, `test_permutation`,
  `test_task_a`. All passing; ruff check clean. Engineered-cluster
  test produces p < 0.01 with effect > 3 SD; null-anchor test does
  not reject.

### Added — ADR sprint (2026-05-19)
- **ADR-0002** — Model coverage (proposed scGPT headline + Geneformer
  robustness).
- **ADR-0003** — Null distribution methodology (proposed gene-label
  permutation, n=1000, per brief §6.4 item 4).
- **ADR-0004** — Reporting standards (proposed effect size + 95% CI +
  floored p-value, per brief §6.4 item 5).
- **ADR-0005** — Negative-result framing (proposed two named results
  subsections with "did not find" before "did find," per brief §6.4
  item 6).
- Decision-log index with dependency graph and reader-by-role guidance.
- QUESTIONS.md reorganized as a per-ADR Saturday-morning review queue.
- STATUS.md updated for the ADR-sprint phase.

### Notes
All five ADRs are in **Proposed — awaiting Armin sign-off**. The
README's two-subsection results structure is committed *before* any
benchmark runs, per ADR-0005's "framing predates results" requirement.

### Added — scaffolding (pre-sprint)
- Initial repository scaffolding per the Cowork brief §2.1.
- CI workflow, docs workflow, release workflow.
- mkdocs-material site skeleton.
