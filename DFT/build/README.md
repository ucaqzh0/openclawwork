# build（结构构建基础功能）

> 与 `Global_optimization` 并行的“建模/结构生成”功能结构。

`build/` 只做“最基本结构的建立/落地”（位点准确 + 分子结构合理），目录与命名架构严格参照你现有 `@absorption` 的 `1_body/2_body` 结构。

本阶段不包含 NEB（不导出 `ini/fin`、不涉及 `nebmake.pl`）。

后续：
- `Global_optimization` 或你已有的 `GO_SEG.py / GO_SLURM.py` 负责把这些结构进一步变成可提交的 VASP 输入（POSCAR/POTCAR/KPOINTS/INCAR 等）。

接口对接请统一按：`接口规范.md`

