# STEP1 Workflow (GO 单位点吸附) — 永久版

更新时间：2026-03-12

## 目标
用于反应前驱体阶段的 GO 单位点吸附计算（1_body），并支持 young-ng(Slurm) + young(SEG) 协同调度。

## 固定目录规范
以任务名 `TASK` 为例：

- `thermol/TASK/absorption/1_body/{GO,TEST,Frequency,Final}`
- `thermol/TASK/absorption/2_body/{GO,TEST,Frequency,Final}`
- `thermol/TASK/tool/`（任务专用 notebook / 脚本）
- `thermol/tool/GO`（全局复用登记）

## 构建规则（单吸附）
1. 先查重：`100_water` 已有结果优先复用，不重复计算。
2. 位点固定：`hollow / top / bridge`。
3. 位点选取遵循中心对齐章法（与单吸附构建.ipynb一致）。
4. 新建结构先放 `1_body/GO`。

## 复用规则（已跑完结构）
仅复制以下三件：
- `CONTCAR` -> 目标任务 `POSCAR`
- `OUTCAR`
- `OSZICAR`

不搬运大体积冗余文件。需要深度追溯时回源目录查。

## check 导出规则
check 包仅包含“新生成、待人工检查”的结构。
已完成/已复用结构不再重复进入 check 包。

## 计算参数要点
- 目前统一使用：`ISPIN = 2`（重要）
- young-ng GO 提交可用 80/120 核策略
- young(SEG)按任务要求可单任务 256 核

## 协同调度策略
### 默认策略
- young-ng 跑主线 GO
- young 接手分流子任务（如 bridge 或指定位点）

### 本次验证策略（可复用模板）
- 当 young-ng 的 hollow 完成、开始 top 时：取消 ng 当前批次，改为双机重分配。
- 若 young 的排队+运行任务数 <= 3，优先投 young。
- Slurm 侧重提时用 120 核模板。

## 运行状态与通知
- 统一记录 jobid
- 后台监控 + 邮件通知到 `ucaqzh0@ucl.ac.uk`

## 执行清单（SOP）
1. 创建任务目录骨架
2. 生成任务内 tool notebook
3. 扫描可复用结构并写入 `thermol/tool/GO`
4. 新结构建模（3 位点）
5. 导出 check 包（仅新建）
6. 按机器策略提交
7. 监控并在触发条件下切换调度
8. 完成后归档 Final

---
如果后续你确认，我们可以把它拆成自动化脚本：
- `build_step1.py`
- `dispatch_dual_cluster.py`
- `monitor_and_rebalance.sh`
