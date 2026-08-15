# Index

所有 wiki 页面的分类目录。看 [CLAUDE.md](CLAUDE.md) 了解组织规则。

## 每日公司动态

由每天 23:59（太平洋时间）的云端定时任务自动写入 `daily/` 目录，摘要全球市值前十公司当天发生的事。

- [2026-08-13](daily/2026-08-13_top10_corp.md) — NVIDIA/苹果/Alphabet/微软/亚马逊/台积电/博通/SpaceX/Meta/特斯拉当日动态（手动测试跑，非云端 routine 产出）

## Concepts

- [LLM Wiki 设计模式](concepts/LLM_Wiki_设计模式.md) — 调研 GitHub 上几种"LLM 维护的个人知识库"实现（Karpathy 原始模式、NicholasSpisak/second-brain、Dendron/Logseq/Foam、Andy Matuschak 的 evergreen notes）后，为本仓库定下的设计取舍
- [网络韧性法案 (CRA) FAQ 总览](concepts/CRA/CRA_总览.md) — 欧盟《网络韧性法案》官方 FAQ 中文译本，按章节拆分为 8 个页面（总览 + 7 章），共 76 条问答
  - [1. 范围](concepts/CRA/CRA_1_范围.md)
  - [2. 与其他立法的相互关系](concepts/CRA/CRA_2_与其他立法的相互关系.md)
  - [3. 重要及关键产品](concepts/CRA/CRA_3_重要及关键产品.md)
  - [4. 制造商的义务](concepts/CRA/CRA_4_制造商的义务.md)
  - [5. 制造商的报告义务](concepts/CRA/CRA_5_制造商的报告义务.md)
  - [6. 合格评定](concepts/CRA/CRA_6_合格评定.md)
  - [7. 过渡期](concepts/CRA/CRA_7_过渡期.md)

## Academic Skills

论文/学术写作相关、可复用的操作流程类页面（跟 `concepts/` 里偏事实/概念性的笔记不同，这里是"怎么做"的 how-to）：

- [Markdown 转 PDF：没有 pandoc/LaTeX 工具链时的本地方案](Academic_skills/Markdown转PDF_无工具链本地方案.md) — 用 python-markdown 预处理 GFM checkbox + headless Chrome 打印，附一个"emoji 当 checkbox 图标会被 PDF 渲染器退化成同一个方框"的坑，以及截图核查多页 PDF 内容的技巧

## Entities

来自每日公司动态里出现的公司，一家公司一篇页面，随时间随新的每日动态积累「相关动态」链接：

- [NVIDIA](entities/NVIDIA.md)
- [Apple](entities/Apple.md)
- [Alphabet / Google](entities/Alphabet.md)
- [Microsoft](entities/Microsoft.md)
- [Amazon](entities/Amazon.md)
- [台积电 / TSMC](entities/TSMC.md)
- [Broadcom](entities/Broadcom.md)
- [SpaceX](entities/SpaceX.md)
- [Meta Platforms](entities/Meta.md)
- [Tesla](entities/Tesla.md)

## Synthesis

- （暂无，需要时再建）
