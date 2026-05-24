"""Canonical PD-associated gene panel for the PD-ranking benchmark.

The benchmark question (per ADR-0001): do single-cell foundation-model
embeddings (scGPT, Geneformer) place known PD genes nearer to each other
than they do random genes, when restricted to substantia-nigra
dopaminergic-neuron context?

This module is the single source of truth for *what counts as a PD gene*
in that benchmark. Two tiers:

* :data:`PD_CORE_GENES` — high-confidence Mendelian PD genes (PARK1-22
  loci where the gene is named) + the strongest GWAS hits. These are
  what the headline benchmark uses.
* :data:`PD_EXTENDED_GENES` — core + lower-confidence GWAS associations.
  Used for a robustness check; results on this set are reported in a
  separate column.

Sources:

* Singleton & Hardy (2019) *Lancet Neurol* 18:1146-1156 (Mendelian).
* Nalls et al. (2019) *Lancet Neurol* 18:1091-1102 (GWAS meta-analysis).
"""

from __future__ import annotations

from typing import Final

PD_CORE_GENES: Final[tuple[str, ...]] = (
    "SNCA",  # PARK1/4 — alpha-synuclein
    "PRKN",  # PARK2 — Parkin
    "PINK1",  # PARK6
    "PARK7",  # DJ-1
    "LRRK2",  # PARK8
    "ATP13A2",  # PARK9
    "FBXO7",  # PARK15
    "VPS35",  # PARK17
    "DNAJC6",  # PARK19
    "SYNJ1",  # PARK20
    "GBA1",  # major risk locus (heterozygous)
    "MAPT",  # tau, also implicated in PD
    "VPS13C",  # autosomal recessive PD
)
"""Thirteen high-confidence PD genes."""

PD_EXTENDED_GENES: Final[tuple[str, ...]] = (
    *PD_CORE_GENES,
    "BST1",
    "RAB29",
    "GAK",
    "DGKQ",
    "STK39",
    "SREBF1",
    "MCCC1",
    "TMEM175",
    "GPNMB",
    "INPP5F",
    "FYN",
    "CRHR1",
    "KANSL1",
    "WNT3",
    "SETD1A",
    "RIT2",
)
"""Core + 16 GWAS-significant loci from Nalls 2019 meta-analysis."""


def pd_core() -> tuple[str, ...]:
    """Return the high-confidence Mendelian + strong-GWAS PD gene list."""
    return PD_CORE_GENES


def pd_extended() -> tuple[str, ...]:
    """Return the extended PD gene list (core + GWAS expansion)."""
    return PD_EXTENDED_GENES


__all__ = ["PD_CORE_GENES", "PD_EXTENDED_GENES", "pd_core", "pd_extended"]
