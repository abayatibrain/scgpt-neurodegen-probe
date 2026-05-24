"""Embedding-model abstraction layer.

Per ADR-0002, scGPT is the headline foundation model; Geneformer is the
robustness check. Both are loaded as frozen-weights and queried for
*gene-level embeddings* (one vector per gene token).

This module defines the :class:`EmbeddingModel` Protocol that downstream
benchmarks consume, plus a :class:`SyntheticEmbeddingModel` for tests
that don't have HuggingFace transformers + GPU available.

The two real implementations (:func:`load_scgpt`, :func:`load_geneformer`)
live in ``models/load_scgpt.py`` and ``models/load_geneformer.py``; both
return objects that satisfy :class:`EmbeddingModel`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

import numpy as np
from numpy.random import PCG64, Generator
from numpy.typing import NDArray


@runtime_checkable
class EmbeddingModel(Protocol):
    """Gene-level embedding model used by the benchmark suite.

    Implementations must:

    * Return a deterministic ``(n_genes_known, dim)`` matrix from
      :meth:`embed_genes`.
    * Skip genes they don't know about (the benchmark filters those out
      with a logged warning).
    * Expose a stable ``name`` and ``dim`` for reporting.
    """

    name: str

    @property
    def dim(self) -> int:
        """Embedding dimensionality."""
        ...

    def embed_genes(self, genes: list[str]) -> tuple[NDArray[np.float64], list[str]]:
        """Return ``(matrix, recognized_genes)``.

        ``matrix`` has shape ``(len(recognized_genes), dim)`` in the same
        order as ``recognized_genes``. Genes the model doesn't know are
        silently dropped — caller is responsible for noticing if the
        recovery rate is low.
        """
        ...


@dataclass
class SyntheticEmbeddingModel:
    """Deterministic synthetic embedder for tests.

    Builds embeddings by hashing each gene symbol into a fixed-dim vector,
    then injecting structure: any gene in :attr:`anchor_set` is offset
    toward a shared anchor direction so that they cluster together. This
    is what lets the PD-ranking benchmark have a known-truthy signal
    without downloading scGPT weights.
    """

    name: str = "synthetic"
    dim_: int = 16
    anchor_set: frozenset[str] = field(default_factory=frozenset)
    anchor_strength: float = 2.0
    seed: int = 0xA1BE
    known_genes: frozenset[str] = field(default_factory=frozenset)

    @property
    def dim(self) -> int:
        return self.dim_

    def _rng_for_gene(self, gene: str) -> Generator:
        # Hash the gene name into a 64-bit seed so vectors are stable but
        # independent across genes.
        h = abs(hash((self.seed, gene))) & 0xFFFFFFFFFFFFFFFF
        return Generator(PCG64(h))

    def embed_genes(self, genes: list[str]) -> tuple[NDArray[np.float64], list[str]]:
        kept = [g for g in genes if g in self.known_genes] if self.known_genes else list(genes)
        if not kept:
            return np.zeros((0, self.dim_), dtype=np.float64), []

        # Anchor direction shared by every gene in anchor_set.
        anchor_rng = Generator(PCG64(self.seed ^ 0xDEADBEEF))
        anchor = anchor_rng.normal(0.0, 1.0, size=self.dim_)
        anchor = anchor / max(float(np.linalg.norm(anchor)), 1e-9)

        out = np.zeros((len(kept), self.dim_), dtype=np.float64)
        for i, gene in enumerate(kept):
            v = self._rng_for_gene(gene).normal(0.0, 1.0, size=self.dim_)
            if gene in self.anchor_set:
                v = v + self.anchor_strength * anchor
            out[i] = v
        return out, kept


def make_synthetic_model(
    *,
    pd_genes: tuple[str, ...] = (),
    background_genes: tuple[str, ...] = (),
    dim: int = 16,
    anchor_strength: float = 2.0,
    seed: int = 0xA1BE,
) -> SyntheticEmbeddingModel:
    """Build a synthetic model where ``pd_genes`` cluster.

    The model "knows" ``pd_genes + background_genes`` and reports the
    given dimension. Use this in tests where the PD-ranking benchmark
    must produce a non-trivial result without downloading scGPT.
    """
    known: frozenset[str] = frozenset(set(pd_genes) | set(background_genes))
    return SyntheticEmbeddingModel(
        name="synthetic-pd-cluster",
        dim_=dim,
        anchor_set=frozenset(pd_genes),
        anchor_strength=anchor_strength,
        seed=seed,
        known_genes=known,
    )


__all__ = [
    "EmbeddingModel",
    "SyntheticEmbeddingModel",
    "make_synthetic_model",
]
