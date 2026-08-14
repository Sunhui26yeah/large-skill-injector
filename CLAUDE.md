# Large Skill Injector — 外置大脑 Schema

这是一个按 [Karpathy 的 LLM Wiki 模式](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 组织的个人知识库。目标不是每次现查现答（RAG），而是持续把新信息"编译"进一套互相引用的 markdown 页面里，越用越完善。

## 三层结构

1. **原始资料** — 不改动的输入（网页链接、粘贴的文章、数据文件等），只作为一次性输入，不必长期保留原文。
2. **wiki 页面** — 本目录下的 markdown 文件：摘要页、主题页、日期页，互相用相对链接引用。
3. **本文件（schema）** — 定义组织规则和三个操作的行为。

## 目录约定

参考了 [Karpathy 模式的一个实际实现（NicholasSpisak/second-brain）](https://github.com/NicholasSpisak/second-brain) 后，采用类似但简化的子目录分类（不用 Obsidian 的 `[[wikilink]]` 语法，统一用标准 markdown 相对路径链接 `[文字](相对路径.md)`，保证脱离 Obsidian、纯 GitHub/纯文本场景下也能跳转）：

- `index.md` — 所有 wiki 页面的分类目录，按主题分组，新增页面必须在这里登记一行。
- `log.md` — 追加写的操作日志，每次 ingest / query / lint 都在末尾加一行，不回溯修改历史记录。
- `daily/` — 日期类页面，命名为 `YYYY-MM-DD_<主题>.md`，例如 `daily/2026-08-13_top10_corp.md`。
- `concepts/` — 主题/概念类页面，一个概念一个文件（借鉴 Andy Matuschak 的 [evergreen notes](https://notes.andymatuschak.org/Evergreen_notes) 原子化原则：一篇笔记只讲一个概念，方便被多处引用而不必扯出整个话题）。内容量大的主题可以开子目录，比如 `concepts/CRA/`，但子目录内必须有一个总览/hub 页面做入口。
- `entities/` — 人物、组织、产品、工具等实体类页面（暂未启用，需要时再建）。
- `synthesis/` — 跨多个 concepts/entities 的综合分析、对比类页面（暂未启用，需要时再建）。
- 所有页面之间的引用一律用**相对路径**的 markdown 链接，不用绝对路径（这样整个 `Large_Skill_Injector/` 目录换位置、被别的机器 clone 之后链接依然有效）；只有引用仓库之外的本地文件（比如 `../../Misc/` 里的原始资料）时才允许链接"跳出"仓库，且要在文字里注明这是本地路径、不在本仓库版本控制范围内。

## 三个操作

### Ingest（吃进新资料）
1. 读输入，提炼关键信息。
2. 如果已有相关页面，更新它（标注矛盾、补充信息、不要覆盖旧结论——保留变更痕迹）；否则新建页面。
3. 在 `index.md` 里登记/更新这条页面的索引。
4. 在 `log.md` 末尾追加一行：`- [YYYY-MM-DD HH:MM] ingest: <做了什么，涉及哪些页面>`。

### Query（查询）
1. 先看 `index.md` 定位相关页面，而不是全文搜索。
2. 如果这次问答产出了值得沉淀的新结论，把它写成新页面或追加到已有页面（视同一次小型 ingest）。

### Lint（体检）
按需触发，检查：矛盾的表述、过时但未标注的结论、孤立（没被 index.md 或其他页面引用）的页面、该建立但缺失的交叉引用。发现问题直接修，并在 `log.md` 记一行。

## 关于每日 Top10 公司动态

这是本 wiki 第一个常驻的自动化 ingest 来源：每天由一个云端定时任务（不在本地跑）搜索当天全球市值前十公司的新闻，摘要写成 `daily/YYYY-MM-DD_top10_corp.md`，提交并推送到本仓库。**这些页面到本地是异步的**——本地要看到最新内容，需要 `git pull`。

该任务只负责"写入原始摘要页"，不负责更新 `index.md`。定期（比如每次你在本地用这个 skill 时）应该把新出现的日期页登记进 `index.md` 的"每日公司动态"分类下，视为一次 ingest。
