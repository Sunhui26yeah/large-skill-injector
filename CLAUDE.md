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
