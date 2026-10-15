# Infeasibility-aware agents: detecting "this cannot be done" and failing fast

Candidate research idea, first written down 2026-10-15 from a conversation with Hui. It has a novelty check (literature search run the same day). Target venue: ICSE-NIER (minimal version) or FSE 2027 (full version). It is a sibling of the thesis directions tracked in Claude's auto-memory as `project-thesis-directions-2026`, especially "hardware-constraint-level migration eval".

## The idea

Self-evolving agents (Reflexion / ExpeL style reflection and memory, built on top of a ReAct loop) mostly accumulate **positive** knowledge: "when X happens, do Y". The idea is for the agent to also detect, and remember, **what cannot be done**, so it can fail fast instead of spending its budget or reporting false success. This amounts to estimating where the agent's capability ends, conditioned on the task.

**Motivating example: PyTorch → TPU migration via PyTorch/XLA.** Some work is infeasible because of the target platform, not because the agent is weak:

| Level | Example | What happens |
|---|---|---|
| Hard infeasible | Custom CUDA kernels; cuDNN/Triton-dependent extensions | Cannot run; needs a rewrite (e.g. Pallas) |
| Soft infeasible | `aten` ops with no XLA lowering | Runs, but **silently falls back to CPU** (graph break plus device↔host copies); tests still pass |
| Structural conflict | Dynamic-shape ops (`nonzero`, `masked_select`, `unique`, ...) | Recompilation storms, or a rewrite to padding/masking |
| Fixable | `.item()` calls, Python control flow on tensor values | The agent can fix it |

**Key point:** "tests pass" ≠ "migration succeeded". An agent can declare success while ops run on the CPU.

## Design points

1. **Failure attribution.** Distinguish these causes of failure:
   - agent capability limit
   - stochastic bad luck (a retry would pass)
   - budget too small
   - environment/tooling problem
   - true task infeasibility

   Only capability limits and true infeasibility should become fail-fast rules. Otherwise the agent learns helplessness.
2. **Automatic infeasibility oracle.** Labels can be read programmatically, so they cost no human annotation:
   - `torch_xla.debug.metrics.metrics_report()` exposes `aten::*` CPU-fallback counters
   - compile counts / CompileTime show recompilation
3. **Boundaries move.** A newer torch_xla release can add a lowering, so negative knowledge must be **scoped and versioned** ("infeasible in environment E at version V") and periodically re-validated through exploration retries. Keep two boundaries apart: the *environment* boundary (backend support) and the *agent* boundary (capability).
4. **Incentive risk.** Rewarding fail-fast invites reward hacking: the agent gives up on anything hard. Evaluate it with:
   - abstention precision and recall
   - false-abandon rate
   - cost saved vs. successes lost

## Candidate RQs

- **RQ1:** Across N real PyTorch models/repos migrated to TPU by an agent, what fraction of reported "successes" carry silent `aten::` fallback or recompilation blow-ups?
- **RQ2:** How are migration failures distributed across hard infeasible / soft infeasible / structural / fixable?
- **RQ3 (full paper):** Can early trajectory signals predict infeasibility and abort early? Measure cost saved vs. false abandons, and whether scoped, versioned negative memory helps across tasks.

RQ1 and RQ2 are enough for NIER. RQ3 plus scale is the FSE version.

**Platform risk:** reviewers may question PyTorch/XLA's long-term relevance. Frame the work as "backend constraints", with TPU as the primary case, and add a small check on a second backend (MPS / ROCm / NPU).

## Novelty check (2026-10-15)

Done with web search. Most hits are 2026 arXiv preprints with unconfirmed review status, the full texts were mostly **not read**, and some author names are unverified. **Re-verify each paper before citing it.**

### Already done (the general framing is not novel)
- **General agent abstention / infeasible-task benchmarks:**
  - *Agentic Abstention: Do Agents Know When to Stop Instead of Act?* (arXiv 2606.28733). In its environment-based abstention setting, infeasibility is discovered only during interaction. Agents abstain late or never (timely recall < 40%). Its CONVOLVE method distills trajectories into reusable stopping rules.
  - *AgentAbstain* (arXiv 2607.10059)
  - *Do Agents Know What They Can't Do?* / FeasiGen (Cheng et al., arXiv 2605.28532). Infeasibility comes from masking tools; the false-continue rate is up to 73.9%.
  - The OSWorld infeasible subset
  - MIRAGE-Bench (arXiv 2507.21017)
