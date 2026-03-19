# -*- coding: utf-8 -*-
"""NEB 前原子排列对齐工具（从你已有 align_fin_for_neb 提取）。"""

from __future__ import annotations

import numpy as np
from collections import defaultdict
from itertools import permutations

from ase import Atoms


def align_fin_for_neb(ini_atoms: Atoms, fin_atoms: Atoms, n_fixed: int = 48) -> Atoms:
    """
    重排 fin 的吸附原子顺序，使线性插值时原子对应位移总和最小。

    参数:
        ini_atoms, fin_atoms: ASE Atoms（原子数、元素种类相同）
        n_fixed: 前 n_fixed 个原子为基底（Cu），不重排

    返回:
        fin_aligned: 重排后的 fin（元素顺序与 ini 一致；位置为最优匹配）
    """
    ini = ini_atoms.copy()
    fin = fin_atoms.copy()

    n = len(ini)
    if len(fin) != n:
        raise ValueError(f"原子数不一致: ini={n}, fin={len(fin)}")

    ini_pos = ini.get_positions()
    fin_pos = fin.get_positions()

    ini_sym = ini.get_chemical_symbols()
    fin_sym = fin.get_chemical_symbols()

    # 按元素分组（仅重排基底之后的吸附原子）
    ini_elements: dict[str, list[int]] = defaultdict(list)
    fin_elements: dict[str, list[int]] = defaultdict(list)
    for i in range(n_fixed, n):
        ini_elements[ini_sym[i]].append(i)
        fin_elements[fin_sym[i]].append(i)

    new_pos = np.zeros_like(ini_pos)
    new_pos[:n_fixed] = fin_pos[:n_fixed]  # 基底不重排

    for elem, ini_idxs in ini_elements.items():
        fin_idxs = fin_elements.get(elem, [])

        # 元素数量不匹配：退化为按原顺序拷贝（避免直接崩）
        if len(ini_idxs) != len(fin_idxs):
            for idx in ini_idxs:
                if idx < len(fin_pos):
                    new_pos[idx] = fin_pos[idx]
            continue

        if len(ini_idxs) == 1:
            new_pos[ini_idxs[0]] = fin_pos[fin_idxs[0]]
            continue

        # 多同类原子：枚举排列，最小化位移平方和
        best_sum = np.inf
        best_perm = list(range(len(fin_idxs)))
        for p in permutations(range(len(fin_idxs))):
            s = sum(
                np.linalg.norm(ini_pos[ini_idxs[j]] - fin_pos[fin_idxs[p[j]]]) ** 2
                for j in range(len(ini_idxs))
            )
            if s < best_sum:
                best_sum = s
                best_perm = list(p)

        for j, idx in enumerate(ini_idxs):
            new_pos[idx] = fin_pos[fin_idxs[best_perm[j]]]

    fin_aligned = Atoms(ini_sym, positions=new_pos, cell=fin.get_cell(), pbc=fin.get_pbc())
    return fin_aligned

