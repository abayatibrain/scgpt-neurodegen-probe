# Data sources for scgpt-neurodegen-probe

## Pretrained models (frozen)
- **scGPT**: weights from the model's release on HuggingFace; pinned to
  a specific revision SHA documented here.
- **Geneformer**: optional second model; pinned similarly.

## Ground-truth gene sets
- **PD-associated genes**: OpenTargets-derived per ADR-0001 (Option A1),
  with manual curation file at `data/curation_pd_genes.md`.

## Held-out atlas
- To be selected per ADR-0001 (Option C1). Must be published *after*
  the chosen model's pretraining cutoff. Cutoff date and atlas publication
  date both recorded here once Q2 of QUESTIONS.md is resolved.

## Provenance
The pretraining cutoff is recorded so reviewers can verify
non-contamination without re-checking the model paper.