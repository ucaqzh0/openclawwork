# absorption 模板（tool_01）

本目录仅用于建立结构构建阶段的标准骨架。

目录固定为：
- 1_body/{GO,TEST,Frequency,Final}
- 2_body/{GO,TEST,Frequency,Final}

说明：
- build 生成的结构统一为 .vasp 文件
- GO：初始结构与计算输入待后续工具补齐
- TEST：新结构人工检查区
- Frequency：频率计算完成后，若有 correction 结构放这里，并用于一次 SCF
- Final：最终确认结构归档
