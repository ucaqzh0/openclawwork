# tool_02 单吸附位点构建

- 参考 `DFT/tool/H2O_单吸附模型构建.ipynb` 与 `DFT/workflow/GO_1body_builder_ase.py`
- 仅负责生成 `.vasp` 结构，不做提交与计算
- 支持位点：`hollow / top / bridge`
- 分子来源：H/O/OH/H2/H2O + CO/CHO/COOH（ASE 标准来源）
- 构建必须指定 `layer_from_top`（1=顶层，2=次顶层）
- 位点搜索中心默认优先使用第一层（顶层）中心：`center_layer_from_top=1`

入口：`auto/build_single_adsorption.ipynb`
