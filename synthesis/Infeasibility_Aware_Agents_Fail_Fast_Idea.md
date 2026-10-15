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

## First study: design (refined 2026-10-15)

The first study is an empirical one: take **research-paper repos that modify or fine-tune foundation models**, have an off-the-shelf coding agent (e.g. Claude Code) do a **project-level** migration to TPU, and measure how often it truly succeeds. The study does not build a custom agent. A custom agent informed by the failure taxonomy comes later, with the off-the-shelf agents as baselines.

### Scope
- **Target is PyTorch/XLA only.** No rewrite to JAX, and no Pallas/C++ kernels. This gives "infeasible" a crisp definition: *cannot be done at the PyTorch/XLA level without a new kernel or a framework change.* Motivation: researchers want *their paper's PyTorch repo* to run on TPU, not a JAX re-implementation. Many of these methods already exist in JAX, which has to be addressed in the paper (and is a contamination risk).
- **Single v5e chip, base models ≤ 1.5B.** Examples: Qwen2.5-0.5B/1.5B, Llama-3.2-1B, OPT-125M/1.3B, Pythia, GPT-2, RoBERTa, CLIP ViT-B/16. This avoids SPMD.
  - SPMD (Single Program Multiple Data, XLA's GSPMD) means you write a single-device program and annotate tensor shardings (`xs.mark_sharding`), then the compiler partitions the work and inserts the collectives.
  - Moving DDP/FSDP code to SPMD is a change of paradigm. Multi-chip work is therefore deferred to an extension, where 7B inference or LoRA would need v5e-4.
- **Allowed and disallowed agent actions:**

| Action | Allowed? |
|---|---|
| Device/AMP/optimizer changes; removing CUDA-only branches | Yes |
| Replacing a CUDA op with a semantically equivalent pure-PyTorch implementation (e.g. a repo's own `ref` path) | Yes, if it passes L1 |
| Writing Pallas/custom kernels, rewriting in JAX | No. The agent should report infeasible |
| An approximation that changes the method (e.g. QLoRA → plain bf16 LoRA) | No, or flagged separately |

### Success levels (cumulative: a level is evaluated only if the previous one passed)

| Level | Question | Criterion | How measured |
|---|---|---|---|
| **L0 Runs** | Does it run on TPU? | Train/inference steps finish on the XLA device without error | Run the entry script |
| **L1 Numerically correct** | Is the migration logic right? | With the TPU at **highest matmul precision**, outputs and loss are within tolerance of an fp32 reference | Fixed seed. The reference runs on CPU, or on GPU with TF32 disabled (`torch.backends.cuda.matmul.allow_tf32=False`, `torch.backends.cudnn.allow_tf32=False`) |
| **L2 Really on TPU** | Is anything silently falling back to the CPU? | Zero `aten::` fallbacks (or only known-unavoidable ones); bounded recompilation count | `metrics_report()` |
| **L3 Reasonable performance** | Is the migrated efficiency acceptable? | Slowdown within a threshold, measured against a **fallback-free TPU version of the same project**. There is no cross-hardware TPU-vs-GPU comparison | Timing |
| **L4 Paper claim reproduces** | Does the paper's core conclusion still hold on TPU? | At the TPU's **default precision**, a small-scale run reproduces the paper's key trend (e.g. the LoRA vs. full-FT gap, GaLore's memory saving, GPTQ perplexity) | Compare against the conclusion from a GPU reference run |

L1 and L4 deliberately use different precisions:
- L1 uses highest precision to separate migration bugs from bf16 error.
- L4 uses default precision because that is what users actually run, so it shows whether precision drift changes the scientific conclusion.

**Outcome labels outside the levels:**
- **Correctly reported infeasible:** the task truly needs a new kernel or a framework change (e.g. QLoRA's bitsandbytes 4-bit) and the agent stops. This is a positive case of failing fast.
- **Falsely reported infeasible:** a feasible path existed (e.g. the repo ships a pure-PyTorch ref implementation) but the agent gave up.
- **Method silently altered:** it runs, but the method changed. It may pass L0–L3 and is caught at L4. This is a form of false success.
- **Agent-claimed success:** recorded and compared with the level actually reached, to measure the agent's self-assessment bias.

**Headline numbers:**
1. Among agent-claimed successes, the fraction that do not reach L2 or L4 (how severe false success is).
2. Precision and recall of infeasibility reports (how accurate failing fast is).

### Precision constraint: a second kind of silent hardware constraint
- The TPU MXU has no native fp32 multiplier. Per the Cloud TPU bfloat16 docs, "by default, TPUs perform matrix multiplication operations with bfloat16 values and accumulations with IEEE float32 values".
- fp32 storage and non-matmul (VPU) ops are fp32, and higher matmul precision is emulated with multi-pass bf16.
- So fp32 PyTorch code silently gets roughly bf16 matmul precision.
- An agent seeing a numeric mismatch may "fix" correct code, or loosen tolerances to hide the mismatch, which is a false success. Add **precision constraint** as a failure category in RQ2.

### Candidate repos (from memory; verify each before inclusion)
Paper-method repos that modify or fine-tune foundation models, each with its expected migration challenge:

| Method (venue) | Repo | Small config | Expected challenge |
|---|---|---|---|
| LoRA (ICLR'22) | microsoft/LoRA | GPT-2 / RoBERTa | Control group |
| CoOp (IJCV'22) | KaiyangZhou/CoOp | CLIP ViT-B/16 | Control group (vision); depends on the Dassl framework |
| DPO (NeurIPS'23) | eric-mitchell/direct-preference-optimization | Pythia-410M/1B | FSDP training code |
| ReFT (NeurIPS'24) | stanfordnlp/pyreft | Llama-3.2-1B | Hook-based interventions vs. XLA graph tracing |
| QLoRA (NeurIPS'23) | artidoro/qlora | ≤1.5B | **Hard infeasible**: bitsandbytes 4-bit CUDA kernels |
| GaLore (ICML'24) | jiaweizzhao/GaLore | LLaMA 60M–350M on C4 | Periodic SVD (possible fallback); optional bnb 8-bit optimizer |
| PiSSA (NeurIPS'24) | GraphPKU/PiSSA | ≤1.5B | SVD initialization |
| GPTQ (ICLR'23) | IST-DASLab/gptq | OPT-125M | Cholesky plus a quantized-matmul CUDA kernel |
| SparseGPT (ICML'23) / Wanda (ICLR'24) | IST-DASLab/sparsegpt, locuslab/wanda | OPT-125M | Pruning with linear algebra and layer-wise calibration |
| MeZO (NeurIPS'23) | princeton-nlp/MeZO | OPT-125M/1.3B | Replays RNG seeds to regenerate perturbations, so it depends on RNG semantics |
| AdaLoRA (ICLR'23) | QingruZhang/AdaLoRA | DeBERTa / RoBERTa | Dynamic rank allocation; `.item()` |
| Medusa / EAGLE (ICML'24) | FasterDecoding/Medusa, SafeAILab/EAGLE | 7B inference (v5e-4; out of the first study's scope) | Tree speculative decoding, dynamic shapes |
| StreamingLLM (ICLR'24) | mit-han-lab/streaming-llm | ≤1.5B | KV-cache eviction, dynamic shapes |
| LongLoRA (ICLR'24) | dvlab-research/LongLoRA | 7B (large) | flash-attn dependency |

**Suggested pilot (8):** LoRA, CoOp, DPO, QLoRA, GaLore, GPTQ, MeZO, StreamingLLM.

**Expanded list:** a broader set of 100 less-famous candidates (plus 48 in reserve), with a static code scan, is in [Infeasibility_Migration_Candidates.md](Infeasibility_Migration_Candidates.md).

Whether SVD and Cholesky have XLA lowerings in the chosen torch_xla version is unverified. Measure it in the pilot, since it is itself data.

**Setup caveat:** pre-build a CPU-working environment for each repo, so the agent's task is only the TPU migration. torch_xla pins the torch version, so old repos otherwise confound the results with dependency problems.

### Compute plan
- **TPU:** v5e-4, using a single chip for the first study. TRC application pending; Kaggle TPU v5e-8 for the pilot.
- **GPU reference:** **L4 Spot** as the workhorse. It has 24 GB (more than a v5e chip's 16 GB) and is sm89, so it supports flash-attn 2. Use an **A100 40GB** on demand only when needed. Skip the T4: it is sm75 and lacks support for newer CUDA extensions.
- **Rough GCP prices** (us-central1, on-demand, mostly third-party data from early Sept 2026; verify in the pricing calculator): T4 ≈ $0.35/GPU-h (plus the N1 VM), L4 (g2-standard-4) ≈ $0.71/h, A100 40GB ≈ $3.67/h, A100 80GB ≈ $5.07/h, H100/H200 ≈ $10.6–11/GPU-h.
- **Rough budget:** about $100–150, mostly environment debugging.
- **Practical notes:** request GPU quota early (`GPUS_ALL_REGIONS` plus a regional L4 quota). Make scripts resumable per project so Spot preemption is harmless.

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
2. Verify the candidate repos. For each, check whether it still reproduces, its torch version, whether a small-model config exists, its license, and whether pytorch/xla has a similar official example (contamination). Expand to a final set.
3. Write the L0–L4 evaluation harness, especially the L1 dual-precision comparison and the L2 fallback/recompile detection.
4. Pilot on the 8 suggested repos with one off-the-shelf agent. Check whether the gap between agent-claimed success and L2/L4 is large enough to carry the story. If it is small, re-scope.

## See also

- [SEIP 2027 gap verification](SEIP2027_Gap_Verification.md): the 2026-10-15 full-text check, which supersedes the earlier novelty check above where they differ. In particular, TorchTPU goes public on 2026-10-19 and Google's Cloud TPU Nexus must be cited.

- [PerfAgent vs. MCTS + self-evolving-KB idea](PerfAgent_vs_MCTS_KB_PyTorch_Perf_Idea.md): another self-evolving-KB thesis idea on PyTorch. Its KB stores positive strategies; this idea adds negative, scoped knowledge.
- [ML Operators primer](../concepts/ML_Operators_Primer.md): background on ATen vs. HLO operator sets, lowering and CPU fallback.
