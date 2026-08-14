# Log

追加写，不改历史记录。

- [2026-08-13 23:30] init: 按 Karpathy 的 LLM Wiki 模式初始化本仓库（CLAUDE.md / index.md / log.md），设置为独立 git 仓库并计划推送到 GitHub private repo `large-skill-injector`。同时配置每天 23:59 PDT 的云端定时任务，抓取全球市值前十公司当天新闻，写入 `daily/YYYY-MM-DD_top10_corp.md`。
- [2026-08-13 23:50] ingest: 云端 routine 创建卡在 "GitHub account not connected"，先在当前会话手动测试一次抓取流程，生成 `daily/2026-08-13_top10_corp.md`，并登记进 index.md。用于验证 prompt 逻辑，不是自动化产出。
- [2026-08-14 00:05] ingest: 按用户要求自主探索 GitHub 上的 LLM wiki / 第二大脑仓库模式（Karpathy 原始 gist、NicholasSpisak/second-brain、Dendron/Logseq/Foam、Andy Matuschak evergreen notes），写成 `concepts/LLM_Wiki_设计模式.md`；并把此前在 Misc/ 整理好的 CRA FAQ 拆成 `concepts/CRA/` 下 8 个互相链接的页面（总览 + 7 章，76 条问答）。据此把 CLAUDE.md 的目录约定更新为 concepts/entities/synthesis 子目录分类 + 相对路径链接原则（不用 Obsidian wikilink 语法）。index.md 已同步登记新页面。这是一轮自定节奏的过夜自主探索的第一次迭代（/loop dynamic mode，目标跑到 2026-08-14 07:00 PDT）。
