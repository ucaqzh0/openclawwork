# tool_03 双吸附构建

- 输入：`1_body/Final` 下的两个单吸附 best 结构（1 与 2）
- 支持 `1->2` 或 `2->1`，由参数 `species_1/species_2` 指定
- 依据两条最小路径方向生成双吸附候选（dir1/dir2）
- 仅生成 `.vasp` + 原子标号，不做计算与提交

入口：`auto/build_double_adsorption.ipynb`

