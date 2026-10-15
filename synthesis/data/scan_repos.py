"""Static scan of candidate repos for TPU/XLA migration challenges.

Usage: python3 -I scan_repos.py <repos_dir> <out_csv>
Each subdirectory of <repos_dir> is a shallow-cloned repo named owner__name.
Counts pattern hits in .py files (plus .cu/.cpp file presence) per category.
"""
import csv, os, re, sys

CATEGORIES = {
    "cuda_ext": [r"cpp_extension", r"\bimport triton\b", r"from triton\b", r"\bflash_attn\b",
                 r"\bxformers\b", r"\bbitsandbytes\b|\bimport bnb\b|\bbnb\.", r"\bapex\b",
                 r"auto_gptq|autogptq", r"\bvllm\b", r"load_inline", r"cupy"],
    "cuda_calls": [r"\.cuda\(", r"torch\.cuda\.amp", r"torch\.cuda\.\w+", r"device\s*=\s*['\"]cuda",
                   r"\bnccl\b", r"torch\.backends\.cudnn"],
    "linalg": [r"torch\.linalg\.\w+", r"torch\.svd\b|\.svd\(", r"cholesky", r"torch\.inverse|\.inverse\(",
               r"\beigh?\b\(", r"torch\.qr|linalg\.qr", r"\.pinverse\(|linalg\.pinv", r"linalg\.solve|triangular_solve"],
    "dynamic_shape": [r"\.nonzero\(|torch\.nonzero", r"masked_select", r"torch\.unique|\.unique\(",
                      r"torch\.where\([^,()]*\)", r"argwhere", r"\bnms\b"],
    "host_sync": [r"\.item\(\)", r"\.cpu\(\)", r"\.numpy\(\)", r"\.tolist\(\)"],
    "distributed": [r"\bdeepspeed\b", r"FullyShardedDataParallel|\bFSDP\b", r"DistributedDataParallel",
                    r"from accelerate|import accelerate", r"torch\.distributed"],
    "xla_already": [r"torch_xla", r"xla_device"],
    "rng": [r"torch\.manual_seed", r"torch\.Generator", r"get_rng_state|set_rng_state", r"torch\.cuda\.manual_seed"],
}
COMPILED = {k: [re.compile(p) for p in v] for k, v in CATEGORIES.items()}
SKIP_DIRS = {".git", "node_modules", "site-packages", "build", "dist"}
# Vendored copies of large libraries: excluded from counts, recorded separately.
VENDORED = {"transformers", "peft", "deepspeed", "diffusers", "accelerate", "fairseq", "timm",
            "megatron", "apex", "detectron2", "mmcv", "dassl", "open_clip", "lm_eval", "trl"}

def scan(repo_dir):
    counts = {k: 0 for k in CATEGORIES}
    n_py = n_cu = py_lines = 0
    vendored = set()
    for root, dirs, files in os.walk(repo_dir):
        for d in dirs:
            if d.lower() in VENDORED and any(
                    os.path.exists(os.path.join(root, d, m)) for m in ("__init__.py", "setup.py", "src")):
                vendored.add(d.lower())
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and d.lower() not in VENDORED]
        for f in files:
            if f.endswith((".cu", ".cuh")):
                n_cu += 1
            if not f.endswith(".py"):
                continue
            n_py += 1
            try:
                text = open(os.path.join(root, f), encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            py_lines += text.count("\n")
            for k, pats in COMPILED.items():
                counts[k] += sum(len(p.findall(text)) for p in pats)
    return n_py, py_lines, n_cu, counts, ";".join(sorted(vendored))

def main(repos_dir, out_csv):
    rows = []
    for name in sorted(os.listdir(repos_dir)):
        path = os.path.join(repos_dir, name)
        if not os.path.isdir(path):
            continue
        n_py, py_lines, n_cu, c, vend = scan(path)
        rows.append({"repo": name.replace("__", "/", 1), "py_files": n_py, "py_lines": py_lines,
                     "cu_files": n_cu, "vendored_libs": vend, **c})
    with open(out_csv, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"scanned {len(rows)} repos -> {out_csv}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
