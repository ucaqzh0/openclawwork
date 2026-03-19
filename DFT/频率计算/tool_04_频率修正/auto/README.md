# tool_04 频率修正 — 507 自动化规范

## 输入
- 来自 tool_03 的 `HAS_IMAG` 结构列表（结构名、目录路径、虚频值）。
- 每个目录需含：OUTCAR、CONTCAR、POSCAR、INCAR、KPOINTS、POTCAR（vaspkit 507 依赖完整输出）。

## 执行流程
1. 进入该结构目录，执行 `vaspkit`，选择功能 **507**。
2. **分支判定**：
   - 若全部虚频 < 50 cm⁻¹：自动选 `no`（或直接校正），输入因子 `0.01`。
   - 若存在虚频 ≥ 50 cm⁻¹：本 main 为 final-purpose，选 `no` 校正所有虚频，输入因子 `0.01`。
3. 将生成的 `POSCAR_NEW` 覆盖为 `POSCAR`。
4. 调用 tool_02 的提交逻辑，重新提交频率任务。
5. 记录修正信息（原虚频、校正因子、迭代轮次）。

## 自动化注意
- vaspkit 507 为交互式，自动化需通过 `echo` 管道或 expect 传入 `no` 和 `0.01`。
- 示例：`echo -e "no\n0.01" | vaspkit`（具体以 vaspkit 实际交互顺序为准）。

## 迭代与失败
- 若校正后重跑仍 HAS_IMAG：可降因子（0.005、0.002）或标记 `CORRECTION_FAILED`。
- 详见 `../../运行规则.md` 第 4 节。
