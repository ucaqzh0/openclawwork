# Global Optimization（GO）

> 输入文件生成 → 任务调度 → 结果收尾。参考 `thermol/tool/GO_SEG.py`、`GO_SLURM.py`。

---

## 结构

```
Global_optimization/
├── README.md
├── 运行规则.md
├── 流程映射.md
├── 任务清单_Global_optimization.md
├── shared/
│   ├── config.py
│   ├── load_config.py
│   ├── pre_check.py
│   ├── input_templates.py    # INCAR、KPOINTS 模板
│   └── 移交检查.md
├── tool_01_输入文件生成/
│   ├── auto/generate_inputs.ipynb
│   └── debug/
├── tool_02_提交调度/
│   ├── auto/submit_dispatch.ipynb
│   └── debug/
└── tool_03_结果收尾/
    ├── auto/wrapup.ipynb
    └── debug/
```

---

## 流程映射

| Step | 工具 | 说明 |
|------|------|------|
| Step1 | tool_01 输入文件生成 | 从 .vasp 生成 POSCAR、POTCAR、KPOINTS、INCAR |
| Step2 | tool_02 提交调度 | 与频率计算等工具一致（job_list、submit.sh） |
| Step3 | tool_03 结果收尾 | 完成态扫描、结果提取、GO_best 筛选 |

---

## 移交检查

返回检查单时需确认：**POSCAR、POTCAR、KPOINTS、INCAR** 四类文件齐全。

---

## 配置

- `shared/config.py`：GO_ROOT、DEFAULT_PARTITION
- 双模式：xiaozhua / clio，路径按执行机填写
