# tool_04 Final 汇总与地址清单

- 作用：把 `1_body/Final` 和 `2_body/Final` 的最终结果统一整理到 `thermol/Cu_100_absorption`
- 输出目录：`/home/ucaqzh0/thermol/Cu_100_absorption/{1_Body,2_Body}`
- 清单输出：`/home/ucaqzh0/thermol/Cu_100_absorption/address_manifest.tsv`
- 用途：后续直接索引已有结构，避免重复计算

入口：`auto/collect_final_to_thermol.ipynb`

说明：
- 仅做结构与结果文件整理，不做提交/计算
- 默认提取 `.vasp` 与 `OUTCAR`，可按参数灵活修改
