"""Tests for the PD gene panel module."""

from __future__ import annotations

from scgpt_neurodegen_probe.pd_genes import (
    PD_CORE_GENES,
    PD_EXTENDED_GENES,
    pd_core,
    pd_extended,
)


def test_core_contains_canonical_pd_genes() -> None:
    core = set(pd_core())
    for g in ("SNCA", "LRRK2", "PRKN", "PINK1", "GBA1"):
        assert g in core, f"{g} missing from PD core"


def test_extended_is_superset() -> None:
    assert set(pd_core()).issubset(set(pd_extended()))
    assert len(pd_extended()) > len(pd_core())


def test_no_duplicates() -> None:
    assert len(PD_CORE_GENES) == len(set(PD_CORE_GENES))
    assert len(PD_EXTENDED_GENES) == len(set(PD_EXTENDED_GENES))


def test_stable_ordering() -> None:
    assert PD_CORE_GENES[0] == "SNCA"
    assert PD_CORE_GENES[1] == "PRKN"
