# Candidate repos for the agent-migration study (100 selected)

Built 2026-10-15 for the first study of [Infeasibility-aware agents](Infeasibility_Aware_Agents_Fail_Fast_Idea.md). The candidates are **published papers (peer-reviewed, 2022–2026) with a public PyTorch repo that modifies or fine-tunes a foundation model**, and whose experiments are feasible with base models ≤1.5B on a single 16 GB v5e chip. Less famous work is preferred: 96 of the 100 have under 1k stars. Repos with CUDA-specific code are deliberately **kept**, because they are the study's core cases for infeasibility.

Full data for all 148 screened repos (100 selected plus 48 in reserve), with every field and the raw scan counts: [data/infeasibility_migration_candidates.csv](data/infeasibility_migration_candidates.csv). The scan script is [data/scan_repos.py](data/scan_repos.py).

## How the list was built

1. **Collection.** Four parallel search agents, one per slice: LM PEFT, LM efficiency/compression, LM post-training (alignment/editing/unlearning/merging/steering/continual/instruction) and vision/VLM/diffusion plus LM architecture/inference. They excluded the famous repos already on the pilot list (LoRA, QLoRA, DoRA, GaLore, PiSSA, AdaLoRA, ReFT, LongLoRA, MeZO, DPO, GPTQ, SparseGPT, Wanda, CoOp, Medusa, EAGLE, StreamingLLM, ...).
2. **Repo checks.** Every repo was checked with `gh api` for stars, last push, license and archived status. Dependencies were read from requirements/setup/environment files.
3. **Static scan.** Every repo was shallow-cloned and scanned with a single regex script over `.py` files plus a count of `.cu` files. Vendored library copies (transformers, peft, lm_eval, deepspeed, dassl, ...) are excluded from the counts and recorded separately. Categories:
   - `cuda_ext`: cpp_extension, triton, flash_attn, xformers, bitsandbytes, apex, auto-gptq, vllm, cupy
   - `linalg`: torch.linalg, svd, cholesky, inverse, eig/eigh, qr, pinv, solve
   - `dyn`: nonzero, masked_select, unique, single-argument torch.where, argwhere, nms
   - `dist`: deepspeed, FSDP, DDP, accelerate, torch.distributed

   Host-sync calls (`.item()`/`.cpu()`) and raw CUDA calls (`.cuda()`) appear in almost every repo, so they are recorded in the CSV but not used for stratification.
4. **Primary challenge.** The first matching label in this precedence order: CUDA ext/kernel > Linear algebra > Dynamic shape > Distributed framework > Pure PyTorch.
5. **Selection.** Domain quotas: PEFT 25, Efficiency 25, Post-training 25, Vision 14, Arch/Inference 11. Within each domain, repos were taken by round-robin over the primary-challenge labels, preferring a lower penalty. A penalty point was given for each of:
   - small config only "likely" (the paper uses 7B+)
   - torch pinned at ≤1.9
   - archived repo
   - extremely large codebase

**Resulting challenge mix:** CUDA ext/kernel 33, Dynamic shape 19, Linear algebra 17, Distributed framework 16, Pure PyTorch 15.

## Caveats (read before using)

- **The static label is a prior, not ground truth.**
  - A regex hit does not mean the code path actually runs. For example, `bitsandbytes` is often an optional import.
  - Whether an op actually lacks an XLA lowering only shows up at run time, in L2 `metrics_report`.
  - Comparing the static prior against the measured outcome is itself a planned analysis.
- **Venues** were confirmed by web search for only a subset of papers. The rest came from repo READMEs or the search agents' knowledge. Re-verify a venue before citing it.
- **"likely" small config:** 18 of the 100 papers only ran 7B-class models. The methods look size-agnostic, but small-model runs are untested. Some of these need code changes (for example, a Llama-specific wrapper).
- **Contamination check:** no selected repo is an actual TPU port. The `torch_xla` references found are guarded TPU branches inside copied HF Trainer code. One candidate (ESD, `rohitgandikota/erasing`) was **dropped** because its requirements already pin `torch_xla`.
- **Licenses:** 39 of the 100 have no license file or an unclear one (NOASSERTION). Check each before redistributing any derived artifacts.
- **Environment confound:** several repos pin old torch or ship forked transformers. The plan is to pre-build a CPU-working environment so the agent's task is only the TPU migration.

