"""Task A — do PD genes cluster in a foundation-model embedding?

The headline benchmark of this repo. Pipeline:

1. Take an :class:`EmbeddingModel` and a list of PD genes
   (:data:`PD_CORE_GENES` by default).
2. Embed the PD genes; embed a "vocabulary" background gene set the
   model recognises.
3. Compute the mean pairwise cosine similarity within the PD set
   (:func:`mean_pairwise_cosine`).
4. Run a gene-label permutation test: re-sample ``len(pd_genes)``
   genes from the background, recompute, repeat ``n_permutations``
   times (ADR-0003 default = 1000).
5. Report effect size + floored p-value + bootstrap CI on the observed
   statistic (ADR-0004).

If the embedding is informative about PD, the observed statistic is
higher than the null distribution and the p-value is small. If it is
not, that's the result — reported plainly per ADR-0005 (two-section
negative-result framing).
"""

from __future__ import annotations

from dataclasses import dataclass

from scgpt_neurodegen_probe.models.embeddings import EmbeddingModel
from scgpt_neurodegen_probe.pd_genes import PD_CORE_GENES
from scgpt_neurodegen_probe.stats.permutation import (
    PermutationResult,
    filter_to_known,
    mean_pairwise_cosine,
    permutation_test,
)


@dataclass(frozen=True)
class TaskAReport:
    """Output of :func:`run_pd_ranking_benchmark`."""

    model_name: str
    pd_genes_used: tuple[str, ...]
    pd_genes_missing: tuple[str, ...]
    background_size: int
    result: PermutationResult

    def as_dict(self) -> dict[str, object]:
        """Flatten to a dict suitable for JSON / dataframe writing."""
        return {
            "model": self.model_name,
            "n_pd_used": len(self.pd_genes_used),
            "n_pd_missing": len(self.pd_genes_missing),
            "background_size": self.background_size,
            "observed_mean_cosine": self.result.observed,
            "null_mean": float(self.result.null_distribution.mean()),
            "null_std": float(self.result.null_distribution.std(ddof=0)),
            "effect_size": self.result.effect_size,
            "p_value": self.result.p_value,
            "ci_low": self.result.ci_95[0],
            "ci_high": self.result.ci_95[1],
            "n_permutations": self.result.n_permutations,
        }


def run_pd_ranking_benchmark(
    model: EmbeddingModel,
    *,
    pd_genes: tuple[str, ...] = PD_CORE_GENES,
    background_genes: tuple[str, ...],
    n_permutations: int = 1000,
    n_bootstrap: int = 500,
    seed: int = 0xA1BE,
) -> TaskAReport:
    """Run Task A end-to-end against ``model``.

    Parameters
    ----------
    model
        Anything satisfying :class:`EmbeddingModel`. The synthetic model
        from :mod:`scgpt_neurodegen_probe.models.embeddings` is the
        default for tests.
    pd_genes
        Gene set to test for clustering.
    background_genes
        Gene vocabulary to draw permutation-null samples from. Must be
        a superset of ``pd_genes``; ``len(background_genes) > len(pd_genes)``.
    n_permutations
        ADR-0003 default = 1000.
    n_bootstrap
        Bootstrap iterations for the observed-statistic CI.
    seed
        RNG seed.
    """
    pd_fg, pd_bg = filter_to_known(pd_genes, background_genes)
    if not pd_fg:
        raise ValueError("no PD genes overlap the background set")

    fg_matrix, fg_recognized = model.embed_genes(pd_fg)
    bg_matrix, _bg_recognized = model.embed_genes(list(background_genes))

    if fg_matrix.shape[0] < 2:
        raise ValueError(f"too few PD genes recognized by model (got {fg_matrix.shape[0]})")
    if bg_matrix.shape[0] < fg_matrix.shape[0] + 1:
        raise ValueError(
            f"background too small ({bg_matrix.shape[0]}) relative to PD set ({fg_matrix.shape[0]})"
        )

    pd_genes_actually_used = tuple(fg_recognized)
    pd_genes_missing = tuple(set(pd_genes) - set(fg_recognized))
    _ = pd_bg  # surfaced for debug; not used further

    result = permutation_test(
        fg_matrix,
        background_matrix=bg_matrix,
        statistic=mean_pairwise_cosine,
        n_permutations=n_permutations,
        n_bootstrap=n_bootstrap,
        seed=seed,
    )

    return TaskAReport(
        model_name=model.name,
        pd_genes_used=pd_genes_actually_used,
        pd_genes_missing=pd_genes_missing,
        background_size=int(bg_matrix.shape[0]),
        result=result,
    )


__all__ = ["TaskAReport", "run_pd_ranking_benchmark"]
