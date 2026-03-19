#!/usr/bin/env python3
"""GO_1body ASE builder spec (authoritative construction logic).

This file is the implementation-side companion of STEP1_GO_WORKFLOW.md.
It captures the corrected structure-construction rules validated on 2026-03-12.

Scope:
- molecule seed generation only (CO / CHO / COOH)
- adsorption placement constraints definition
- scheduler constraints summary

Notes:
- CHO uses ASE G2 formyl (HCO).
- COOH is derived from HCOOH by removing the H bonded to C.
- Bridge site must be midpoint of adjacent top-layer Cu pair.
- On young.ng, requested core count must be a multiple of 40.
"""

import numpy as np
from ase.build import molecule
from ase.collections import g2


def get_species_molecule(spec: str):
    """Return ASE Atoms with canonical atom order used in GO_1body.

    Orders:
    - CO   -> C O
    - CHO  -> C H O
    - COOH -> C O O H
    """
    if spec == "CO":
        m = molecule("CO")
        sy = m.get_chemical_symbols()
        return m[[sy.index("C"), sy.index("O")]]

    if spec == "CHO":
        # ASE G2 name: HCO (formyl radical)
        m = g2["HCO"].copy()
        sy = m.get_chemical_symbols()
        return m[[sy.index("C"), sy.index("H"), sy.index("O")]]

    if spec == "COOH":
        # Build COOH radical from formic acid by removing the H attached to C
        m0 = molecule("HCOOH")
        sy = m0.get_chemical_symbols()
        p = m0.get_positions()
        c = sy.index("C")
        h_ids = [i for i, s in enumerate(sy) if s == "H"]
        h_on_c = min(h_ids, key=lambda i: np.linalg.norm(p[i] - p[c]))

        keep = [i for i in range(len(m0)) if i != h_on_c]
        m1 = m0[keep]
        sy1 = m1.get_chemical_symbols()
        c1 = sy1.index("C")
        o_ids = [i for i, s in enumerate(sy1) if s == "O"]
        h1 = sy1.index("H")
        return m1[[c1, o_ids[0], o_ids[1], h1]]

    raise ValueError(f"Unsupported species: {spec}")


def construction_constraints() -> dict:
    """Single source of truth for GO_1body construction constraints."""
    return {
        "sites": ["top", "bridge", "hollow"],
        "bridge_definition": "midpoint of adjacent top-layer Cu pair",
        "placement_rule": "rigid translation/rotation only; do not distort intramolecular geometry",
        "test_path_rule": "TEST is parallel to GO under 1_body",
        "young_ng_core_rule": "cores must be multiples of 40",
    }


def main():
    c = construction_constraints()
    print("GO_1body builder constraints loaded.")
    print(c)


if __name__ == "__main__":
    main()
