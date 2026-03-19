# 任务清单 — Global Optimization（GO_1body / GR）

> 本清单用于 xiaozhua 生成任务后，发给 clio 或在本机执行。执行前请逐项勾选。

---

## 1. 任务信息

| 项 | 值 |
|----|-----|
| 任务名称 | _（填写，如：GO_1body H2O 吸附）_ |
| 流程 | Global Optimization（GO_1body / GR） |
| 日期 | _（自动或手动）_ |
| 执行机 | ☐ xiaozhua  ☐ clio |

---

## 2. 配置项（执行机本地 config.py）

**路径**：`Global_optimization/shared/config.py`

| 变量 | 本机应设值 | 说明 |
|------|------------|------|
| GO_ROOT | _（执行机上的 GO 根路径）_ | 含 .vasp 结构文件，job_* 任务目录将在此生成 |
| DEFAULT_PARTITION | young / young_ng | 提交分区（young=SGE, young_ng=Slurm） |

**注意**：在 clio 执行时，GO_ROOT 必须为 clio 可访问的路径（如挂载或同步后的路径）。

---

## 3. 移交检查（提交前必检）

### 3.1 输入文件完整
- [ ] 各任务目录具备 **POSCAR、POTCAR、KPOINTS、INCAR**
- [ ] POTCAR 元素顺序与 POSCAR 一致

### 3.2 额外修改
- [ ] 无额外修改
- [ ] 或有修改，已记录：_____________________

---

## 4. 执行步骤（按需勾选）

| 步骤 | 工具 | 说明 | 状态 |
|------|------|------|------|
| 1 | tool_01 generate_inputs | 从 .vasp 生成 POSCAR、POTCAR、KPOINTS、INCAR | ☐ |
| 2 | 移交检查 | 运行 pre_check 或按 3.1–3.2 人工核对 | ☐ |
| 3 | tool_02 submit_dispatch | 生成 job_list、submit.sh，与其他工具调度一致 | ☐ |
| 4 | tool_03 wrapup | 完成态扫描、结果提取、GO_best 筛选 | ☐ |

---

## 5. 独立执行说明

各 tool 可**单独运行**，不依赖前置步骤：

- **仅输入文件生成**：运行 `tool_01/auto/generate_inputs.ipynb`（GO_ROOT 下需有 .vasp 文件）
- **仅提交**：先确认 3.1–3.2，再运行 `submit_dispatch`
- **仅收尾**：运行 `tool_03/auto/wrapup.ipynb`（需 GO_ROOT 下已有 job_* 结果）

---

## 6. 发送 clio 执行时

1. 将本清单 + 相关文件/路径说明 发给执行人
2. 执行人在 clio 上：编辑 `config.py`（GO_ROOT 等）→ 按 3 做移交检查 → 执行 4 中勾选的步骤
3. 执行完成后反馈结果
