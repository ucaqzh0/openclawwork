# -*- coding: utf-8 -*-
"""单吸附结构构建（build tool_02）。

参考来源：
- DFT/tool/H2O_单吸附模型构建.ipynb（位点与放置逻辑）
- DFT/workflow/GO_1body_builder_ase.py（CO/CHO/COOH 分子来源）
"""

from __future__ import annotations

import numpy as np
from ase import Atoms
from ase.build import molecule
from ase.collections import g2


SUPPORTED_SITES = ["hollow", "top", "bridge"]


def _get_cu_layer_positions(surface_atoms: Atoms, layer_from_top: int, tol: float = 0.1) -> tuple[np.ndarray, float]:
    """返回指定 Cu 层（从顶层起 1-based）的原子坐标与该层 z。"""
    if layer_from_top < 1:
        raise ValueError(f"layer_from_top 必须 >= 1，当前: {layer_from_top}")

    cu_indices = [i for i, s in enumerate(surface_atoms.get_chemical_symbols()) if s.upper() == "CU"]
    if not cu_indices:
        raise ValueError("未找到 Cu 原子，无法构建位点")

    cu_positions = surface_atoms.get_positions()[cu_indices]
    z_values = sorted({round(float(z), 6) for z in cu_positions[:, 2]}, reverse=True)
    # 按 tol 合并近似同层 z 值
    merged = []
    for z in z_values:
        if not merged or abs(z - merged[-1]) > tol:
            merged.append(z)

    if layer_from_top > len(merged):
        raise ValueError(f"指定层超出范围：共有 {len(merged)} 层 Cu，要求第 {layer_from_top} 层")

    target_z = merged[layer_from_top - 1]
    layer_positions = cu_positions[np.abs(cu_positions[:, 2] - target_z) <= tol]
    if len(layer_positions) == 0:
        raise ValueError(f"未识别到第 {layer_from_top} 层 Cu 原子")
    return layer_positions, float(target_z)


def _get_layer_center_xy(surface_atoms: Atoms, layer_from_top: int = 1, tol: float = 0.1) -> np.ndarray:
    """返回指定层 Cu 的几何中心 (x, y)。"""
    layer_positions, _ = _get_cu_layer_positions(surface_atoms, layer_from_top=layer_from_top, tol=tol)
    return np.mean(layer_positions[:, :2], axis=0)


def get_surface_site_position(
    surface_atoms: Atoms,
    site: str = "hollow",
    layer_from_top: int = 1,
    center_layer_from_top: int = 1,
) -> np.ndarray:
    """计算指定 Cu 层上的 hollow/top/bridge 位点坐标。

    说明：
    - 位点搜索中心优先使用 `center_layer_from_top`（默认第一层）；
    - 目标位点高度取 `layer_from_top` 对应层的 z。
    """
    cell = surface_atoms.get_cell()
    a = np.linalg.norm(cell[0])
    b = np.linalg.norm(cell[1])
    # “尽量在第一层中心寻找”：默认中心来自第一层 Cu 几何中心
    center_xy = _get_layer_center_xy(surface_atoms, layer_from_top=center_layer_from_top, tol=0.1)
    top_cu_positions, top_z = _get_cu_layer_positions(surface_atoms, layer_from_top=layer_from_top, tol=0.1)

    if site == "hollow":
        return np.array([center_xy[0], center_xy[1], top_z])

    if site == "top":
        distances_to_center = np.linalg.norm(top_cu_positions[:, :2] - center_xy, axis=1)
        min_distance = np.min(distances_to_center)
        candidates = np.where(distances_to_center < min_distance + 1e-6)[0]
        if len(candidates) > 1:
            xy_sum = top_cu_positions[candidates][:, 0] + top_cu_positions[candidates][:, 1]
            nearest_idx = candidates[np.argmax(xy_sum)]
        else:
            nearest_idx = candidates[0]
        site_pos = top_cu_positions[nearest_idx].copy()
        site_pos[2] = top_z
        return site_pos

    if site == "bridge":
        # workflow 约束：bridge = 相邻 top-layer Cu 的中点
        distances_to_center = np.linalg.norm(top_cu_positions[:, :2] - center_xy, axis=1)
        min_distance = np.min(distances_to_center)
        candidates = np.where(distances_to_center < min_distance + 1e-6)[0]
        if len(candidates) > 1:
            xy_sum = top_cu_positions[candidates][:, 0] + top_cu_positions[candidates][:, 1]
            nearest_idx = candidates[np.argmax(xy_sum)]
        else:
            nearest_idx = candidates[0]
        p1 = top_cu_positions[nearest_idx]

        distances_to_p1 = np.linalg.norm(top_cu_positions[:, :2] - p1[:2], axis=1)
        distances_to_p1[nearest_idx] = np.inf
        neighbor_distances = np.abs(distances_to_p1 - a / 2)
        min_neighbor_distance = np.min(neighbor_distances)

        if min_neighbor_distance < 0.3:
            neighbor_candidates = np.where(neighbor_distances < min_neighbor_distance + 1e-6)[0]
            if len(neighbor_candidates) > 1:
                xy_sum_neighbors = (
                    top_cu_positions[neighbor_candidates][:, 0] + top_cu_positions[neighbor_candidates][:, 1]
                )
                neighbor_idx = neighbor_candidates[np.argmax(xy_sum_neighbors)]
            else:
                neighbor_idx = neighbor_candidates[0]
            p2 = top_cu_positions[neighbor_idx]
            site_pos = (p1 + p2) / 2
            site_pos[2] = top_z
            return site_pos

        # 回退：理论 bridge 位置
        bridge_candidates = [
            np.array([center_xy[0], center_xy[1] - a / 4, top_z]),
            np.array([center_xy[0] - a / 4, center_xy[1], top_z]),
            np.array([center_xy[0], center_xy[1] + a / 4, top_z]),
            np.array([center_xy[0] + a / 4, center_xy[1], top_z]),
        ]
        xy_sums = [cand[0] + cand[1] for cand in bridge_candidates]
        return bridge_candidates[int(np.argmax(xy_sums))]

    raise ValueError(f"不支持位点: {site}")


