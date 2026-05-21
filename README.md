# 5G FFR 仿真复现作品展示

这是一个面向作品集、简历和面试讲解的 5G 分数频率复用（Fractional Frequency Reuse, FFR）公开展示仓库。仓库用 Python 构建可重复的合成数据仿真流程，复刻 MATLAB 风格论文验证管线的结构：生成 SNR 与用户密度扫描、比较 IFR3/SWF/FFR 组合策略、验证定性趋势，并输出论文风格图表。

> 公开边界：本仓库包含的是 synthetic/demo 数据和脱敏后的 Python 展示流程，不复制私有 MATLAB 源码，不包含未公开原始实验输出，也不把 demo 结果表述为真实论文数据。

## Related Paper

- Paper: [Research on Fractional Frequency Multiplexing Strategies in 5G Networks](https://drpress.org/ojs/index.php/HSET/article/view/28966)

该论文链接用于说明项目主题来源和研究方向。仓库中的图表、CSV 和 JSON 输出均由本仓库代码生成，是公开展示用的合成 demo，不等同于论文原始数据或私有实现。

## English Summary

This repository is a public synthetic-data showcase for a 5G fractional frequency reuse simulation workflow. It demonstrates reproducibility discipline, communication-network reasoning, trend validation, and paper-style figure generation without shipping private source files or unpublished raw experiment data.

## 展示范围

- 主题：5G cellular / heterogeneous network interference mitigation with fractional frequency reuse。
- 方法：`IFR3`、`SWF`、`FFR+IFR3`、`FFR+SWF`。
- 指标：capacity、spectral efficiency、edge capacity、edge SINR、interference index。
- 复现形式：用确定性 Python 流程模拟 MATLAB 风格 alignment workflow。
- 数据边界：所有数据均为 synthetic/demo 数据，仅用于公开作品集展示。

## 图表复现状态

| Figure | Public demo target | Script | Status | Data note |
| --- | --- | --- | --- | --- |
| Fig.3 Capacity vs SNR | Capacity increases with SNR; SWF variants improve total capacity | `python scripts/generate_figures.py` | Implemented | Synthetic/demo data |
| Fig.4 Edge SINR | FFR variants improve edge-user SINR under interference | `python scripts/generate_figures.py` | Implemented | Synthetic/demo data |
| Capacity vs user density | Capacity/interference changes under denser users | `python scripts/run_paper_alignment.py` | Implemented | Synthetic/demo data |
| Trend verification | Monotonic SNR gain, FFR edge gain, SWF capacity gain | `python scripts/verify_paper_trends.py` | Implemented | Synthetic/demo data |

## 快速运行

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[test]"
python scripts/run_paper_alignment.py
python scripts/verify_paper_trends.py
python scripts/generate_figures.py
pytest
```

生成的 CSV、JSON 和 PNG 文件会写入 `outputs/`。

## 仓库结构

```text
src/ffr_showcase/      Synthetic simulation, trend checks, and plotting
scripts/               Command-line entry points
tests/                 Pytest smoke and trend tests
docs/                  Public methodology notes and static demo page
data/                  Data policy and synthetic-data notes
outputs/               Generated local artifacts, kept out of source by default
```

## 为什么使用合成数据？

该仓库面向公开作品集审阅，重点展示仿真设计、复现意识和通信网络推理能力。它不公开私有路径、原始 MATLAB 代码、敏感账号信息或未发布原始材料。

## 趋势检查

`verify_paper_trends.py` 检查：

- 每种方法在中位用户密度下，capacity 随 SNR 增长；
- FFR 变体相比非 FFR 对照提升 edge-user SINR；
- 用户密度增加时 interference index 上升；
- SWF 相比对应 IFR3-style baseline 提升 total capacity。
