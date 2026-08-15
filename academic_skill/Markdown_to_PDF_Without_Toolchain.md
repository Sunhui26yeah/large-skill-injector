# Markdown to PDF: a Local Fallback When There's No pandoc/LaTeX Toolchain

**When this applies**: the user wants a Markdown file — especially one with GFM-style checkboxes, like a paper review-comment resolution checklist — converted to PDF, and the local machine has none of `pandoc`, `wkhtmltopdf`, `weasyprint`, and no usable LaTeX toolchain (`pdflatex`/`bibtex` missing). First hit this converting [`ESEM2026Replication/REVIEW_TODO.md`](../../ESEM2026Replication/REVIEW_TODO.md) (a local path, not under this repo's version control) to PDF.

**Check first**: confirm none of these exist with `which pandoc wkhtmltopdf weasyprint prince pdflatex bibtex`. If pandoc or a LaTeX toolchain is actually present, just use that — it's less work. On macOS there's almost always a Chrome/Edge/Chromium install somewhere (`ls /Applications/ | grep -i chrome`), which is what this approach depends on.

## Pipeline

```
Markdown  --(python-markdown, checkbox preprocessing)-->  HTML  --(headless Chrome --print-to-pdf)-->  PDF
```

### 1. Install dependencies in an isolated environment

System Python is likely PEP 668 "externally-managed-environment," so a bare `pip install` will be refused. Make a throwaway venv in scratchpad:

```bash
python3 -m venv /path/to/scratchpad/venv_stats
/path/to/scratchpad/venv_stats/bin/pip install --quiet markdown pillow
```

`pillow` is only needed if you'll be screenshotting to verify multi-page rendering (see step 4) — skip it if you're just doing the conversion.

### 2. Markdown → HTML, with manual checkbox handling

**`python-markdown` doesn't understand GFM task-list syntax** (`- [x]` / `- [ ]`) — it renders the brackets as literal text, which looks bad. You have to swap checkboxes for placeholder tokens the parser won't touch *before* calling `markdown.markdown()`, then replace those tokens with real HTML *after* conversion:

```python
import re, markdown

def checkbox_repl(m):
    indent, mark = m.group(1), m.group(2).strip()
    if mark.upper() == 'X':
        return f'{indent}- @@CHECKED@@ '
    elif mark == '✗':          # custom marker this project used for "rejected"
        return f'{indent}- @@REJECTED@@ '
    else:
        return f'{indent}- @@UNCHECKED@@ '

text = re.sub(r'^(\s*)- \[([Xx ✗])\]\s*', checkbox_repl, text, flags=re.MULTILINE)
html_body = markdown.markdown(text, extensions=['extra', 'sane_lists'])

html_body = (html_body
    .replace('@@CHECKED@@',   '<input type="checkbox" checked disabled class="cb">')
    .replace('@@UNCHECKED@@', '<input type="checkbox" disabled class="cb">')
    .replace('@@REJECTED@@',  '<input type="checkbox" disabled class="cb cb-rejected">'
                               '<span class="rejected-tag">REJECTED</span>'))
```

This generalizes to any tri-state (done / not done / rejected) — the placeholder tokens just need to avoid markdown special characters and survive one pass of `markdown.markdown()`.

### 3. Gotcha: don't use emoji as checkbox glyphs

The first version put `✅ / ☐ / ❌` emoji directly in the HTML as checkbox visuals, for convenience. Headless Chrome's PDF renderer **collapsed all three emoji into the same empty box glyph** — checked, unchecked, and rejected items were **visually indistinguishable** in the final PDF. This was only caught by the visual-verification habit in step 4 below — the exit code and file size gave no hint anything was wrong.

Fix: use native `<input type="checkbox" checked disabled>` / `<input type="checkbox" disabled>` elements — standard HTML, doesn't depend on any font or emoji support, checked state colored via CSS `accent-color`. For a third state in a tri-state checklist (like "rejected"), don't count on a third glyph being distinguishable either — give it an explicit text label instead (e.g. a red-bordered "REJECTED" span).

Minimal matching CSS:

```css
input.cb { width:12px; height:12px; margin-right:6px; vertical-align:middle; accent-color:#2e7d32; }
input.cb-rejected { accent-color:#b03a2e; }
.rejected-tag { color:#b03a2e; font-weight:700; font-size:.78em; letter-spacing:.04em;
                margin-right:6px; border:1px solid #b03a2e; border-radius:3px; padding:0 4px; }
ul { list-style: none; }  /* checkboxes replace the bullet, otherwise you get both */
```

Wrap everything in a minimal styled HTML document: system font stack (`-apple-system, "Segoe UI", Helvetica, Arial`), a print-friendly body font size (~10.5pt keeps page count reasonable), header/rule/code colors as desired — none of that is critical.

### 4. HTML → PDF: headless Chrome

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-sandbox \
  --print-to-pdf="out.pdf" \
  --print-to-pdf-no-header --no-pdf-header-footer \
  "file:///absolute/path/to.html"
```

Chrome or Edge is usually already installed on a Mac, so this needs no extra setup. The `file://` path must be absolute.

### 5. Core discipline: always look at the render before delivering

Never trust the exit code or file size alone — actually screenshot and inspect before calling it done. That's exactly how the emoji-checkbox bug in step 3 got caught. Two techniques, depending on how much of the document you need to check:

- **First page only** (covers most cases, built into macOS, zero extra dependencies):
  ```bash
  qlmanage -t -s 1000 -o /output/dir file.pdf
  # produces /output/dir/file.pdf.png — Read it directly
  ```
- **Any/multiple pages**: `qlmanage` only thumbnails page 1, and this machine had no `pdftoppm`/poppler to rasterize arbitrary PDF pages. The workaround is to **screenshot the source HTML directly at a very tall window height** instead of the PDF itself (HTML and the final PDF are the same render, so screenshotting the HTML is equivalent to seeing multiple PDF pages stitched together):
  ```bash
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --headless --disable-gpu --no-sandbox \
    --window-size=900,9000 --screenshot="full.png" \
    "file:///absolute/path/to.html"
  ```
  Give the window height plenty of headroom (too short and the screenshot gets clipped; too tall and there's a big blank margin — start with something clearly oversized like 9000, then locate the real content boundary):
  ```python
  from PIL import Image
  import numpy as np
  arr = np.array(Image.open('full.png').convert('L'))
  last_content_row = np.where(arr.min(axis=1) < 250)[0].max()
  # crop around this to inspect a specific region, e.g. the tail end
  Image.open('full.png').crop((0, max(0, last_content_row-1200), arr.shape[1], last_content_row+30)).save('crop_end.png')
  ```

### 6. Where to save the output

Put the final PDF next to the source `.md` file (not just in scratchpad) — it's a deliverable for the project, not a throwaway.

## Related

Only this one page under `academic_skill/` for now — see [index.md](../index.md). If more pages accumulate here later, add an overview/hub page as the entry point (see `CLAUDE.md`'s directory conventions for the pattern).
