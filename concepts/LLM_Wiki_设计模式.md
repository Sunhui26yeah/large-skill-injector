# LLM Wiki 设计模式

对"LLM 维护的个人知识库"这一类系统的调研笔记，写于搭建本仓库（[Large Skill Injector](../README.md)）的过程中。目的是不重复造轮子，看看别人已经踩过哪些坑、沉淀出哪些约定。

## 源头：Karpathy 的 LLM Wiki

本仓库直接照搬的起点，参见 [README.md](../README.md) 里的引用和 [CLAUDE.md](../CLAUDE.md) 的 schema。核心主张：用 LLM 把零散资料"编译"成一份持续存在、互相引用、随时间收敛的 wiki，而不是每次现查现答（RAG）。三层架构（原始资料 / wiki 页面 / schema 配置）+ 三个操作（Ingest / Query / Lint）都来自这里，细节不重复，见 [CLAUDE.md](../CLAUDE.md)。

## 一个真实实现：NicholasSpisak/second-brain

[github.com/NicholasSpisak/second-brain](https://github.com/NicholasSpisak/second-brain) 是 Karpathy 模式的一个具体落地，给 Obsidian 用的。目录结构大致是：

```
raw/                  # 待处理的原始资料（含 assets/ 存图片附件）
wiki/
  sources/            # 单篇资料的摘要
  entities/           # 人物、组织、产品、工具
  concepts/           # 想法、框架、理论
  synthesis/          # 跨主题的对比分析
  index.md            # 总目录
  log.md              # 操作日志
output/                # 生成的报告类产物
CLAUDE.md              # agent 配置
```

学到的东西：
- **按内容类型分子目录**（entities / concepts / synthesis）比全部堆在一个平面目录里更容易维护，尤其页面数量上来之后。本仓库的 [CLAUDE.md](../CLAUDE.md) 已经采纳了类似的 `concepts/` / `entities/` / `synthesis/` 划分，但目前只有 `concepts/` 有实际内容。
- 它用 Obsidian 的 `[[wikilink]]` 语法做交叉引用，配一个 lint 环节专门抓"改名后失效的 wikilink"。**本仓库没有采用这个语法**——因为不是所有场景都在 Obsidian 里打开（比如直接在 GitHub 网页、纯文本编辑器、或者被其他 agent clone 下来读取），标准 markdown 相对路径链接 `[文字](路径.md)` 兼容性更好，代价是重命名文件时要手动改所有引用它的链接（lint 阶段的重点工作之一）。
- `raw/` 和 `wiki/` 分离的思路是对的（原始资料不改动，wiki 页面是加工产物），但本仓库目前没有单独建 `raw/` 目录，因为大部分"原始资料"本来就在项目里别的地方（比如 `../../Misc/`），没必要复制一份，直接在 wiki 页面里标注来源路径即可，见 [CRA FAQ 总览](CRA/CRA_总览.md) 的做法。

## 笔记类工具生态（背景知识，不直接照搬）

搜索时还看到几类相关但设计目标不同的工具：

- **Dendron / Logseq / Foam**：都是"人手写、机器辅助导航"的笔记工具，不是"LLM 自动维护"。Dendron 用文件名里的点号做层级（`project.foo.bar.md`），Logseq 偏 outliner + 双向链接，Foam 是 VS Code 里的轻量笔记扩展。它们解决的是"人类如何组织笔记"，跟本仓库"LLM 如何组织笔记"的问题不完全一样，但双向链接、graph view 这些概念是共通的参考。
- **Digital gardens**（数字花园，参考 [MaggieAppleton/digital-gardeners](https://github.com/MaggieAppleton/digital-gardeners)）：强调笔记是"活的"、允许公开半成品、随时间生长，而不是写完就定稿的博客文章。这个心态和 Karpathy 说的"wiki 是持续编译的 artifact"是一个意思。

## Andy Matuschak 的 Evergreen Notes：原子化原则

[notes.andymatuschak.org/Evergreen_notes](https://notes.andymatuschak.org/Evergreen_notes)：

- 一篇笔记只讲**一个概念**，不是一本书、不是一个话题、不是一个项目。这样笔记才能被很多不同的地方引用，而不会因为话题太宽导致链接意义模糊。
- 笔记应该被期待"越改越好"，而不是写一次就存档不动——跟传统 wiki "写完就是历史记录"不一样，更接近本仓库 Ingest 操作里"更新已有页面而不是简单追加"的要求（见 [CLAUDE.md](../CLAUDE.md)）。
- 血缘上接近 Zettelkasten（卡片盒笔记法），但规则更松、更强调随时间修订。

**本仓库的取舍**：CRA FAQ 那批页面（[CRA_总览](CRA/CRA_总览.md)）目前是按原文档章节切的，不是严格"一个概念一篇"——因为原始资料本身就是问答对形式，保留原文档结构方便和官方 FAQ 对照查阅优先于严格原子化。如果以后这个主题的引用需求变多（比如某一条具体问答被很多其他页面引用），再考虑把高频引用的问答拆成独立的 concepts 页面。

## 结论：本仓库目前的设计决定

1. schema 定义在 [CLAUDE.md](../CLAUDE.md)，是唯一的"操作手册"来源，其他页面不重复解释规则。
2. 交叉引用一律相对路径 markdown 链接，不用 wikilink 语法。
3. 子目录按内容类型分（`daily/` 日期类、`concepts/` 主题类，`entities/`/`synthesis/` 按需启用），大主题在子目录内建总览页面做入口（模式参考 [CRA_总览](CRA/CRA_总览.md)）。
4. 原始资料能不复制就不复制，链接回原始位置并注明是否在版本控制范围内。
5. 笔记允许随时间被修订、扩写，不是写一次就不动的存档。

---
延伸阅读（未在正文展开，仅作为进一步调研的线索）：[TiddlyWiki](https://tiddlywiki.com/)、[Roam Research](https://roamresearch.com/) 的双向链接机制、Zettelkasten 卡片盒方法论原始出处（Niklas Luhmann）。
