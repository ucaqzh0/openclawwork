# GO_WRAPUP_MAIN — GO 收尾主流程（第四个 main）

更新时间：2026-03-13

## 定位
用于 GO 计算完成后的统一收尾流程。
目标：把 GO 的结果整理成可直接进入后续（频率/NEB/汇报）的干净产物。

---

## 适用范围
- GO_1body / GO_2body 的阶段性完成后
- 需要做结果汇总、筛选、检查包导出、交接归档

---

## 输入
- GO 任务目录（含各 job 的 OUTCAR / OSZICAR / CONTCAR）
- `tool/frequency.ipynb`（频率流程入口，按你后续指令启用）
- `tool/extract_results.ipynb`（结果提取）

---

## 主流程（Main）
1. **完成态扫描**
   - 统计每个 job：COMPLETED / FAILED / RUNNING / 待重启
   - 形成收尾清单（可追溯到 job 路径）

2. **结果提取与表格化**
   - 调用 `extract_results.ipynb` 逻辑导出能量与关键状态
   - 输出排序表（按物种/位点/取向）

3. **最低能结构筛选（GO_best）**
   - 按“同物种内最低能”规则筛选 best
   - `GO_best` 与 `GO` 处于同一级目录
   - `GO_best` 目录结构固定为：
     - `GO_best/1_body/primary`
     - `GO_best/1_body/final`
     - `GO_best/2_body/primary`
     - `GO_best/2_body/final`
   - 结构文件统一输出到对应层级（.vasp）
  - 语义定义：
    - `primary`：完成初步扫描后确认的结构
    - `final`：完成全部 TEST + ZPE 后最终确认的完整结构

4. **复用最小包生成**
   - 每个可复用 case 仅保留：`CONTCAR / OUTCAR / OSZICAR`
   - 与历史规则一致，避免重文件复制

5. **检查包导出**
   - 只导出本轮新增、待人工复核结构
   - 已完成/已复用结构不重复导出

6. **频率入口准备（不自动运行）**
   - 按你的指令决定是否进入 `frequency.ipynb`
   - 仅先生成“可进入频率”的候选清单

7. **路径提取（独立步骤）**
   - 路径提取与 GO_best 结构筛选分开执行
   - 单独导出后续流程需要的路径清单（供 TEST/ZPE/NEB 连接）

8. **收尾交付**
   - 输出：
     - 结果总表
     - 最低能结构包
     - 复用最小包
     - check 包
     - 下一步建议（是否进频率/NEB）

---

## 默认约束
- 不改变你已确认的主建模规则（主线仍由单吸附/双位点 notebook 决定）
- 收尾阶段不引入新构型，只做筛选/整理/交付
- 涉及调度时沿用 GR_main（含 ng 优先等默认方案）

---

## 与其它 main 的关系
- GO_1body_MAIN：负责构建与提交前主线
- GR_main：负责批量运行与调度
- **GO_WRAPUP_MAIN（本流程）**：负责运行后的标准收尾与交接
