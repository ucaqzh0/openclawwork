#!/usr/bin/env python3
"""Build GO_1body/TEST structures with corrected rules.
- bridge = midpoint of adjacent top-layer Cu atoms
- molecules from ASE database (CO, HCO as CHO, HCOOH->COOH radical)
- keep molecular internal geometry (rigid placement only)
"""
from pathlib import Path
import numpy as np
from ase.io import read
from ase.build import molecule
from ase.collections import g2


def get_species_molecule(spec):
    if spec == 'CO':
        m = molecule('CO')
        sy = m.get_chemical_symbols()
        return m[[sy.index('C'), sy.index('O')]]
    if spec == 'CHO':
        m = g2['HCO'].copy()
        sy = m.get_chemical_symbols()
        return m[[sy.index('C'), sy.index('H'), sy.index('O')]]
    if spec == 'COOH':
        m0 = molecule('HCOOH')
        sy = m0.get_chemical_symbols()
        p = m0.get_positions()
        c = sy.index('C')
        h_ids = [i for i, s in enumerate(sy) if s == 'H']
        h_on_c = min(h_ids, key=lambda i: np.linalg.norm(p[i] - p[c]))
        keep = [i for i in range(len(m0)) if i != h_on_c]
        m1 = m0[keep]
        sy1 = m1.get_chemical_symbols()
        c1 = sy1.index('C')
        o_ids = [i for i, s in enumerate(sy1) if s == 'O']
        h1 = sy1.index('H')
        return m1[[c1, o_ids[0], o_ids[1], h1]]
    raise ValueError(spec)


def main():
    print('Use cluster-side validated builder used on 2026-03-12 (see chat logs).')


if __name__ == '__main__':
    main()
