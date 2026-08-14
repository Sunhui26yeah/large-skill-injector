# Large Skill Injector

> "The LLM writes and maintains all of it. You're in charge of sourcing, exploration, and asking the right questions."
> — Andrej Karpathy, [*LLM Wiki*](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

## Where the name comes from

In **EVE Online**, a *Skill Injector* is an item you use on your character to instantly grant skill points — bypassing the game's normal real-time training queue, where skills are learned passively, minute by minute, day by day, for months or years. A **Large Skill Injector** is the bigger version: one use hands your character 500,000 skill points on the spot. Capability that would normally take weeks of waiting is just... there, immediately usable.

That's the whole appeal of the item: it converts *time and patience* into *instant, applied capability* — which is also the point of this folder: an external brain that, once "injected" with new material, just knows it.

## What this actually is

A personal knowledge base following Karpathy's [*LLM Wiki*](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern — instead of re-deriving answers from scratch every time (RAG-style), Claude incrementally builds and maintains a persistent, cross-linked set of markdown pages here. New material gets read, synthesized, and woven into existing pages rather than just filed away.

- **[`CLAUDE.md`](CLAUDE.md)** — the schema: how pages are organized and how Ingest / Query / Lint work here. Read this first.
- **`index.md`** — catalog of every page in this wiki, grouped by topic.
- **`log.md`** — append-only record of what got ingested/queried/linted, and when.
- **`daily/`** — dated pages (`YYYY-MM-DD_<topic>.md`), currently populated by an automated daily routine (see below).

## Automated: daily Top 10 company digest

A cloud routine runs every day at 23:59 (Pacific time), searches for that day's news on the top 10 companies by global market cap, and commits a summary as `daily/YYYY-MM-DD_top10_corp.md` to this repo. Since it runs in the cloud against this repo (not on the local machine), pull to see the latest:

```bash
git pull
```

## Source

Full original idea: [gist.github.com/karpathy/442a6bf555914893e9891c11519de94f](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
