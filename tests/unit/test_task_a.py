"""End-to-end tests for the PD-ranking benchmark (Task A)."""

from __future__ import annotations

import pytest

from scgpt_neurodegen_probe.benchmarks.task_a_pd_ranking import (
    TaskAReport,
    run_pd_ranking_benchmark,
)
from scgpt_neurodegen_probe.models.embeddings import (
    EmbeddingModel,
    SyntheticEmbeddingModel,
    make_synthetic_model,
)
from scgpt_neurodegen_probe.pd_genes import PD_CORE_GENES


def _background(n: int = 120) -> tuple[str, ...]:
    return tuple(f"BG{i:04d}" for i in range(n))


def test_synthetic_model_satisfies_protocol() -> None:
    model = SyntheticEmbeddingModel(known_genes=frozenset({"X"}))
    assert isinstance(model, EmbeddingModel)


def test_task_a_detects_engineered_cluster() -> None:
    bg = _background(200)
    model = make_synthetic_model(
        pd_genes=PD_CORE_GENES,
        background_genes=bg,
        anchor_strength=3.0,
        seed=0xA1BE,
    )
    report = run_pd_ranking_benchmark(
        model,
        background_genes=bg + PD_CORE_GENES,
        n_permutations=200,
        n_bootstrap=50,
    )
    assert isinstance(report, TaskAReport)
    # The synthetic model deliberately clusters PD genes; the test must
    # see it as significant.
    assert report.result.p_value < 0.05
    assert report.result.effect_size > 1.0
    # Most PD genes should have been recognized (synthetic model's known
    # set includes them).
    assert len(report.pd_genes_used) >= len(PD_CORE_GENES) - 1


def test_task_a_no_cluster_when_anchor_strength_zero() -> None:
    bg = _background(200)
    model = make_synthetic_model(
        pd_genes=PD_CORE_GENES,
        background_genes=bg,
        anchor_strength=0.0,  # no engineered cluster
        seed=0x1234,
    )
    report = run_pd_ranking_benchmark(
        model,
        background_genes=bg + PD_CORE_GENES,
        n_permutations=200,
        n_bootstrap=20,
    )
    # Without anchor, the test should usually NOT reject at alpha=0.01.
    # We allow a wide margin because the synthetic geometry is small.
    assert report.result.p_value > 0.01


def test_task_a_raises_when_pd_genes_unknown_to_model() -> None:
    bg = _background(50)
    # Model only knows background, not PD genes.
    model = make_synthetic_model(
        pd_genes=(),
        background_genes=bg,
        seed=0,
    )
    with pytest.raises(ValueError, match=r"no PD genes overlap|too few PD genes recognized"):
        run_pd_ranking_benchmark(
            model,
            background_genes=bg,
            n_permutations=50,
            n_bootstrap=10,
        )


def test_task_a_report_as_dict() -> None:
    bg = _background(80)
    model = make_synthetic_model(pd_genes=PD_CORE_GENES, background_genes=bg, seed=0)
    report = run_pd_ranking_benchmark(
        model,
        background_genes=bg + PD_CORE_GENES,
        n_permutations=50,
        n_bootstrap=10,
    )
    d = report.as_dict()
    for key in ("model", "observed_mean_cosine", "p_value", "effect_size"):
        assert key in d
