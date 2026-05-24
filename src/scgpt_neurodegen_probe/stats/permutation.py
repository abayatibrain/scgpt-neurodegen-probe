"""Gene-label permutation null per ADR-0003.

The hypothesis for every benchmark task: a foundation model's gene
embeddings place "interesting" genes (PD genes, disease genes, cell-
type-marker genes) closer to each other than a randomly chosen gene set
of the same size.

The null is constructed by *permuting gene labels* — re-sampling
``len(gene_set)`` gene names from the same model's vocabulary,
recomputing the statistic of interest, and repeating ``n_permutations``
times. This explicitly accounts for the model's overall geometry
(some embeddings have natural clustering that has nothing to do with
disease relevance).

Per ADR-0004, p-values are *floored* at ``1 / (n_permutations + 1)`` so
the test never reports ``p = 0`` even when no permutation beats the
observed statistic. The literature convention (Phipson & Smyth 2010).
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

import numpy as np
from numpy.random import PCG64, Generator
from numpy.typing import NDArray

Statistic = Callable[[NDArray[np.float64]], float]
"""A statistic that takes an ``(n_genes, dim)`` embedding matrix and
returns a single float (e.g., mean pairwise cosine similarity)."""


@dataclass(frozen=True)
class PermutationResult:
    """Output of :func:`permutation_test`."""

    observed: float
    """Statistic value on the actual gene set."""

    null_distribution: NDArray[np.float64]
    """Statistic values under permuted labels."""

    p_value: float
    """Floored one-sided p-value (fraction of nulls >= observed)."""

    n_permutations: int
    """Size of ``null_distribution``."""

    effect_size: float
    """``(observed - null_mean) / null_std`` (z-score) when null_std > 0,
    else 0.0. ADR-0004's "effect size beside p-value" requirement."""

    ci_95: tuple[float, float]
    """Bootstrap 95% CI on ``observed`` itself (sub-sampling the gene
    set with replacement). Width signals how stable the observed
    statistic is to gene-set composition."""


def _floor_pvalue(observed: float, null: NDArray[np.float64]) -> float:
    n = null.size
    if n == 0:
        return float("nan")
    tail = int(np.sum(null >= observed))
    # Phipson & Smyth 2010 floor.
    return (tail + 1) / (n + 1)


def _bootstrap_observed_ci(
    matrix: NDArray[np.float64],
    statistic: Statistic,
    n_boot: int,
    rng: Generator,
) -> tuple[float, float]:
    """95% CI on the statistic via bootstrap over gene-set composition."""
    if matrix.shape[0] < 2 or n_boot < 1:
        return (float("nan"), float("nan"))
    n = matrix.shape[0]
    vals = np.empty(n_boot, dtype=np.float64)
    for i in range(n_boot):
        idx = rng.integers(0, n, size=n)
        vals[i] = statistic(matrix[idx])
    lo, hi = np.quantile(vals, [0.025, 0.975])
    return float(lo), float(hi)


def permutation_test(
    foreground_matrix: NDArray[np.float64],
    *,
    background_matrix: NDArray[np.float64],
    statistic: Statistic,
    n_permutations: int = 1000,
    n_bootstrap: int = 500,
    seed: int = 0xA1BE,
) -> PermutationResult:
    """Run a gene-label permutation test.

    Parameters
    ----------
    foreground_matrix
        ``(n_fg, dim)`` matrix of embeddings for the "interesting" gene
        set (the alternative hypothesis).
    background_matrix
        ``(n_bg, dim)`` matrix of embeddings for the model's recognized
        gene vocabulary. The null is built by sampling ``n_fg`` rows from
        this matrix, ``n_permutations`` times, and recomputing the
        statistic.
    statistic
        Callable from a 2-D matrix to a scalar.
    n_permutations
        ADR-0003 default = 1000.
    n_bootstrap
        Bootstrap iterations for the observed-statistic CI. 0 disables.
    seed
        RNG seed.
    """
    if foreground_matrix.ndim != 2 or background_matrix.ndim != 2:
        raise ValueError("both matrices must be 2-D")
    if foreground_matrix.shape[1] != background_matrix.shape[1]:
        raise ValueError(
            f"dim mismatch: foreground dim={foreground_matrix.shape[1]} vs "
            f"background dim={background_matrix.shape[1]}"
        )
    if background_matrix.shape[0] < foreground_matrix.shape[0]:
        raise ValueError("background must have at least as many rows as foreground")

    rng = Generator(PCG64(seed))
    observed = float(statistic(foreground_matrix))

    n_fg = foreground_matrix.shape[0]
    n_bg = background_matrix.shape[0]
    null = np.empty(n_permutations, dtype=np.float64)
    for i in range(n_permutations):
        idx = rng.choice(n_bg, size=n_fg, replace=False)
        null[i] = statistic(background_matrix[idx])

    p = _floor_pvalue(observed, null)
    mu_null = float(null.mean())
    sd_null = float(null.std(ddof=0))
    effect = 0.0 if sd_null == 0.0 else (observed - mu_null) / sd_null

    ci = _bootstrap_observed_ci(foreground_matrix, statistic, n_bootstrap, rng)

    return PermutationResult(
        observed=observed,
        null_distribution=null,
        p_value=p,
        n_permutations=n_permutations,
        effect_size=effect,
        ci_95=ci,
    )


# ---------------------------------------------------------------------------
# Standard statistics used by the benchmark tasks.
# ---------------------------------------------------------------------------


def mean_pairwise_cosine(matrix: NDArray[np.float64]) -> float:
    """Mean pairwise cosine similarity of all rows in ``matrix``.

    Used by the PD-ranking benchmark (task A) — if PD genes cluster, this
    mean should be larger than the random-set mean.
    """
    if matrix.shape[0] < 2:
        return float("nan")
    norms = np.linalg.norm(matrix, axis=1)
    safe = np.where(norms == 0, 1.0, norms)
    normalized = matrix / safe[:, None]
    sims = normalized @ normalized.T
    # Drop the diagonal (self-similarity) before averaging.
    n = matrix.shape[0]
    mask = ~np.eye(n, dtype=bool)
    return float(sims[mask].mean())


def mean_centroid_distance(matrix: NDArray[np.float64]) -> float:
    """Mean Euclidean distance from each row to the centroid.

    Used by tasks that ask "how compact is this set?" (lower = more
    compact). Inverted in :func:`permutation_test` if you want
    "higher = better."
    """
    if matrix.shape[0] < 2:
        return float("nan")
    centroid = matrix.mean(axis=0, keepdims=True)
    diffs = matrix - centroid
    return float(np.linalg.norm(diffs, axis=1).mean())


def compactness_score(matrix: NDArray[np.float64]) -> float:
    """Inverse of mean centroid distance, so higher = more compact."""
    d = mean_centroid_distance(matrix)
    if not np.isfinite(d) or d == 0.0:
        return float("nan")
    return 1.0 / d


def filter_to_known(requested: Sequence[str], known: Sequence[str]) -> tuple[list[str], list[str]]:
    """Split ``requested`` into ``(in_known, missing)``, preserving order."""
    known_set = set(known)
    in_known = [g for g in requested if g in known_set]
    missing = [g for g in requested if g not in known_set]
    return in_known, missing


__all__ = [
    "PermutationResult",
    "Statistic",
    "compactness_score",
    "filter_to_known",
    "mean_centroid_distance",
    "mean_pairwise_cosine",
    "permutation_test",
]
