# xiaozhua — DFT 自动化流程

## 概述

本库为 openclaw 自动化流程的 DFT 部分，支持在 **xiaozhua**（服务器）或 **clio**（功能机）上执行。各板块可**独立运行**，不依赖完整流水线。

---

## 目录结构

```
DFT/
├── README.md                 # 本文件
├── 任务清单.md               # 标准任务清单（发给 clio 或本机执行时使用）
├── workflow/                 # 主流程规范（GO、GR、频率）
├── tool/                     # 通用建模工具
└── 频率计算/                 # 频率计算子流程
    ├── 运行规则.md
    ├── 流程映射.md
    ├── shared/               # 共享配置与检查
    │   ├── config.py         # 配置入口（clio 可直接修改）
    │   ├── pre_check.py      # 提交前检查脚本
    │   ├── pre_check.ipynb   # 提交前检查（独立执行）
    │   ├── 提交前检查.md
    │   └── README_config.md
    ├── tool_01_结构准备/     # 结构转移、原子固定、Input 生成
    ├── tool_02_提交调度/     # 提交脚本、核数、Hub 分区
    ├── tool_03_结果解析/     # 频率提取、最终结构提取
    └── tool_04_频率修正/     # 507 虚频修正
```

---

## 执行模式

### 1. xiaozhua 执行

- 在 xiaozhua 上编辑 `频率计算/shared/config.py`，设置 `ZPE_ROOT` 等为**本机路径**
- 直接运行各 tool 的 notebook

### 2. clio 执行（发送执行）

- xiaozhua 生成任务后，将 **`任务清单.md`** 填充并发给执行人
- 执行人在 clio 上：按清单编辑 `config.py`（`ZPE_ROOT` 用 clio 可访问路径）→ 做提交前检查 → 执行勾选步骤

---

## 各板块独立执行

| 板块 | 路径 | 独立执行说明 |
|------|------|--------------|
| 结构准备 | tool_01/auto/prepare_structure.ipynb | 仅需 config 中 ZPE_ROOT 指向含 .vasp/POSCAR 的目录 |
| 提交前检查 | shared/pre_check.ipynb | 独立运行，检查原子固定、INCAR |
| 提交调度 | tool_02/auto/submit_dispatch.ipynb | 内置提交前检查，不通过则禁止生成 |
| 频率提取（循环） | tool_03/auto/extract_freq_loop.ipynb | 仅提取频率、打印 PASS/HAS_IMAG/INCOMPLETE |
| 最终结构提取 | tool_03/auto/extract_final_structures.ipynb | 提取 CONTCAR→.vasp，507 修正结构可单独输出 |
| 507 虚频修正 | tool_04/auto/507_fix.ipynb | 需 HAS_IMAG 目录或 zpe_root 扫描 |

---

## 频率计算 — 提交前必检

每次提交频率任务前**必须**完成：

1. **原子固定**：Cu 基底全部固定（Selective Dynamics F F F）
2. **INCAR**：存在且关键参数符合运行规则
3. **额外修改**：若有手动修改，需在任务清单 3.3 中记录

运行 `shared/pre_check.ipynb` 或 `python shared/pre_check.py` 进行自动检查。

---

## 配置

编辑 `频率计算/shared/config.py`：

| 变量 | 说明 |
|------|------|
| ZPE_ROOT | 频率任务根目录（xiaozhua 与 clio 路径不同） |
| DEFAULT_PARTITION | young (SGE) / young_ng (Slurm) |
| CORRECTED_OUTPUT_DIR | 507 修正结构输出目录（可选） |
| EXECUTION_HOST | xiaozhua / clio（用于任务清单） |

---

## 任务清单

`DFT/任务清单.md` 为标准模板。当从 xiaozhua 发送给 clio 执行时：

1. 填写任务信息、配置项、执行步骤
2. 将清单与相关说明发给执行人
3. 执行人按清单在 clio 上完成配置与运行

---

## 流程映射（频率计算）

1. Step1 结构准备 → tool_01  
2. Step2 提交 → tool_02（含提交前检查）  
3. Step3 监控 → tool_02  
4. Step4 结果提取 → tool_03（extract_freq_loop / extract_final_structures）  
5. Step5 虚频修正 → tool_04（HAS_IMAG 时）
