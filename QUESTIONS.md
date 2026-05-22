# Open questions for Armin — scgpt-neurodegen-probe

This file is **append-only with respect to Armin's responses**. Cowork
never edits Armin's responses. New questions go at the bottom under the
next-empty heading.

When Armin replies inline, prefix with a timestamp:
`> Armin (2026-05-24): ...`

---

## How to use this file
The repository now has five ADRs in `docs/decisions/`. Each ADR
carries its own "Open questions for Armin" section. This file is the
rolled-up review queue. ADRs with no remaining open questions move
from **Proposed** to **Accepted**.

---

## ADR-0001 — Ground truth + held-out atlas

**Q1.1** — Confirm Option A1 + manual curation for the PD-associated
gene set, or override to A2 (OMIM only) or A3 (GWAS+Mendelian union).

> Armin: <reply>

**Q1.2** — Held-out atlas selection: Cowork needs a specific atlas
published after the chosen model's pretraining cutoff. Suggestions?

> Armin: <reply>

---

## ADR-0002 — Model coverage

**Q2.1** — Confirm Option D (scGPT headline + Geneformer robustness),
or override to Option A (scGPT only) / Option C (both equally).

> Armin: <reply>

**Q2.2** — Confirm pinning a specific HuggingFace revision SHA for
each model rather than tracking "latest."

> Armin: <reply>

---

## ADR-0003 — Null distribution

**Q3.1** — Confirm Option A (gene-label permutation, n=1000).

> Armin: <reply>

**Q3.2** — Confirm covariate-matched permutation (Option D) is
acceptably deferred. What result would trigger adding it?

> Armin: <reply>

---

## ADR-0004 — Reporting standards

**Q4.1** — Confirm Option A (effect size + 95% bootstrap CI as
headline; p-value floored at 0.001 reported alongside).

> Armin: <reply>

**Q4.2** — Confirm n_boot = 1000 and n_perm = 1000 as defaults.

> Armin: <reply>

**Q4.3** — Confirm the README's effect-size interpretation guide
(AUC 0.5/0.6/0.7/0.8+) is in scope for v1.0.0.

> Armin: <reply>

---

## ADR-0005 — Negative-result framing

**Q5.1** — Confirm Option D (two named results subsections in the
README, "did not find" before "did find"). This is the most
portfolio-defensibility-critical question in this queue.

> Armin: <reply>

**Q5.2** — Confirm the "all positive" / "all negative" template
sentences, or specify alternative wording.

> Armin: <reply>
