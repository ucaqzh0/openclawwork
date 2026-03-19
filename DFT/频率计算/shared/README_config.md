# 配置说明（功能机 clio 可直接修改）

## 修改入口

**`config.py`** — 所有 tool 的路径与分区均从此读取。

## 可修改项

| 变量 | 说明 | 示例 |
|------|------|------|
| `ZPE_ROOT` | 频率计算任务根目录 | `/home/ucaqzh0/thermol/.../ZPE/high/` |
| `DEFAULT_PARTITION` | 默认提交分区 | `young` (SGE) / `young_ng` (Slurm) |
| `CORRECTED_OUTPUT_DIR` | 507 修正结构的输出目录（稍后统一指定） | `None` 或 `/path/to/corrected_structures` |
| `EXECUTION_HOST` | 执行机（用于任务清单） | `xiaozhua` / `clio` |

## 使用方式

1. 在 clio 上打开 `频率计算/shared/config.py`
2. 修改 `ZPE_ROOT` 为当前任务的 ZPE 路径
3. 保存后，各 tool 下次运行时会自动读取新配置

**可选**：设置环境变量 `XIAOZHUA_FREQ_DIR` 指向 `频率计算` 目录，可覆盖自动查找逻辑。

## 生效范围

- tool_01 结构准备
- tool_02 提交调度（含提交前检查）
- tool_03 结果解析
- tool_04 频率修正
- pre_check（独立执行）
