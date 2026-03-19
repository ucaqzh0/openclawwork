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
from ase.geometry import find_mic


SUPPORTED_SITES = ["hollow", "top", "bridge"]


def _get_cu_layer_positions(
    surface_atoms: Atoms, layer_from_top: int, tol: float = 0.1
) -> tuple[np.ndarray, np.ndarray, float]:
    """返回指定 Cu 层（从顶层起 1-based）的原子 index、坐标与该层 z。"""
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
    mask = np.abs(cu_positions[:, 2] - target_z) <= tol
    layer_positions = cu_positions[mask]
    layer_indices = np.array(cu_indices, dtype=int)[mask]
    if len(layer_positions) == 0:
        raise ValueError(f"未识别到第 {layer_from_top} 层 Cu 原子")
    return layer_indices, layer_positions, float(target_z)


def _get_layer_center_xy(surface_atoms: Atoms, layer_from_top: int = 1, tol: float = 0.1) -> np.ndarray:
    """返回指定层 Cu 的几何中心 (x, y)。"""
    _, layer_positions, _ = _get_cu_layer_positions(surface_atoms, layer_from_top=layer_from_top, tol=tol)
    return np.mean(layer_positions[:, :2], axis=0)


def _mic_2d_vectors(
    xy_from: np.ndarray, xy_to: np.ndarray, cell, pbc_xy: tuple[bool, bool] = (True, True)
) -> tuple[np.ndarray, np.ndarray]:
    """返回从 xy_from 到 xy_to 的最小镜像 2D 向量与距离（只在 x/y 上考虑 PBC）。"""
    d = np.array([xy_to[0] - xy_from[0], xy_to[1] - xy_from[1], 0.0], dtype=float)
    mic_vec3, dist = find_mic(d, cell=cell, pbc=(pbc_xy[0], pbc_xy[1], False))
    v = np.array([mic_vec3[0], mic_vec3[1]], dtype=float)
    return v, float(dist)


def _pairwise_mic_2d_distances(xy: np.ndarray, cell, pbc_xy: tuple[bool, bool] = (True, True)) -> np.ndarray:
    """计算一组点之间的最小镜像 2D 距离矩阵。"""
    n = len(xy)
    dmat = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(i + 1, n):
            _, dij = _mic_2d_vectors(xy[i], xy[j], cell=cell, pbc_xy=pbc_xy)
            dmat[i, j] = dij
            dmat[j, i] = dij
    return dmat


def _estimate_nn_distance(xy: np.ndarray, cell, pbc_xy: tuple[bool, bool] = (True, True)) -> float:
    """估计该层最近邻 2D 距离（最小非零距离）。"""
    dmat = _pairwise_mic_2d_distances(xy, cell=cell, pbc_xy=pbc_xy)
    dmat[dmat == 0.0] = np.inf
    nn = float(np.min(dmat))
    if not np.isfinite(nn):
        raise ValueError("无法估计最近邻距离：该层原子数不足或坐标异常")
    return nn


def _neighbors_within(xy: np.ndarray, cell, cutoff: float, pbc_xy: tuple[bool, bool] = (True, True)) -> list[list[int]]:
    """基于最小镜像 2D 距离的邻接表（i 的邻居 j 满足 d(i,j) <= cutoff）。"""
    dmat = _pairwise_mic_2d_distances(xy, cell=cell, pbc_xy=pbc_xy)
    n = len(xy)
    neigh: list[list[int]] = []
    for i in range(n):
        js = [j for j in range(n) if j != i and dmat[i, j] <= cutoff]
        neigh.append(js)
    return neigh


