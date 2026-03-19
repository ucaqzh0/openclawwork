# -*- coding: utf-8 -*-
# ============================================================
# 功能机 clio 可直接修改此文件
# xiaozhua 执行：用 xiaozhua 路径；clio 执行：用 clio 可访问路径
# 详见 README_config.md
# ============================================================

# ZPE 根目录（频率计算任务所在路径）
# xiaozhua: /home/ucaqzh0/...  clio: 本机或挂载路径
ZPE_ROOT = "/home/ucaqzh0/thermol/100_water/absorption/absorption/ZPE/high/"

# 默认提交分区：young (SGE) / young_ng (Slurm)
DEFAULT_PARTITION = "young"

# 最终结构提取：被 507 修正的结构输出目录（稍后统一指定）
CORRECTED_OUTPUT_DIR = None  # 例如 "/path/to/corrected_structures"

# 执行机（可选，用于任务清单）：xiaozhua / clio
EXECUTION_HOST = "xiaozhua"
