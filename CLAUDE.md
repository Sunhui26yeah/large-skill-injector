# Large Skill Injector — Schema

This is a personal knowledge base organized after [Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). The goal isn't to look things up fresh every time (RAG-style), but to continuously "compile" new information into a set of cross-referenced markdown pages that gets better the more it's used.

**Language: everything in this repo — schema, index, log, and every wiki page in any subdirectory — is written in English, regardless of the language of the source material being ingested.** Translate as needed when ingesting non-English input.

## Three layers

1. **Raw material** — unmodified input (web links, pasted articles, data files, etc.), used once and not necessarily kept long-term in its original form.
2. **Wiki pages** — the markdown files in this directory: summary pages, topic pages, dated pages, cross-linked with each other.
3. **This file (the schema)** — defines the organizing rules and the behavior of the three operations.

## Directory conventions

Modeled on [a real implementation of the Karpathy pattern (NicholasSpisak/second-brain)](https://github.com/NicholasSpisak/second-brain), with similar but simplified subdirectory categories (not using Obsidian's `[[wikilink]]` syntax — all cross-references use standard markdown relative-path links `[text](relative/path.md)`, so navigation still works outside Obsidian, e.g. plain GitHub or plain text editors):

- `index.md` — the catalog of every wiki page, grouped by topic. Every new page must be registered here.
- `log.md` — an append-only operation log; every ingest/query/lint adds a line at the end, history is never rewritten.
- `daily/` — dated pages, named `YYYY-MM-DD_<topic>.md`, e.g. `daily/2026-08-13_top10_corp.md`.
- `concepts/` — topic/concept pages, one concept per file (borrowing the atomicity principle from Andy Matuschak's [evergreen notes](https://notes.andymatuschak.org/Evergreen_notes): one note covers one concept, so it can be referenced from many places without dragging in an entire topic). Topics with a lot of content can get their own subdirectory, but any such subdirectory must have an overview/hub page as its entry point.
- `entities/` — pages for people, organizations, products, tools, etc. (enabled as needed).
- `synthesis/` — cross-cutting analysis/comparison pages spanning multiple concepts/entities (enabled as needed).
- `academic_skill/` — reusable how-to pages for academic/paper-writing workflows (procedural, unlike the fact/concept-oriented `concepts/`).
- All cross-page references use **relative-path** markdown links, never absolute paths (so the whole `Large_Skill_Injector/` directory stays portable if moved or cloned elsewhere). Linking "out" of the repo (e.g. to raw material in `../../Misc/`) is only allowed for local files outside version control, and must be noted as such in the surrounding text.

## The three operations

### Ingest (absorb new material)
1. Read the input, extract the key information.
2. If a relevant page already exists, update it (flag contradictions, add information, don't overwrite prior conclusions — preserve the trail of changes); otherwise create a new page.
3. Register/update the entry for this page in `index.md`.
4. Append a line to `log.md`: `- [YYYY-MM-DD HH:MM] ingest: <what was done, which pages were touched>`.

### Query
1. Check `index.md` first to locate relevant pages, rather than full-text search.
2. If the query produces a new conclusion worth keeping, write it into a new page or append it to an existing one (treat this as a small ingest).

### Lint (health check)
Triggered as needed. Checks for: contradictory statements, outdated-but-unflagged conclusions, orphaned pages (not referenced by `index.md` or any other page), and cross-references that should exist but are missing. Fix issues directly, and log a line in `log.md`.

## On the daily Top 10 company digest

This is the wiki's first standing automated ingest source: every day a cloud routine (not run locally) searches for that day's news on the top 10 companies by global market cap, summarizes it into `daily/YYYY-MM-DD_top10_corp.md`, and commits/pushes it to this repo. **These pages arrive asynchronously** — `git pull` locally to see the latest.

That routine is only responsible for writing the raw summary page; it does not update `index.md`. Periodically (e.g. whenever this skill runs locally), newly appeared dated pages should be registered under the "Daily Company Digest" category in `index.md`, treated as an ingest.

## On the daily people-watch digest

A second standing automated ingest source, parallel to the company digest above: every day a separate cloud routine reads `daily/people_watchlist.md` (a maintained list of named individuals with their roles, plus a "Companies / Organizations" group for orgs worth tracking that are too small or too private to ever show up in the top-10-by-market-cap company digest — e.g. World Labs), searches the prior 24 hours for public activity/mentions of each entry (web search, X/Twitter, LinkedIn where reachable), and writes `daily/YYYY-MM-DD_people_watch.md`. Same async-arrival caveat applies — `git pull` to see the latest.

`daily/people_watchlist.md` is the input the routine reads fresh every run — to add or remove a tracked person or organization, edit that file (or ask Claude to), not the routine itself. Because the routine iterates whatever entries the file contains and preserves its grouping, a new group like "Companies / Organizations" needs no routine-side change. The routine is likewise only responsible for the raw daily page; it does not update `index.md`, and it does not create `entities/` profile pages for the tracked people (deliberately kept out of scope unless requested — don't build that layer speculatively). Newly appeared dated pages get registered under a "Daily People-Watch Digest" category in `index.md` the same way as the company digest.

## On the daily digest email

A third standing cloud routine (`large-skill-injector-daily-digest-email`) runs nightly at 00:20 America/Los_Angeles, after the ingest routines above. It does **not** write to the repo — it only reads `git log` to find every file newly added under `daily/` in the last 4 hours, then sends **one** email to hsun26@ncsu.edu, subject exactly `[Daily Digest]`, with a link to each new file under a "Daily Digest Files" section. The email always sends (even if that section is empty for the night), because it also always includes a static "Job Search Sources" section with two fixed reference links (kept in sync with `concepts/New_Grad_2027_Job_Search_Sources.md`): 留学生海投网 (`https://haitou.zhitongguigu.com/newJob`) and `speedyapply/2027-AI-College-Jobs` (`https://github.com/speedyapply/2027-AI-College-Jobs/blob/main/NEW_GRAD_USA.md`). If a third static link is ever wanted, add it directly to the routine's prompt via `RemoteTrigger update` and mirror the change here.

**This is deliberately generic, not hardcoded to the two sources above.** Any future automated daily ingest routine is picked up by the digest email for free, with no changes needed to the digest routine itself, as long as it:
1. Writes its output as a new file under `daily/` (any filename), and
2. Commits and pushes that file to `main`, and
3. Finishes running sometime between roughly 20:20 and 00:20 America/Los_Angeles (inside the digest routine's 4-hour lookback window).

The digest routine derives a human-readable email label from the filename suffix (e.g. `_top10_corp.md` → "Top 10 Company Digest"); anything it doesn't recognize falls back to a generic title-cased label rather than being skipped. When adding a new daily automated source, prefer a `daily/YYYY-MM-DD_<topic>.md` naming convention consistent with the two above so the fallback label reads sensibly, but it isn't required for the email to include it — only steps 1–3 above are required.
