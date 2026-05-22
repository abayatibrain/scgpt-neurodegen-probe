# Decision log

Every non-trivial decision in this repo lives here as an Architecture
Decision Record (ADR). Reading these in order should let you
reconstruct every meaningful judgment call that shaped the code,
without reading the code itself.

The ADR template lives at [`templates/adr.md`](../templates/adr.md).

## Index — current ADRs

| ADR | Title | Status |
|-----|---------------------------------------------------------|--------|
| [0001](0001.md) | Ground-truth construction and training-data leakage handling | Proposed |
| [0002](0002.md) | Model coverage (scGPT headline + Geneformer robustness) | Proposed |
| [0003](0003.md) | Null distribution methodology (gene-label permutation) | Proposed |
| [0004](0004.md) | Reporting standards (effect sizes, CIs, p-value floor) | Proposed |
| [0005](0005.md) | Negative-result framing | Proposed |

All five ADRs are in **Proposed — awaiting Armin sign-off**.
Implementation work waits until the relevant ADR ratifies.

## Dependency graph

```
ADR-0001 (ground truth + held-out)
   └── ADR-0002 (model coverage; pretraining-cutoff check per model)
        └── ADR-0003 (gene-label permutation null)
             └── ADR-0004 (reporting: CI + floored p-value)
                  └── ADR-0005 (negative-result framing; uses ADR-0004's CI to discriminate "at chance")
```

## How to read these ADRs

ADR-0005 (negative-result framing) is the most defensibility-critical
of the five. A hiring panel scanning this repo for honesty will look
at how negative results are reported.

ADR-0003 (null distribution) is the most consequential methodology
choice — get this wrong and every benchmark p-value is meaningless.

ADR-0002 (model coverage) is where to push back if you want the probe
to test a different model or both equally.