## Selected 100

### LM PEFT (25)

| # | Method | Venue | Repo | ★ | Static primary challenge | Scan flags (hit counts) | Small cfg |
|---|---|---|---|---|---|---|---|
| 1 | HiRA | ICLR 2025 | [hqsiswiliam/hira](https://github.com/hqsiswiliam/hira) | 37 | CUDA ext/kernel | cuda-ext:5 linalg:1 dist:19 | likely |
| 2 | Late Prompt Tuning | Findings of EMNLP 2022 | [xyltt/LPT](https://github.com/xyltt/LPT) | 12 | CUDA ext/kernel | cuda-ext:14 dist:14 | yes |
| 3 | LoRA+ | ICML 2024 | [nikhil-ghosh-berkeley/loraplus](https://github.com/nikhil-ghosh-berkeley/loraplus) | 234 | CUDA ext/kernel | cuda-ext:3 dyn:1 | yes |
| 4 | LoRETTA | NAACL 2024 | [yifanycc/loretta](https://github.com/yifanycc/loretta) | 40 | CUDA ext/kernel | cuda-ext:48 dyn:1 dist:45 | yes |
| 5 | MELoRA | ACL 2024 | [ChasonShi/MELoRA](https://github.com/ChasonShi/MELoRA) | 33 | CUDA ext/kernel | cuda-ext:11 dyn:1 vendored:peft | yes |
| 6 | NOLA | ICLR 2024 | [UCDvision/NOLA](https://github.com/UCDvision/NOLA) | 60 | CUDA ext/kernel | cuda-ext:10 dyn:2 dist:14 vendored:peft | yes |
| 7 | P-Tuning v2 | ACL 2022 | [THUDM/P-tuning-v2](https://github.com/THUDM/P-tuning-v2) | 2077 | CUDA ext/kernel | cuda-ext:10 dyn:6 dist:22 | yes |
| 8 | RandLoRA | ICLR 2025 | [PaulAlbert31/RandLoRA](https://github.com/PaulAlbert31/RandLoRA) | 32 | CUDA ext/kernel | cuda-ext:14 linalg:2 dyn:1 dist:9 vendored:peft+transformers | likely |
| 9 | RoSA | ICML 2024 | [IST-DASLab/RoSA](https://github.com/IST-DASLab/RoSA) | 46 | CUDA ext/kernel | cuda-ext:7 linalg:14 dist:41 | likely |
| 10 | SMoP | Findings of EMNLP 2023 | [jyjohnchoi/SMoP](https://github.com/jyjohnchoi/SMoP) | 9 | CUDA ext/kernel | cuda-ext:4 dist:11 | yes |
| 11 | SoRA | EMNLP 2023 | [TsinghuaC3I/SoRA](https://github.com/TsinghuaC3I/SoRA) | 87 | CUDA ext/kernel | cuda-ext:1 dyn:4 dist:24 | yes |
| 12 | Spectral Adapter | NeurIPS 2024 | [pilancilab/spectral_adapter](https://github.com/pilancilab/spectral_adapter) | 12 | CUDA ext/kernel | cuda-ext:53 linalg:13 dist:81 vendored:lm_eval+peft | yes |
| 13 | SVFT | NeurIPS 2024 | [VijayLingam95/SVFT](https://github.com/VijayLingam95/SVFT) | 35 | CUDA ext/kernel | cuda-ext:3 linalg:3 dist:2 vendored:peft | yes |
| 14 | DePT | ICLR 2024 | [ZhengxiangShi/DePT](https://github.com/ZhengxiangShi/DePT) | 101 | Distributed framework | dist:1 vendored:peft | yes |
| 15 | ATTEMPT | EMNLP 2022 | [AkariAsai/ATTEMPT](https://github.com/AkariAsai/ATTEMPT) | 104 | Dynamic shape | dyn:1 dist:5 | yes |
| 16 | LoraHub | CoLM 2024 | [sail-sg/lorahub](https://github.com/sail-sg/lorahub) | 669 | Dynamic shape | dyn:1 | yes |
| 17 | Prefix-Propagation | ACL 2023 | [MonliH/prefix-propagation](https://github.com/MonliH/prefix-propagation) | 7 | Dynamic shape | dyn:18 dist:13 | yes |
| 18 | SparseAdapter | Findings of EMNLP 2022 | [Shwai-He/SparseAdapter](https://github.com/Shwai-He/SparseAdapter) | 23 | Dynamic shape | dyn:3 dist:6 vendored:transformers | yes |
| 19 | UniPELT | ACL 2022 | [morningmoni/UniPELT](https://github.com/morningmoni/UniPELT) | 64 | Dynamic shape | dyn:1 vendored:transformers | yes |
| 20 | BLoB | NeurIPS 2024 | [Wang-ML-Lab/bayesian-peft](https://github.com/Wang-ML-Lab/bayesian-peft) | 42 | Linear algebra | linalg:4 dist:3 | likely |
| 21 | Laplace-LoRA | ICLR 2024 | [adamxyang/laplace-lora](https://github.com/adamxyang/laplace-lora) | 29 | Linear algebra | linalg:21 dyn:3 dist:13 | likely |
| 22 | S2FT | NeurIPS 2024 | [Infini-AI-Lab/S2FT](https://github.com/Infini-AI-Lab/S2FT) | 19 | Linear algebra | linalg:1 dist:30 | likely |
| 23 | BitFit | ACL 2022 | [benzakenelad/BitFit](https://github.com/benzakenelad/BitFit) | 143 | Pure PyTorch |  | yes |
| 24 | DeLoRA | ICLR 2025 | [ExplainableML/DeLoRA](https://github.com/ExplainableML/DeLoRA) | 15 | Pure PyTorch | vendored:peft | likely |
| 25 | Residual Prompt Tuning | Findings of ACL 2023 | [arazd/ResidualPrompts](https://github.com/arazd/ResidualPrompts) | 56 | Pure PyTorch |  | yes |

### LM Efficiency/Compression (25)

| # | Method | Venue | Repo | ★ | Static primary challenge | Scan flags (hit counts) | Small cfg |
|---|---|---|---|---|---|---|---|
| 26 | Flora | ICML 2024 | [BorealisAI/flora-opt](https://github.com/BorealisAI/flora-opt) | 108 | CUDA ext/kernel | cuda-ext:2 linalg:1 dist:4 | yes |
| 27 | GoLore | ICML 2025 | [pkumelon/Golore](https://github.com/pkumelon/Golore) | 9 | CUDA ext/kernel | cuda-ext:23 linalg:20 dyn:3 dist:55 | yes |
| 28 | HiZOO | ICLR 2025 | [Yanjun-Zhao/HiZOO](https://github.com/Yanjun-Zhao/HiZOO) | 28 | CUDA ext/kernel | cuda-ext:2 dist:16 | yes |
| 29 | LQ-LoRA | ICLR 2024 | [HanGuo97/lq-lora](https://github.com/HanGuo97/lq-lora) | 130 | CUDA ext/kernel | cuda-ext:11 linalg:19 dyn:6 dist:1 | yes |
| 30 | MetaDistil | ACL 2022 | [JetRunner/MetaDistil](https://github.com/JetRunner/MetaDistil) | 87 | CUDA ext/kernel | cuda-ext:7 linalg:3 dist:15 | yes |
| 31 | SLTrain | NeurIPS 2024 | [andyjm3/SLTrain](https://github.com/andyjm3/SLTrain) | 39 | CUDA ext/kernel | cuda-ext:5 dist:2 | yes |
| 32 | VeLoRA | NeurIPS 2024 | [roymiles/VeLoRA](https://github.com/roymiles/VeLoRA) | 22 | CUDA ext/kernel | cuda-ext:2 linalg:3 dyn:1 dist:2 | yes |
| 33 | ZO-Bench (ZO-SGD/ZO-Adam/forward-grad) | ICML 2024 | [ZO-Bench/ZO-LLM](https://github.com/ZO-Bench/ZO-LLM) | 130 | CUDA ext/kernel | cuda-ext:8 dyn:2 dist:37 | yes |
| 34 | DistiLLM | ICML 2024 | [jongwooko/distillm](https://github.com/jongwooko/distillm) | 269 | Distributed framework | dist:36 | yes |
| 35 | LOMO / AdaLomo | ACL 2024 | [OpenLMLab/LOMO](https://github.com/OpenLMLab/LOMO) | 993 | Distributed framework | dist:67 | likely |
| 36 | CoFi | ACL 2022 | [princeton-nlp/CoFiPruning](https://github.com/princeton-nlp/CoFiPruning) | 198 | Dynamic shape | dyn:4 dist:1 | yes |
| 37 | DSKD | EMNLP 2024 | [songmzhang/DSKD](https://github.com/songmzhang/DSKD) | 65 | Dynamic shape | dyn:4 dist:21 | yes |
| 38 | Outlier Suppression | NeurIPS 2022 | [wimh966/outlier_suppression](https://github.com/wimh966/outlier_suppression) | 50 | Dynamic shape | dyn:3 | yes |
| 39 | Outlier Suppression+ | EMNLP 2023 | [ModelTC/Outlier_Suppression_Plus](https://github.com/ModelTC/Outlier_Suppression_Plus) | 52 | Dynamic shape | dyn:2 dist:1 vendored:lm_eval | yes |
| 40 | SIFT | ICML 2024 | [song-wx/SIFT](https://github.com/song-wx/SIFT) | 24 | Dynamic shape | dyn:1 | yes |
| 41 | Task-aware layerwise distillation (TED) | ICML 2023 | [cliang1453/task-aware-distillation](https://github.com/cliang1453/task-aware-distillation) | 41 | Dynamic shape | dyn:4 dist:18 | yes |
| 42 | ALPS | NeurIPS 2024 | [mazumder-lab/ALPS](https://github.com/mazumder-lab/ALPS) | 5 | Linear algebra | linalg:2 dyn:2 | yes |
| 43 | BiLLM | ICML 2024 | [Aaronhuang-778/BiLLM](https://github.com/Aaronhuang-778/BiLLM) | 238 | Linear algebra | linalg:5 | yes |
| 44 | LoSparse | ICML 2023 | [yxli2123/LoSparse](https://github.com/yxli2123/LoSparse) | 64 | Linear algebra | linalg:2 dyn:3 dist:12 | yes |
| 45 | OBC / ExactOBS | NeurIPS 2022 | [IST-DASLab/OBC](https://github.com/IST-DASLab/OBC) | 136 | Linear algebra | linalg:9 dyn:1 | yes |
| 46 | PB-LLM | ICLR 2024 | [hahnyuan/PB-LLM](https://github.com/hahnyuan/PB-LLM) | 159 | Linear algebra | linalg:5 dyn:1 | yes |
| 47 | SliceGPT | ICLR 2024 | [microsoft/TransformerCompression](https://github.com/microsoft/TransformerCompression) | 463 | Linear algebra | linalg:3 dist:2 | yes |
| 48 | SparseLLM | NeurIPS 2024 | [BaiTheBest/SparseLLM](https://github.com/BaiTheBest/SparseLLM) | 71 | Linear algebra | linalg:15 | yes |
| 49 | BiBERT | ICLR 2022 | [AI-Efficiency/BiBERT](https://github.com/AI-Efficiency/BiBERT) | 89 | Pure PyTorch |  | yes |
| 50 | SmoothQuant | ICML 2023 | [mit-han-lab/smoothquant](https://github.com/mit-han-lab/smoothquant) | 1698 | Pure PyTorch |  | yes |

### LM Post-training (25)

| # | Method | Venue | Repo | ★ | Static primary challenge | Scan flags (hit counts) | Small cfg |
|---|---|---|---|---|---|---|---|
| 51 | DARE | ICML 2024 | [yule-BUAA/MergeLM](https://github.com/yule-BUAA/MergeLM) | 878 | CUDA ext/kernel | cuda-ext:2 linalg:1 dyn:2 | yes |
| 52 | Instruction Modelling | NeurIPS 2024 | [ZhengxiangShi/InstructionModelling](https://github.com/ZhengxiangShi/InstructionModelling) | 38 | CUDA ext/kernel | cuda-ext:41 dist:30 | likely |
| 53 | MELO | AAAI 2024 | [ECNU-ICALK/MELO](https://github.com/ECNU-ICALK/MELO) | 28 | CUDA ext/kernel | cuda-ext:4 vendored:peft | yes |
| 54 | SimNPO | NeurIPS 2025 | [OPTML-Group/Unlearn-Simple](https://github.com/OPTML-Group/Unlearn-Simple) | 47 | CUDA ext/kernel | cuda-ext:1 dist:19 | likely |
| 55 | SOUL | EMNLP 2024 | [OPTML-Group/SOUL](https://github.com/OPTML-Group/SOUL) | 31 | CUDA ext/kernel | cuda-ext:5 dist:11 vendored:lm_eval | likely |
| 56 | beta-DPO | NeurIPS 2024 | [junkangwu/beta-DPO](https://github.com/junkangwu/beta-DPO) | 52 | Distributed framework | dist:32 | yes |
| 57 | Knowledge Unlearning | ACL 2023 | [joeljang/knowledge-unlearning](https://github.com/joeljang/knowledge-unlearning) | 87 | Distributed framework | dist:5 | yes |
| 58 | LLM Unlearn | NeurIPS 2024 | [kevinyaobytedance/llm_unlearn](https://github.com/kevinyaobytedance/llm_unlearn) | 188 | Distributed framework | dist:1 | yes |
| 59 | O-LoRA | Findings of EMNLP 2023 | [cmnfriend/O-LoRA](https://github.com/cmnfriend/O-LoRA) | 217 | Distributed framework | dist:9 vendored:peft | yes |
| 60 | TDPO | ICML 2024 | [Vance0124/Token-level-Direct-Preference-Optimization](https://github.com/Vance0124/Token-level-Direct-Preference-Optimization) | 155 | Distributed framework | dist:32 | yes |
| 61 | TOFU | CoLM 2024 | [locuslab/tofu](https://github.com/locuslab/tofu) | 29 | Distributed framework | dist:8 | yes |
| 62 | EUL | EMNLP 2023 | [SALT-NLP/Efficient_Unlearning](https://github.com/SALT-NLP/Efficient_Unlearning) | 37 | Dynamic shape | dyn:1 dist:10 vendored:transformers | yes |
| 63 | f-DPO | ICLR 2024 | [alecwangcq/f-divergence-dpo](https://github.com/alecwangcq/f-divergence-dpo) | 17 | Dynamic shape | dyn:2 dist:32 | yes |
| 64 | NPO | CoLM 2024 | [licong-lin/negative-preference-optimization](https://github.com/licong-lin/negative-preference-optimization) | 78 | Dynamic shape | dyn:1 dist:8 | likely |
| 65 | Progressive Prompts | ICLR 2023 | [arazd/ProgressivePrompts](https://github.com/arazd/ProgressivePrompts) | 97 | Dynamic shape | dyn:1 | yes |
| 66 | SERAC | ICML 2022 | [eric-mitchell/serac](https://github.com/eric-mitchell/serac) | 72 | Dynamic shape | dyn:1 | yes |
| 67 | EMMET | Findings of EMNLP 2024 | [scalable-model-editing/unified-model-editing](https://github.com/scalable-model-editing/unified-model-editing) | 28 | Linear algebra | linalg:21 dyn:1 | yes |
| 68 | LM-Steer | ACL 2024 | [Glaciohound/LM-Steer](https://github.com/Glaciohound/LM-Steer) | 151 | Linear algebra | linalg:8 | yes |
| 69 | MALMEN | ICLR 2024 | [ChenmienTan/malmen](https://github.com/ChenmienTan/malmen) | 38 | Linear algebra | linalg:4 dyn:3 | yes |
| 70 | PCB-Merging | NeurIPS 2024 | [duguodong7/pcb-merging](https://github.com/duguodong7/pcb-merging) | 48 | Linear algebra | linalg:1 dyn:1 dist:4 | yes |
| 71 | TIES-Merging | NeurIPS 2023 | [prateeky2806/ties-merging](https://github.com/prateeky2806/ties-merging) | 224 | Linear algebra | linalg:1 dyn:1 dist:4 | yes |
| 72 | GRACE | NeurIPS 2023 | [Thartvigsen/GRACE](https://github.com/Thartvigsen/GRACE) | 85 | Pure PyTorch |  | yes |
| 73 | ITI | NeurIPS 2023 | [likenneth/honest_llama](https://github.com/likenneth/honest_llama) | 587 | Pure PyTorch |  | likely |
| 74 | MEND | ICLR 2022 | [eric-mitchell/mend](https://github.com/eric-mitchell/mend) | 259 | Pure PyTorch |  | yes |
| 75 | Superfiltering | ACL 2024 | [tianyi-lab/Superfiltering](https://github.com/tianyi-lab/Superfiltering) | 190 | Pure PyTorch |  | likely |

### Vision/VLM/Diffusion (14)

| # | Method | Venue | Repo | ★ | Static primary challenge | Scan flags (hit counts) | Small cfg |
|---|---|---|---|---|---|---|---|
| 76 | DDPO | ICLR 2024 | [kvablack/ddpo-pytorch](https://github.com/kvablack/ddpo-pytorch) | 775 | CUDA ext/kernel | cuda-ext:5 linalg:1 dyn:1 dist:3 | yes |
| 77 | H-SAM | CVPR 2024 | [Cccccczh404/H-SAM](https://github.com/Cccccczh404/H-SAM) | 138 | CUDA ext/kernel | cuda-ext:1 dyn:7 dist:6 | yes |
| 78 | SSF | NeurIPS 2022 | [dongzelian/SSF](https://github.com/dongzelian/SSF) | 200 | CUDA ext/kernel | cuda-ext:17 dist:8 | yes |
| 79 | AdaptFormer | NeurIPS 2022 | [ShoufaChen/AdaptFormer](https://github.com/ShoufaChen/AdaptFormer) | 391 | Distributed framework | dist:7 | yes |
| 80 | E2VPT | ICCV 2023 | [ChengHan111/E2VPT](https://github.com/ChengHan111/E2VPT) | 73 | Distributed framework | dist:9 | yes |
| 81 | VPT | ECCV 2022 | [KMnP/vpt](https://github.com/KMnP/vpt) | 1247 | Distributed framework | dist:9 | yes |
| 82 | KgCoOp | CVPR 2023 | [htyao89/KgCoOp](https://github.com/htyao89/KgCoOp) | 110 | Dynamic shape | dyn:6 vendored:dassl | yes |
| 83 | MaPLe | CVPR 2023 | [muzairkhattak/multimodal-prompt-learning](https://github.com/muzairkhattak/multimodal-prompt-learning) | 823 | Dynamic shape | dyn:1 | yes |
| 84 | PromptSRC | ICCV 2023 | [muzairkhattak/PromptSRC](https://github.com/muzairkhattak/PromptSRC) | 290 | Dynamic shape | dyn:1 | yes |
| 85 | Concept Ablation | ICCV 2023 | [nupurkmr9/concept-ablation](https://github.com/nupurkmr9/concept-ablation) | 170 | Linear algebra | linalg:1 dyn:2 | likely |
| 86 | UCE | WACV 2024 | [rohitgandikota/unified-concept-editing](https://github.com/rohitgandikota/unified-concept-editing) | 193 | Linear algebra | linalg:5 | yes |
| 87 | TDA | CVPR 2024 | [kdiAAA/TDA](https://github.com/kdiAAA/TDA) | 125 | Pure PyTorch |  | yes |
| 88 | Tip-Adapter | ECCV 2022 | [gaopengcuhk/Tip-Adapter](https://github.com/gaopengcuhk/Tip-Adapter) | 679 | Pure PyTorch |  | yes |
| 89 | TPT | NeurIPS 2022 | [azshue/TPT](https://github.com/azshue/TPT) | 217 | Pure PyTorch |  | yes |

### LM Arch/Inference (11)

| # | Method | Venue | Repo | ★ | Static primary challenge | Scan flags (hit counts) | Small cfg |
|---|---|---|---|---|---|---|---|
| 90 | BiLD | NeurIPS 2023 | [kssteven418/BigLittleDecoder](https://github.com/kssteven418/BigLittleDecoder) | 99 | CUDA ext/kernel | cuda-ext:132 linalg:2 dyn:58 dist:170 vendored:transformers | yes |
| 91 | Contrastive Decoding | ACL 2023 | [XiangLi1999/ContrastiveDecoding](https://github.com/XiangLi1999/ContrastiveDecoding) | 206 | CUDA ext/kernel | cuda-ext:1 vendored:transformers | yes |
| 92 | LESS | ICML 2024 | [hdong920/LESS](https://github.com/hdong920/LESS) | 53 | CUDA ext/kernel | cuda-ext:1 vendored:lm_eval | likely |
| 93 | LTMP | TMLR 2023 | [Mxbonn/ltmp](https://github.com/Mxbonn/ltmp) | 17 | CUDA ext/kernel | cuda-ext:15 dist:4 vendored:timm | yes |
| 94 | DiffRate | ICCV 2023 | [OpenGVLab/DiffRate](https://github.com/OpenGVLab/DiffRate) | 103 | Distributed framework | dist:8 | yes |
| 95 | FREE | EMNLP 2023 | [raymin0223/fast_robust_early_exit](https://github.com/raymin0223/fast_robust_early_exit) | 67 | Distributed framework | dist:17 | yes |
| 96 | LayerSkip | ACL 2024 | [facebookresearch/LayerSkip](https://github.com/facebookresearch/LayerSkip) | 379 | Distributed framework | dist:1 | yes |
| 97 | MCTF | CVPR 2024 | [mlvlab/MCTF](https://github.com/mlvlab/MCTF) | 40 | Distributed framework | dist:8 | yes |
| 98 | PASTA | ICLR 2024 | [QingruZhang/PASTA](https://github.com/QingruZhang/PASTA) | 142 | Pure PyTorch |  | likely |
| 99 | ToMe | ICLR 2023 | [facebookresearch/ToMe](https://github.com/facebookresearch/ToMe) | 1204 | Pure PyTorch |  | yes |
| 100 | TOVA | EMNLP 2024 | [schwartz-lab-NLP/TOVA](https://github.com/schwartz-lab-NLP/TOVA) | 129 | Pure PyTorch |  | likely |

## Reserve (48, in the CSV)

(IA)3 / T-Few, AdaMix, AutoPEFT, CorDA, DyLoRA, HydraLoRA, Ladder Side-Tuning, LoRA-GA, LoRA-Pro, LoRAPrune, MAM Adapter (unified view), QA-LoRA, VB-LoRA, Adam-mini, APOLLO, BAdam, BiT, LoftQ, OmniQuant, PLATON, ReLoRA, Retraining-free pruning, SpinQuant, SVD-LLM, DSnoT, OWL, Function Vectors, KTO (HALOs), RegMean, CAA, ContinualLM (DAS), LFPT5, NEFTune, ORPO, AlphaEdit, ICV, LEACE, MEMIT, PMET, SEA, Custom Diffusion, OFT, PerSAM, DoLa, MoEfication, PoSE, Self-Extend, EViT

## See also

- [Infeasibility-aware agents idea and study design](Infeasibility_Aware_Agents_Fail_Fast_Idea.md)