def get_species_molecule(species: str) -> tuple[Atoms, int]:
    """返回分子与锚点原子 index（优先使用 ASE 标准分子来源）。"""
    if species == "H":
        return Atoms("H", positions=[[0, 0, 0]]), 0
    if species == "O":
        return Atoms("O", positions=[[0, 0, 0]]), 0
    if species == "OH":
        m = molecule("OH")
        sy = m.get_chemical_symbols()
        return m[[sy.index("O"), sy.index("H")]], 0
    if species == "H2":
        m = molecule("H2")
        sy = m.get_chemical_symbols()
        # 固定顺序 H H
        first_h = sy.index("H")
        second_h = [i for i, s in enumerate(sy) if s == "H" and i != first_h][0]
        return m[[first_h, second_h]], 0
    if species == "H2O":
        m = molecule("H2O")
        sy = m.get_chemical_symbols()
        o = sy.index("O")
        h_ids = [i for i, s in enumerate(sy) if s == "H"]
        return m[[o, h_ids[0], h_ids[1]]], 0

    # workflow 的 GO_1body 分子来源
    if species == "CO":
        m = molecule("CO")
        sy = m.get_chemical_symbols()
        return m[[sy.index("C"), sy.index("O")]], 0
    if species == "CHO":
        m = g2["HCO"].copy()
        sy = m.get_chemical_symbols()
        # 固定顺序 C H O
        return m[[sy.index("C"), sy.index("H"), sy.index("O")]], 0
    if species == "COOH":
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
        return m1[[c1, o_ids[0], o_ids[1], h1]], 0

    raise ValueError(f"不支持分子: {species}")


def create_single_adsorption_structure(
    surface_atoms: Atoms,
    species: str,
    site: str,
    layer_from_top: int,
    center_layer_from_top: int = 1,
    adsorption_distance: float = 2.0,
) -> Atoms:
    """构建单吸附结构（刚体平移，不改分子内部几何）。"""
    site_pos = get_surface_site_position(
        surface_atoms,
        site=site,
        layer_from_top=layer_from_top,
        center_layer_from_top=center_layer_from_top,
    )
    mol, anchor_idx = get_species_molecule(species)

    mol_positions = mol.get_positions()
    # 对分子（多原子）用锚点或几何中心放置
    if species in ["H2", "H2O"]:
        ref_pos = np.mean(mol_positions, axis=0)
    else:
        ref_pos = mol_positions[anchor_idx]

    target = site_pos.copy()
    target[2] += adsorption_distance
    shift = target - ref_pos
    mol.set_positions(mol_positions + shift)

    final_atoms = surface_atoms.copy()
    final_atoms.extend(mol)
    return final_atoms