- **Early failure prediction for SWE agents:**
  - *EarlyEval* (arXiv 2609.02783)
  - *Fail-Fast, Restart-Smart* (arXiv 2608.03222)
  - *Before the Rollout Ends* (arXiv 2609.31995)

  All of these predict "this run will fail" and then retry. None separates infeasibility from a capability limit.
- **Negative / failure memory:**
  - *Negative Knowledge as Failure-aware Shared Memory for AutoResearch* (arXiv 2606.21024)
  - ReasoningBank
  - MAGE (arXiv 2605.10064)
  - Reflexion and ExpeL
  - OEP (arXiv 2605.18930) shows that experience which does not transfer gets over-generalized into harmful rules. This supports the staleness and scoping concern.
- **False success / impossible coding tasks:**
  - *ImpossibleBench* (Zhong, Raghunathan, Carlini, ICLR 2026). Spec and tests contradict, so any pass is cheating; stronger models cheat more.
  - *From Confident Closing to Silent Failure* (arXiv 2606.09863). False success reaches 75.8% on AppWorld.
  - *Confident and Wrong* (Mehta, arXiv 2603.25764)
- **LLM ML-framework migration:**
  - T2J (arXiv 2510.09898)
  - T2J-Bench (arXiv 2605.29054), 63 repo-level PyTorch→JAX tasks
  - An agentic PyTorch→JAX in-context-learning framework (arXiv 2606.15994)
  - *From PyTorch to the NPU* (arXiv 2609.27249)
  - JAXBench (arXiv 2607.20466)
  - MultiKernelBench (arXiv 2507.17773), where Pallas Pass@1 is about 8% vs. CUDA about 47%
- **Accelerator inconsistency:** *Mind the Gap* (arXiv 2511.11601) notes that silent CPU fallback hides unimplemented ops, but it studies Mac and Huawei devices, not TPU.

### Open, as far as the search found
1. **Infeasibility that arises naturally from the environment and depends on the backend** in SE/migration tasks. Prior work makes infeasibility synthetically: masked tools, edited environments, contradictory specs.
2. **Automatic execution-telemetry oracles** (XLA `aten::` fallback counters, compile counts) as ground-truth labels. They make "tests pass" false success measurable. The PyTorch/XLA docs already tell humans to check `metrics_report`, but nobody uses it as a label.
3. **Separating capability limits from true infeasibility.**
4. **Scoped, versioned, expiring negative knowledge** that is re-validated as backends add lowerings. No staleness treatment was found.
5. **No study of PyTorch/XLA silent fallback in agent-driven migration**, and no empirical study of PyTorch/XLA or TPU bugs was found.

### Closest papers to differentiate against
1. Agentic Abstention / CONVOLVE (arXiv 2606.28733)
2. ImpossibleBench (ICLR 2026)
3. FeasiGen (arXiv 2605.28532)

Runner-up on the migration side: T2J-Bench (arXiv 2605.29054).

### Positioning sentence (draft)
> Prior work studies abstention on *synthetically* infeasible tasks (masked tools, contradictory specs) and predicts run-level failure. We study *environment-induced* infeasibility in ML-system migration, where feasibility depends on the backend version. Ground-truth labels come automatically from compiler/runtime telemetry (XLA CPU-fallback and recompilation counters). This exposes false success that test suites cannot catch. It also lets agents separate their own capability limits from true infeasibility, and accumulate, scope and expire negative knowledge as backends evolve.

## Next steps

1. Re-verify the three closest papers, reading the full text, in particular CONVOLVE's stopping rules vs. scoped/versioned negative knowledge.
2. Pilot study: 5–10 PyTorch models, an agent-driven migration to TPU, and a fallback/recompile detection script. Check whether the silent-fallback rate is large enough to carry the story. If it is low, the story does not hold.

## See also

- [PerfAgent vs. MCTS + self-evolving-KB idea](PerfAgent_vs_MCTS_KB_PyTorch_Perf_Idea.md): another self-evolving-KB thesis idea on PyTorch. Its KB stores positive strategies; this idea adds negative, scoped knowledge.
