# FREQUENCY_MAIN — 最终结构频率主流程（第五个 main）

更新时间：2026-03-13

## 0) 定位与边界
- 本 main 只用于**最终结构（final-purpose）**的频率测试。
- 当前仅定义：
  1. 结构提取与频率任务构建
  2. 频率检查（OUTCAR）
- 第三步（507 虚频修正）已形成逻辑框架，后续按用户最终版本落盘。
- 过渡态（TS）频率测试不在本 main，另走并行策略。

---

## 1) 输入与目录约定

### 1.1 结构来源
- 频率输入结构直接来自 `GO_best` 的对应结构目录（`1_body` / `2_body`）。
- `GO_best` 不再使用 `primary/final` 分层。

### 1.2 频率总目录
- 与 `GO_best` 平级建立频率总目录。
- 总目录下固定三类子目录：
  - `1_body/`
  - `2_body/`
  - `transition/`

### 1.3 单结构目录规则
- 每个结构建立一个独立 ZPE 计算文件夹。
- 文件夹名称与 `GO_best` 中对应 best 名称完全一致。
- 每个结构目录必须可追溯（来源结构名、来源路径、创建时间）。

---

## 2) Step 1 — 提取结构并构建频率任务

### 2.1 执行基准
- 必须按 `tool/frequency.ipynb` 主线逻辑执行。
- 该步骤不引入新的构型变换，仅做任务构建与输入准备。

### 2.2 任务输入文件
每个结构目录至少具备：
- `POSCAR`（由对应 best 结构写入）
- `INCAR`
- `KPOINTS`
- `POTCAR`

### 2.3 输出要求（与 GO 区别）
- 频率流程不走 GO 的“最小复用包”思路。
- 频率流程需保留 `vaspkit 507` 后续分析/修正所需的完整输出环境。

### 2.4 频率 INCAR 基准（仅频率使用）
以下为用户确认基准参数（频率专用）：

```ini
ISTART = 1
ENCUT = 450
PREC = ACCURATE
LREAL = .FALSE.
ISMEAR = 1
SIGMA = 0.2
GGA = PE
NELM = 120
NELMIN = 8
NELMDL = -5
EDIFF = 1E-7
EDIFFG = -0.01
NSW = 1
ISIF = 2
IBRION = 5
POTIM = 0.01
NFREE = 2
NWRITE = 3
LWAVE = .FALSE.
LCHARG = .FALSE.
ISPIN = 1
LORBIT = 11
IVDW = 12
IDIPOL = 3
LDIPOL = .TRUE.
NCORE = 8
ISYM = 0
IALGO = 48
```

> 注意：这套参数仅用于频率计算，不外溢到 GO 等其他流程。

### 2.5 Step 1 交付
- 频率任务目录树（1_body/2_body/transition）
- 结构映射表（best_name -> 频率目录路径）
- 可提交任务清单

---

## 3) Step 2 — 频率检查（基于 OUTCAR）

### 3.1 检查对象
- 每个频率任务目录的 `OUTCAR`。

### 3.2 检查内容
- 提取频率信息与虚频情况。
- 核查任务是否完整完成（避免伪结果）。

### 3.3 状态定义
- `PASS`：无虚频，频率检查通过。
- `HAS_IMAG`：存在虚频，进入 Step 3（507 修正流程）。
- `INCOMPLETE`：输出不完整/未收敛，需重算或排错。

### 3.4 Step 2 交付
输出频率检查汇总表，至少包含：
- 结构名
- 目录路径
- 最低频率 / 虚频数量
- 当前状态（PASS / HAS_IMAG / INCOMPLETE）
- 备注（是否进入 Step 3）

---

## 4) Step 3 预留（507 虚频修正）
- 本步骤逻辑已讨论完成（507、位移降级、分支判定）。
- 将按用户最终文字版单独落为同 main 的 Step 3 正式条目。

---

## 5) 与其他 main 的关系
- `GO_1body_MAIN`：负责构建主线
- `GR_main`：负责批量运行与调度
- `GO_WRAPUP_MAIN`：负责 GO 收尾整理
- `FREQUENCY_MAIN`（本流程）：负责 final-purpose 频率构建与检查
