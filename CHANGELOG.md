# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
