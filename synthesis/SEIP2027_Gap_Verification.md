# Gap verification for the ICSE 2027 SEIP paper

**Paper:** "Can Coding Agents Migrate Machine Learning Projects Across Hardware Accelerators?"
**Date:** 2026-10-15. The submission deadline is 2026-10-23 AoE.

**Scope.** This file checks about 60 works:
- every paper in Hui's local folders (`Project_Level_Migration/`, `ML_Migration_Evaluation/`, `ML_Migration_method/`, `Hardware_Migration_Checker/`, `Hardware_In_Migration_Loop/`, `Agent_Early_Stopping/`, `fail_fast_agent_trace/`, plus JAXBench from `ML_Performance_AutoResearch/`)
- every paper discussed in earlier sessions (2026-08-20 discussion notes, the 2026-10-14 SEIP/migration-landscape session, today's session)
- a fresh web sweep (2026-10-15) for anything published Aug–Oct 2026

Six reading agents each read the full text of their group under one shared rubric (`Project_Level_Migration/gap_verification/per_group/SPEC.md` (local, outside this repo)). Per-paper blocks with page-referenced quotes are in `Project_Level_Migration/gap_verification/per_group/` (local), and downloaded PDFs are in `Project_Level_Migration/gap_verification/pdfs/` (local).

---

## 1. Verdict

**The gap claim holds, but only in its precise form.** No work found does all of the following:

1. **agent-driven** migration of an
2. **existing ML project/repository** (training/fine-tuning code, not a single exported inference graph or kernel)
3. **across hardware accelerators** with the framework held fixed,
4. evaluated **systematically** for whether the result is correct, actually executes on the accelerator, and preserves the original work's claims.

The two nearest neighbours each lack one or more of these properties:

| Nearest neighbour | Agent-driven | Project-level | Hardware changes | Systematic evaluation |
|---|---|---|---|---|
| T2J-Bench (2605.29054 v3, Google) | yes | yes | **no**: framework change on one pinned H100; "cross-hardware portability" is an explicit non-goal (p.6) | yes |
| KForge (2606.02963) | yes | **no** (kernels) | yes | yes |
| From PyTorch to the NPU (2609.27249) / AIPC (2604.14661), Qualcomm | yes | **no**: single-model inference graphs via ONNX export | yes | **no**: 2–7 models, self-declared not significant |
| Li et al., XDNA2 NPU (2606.07586) | yes | **no**: builds new LLM inference implementations | yes | **no** |
| Sun et al., weather/ocean → Ascend/DCU (2510.17852) | **no** (manual) | partly (1 model ported) | yes | **no** (case study) |
| **Google Cloud TPU Nexus** (PyTorch Conf NA, 2026-10-20) | yes | likely | **yes (GPU→TPU, PyTorch)** | **no**: sponsored talk, no paper/code/method, one performance ratio |

**Cloud TPU Nexus is the one item that comes close.** It is a product announcement, not prior work, but it must be cited and differentiated (see §4).

---

## 2. What we must NOT claim (each has prior evidence)

| Do not claim | Why | Cite instead |
|---|---|---|
| The area is untouched | Google is publicly presenting an agentic GPU→TPU PyTorch migration system (Cloud TPU Nexus) on 2026-10-20 | Cloud TPU Nexus; Bill Jia keynote "Workload Fungibility in the Age of Agents" (2026-10-21) |
| First to observe agents falsely reporting success | 2609.27249 §5.3.2 (agent reported success while the NPU was inactive); 2606.15994 p.6 ("a false sense of success"); Nikolov et al. 2603.27296 p.8 (agents "declared success despite implementing only a skeleton"); RECLAIM 2609.28850 (128 claimed vs 73 audited reproductions); RepoRescue 2607.01213 | Use those as anecdotal or non-hardware precedents |
| "False success" as our coined term | Defined in Advani, *From Confident Closing to Silent Failure* (ICML 2026 FAGEN workshop, 2606.09863): 45–48% of failures on tau2-bench, 75.8% on AppWorld; LLM judges AUROC ≤ 0.65 | Cite it, and say we extend binary false success to a **graded, hardware-aware** claimed-vs-reached level |
| First to notice silent CPU fallback | Mind the Gap (2511.11601, p.5): operators "silently fall back to CPU implementations without warning", noticed but never counted; 2609.27249: 4 ops fall back on RKNN; AIPC 2604.14661 p.14: Whisper decoder falls back to CPU | "first to **measure** it systematically as a migration outcome" |
| Abstention / infeasibility recognition as new concepts | Agentic Abstention (2606.28733), AgentAbstain (2607.10059), FeasiGen (2605.28532), ImpossibleBench (2510.20270) | Ours is the first with **naturally occurring, hardware-induced** infeasibility; all prior infeasibility is synthetic (deleted files, masked tools, mutated tests) and all-or-nothing |
| T2J-Bench's "26.7–28.9% pass" and "66.6–97.8 pp overestimation" as current numbers | These are in **v2 only**. v3 (posted 2026-10-14, retitled, new first author Tao Feng) removes them: 63 torch-free repo migrations, best reward 0.676 | Cite v2 explicitly by version if we use those numbers, or use the v3 numbers |
| "torch_xla has been deprecated since 2.5" | Wrong. What was deprecated in 2.5 is the old `xm.*` API surface (issue #8000). The README (2026-04-22) says only: "Once TorchTPU is public it will replace PyTorch/XLA." | See §5 |

---

## 3. Claim wording to use

> To the best of our knowledge, no prior work systematically evaluates agent-driven, project-level migration of machine learning research code across hardware accelerators, that is, moving an existing PyTorch project to a different accelerator while keeping its framework, and checking not only whether the result runs but whether it is numerically correct, actually executes on the target hardware, and still reproduces the original work's claims.

### Revised Introduction gap paragraph (draft)

> Existing work leaves this problem largely unexplored. Research on project-level code migration has targeted programming languages and versions, such as C-to-Rust translation [RustRepoTrans, RustPrint], multilingual repository translation [RepoTransBench], Java upgrades [MigrationBench], and LLM-assisted migrations at Google [Ziftci et al.]. Success in these settings is defined by compilation and test outcomes, and the hardware never enters the picture. RepoTransBench even excludes repositories that depend on PyTorch or TensorFlow. Research on ML across hardware, in turn, has operated at three other granularities:
> - **Kernel generation and translation** [KForge, JAXBench, MultiKernelBench, CASS].
> - **Framework translation on fixed hardware.** Examples are TensorFlow-to-JAX [Nikolov et al.] and PyTorch-to-JAX [Liang et al., T2J-Bench]. T2J-Bench explicitly fixes a single GPU "so the choice of device never enters a verdict."
> - **Deployment of exported inference graphs to edge runtimes** [Su et al., AIPC; Li et al.].
>
> Manual case studies [Sun et al.; Yu] document how costly porting to non-GPU accelerators remains. Meanwhile, industry has begun to ship agents for exactly this task: Google recently presented Cloud TPU Nexus, a multi-agent system for GPU-to-TPU PyTorch migration [PyTorch Conference 2026]. It reports only a performance ratio, with no public methodology for judging whether a migrated project is correct. Several studies have observed, anecdotally, that agents report success when the accelerator was never used or operators silently fell back to the CPU [Su et al.; Wen et al.]. None measures these silent hardware constraints systematically. To the best of our knowledge, this is the first study of agent-driven, project-level ML migration across hardware accelerators that evaluates migrations against such constraints.

---

## 4. Must-cite list for the SEIP paper (by role)

**Project-level migration (gap point 1):**
- RustRepoTrans (ASE'25)
- RepoTransBench (TSE'26): §III-B Rule 3 excludes PyTorch/TF repos
- MigrationBench (KDD'26)
- RustPrint (arXiv 2026)
- Ziftci et al., *Migrating Code At Scale With LLMs At Google* (FSE'25 industry): an SEIP-style precedent
- Environment-in-the-Loop (ReCode'26 @ ICSE, 2602.09944): a position paper; "environment" there means library and Docker, never hardware
- ParEval-Repo (ICPP'25, 2506.20938): repo-level CUDA→OpenMP/Kokkos, but on the same A100 and HPC-oriented

**Framework translation (gap point 2a):**
- Nikolov et al. (2603.27296, includes our co-authors Ann Yan and Yaning Liang). TPU appears only as motivation, with no runs on TPU.
- Liang et al. / MaxCode (2606.15994). The first author is **Qiyue** Liang, not our co-author. No TPU runs; the repository level is human-guided.
- T2J-Bench (2605.29054; cite v2 or v3 explicitly). Quote p.26: "the suite fixes a single H100 GPU so the choice of device never enters a verdict."
- T2J (2510.09898, ICML'26 DL4C workshop)
- Daoudi et al. (2511.02610, AIware'26): rule-based, PyTorch↔TF

**Kernel level (gap point 2b):**
- KForge (2606.02963)
- JAXBench (2607.20466). Quote §4: "the correctness bottleneck is information rather than reasoning".
- MultiKernelBench (2507.17773). Pallas compiles at 99.6% (Comp@1) but passes at 8.4% (Pass@1); its tolerance is loose (1e-2) "to accommodate BF16/FP8".
- CASS (2505.16968)
- AMDKernelVault (2609.12471)

**Deployment and case studies (gap point 2c):**
- Su et al., *From PyTorch to the NPU* (2609.27249)
- AIPC (2604.14661)
- Li et al., XDNA2 (2606.07586, MLArchSys@ISCA'26)
- Sun et al. (2510.17852, arXiv; the venue is unverified, the PDF only carries an AAAI-style footer)
- Yu, Ascend field study (2607.08215)

**Silent hardware inconsistency:**
- Mind the Gap (2511.11601)
- Guo et al. (1909.06727; the venue should be ASE'19, verify before citing): silent accuracy drops across platforms
- GraphMend (2509.16248, CGO'27): graph breaks cause eager/CPU fallback and about 5× slowdowns

**Industry context:**
- Cloud TPU Nexus (PyTorch Conf NA 2026-10-20)
- TorchTPU (Google Developers Blog, 2026)
- AWS TorchNeuron ("switch .to('cuda') to .to('neuron') with no rewrite")
- awesome-ascend-skills: Claude Code skills for CUDA→torch_npu, never evaluated

These show that hardware heterogeneity is now the default. The PyTorch blog says "hardware heterogeneity is no longer an edge case, it's the default."

**False success and abstention (RQ2/RQ3):**
- Advani (2606.09863), RECLAIM (2609.28850), RepoRescue (2607.01213)
- ImpossibleBench (2510.20270)
- Agentic Abstention (2606.28733), AgentAbstain (2607.10059), FeasiGen (2605.28532)
- RealTimeDetectRepair (2608.02464): deterministic checks catch 60% of failures with zero false positives. This supports programmatic L2 checks over LLM judges.

**Sustainability (encouraged by the SEIP CFP):**
- ML-EcoLyzer (2511.06694): ESS of 0.09 on CPU vs 1,313 on A100. Silent CPU fallback is therefore an energy cost.

**Methodological precedent:**
- Meganeura (2608.01563) gates forward and backward correctness separately: "an accurate forward pass did not launder a backward disagreement." This supports our cumulative levels.

---

## 5. Decisions needed (they affect the paper this week)

1. **Migration target: PyTorch/XLA vs TorchTPU.** TorchTPU is **not public today**. Its GitHub repo and PyPI package are scheduled to go public on **2026-10-19** (per a PyTorch website issue opened by a Google employee; the PyPI `torch-tpu` package is currently a 0.0.0 placeholder). That is four days before our deadline. PyTorch/XLA is not formally deprecated. Its latest release is 2.9.0 (2025-11-17), and Google Cloud's PyTorch-on-TPU page (updated 2026-10-13) still pins `torch_xla[tpu]~=2.6.0`.
   **Recommendation:** run the study on PyTorch/XLA 2.9.0. Add a timeliness paragraph explaining that our L0–L4 constraint classes (op coverage/CPU fallback, recompilation, precision, kernel rewrites) are stack-agnostic and persist in TorchTPU. Note that TorchTPU has no announced equivalent of the `aten::` fallback counter.
2. **Cloud TPU Nexus and our Google co-authors.** Ask Ann, Yaning and Ivan whether they are involved with, or know the team behind, Cloud TPU Nexus. If they are, it is either a conflict to manage or an industrial context to use (SEIP values exactly that). Either way, re-check for a paper, repo or slides after 2026-10-21, before camera-ready.
3. **Rename our levels.** T2J-Bench v3 uses "L0–L6" for its own grading lattice. To avoid confusion, either rename ours (e.g., "M0–M4" for migration levels, or "H0–H4" for hardware-aware levels) or add an explicit sentence contrasting the two.
4. **T2J-Bench numbers.** Decide between v2 numbers cited by version and the v3 numbers.

---

## 6. Errors found in earlier local notes

`Project_Level_Migration/summary.md` and `detailed_notes.md` contain 12 numbers or attributions that do not match the papers. Examples:
- The RustRepoTrans winning margins belong to DeepSeek-V3, not R1.
- E0609 has 906 occurrences, not 639.
- The DeepSeek-R1 debug score is 62.1%, not 61.2%.
- MigrationBench's 71.67→97.67 is ×1.36, not "nearly doubles".
- The first author is Yanlin Wang, not Yanli Wang.

The full list is in `Project_Level_Migration/gap_verification/per_group/g4_projectlevel.md` (local). Fix these before reusing the notes in the paper.

The memory note from 2026-08-19 ("torch_xla bridge on a deprecation path since 2.5") has been corrected (see §2).

---

## 7. Venue status (verify before citing)

| Status | Papers |
|---|---|
| Peer-reviewed, confirmed | RepoTransBench (TSE'26), MigrationBench (KDD'26), RustRepoTrans (ASE'25), Ziftci et al. (FSE'25 industry), ParEval-Repo (ICPP'25), Environment-in-the-Loop (ReCode'26), Daoudi et al. (AIware'26), GraphMend (CGO'27) |
| Workshop papers | KForge (MLArchSys@ISCA'26), Li et al. XDNA2 (MLArchSys@ISCA'26), T2J (DL4C@ICML'26), Advani (FAGEN@ICML'26) |
| Unconfirmed | Guo et al. 1909.06727 (ASE'19?), Sun et al. 2510.17852 (AAAI footer only), EGG (ICML'26?), ML-EcoLyzer (AAAI'26?), ImpossibleBench (was "under review"). JAXBench's arXiv ID (2607) and its stated date (19 May 2026) do not reconcile. |
| arXiv preprints only | Everything else, including T2J-Bench, MaxCode, 2609.27249, AIPC, Mind the Gap and RECLAIM |
