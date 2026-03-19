# tool_01 文档建立（build 最基本结构）

该 tool 负责两件事：
- 定义并说明 `@absorption` 的标准目录接口；
- 提供 `auto` 入口，在你指定的母目录下自动建立 `absorption` 目录结构。

`tool_01_文档建立/absorption` 目录本身仅作为 **example 模板**，用于展示格式，不作为唯一物理落点。

build 阶段不涉及 NEB（不导出 `ini/fin`、不生成 `nebmake.pl` 输入）。

---

## 0) auto 入口（按母目录动态创建）

入口 notebook：`auto/build_absorption_example.ipynb`

你只需要改一个参数：
- `parent_root`：母目录（例如 `/home/ucaqzh0/thermol/100_water`）

运行后会自动创建：

```text
<parent_root>/absorption/
  1_body/{GO,TEST,Frequency,Final}
  2_body/{GO,TEST,Frequency,Final}
```

---

## 1) `@absorption` 的分类/目录架构（1_body / 2_body）

这里的 `1_body` / `2_body` 不是表示某个固定物理路径，而是用来定义“组织分类规则”：

### 1_body（单吸附）
- `1_body` 对应：`<Species>` + `<site>`
- `<site>` 只覆盖三类：`hollow / top / bridge`

你当前 thermol 目录中典型的“物理落点”是 `GO/` 下的单吸附目录，例如：
- `thermol/100_water/absorption/absorption/GO/absorption_single_H/`
  - 里面有 `job_POSCAR_H_hollow/`、`job_POSCAR_H_top/`、`job_POSCAR_H_bridge/` 等

最终被提取/汇总后，“best 的物理落点”通常在：
- `thermol/100_water/absorption/absorption/GO_final/1_body/<Species>/<site>/`

### 2_body（双吸附）
- `2_body` 对应：`<case_name>`（由 A/B 位点与分子组合命名）
- 典型 case_name 示例（来自你已有目录风格）：
  - `top_OH_bridgeH`
  - `hollow_OH_hollow_H`
  - `top_OH_topH`
  - `mo_hollow_H_hollow_H`

你当前 thermol 目录中典型的“物理落点”是 `GO/` 下的双吸附目录，例如：
- `thermol/100_water/absorption/absorption/GO/top_OH_bridgeH/`
  - 内部包含 `job_*.vasp`（或 job 目录中的 `.vasp` 文件）

最终被提取/汇总后，“best 的物理落点”通常在：
- `thermol/100_water/absorption/absorption/GO_final/2_body/<case_name>/`

> 注：后续 tool_03 负责生成 `case_name` 并输出与上述目录组织一致的结构。

---

## 2) build 阶段的最小文件集

build 阶段统一输出结构文件为 `.vasp` 格式，例如：
- `job_POSCAR_H_hollow.vasp`
- `job_POSCAR_A_hollow_OH__B_hollow_H.vasp`

本阶段不要求生成 `POTCAR/KPOINTS/INCAR`（这些属于后续输入文件生成/提交工具的职责）。

---

## 3) 下一步衔接（build 之后）

- `tool_02`：生成单吸附基础结构，并输出单吸附的 best（或“可进入最佳筛选的候选集”）
- `tool_03`：根据单吸附 best 构建双吸附基础结构（期间使用 align 思路，但仍以结构建立为主）
- `tool_04`：提取 best 结构，交给后续的 NEB/其它流程

