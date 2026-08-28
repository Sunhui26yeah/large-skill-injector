# Index

Catalog of every wiki page, grouped by topic. See [CLAUDE.md](CLAUDE.md) for the organizing rules.

## Daily Company Digest

Written automatically to `daily/` by a cloud routine at 23:59 (Pacific time) every day, summarizing what happened that day for the top 10 companies by global market cap.

- [2026-08-13](daily/2026-08-13_top10_corp.md) — Same-day activity for NVIDIA/Apple/Alphabet/Microsoft/Amazon/TSMC/Broadcom/SpaceX/Meta/Tesla (a manual test run, not produced by the cloud routine)

## Daily People-Watch Digest

Written automatically to `daily/` by a separate cloud routine at 23:45 (Pacific time) every day — 15 minutes before the company digest above — summarizing the prior 24 hours of public activity/mentions for the people on [`daily/people_watchlist.md`](daily/people_watchlist.md).

- [people_watchlist.md](daily/people_watchlist.md) — the maintained list of 20 tracked people (AI labs/model developers, chips/infrastructure, big tech CEOs, AI safety/academia, capital/governance); edit this to add/remove who gets tracked
- (no daily digest pages yet — routine created 2026-08-14, first scheduled fire pending)

## Concepts

- [LLM Wiki Design Patterns](concepts/LLM_Wiki_Design_Patterns.md) — Survey of several "LLM-maintained personal knowledge base" implementations on GitHub (Karpathy's original pattern, NicholasSpisak/second-brain, Dendron/Logseq/Foam, Andy Matuschak's evergreen notes), and the design decisions made for this repo as a result
- [New Grad 2027 Job Search — Primary Sources](concepts/New_Grad_2027_Job_Search_Sources.md) — The two sources to check first when asked about 2027 new-grad openings: 留学生海投网 (international-student-focused, broad roles/geos) and speedyapply/2027-AI-College-Jobs' NEW_GRAD_USA.md (AI/ML-specific, US-only, GitHub-native)
- [US Visa Scheduling Website](concepts/US_Visa_Scheduling_Website.md) — Official link for scheduling US visa appointments, return this when asked for "the US visa website"
- [PerfAgent (arXiv 2607.19653)](concepts/PerfAgent_2607_19653.md) — Profiler-guided, verifier-in-the-loop agent workflow for repository-level code optimization; closest existing baseline for Hui's PyTorch MCTS+KB thesis idea
- [NC State CSC PhD Seminar Check-in](concepts/NC_State_CSC_PhD_Seminar_Checkin.md) — Link for the CSC department's PhD graduate seminar attendance check-in system (Unity ID SSO required)

## Academic Skills

Reusable how-to pages for paper/academic-writing workflows (procedural, unlike the fact/concept-oriented `concepts/`):

- [Markdown to PDF Without a pandoc/LaTeX Toolchain](academic_skill/Markdown_to_PDF_Without_Toolchain.md) — python-markdown + GFM checkbox preprocessing + headless Chrome printing, plus a gotcha where emoji used as checkbox glyphs collapse to the same box in the PDF renderer, and a technique for screenshot-verifying multi-page renders

## Entities

Companies that showed up in the daily digest, one page per company, accumulating "related activity" links as new daily digests come in:

- [NVIDIA](entities/NVIDIA.md)
- [Apple](entities/Apple.md)
- [Alphabet / Google](entities/Alphabet.md)
- [Microsoft](entities/Microsoft.md)
- [Amazon](entities/Amazon.md)
- [TSMC](entities/TSMC.md)
- [Broadcom](entities/Broadcom.md)
- [SpaceX](entities/SpaceX.md)
- [Meta Platforms](entities/Meta.md)
- [Tesla](entities/Tesla.md)

## Synthesis

- [PerfAgent vs. Hui's MCTS + Self-Evolving-KB Idea for PyTorch Performance Optimization](synthesis/PerfAgent_vs_MCTS_KB_PyTorch_Perf_Idea.md) — Compares PerfAgent's single-chain profiler-guided refinement loop against Hui's candidate thesis idea (branching MCTS over a self-evolving KB, PyTorch-specific); PerfAgent is broader in target domain, Hui's idea is broader in search mechanism and knowledge use
