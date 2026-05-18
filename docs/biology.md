# Biology primer for scgpt-neurodegen-probe

Audience: ML / engineering readers who need the biological context to read
this repo's README confidently. Skip if you already know the territory.

## Single-cell foundation models, in one paragraph
"Foundation model" here means a transformer (or similar) pretrained on
a very large single-cell transcriptomics corpus, producing an embedding
of cells (and sometimes genes) that downstream tasks can use without
further training. scGPT (Cui et al. 2024, Nat Methods) and Geneformer
(Theodoris et al. 2023, Nature) are the two most cited. Both have
documented strengths on cell-type clustering and gene-network reasoning,
and both have published critiques on disease tasks. The probe here is
not arguing either side — it is asking, on a small set of well-defined
neurodegeneration benchmarks, what the embeddings actually do.

## Why ranking and separation, not classification
Zero-shot classification on cell types is the most-reported benchmark
in this space, and it is also the easiest one to look good on. Disease
biology asks harder questions: does the embedding place known PD-associated
genes near each other? Does it separate PD from HD without supervision?
These are the questions the field cares about, and they are where
pretrained models struggle most visibly. This probe focuses there
deliberately.

## Authoritative sources
This primer was written from public, citable sources. Where a claim is made
about disease biology, the underlying source is one of:

- HGNC (https://www.genenames.org/) — gene symbols
- OpenTargets (https://platform.opentargets.org/) — target-disease associations
- Reactome (https://reactome.org/) — pathway definitions
- UniProt (https://www.uniprot.org/) — protein function
- Primary literature (cited in README §Method)

If you find a claim here that is not defensible from these sources, open
an issue — that is a defect.