def _mic_midpoint_xy(xy1: np.ndarray, xy2: np.ndarray, cell, pbc_xy: tuple[bool, bool] = (True, True)) -> np.ndarray:
    """返回两点连线在最小镜像下的中点（以 xy1 为参考）。"""
    v, _ = _mic_2d_vectors(xy1, xy2, cell=cell, pbc_xy=pbc_xy)
    return np.array([xy1[0] + 0.5 * v[0], xy1[1] + 0.5 * v[1]], dtype=float)


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
    # “尽量在第一层中心寻找”：默认中心来自第一层 Cu 几何中心
    center_xy = _get_layer_center_xy(surface_atoms, layer_from_top=center_layer_from_top, tol=0.1)
    _, top_cu_positions, top_z = _get_cu_layer_positions(surface_atoms, layer_from_top=layer_from_top, tol=0.1)
    xy = top_cu_positions[:, :2].copy()
    if len(xy) < 2:
        raise ValueError("目标 Cu 层原子数不足，无法构造 top/bridge/hollow 位点")

    nn = _estimate_nn_distance(xy, cell=cell)
    # cutoff 略放宽，避免因轻微弛豫导致邻居断开
    neigh = _neighbors_within(xy, cell=cell, cutoff=nn * 1.25)

    if site == "top":
        d_to_center = np.array(
            [_mic_2d_vectors(center_xy, xy[i], cell=cell)[1] for i in range(len(xy))], dtype=float
        )
        nearest_idx = int(np.argmin(d_to_center))
        site_pos = top_cu_positions[nearest_idx].copy()
        site_pos[2] = top_z
        return site_pos

    if site == "bridge":
        # bridge = 最近邻 Cu-Cu 键的中点（选离中心最近的那个）
        d_to_center = np.array(
            [_mic_2d_vectors(center_xy, xy[i], cell=cell)[1] for i in range(len(xy))], dtype=float
        )
        i0 = int(np.argmin(d_to_center))
        candidates: list[tuple[float, np.ndarray]] = []
        for j in neigh[i0]:
            mid_xy = _mic_midpoint_xy(xy[i0], xy[j], cell=cell)
            dmid = _mic_2d_vectors(center_xy, mid_xy, cell=cell)[1]
            candidates.append((dmid, mid_xy))
        if not candidates:
            # 兜底：全局搜索最近的键中点
            for i in range(len(xy)):
                for j in neigh[i]:
                    if j <= i:
                        continue
                    mid_xy = _mic_midpoint_xy(xy[i], xy[j], cell=cell)
                    dmid = _mic_2d_vectors(center_xy, mid_xy, cell=cell)[1]
                    candidates.append((dmid, mid_xy))
        if not candidates:
            raise ValueError("未找到 bridge：该层未构建出最近邻关系（可能 tol/结构异常）")
        _, best_xy = min(candidates, key=lambda t: t[0])
        return np.array([best_xy[0], best_xy[1], top_z], dtype=float)

    if site == "hollow":
        # hollow = 最近邻三角形（3 个互为近邻的 Cu）质心（选离中心最近的那个）
        d_to_center = np.array(
            [_mic_2d_vectors(center_xy, xy[i], cell=cell)[1] for i in range(len(xy))], dtype=float
        )
        seed = int(np.argmin(d_to_center))
        triangles: list[tuple[float, np.ndarray]] = []

        # 优先用 seed 周围构三角
        for j in neigh[seed]:
            for k in neigh[seed]:
                if k <= j:
                    continue
                # 要求 j-k 也互为近邻，形成三角形
                if k not in neigh[j]:
                    continue
                # 用最小镜像把三点放到 seed 邻域再求质心
                p0 = xy[seed]
                vj, _ = _mic_2d_vectors(p0, xy[j], cell=cell)
                vk, _ = _mic_2d_vectors(p0, xy[k], cell=cell)
                pj = p0 + vj
                pk = p0 + vk
                cen = (p0 + pj + pk) / 3.0
                dcen = _mic_2d_vectors(center_xy, cen, cell=cell)[1]
                triangles.append((dcen, cen))

        # 如果 seed 附近没构成三角形，做一次全局兜底
        if not triangles:
            for i in range(len(xy)):
                for j in neigh[i]:
                    if j <= i:
                        continue
                    for k in neigh[i]:
                        if k <= j:
                            continue
                        if k not in neigh[j]:
                            continue
                        p0 = xy[i]
                        vj, _ = _mic_2d_vectors(p0, xy[j], cell=cell)
                        vk, _ = _mic_2d_vectors(p0, xy[k], cell=cell)
                        pj = p0 + vj
                        pk = p0 + vk
                        cen = (p0 + pj + pk) / 3.0
                        dcen = _mic_2d_vectors(center_xy, cen, cell=cell)[1]
                        triangles.append((dcen, cen))

        # 4-fold hollow 兜底：寻找四元环 i-j-l-k（j,k 为 i 的邻居且共享一个公共邻居 l）
        if not triangles:
            quads: list[tuple[float, np.ndarray]] = []
            for i in range(len(xy)):
                for j in neigh[i]:
                    for k in neigh[i]:
                        if k <= j:
                            continue
                        common = set(neigh[j]).intersection(neigh[k])
                        common.discard(i)
                        for l in common:
                            p0 = xy[i]
                            vj, _ = _mic_2d_vectors(p0, xy[j], cell=cell)
                            vk, _ = _mic_2d_vectors(p0, xy[k], cell=cell)
                            pl_j = p0 + vj
                            pl_k = p0 + vk
                            # 将 l 也映射到 i 的最小镜像邻域
                            vl, _ = _mic_2d_vectors(p0, xy[l], cell=cell)
                            pl_l = p0 + vl
                            cen = (p0 + pl_j + pl_k + pl_l) / 4.0
                            dcen = _mic_2d_vectors(center_xy, cen, cell=cell)[1]
                            quads.append((dcen, cen))
            if quads:
                _, best_cen = min(quads, key=lambda t: t[0])
                return np.array([best_cen[0], best_cen[1], top_z], dtype=float)

        if not triangles:
            # 最终兜底：至少返回层中心，避免 tool 直接崩溃
            return np.array([center_xy[0], center_xy[1], top_z], dtype=float)

        _, best_cen = min(triangles, key=lambda t: t[0])
        return np.array([best_cen[0], best_cen[1], top_z], dtype=float)

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

