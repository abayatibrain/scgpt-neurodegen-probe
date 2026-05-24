"""Tests for the embedding permutation-test framework."""

from __future__ import annotations

import numpy as np
import pytest

from scgpt_neurodegen_probe.stats.permutation import (
    compactness_score,
    mean_centroid_distance,
    mean_pairwise_cosine,
    permutation_test,
)


def _make_matrices(seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    fg = rng.normal(0.0, 1.0, size=(10, 8))
    bg = rng.normal(0.0, 1.0, size=(200, 8))
    return fg, bg


class TestStatistics:
    def test_cosine_of_identical_rows_is_one(self) -> None:
        m = np.tile([1.0, 0.0, 0.0], (5, 1))
        assert mean_pairwise_cosine(m) == pytest.approx(1.0)

    def test_cosine_orthogonal_pair_is_zero(self) -> None:
        m = np.array([[1.0, 0.0], [0.0, 1.0]])
        assert mean_pairwise_cosine(m) == pytest.approx(0.0, abs=1e-9)

    def test_compactness_inverse_of_distance(self) -> None:
        m = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
        d = mean_centroid_distance(m)
        c = compactness_score(m)
        assert c == pytest.approx(1.0 / d)


class TestPermutationTest:
    def test_random_set_p_is_not_significant(self) -> None:
        fg, bg = _make_matrices()
        result = permutation_test(
            fg,
            background_matrix=bg,
            statistic=mean_pairwise_cosine,
            n_permutations=200,
            n_bootstrap=50,
            seed=0,
        )
        # Foreground is drawn from the same distribution as background, so
        # the test should rarely (but not never) reject.
        assert 0.01 < result.p_value <= 1.0

    def test_clustered_set_p_is_significant(self) -> None:
        rng = np.random.default_rng(1)
        bg = rng.normal(0.0, 1.0, size=(200, 8))
        # Engineer foreground to cluster along a single axis.
        anchor = rng.normal(0.0, 1.0, size=8)
        anchor = anchor / np.linalg.norm(anchor)
        fg = rng.normal(0.0, 0.1, size=(15, 8)) + 3.0 * anchor[None, :]

        result = permutation_test(
            fg,
            background_matrix=bg,
            statistic=mean_pairwise_cosine,
            n_permutations=500,
            n_bootstrap=100,
            seed=2,
        )
        # Engineered cluster: very strong effect; p must be at the floor.
        assert result.p_value < 0.01
        # Effect-size z-score should be many SDs above null mean.
        assert result.effect_size > 3.0
        # CI on the observed statistic should not be NaN.
        assert all(np.isfinite(b) for b in result.ci_95)

    def test_dim_mismatch_raises(self) -> None:
        with pytest.raises(ValueError, match="dim mismatch"):
            permutation_test(
                np.zeros((5, 4)),
                background_matrix=np.zeros((50, 8)),
                statistic=mean_pairwise_cosine,
                n_permutations=10,
            )

    def test_small_background_raises(self) -> None:
        with pytest.raises(ValueError, match="background must have at least"):
            permutation_test(
                np.zeros((20, 4)),
                background_matrix=np.zeros((5, 4)),
                statistic=mean_pairwise_cosine,
                n_permutations=10,
            )

    def test_p_is_floored(self) -> None:
        rng = np.random.default_rng(7)
        bg = rng.normal(0.0, 1.0, size=(50, 4))
        # Make foreground identical so cosine = 1, beats every null.
        fg = np.tile(rng.normal(0.0, 1.0, size=4), (8, 1))
        result = permutation_test(
            fg,
            background_matrix=bg,
            statistic=mean_pairwise_cosine,
            n_permutations=20,
            n_bootstrap=10,
            seed=0,
        )
        # Phipson-Smyth floor: 1 / (n_permutations + 1).
        assert result.p_value == pytest.approx(1.0 / 21.0)
