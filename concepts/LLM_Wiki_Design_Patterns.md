# LLM Wiki Design Patterns

Research notes on "LLM-maintained personal knowledge base" systems, written while setting up this repo ([Large Skill Injector](../README.md)). Goal: don't reinvent the wheel — see what pitfalls others have already hit and what conventions they settled on.

## The source: Karpathy's LLM Wiki

The direct starting point this repo copies from; see the citation in [README.md](../README.md) and the schema in [CLAUDE.md](../CLAUDE.md). Core claim: use an LLM to "compile" scattered material into a persistent, cross-referenced wiki that converges over time, instead of looking things up fresh every time (RAG-style). The three-layer architecture (raw material / wiki pages / schema config) and the three operations (Ingest / Query / Lint) both come from there — details aren't repeated here, see [CLAUDE.md](../CLAUDE.md).

## A real implementation: NicholasSpisak/second-brain

[github.com/NicholasSpisak/second-brain](https://github.com/NicholasSpisak/second-brain) is one concrete implementation of the Karpathy pattern, built for Obsidian. Its directory structure roughly looks like:

```
raw/                  # unprocessed source material (assets/ holds image attachments)
wiki/
  sources/            # per-source summaries
  entities/           # people, organizations, products, tools
  concepts/           # ideas, frameworks, theories
  synthesis/          # cross-topic comparative analysis
  index.md            # master catalog
  log.md              # operation log
output/                # generated report-type artifacts
CLAUDE.md              # agent config
```

Takeaways:
- **Splitting subdirectories by content type** (entities / concepts / synthesis) is easier to maintain than dumping everything in one flat directory, especially once the page count grows. This repo's [CLAUDE.md](../CLAUDE.md) already adopted a similar concepts/entities/synthesis split.
- It uses Obsidian's `[[wikilink]]` syntax for cross-references, plus a lint step specifically for catching "wikilinks broken by a rename." **This repo doesn't use that syntax** — not every context opens this in Obsidian (e.g. straight from the GitHub web UI, a plain text editor, or another agent cloning it down to read). Standard markdown relative-path links `[text](path.md)` are more portable, at the cost of having to manually fix every link pointing at a file when you rename it (one of the main things a lint pass checks for).
- The `raw/` vs `wiki/` separation is the right idea (source material stays untouched, wiki pages are the processed output), but this repo doesn't currently have a separate `raw/` directory, since most "raw material" already lives elsewhere in the project (e.g. `../../Misc/`) — no need to duplicate it, just note the source path in the wiki page itself.

## Note-taking tool landscape (background, not directly adopted)

A few related-but-different-purpose tools also came up during research:

- **Dendron / Logseq / Foam**: all "human writes, machine assists navigation" note tools, not "LLM auto-maintained." Dendron uses dot-separated filenames for hierarchy (`project.foo.bar.md`), Logseq leans outliner + bidirectional links, Foam is a lightweight VS Code note extension. They solve "how should a human organize notes," which isn't quite the same problem as this repo's "how should an LLM organize notes" — but concepts like bidirectional links and graph views are common reference points.
- **Digital gardens** (see [MaggieAppleton/digital-gardeners](https://github.com/MaggieAppleton/digital-gardeners)): the idea that notes are "alive" — allowed to be published half-finished and grow over time, rather than being a blog post that's done once written. That mindset matches what Karpathy means by "the wiki is a continuously compiled artifact."

## Andy Matuschak's Evergreen Notes: the atomicity principle

[notes.andymatuschak.org/Evergreen_notes](https://notes.andymatuschak.org/Evergreen_notes):

- A note covers **one concept** — not a book, not a whole topic, not a project. That's what lets it be referenced from many different places without the link's meaning getting diluted by too broad a topic.
- Notes should be expected to "get better as you revise them," not written once and archived — different from a traditional wiki where "once written, it's a historical record," and closer to this repo's Ingest requirement to "update an existing page rather than just appending" (see [CLAUDE.md](../CLAUDE.md)).
- Lineage-wise it's close to Zettelkasten (the slip-box method), but with looser rules and more emphasis on revising over time.

## Conclusion: this repo's current design decisions

1. The schema lives in [CLAUDE.md](../CLAUDE.md) — the single source of truth for "how this operates"; other pages don't re-explain the rules.
2. Cross-references are always relative-path markdown links, never wikilink syntax.
3. Subdirectories split by content type (`daily/` for dated pages, `concepts/` for topics, `entities/`/`synthesis/` enabled as needed); a large topic that outgrows a single page gets its own subdirectory with an overview/hub page as the entry point.
4. Don't duplicate source material if avoidable — link back to where it actually lives, and note whether that location is under version control.
5. Notes are allowed to be revised and expanded over time; they aren't write-once archives.

---
Further reading (not expanded on in the main text, just leads for later): [TiddlyWiki](https://tiddlywiki.com/), Roam Research's bidirectional-link mechanism, the original source of the Zettelkasten method (Niklas Luhmann).
