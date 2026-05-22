# Status — week of 2026-05-19
Repo: scgpt-neurodegen-probe
Phase: Reasoning — ADR sprint complete, awaiting Armin sign-off

## Completed this week
- **ADR sprint complete** for the §6.4 reasoning checkpoints. Five
  ADRs in `docs/decisions/`, all in **Proposed**:
  - ADR-0001 — Ground-truth construction + held-out atlas.
  - ADR-0002 — Model coverage (proposed scGPT headline + Geneformer
    robustness).
  - ADR-0003 — Null distribution (proposed gene-label permutation,
    n=1000, per brief §6.4 item 4).
  - ADR-0004 — Reporting standards (proposed effect size + 95% CI +
    floored p-value, per brief §6.4 item 5).
  - ADR-0005 — Negative-result framing (proposed two named subsections
    with "did not find" before "did find," per brief §6.4 item 6).
- Decision-log index with dependency graph and reader-by-role guidance.
- QUESTIONS.md reorganized as a Saturday-morning review queue.

## Blockers and questions for Armin
- See `QUESTIONS.md` — sections Q1.x through Q5.x. The most
  portfolio-defensibility-critical item is Q5.1 (negative-result
  framing); the most methodology-critical is Q3.1 (gene-label
  permutation).

## Plan for next week (post-sign-off)
- Implement `models/load_scgpt.py` against a pinned HuggingFace
  revision SHA.
- Implement Task A (PD-gene ranking on DA-neuron embedding) end-to-
  end on the held-out atlas, with the ADR-0003 null + ADR-0004
  reporting format.
- Implement Tasks B and C with the same scaffolding.
- README's two-subsection results structure committed before any
  benchmark runs (per ADR-0005's "framing predates results" rule).

## Burn rate
- Hours this session: ~2 (ADR sprint only)
- Hours to `v0.1.0`: estimated 12-15 once ADRs are signed off
  (scGPT + Geneformer loaders + 3 benchmarks + permutation null +
  reporting + the two-subsection README structure).
