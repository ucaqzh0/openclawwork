# GO_1body Workflow（原 Step1 GO 单位点吸附）— 永久版

更新时间：2026-03-12（按用户修订）

## 目标
该基础指令体系命名为 **GO_1body**。
用于反应前驱体阶段的 GO 单位点吸附计算（1_body），支持 young-ng（Slurm）与 young（SEG）单机或协同调度。

## 固定目录规范
以任务名 `TASK` 为例：

- `thermol/TASK/absorption/1_body/{GO,TEST,Frequency,Final}`
- `thermol/TASK/absorption/2_body/{GO,TEST,Frequency,Final}`
- `thermol/TASK/tool/`（任务专用 notebook / 脚本）
- `thermol/tool/GO`（全局地址与复用登记）

## 1) 调用与地址登记（关键）
每次调用后必须更新 `thermol/tool/GO`：
- 复写本次任务涉及的源地址、目标地址、复用地址。
- 在用户确认“可用/通过”后，再将这些地址标记为可复用地址，供后续直接调用。
- 地址记录必须可追溯（任务名、分子/位点、来源路径）。

## 2) 构建规则（关键）
- 必须使用用户提供的 notebook 逻辑（不自创简化版）。
- 必须输出“完整 ipynb 文件”（非只写脚本片段），放在 `TASK/tool/`，用于人工审查生成逻辑。
- **构建实现以 `workflows/GO_1body_builder_ase.py` 为准**（文档与脚本同步维护）。
- 单吸附固定三个位点：`hollow / top / bridge`。
- `bridge` 严格定义为**相邻两个 Cu 原子的中点**（不是任意两点中点）。
- 新建结构先进入 `1_body/GO`；用于人工复核的样本放在与 `GO` 同级的 `1_body/TEST`。
- 分子初始结构必须来自 ASE 标准来源（避免手写失真）：
  - CO：`ase.build.molecule("CO")`
  - CHO：使用 ASE `g2["HCO"]`（formyl）
  - COOH：由 `HCOOH` 去除与 C 相连的 H 得到 COOH 自由基
- 吸附放置阶段仅允许刚体平移/旋转，不允许随意改写分子内部键长键角。

## 3) 复用规则（已跑完结构）
仅复制最小三件：
- `CONTCAR` -> 目标任务 `POSCAR`
- `OUTCAR`
- `OSZICAR`

不搬运大体积冗余文件；深度文件按需回源目录查。

## 4) 提交与调度
- 任务必须拆成独立任务（按分子/位点拆分）以便灵活调度、取消、迁移。
- 是否使用 young、young-ng、或联合使用：由用户每次任务前指定。
- 联合使用时保持参数一致（INCAR/KPOINTS/POTCAR 与关键开关一致）。
- young.ng 提交核数必须使用 **40 的整数倍**（匹配节点 40 核拓扑）。
- 参数修改方式按当次需求执行：用户可能要求我自动改参数，也可能由用户直接编辑输入（如 ISPIN）；两种模式都支持。

## 5) check 导出规则
- check 包仅包含“新生成、待检查”结构。
- 已完成/已复用结构不重复进入 check。

## 6) 通知
- 支持后台监控与邮件通知到 `ucaqzh0@ucl.ac.uk`。

## 7) 重要边界
- 某次任务的临时调度触发条件（例如“跑到 top 就取消”）属于**任务特例**，不写入永久规则。
- 用户会在具体任务中单独下达这类策略。

## 执行清单（SOP）
1. 创建任务目录骨架
2. 使用用户 notebook 生成完整任务级 ipynb
3. 扫描复用项并复写 `thermol/tool/GO` 地址
4. 新结构建模（3 位点）
5. 导出 check 包（仅新建）
6. 按用户指定机器策略提交（独立任务）
7. 监控与通知
8. 用户确认后更新 `thermol/tool/GO` 为可复用地址
