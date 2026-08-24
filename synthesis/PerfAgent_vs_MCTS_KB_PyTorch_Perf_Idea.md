# PerfAgent vs. Hui's MCTS + self-evolving-KB idea for PyTorch performance optimization

Comparison written 2026-08-24, after reading [PerfAgent](../concepts/PerfAgent_2607_19653.md)'s abstract against Hui's candidate PhD thesis-direction idea (tracked outside this repo, in Claude's auto-memory as `project-thesis-directions-2026`, 2026-08-19 entry): *"PyTorch performance optimization framed as search over an LLM-curated knowledge base, pruned by MCTS."*

## The idea, restated

An auto-research agent builds a structured, self-evolving knowledge base of optimization strategies (trigger condition / transformation / expected effect / verification method) mined from docs, GitHub issues/PRs, papers, and the project's own profiling/failure traces. MCTS then treats optimization sequences as a tree — state = current code/graph, action = a KB-retrieved strategy, reward = measured speedup with correctness as a hard pruning constraint — using cheap proxy rollouts plus real profiling for final validation.

## Where the two overlap

Both frame performance optimization as an agentic loop gated by a hard correctness constraint, with profiling as the primary evidence used to decide what to optimize next rather than trusting the agent's instincts.

## Where they diverge — not a strict subset in either direction

**PerfAgent is broader on target domain:** it optimizes arbitrary repository-level code (evaluated on GSO and SWE-efficiency-Lite, general software engineering benchmarks), not ML-specific. Hui's idea is scoped to PyTorch performance optimization specifically — a vertical.

**Hui's idea is broader on search mechanism:** PerfAgent's "loop controller" is single-chain iterative refinement — it resubmits, rebuilds, and re-profiles along one line of attempts, keeping the best correct patch seen so far. It does not branch. Hui's MCTS formulation is an explicit tree search that can systematically explore multiple candidate strategies per state rather than committing to one line and retrying, which in principle covers more of the optimization-strategy space per unit of compute.

**Hui's idea is broader on knowledge use:** PerfAgent supplies no external knowledge base — it relies entirely on the underlying off-the-shelf agent's pretrained knowledge plus the profiler's hotspot summaries each round. Hui's idea adds a structured, self-evolving KB explicitly mined from docs/issues/PRs/papers/failure traces, which is a mechanism PerfAgent has no equivalent of, and which directly exercises the "LLMs' knowledge goes stale re: new package versions/APIs" theme that recurs across Hui's advisor meetings (per `project-thesis-directions-2026`).

## Why this matters for the thesis

PerfAgent is the closest existing published baseline for this thesis direction as of 2026-08-24. If this idea becomes a paper, the related-work section needs an explicit differentiation argument on exactly the two axes above:
1. Branching MCTS search vs. PerfAgent's single-chain retry loop — argue for better coverage of the optimization-strategy space.
2. A reusable, self-evolving structured KB vs. relying on the base agent's static pretrained knowledge — argue for better cross-project generalization and resistance to API/package staleness.

This comparison also gives a natural empirical hook: PerfAgent could be run as a baseline on a PyTorch-specific benchmark subset to quantify the gap the MCTS+KB approach is meant to close, rather than just arguing it qualitatively.

## See also

- [PerfAgent paper summary](../concepts/PerfAgent_2607_19653.md)
