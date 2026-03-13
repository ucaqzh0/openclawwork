# GR_main — Global Optimization Runflow

更新时间：2026-03-13

## 定位
`GR` 是用于 Global Optimization 类型计算的统一运行主流程。
`GO_HybridDrain` 已并入 `GR_main`，作为其内置双机调度机制（不再作为独立 main）。

## 适用范围
- 面向可拆分的批任务（如 GO_1body 的多构型并行）
- 目标是最大化 young.ng 吞吐，同时利用 young 兜底排队

## 资源模板
- young.ng（Slurm）
  - 每任务：3 节点
  - 每节点：40 tasks
  - 总计：120 tasks（40 的整数倍约束）
- young（SEG）
  - 每任务：128 核（2 个完整节点）

## 调度前置（必须）
- 每次提交前，先汇报各服务器可用算力：
  - young
  - young.ng
  - 用户后续新增的任意服务器
- 对于无法查询的服务器，明确输出：`N/A`。

## 内置双机调度机制（原 GO_HybridDrain）
- 默认方案（用户未给特殊安排时）：优先提交到 young.ng，且每任务使用 3 nodes。
1. 读取 young.ng 当前空闲节点数
2. 按 `floor(idle_nodes / 3)` 计算 ng 可接收任务数
3. 先提交可容纳的任务到 young.ng
4. 剩余任务提交到 young（排队）
5. 每当 young.ng 完成 1 个任务：
   - 从 young 中选 1 个尚未启动（qw）的任务
   - 取消该 young 排队任务
   - 迁移并重投到 young.ng

## 提交前检查
- 输入完整：POSCAR/INCAR/KPOINTS/POTCAR
- POTCAR 与 POSCAR 元素顺序严格匹配
- 任务目录可追溯（task/species/site/orientation）

## 运行产物
- 任务分发表：`memory/GR_dispatch_*.tsv`
- 迁移日志：`memory/GR_migrator_*.log`
- 迁移进程 PID：`memory/GR_migrator_*.pid`

## 与 GO_1body 的关系
- GO_1body 定义“如何构建结构”
- GR_main 定义“如何批量运行计算（含双机调度）”
- 两者解耦：构建逻辑可变，调度主流程稳定复用
