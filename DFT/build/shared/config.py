# -*- coding: utf-8 -*-
# build（结构构建）配置（由执行机本地修改）

# 结构落地根目录：
# 你的 thermol 体系里，基础结构（POSCAR 等）通常落在 GO/ 下，
# 例如：
#   .../absorption/absorption/GO/absorption_single_H/...
GO_ROOT = "/home/ucaqzh0/thermol/100_water/absorption/absorption/GO"

# 构建所需表面 POSCAR（Cu(100) slab）
SURFACE_POSCAR = "/home/ucaqzh0/thermol/100_water/absorption/absorption/POSCAR"

# 默认 Cu 基底原子数（用于后续 align/筛选兼容：前 n_fixed 个原子不重排）
DEFAULT_N_FIXED = 48

EXECUTION_HOST = "xiaozhua"

