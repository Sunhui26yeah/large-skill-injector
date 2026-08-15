# Markdown 转 PDF：没有 pandoc/LaTeX 工具链时的本地方案

**触发场景**：用户要求把一个 Markdown 文件（尤其是带 GFM 风格 checkbox 的清单，比如论文 review comment 的 resolution checklist）转成 PDF，而本地环境里没有 `pandoc`、`wkhtmltopdf`、`weasyprint`，也没有可用的 LaTeX 工具链（`pdflatex`/`bibtex` 不存在）。第一次遇到这个场景是把 [`ESEM2026Replication/REVIEW_TODO.md`](../../ESEM2026Replication/REVIEW_TODO.md)（本地路径，不在本仓库版本控制范围内）转成 PDF。

**前提检查**：先用 `which pandoc wkhtmltopdf weasyprint prince pdflatex bibtex` 确认这些都不存在，再走下面的路径；如果 pandoc 或 LaTeX 工具链本来就在，直接用那些更省事，不需要这套。macOS 上几乎总能找到一个 Chrome/Edge/Chromium（`ls /Applications/ | grep -i chrome`），本方案依赖它。

## 整体流程

```
Markdown  --(python-markdown, 预处理 checkbox)-->  HTML  --(headless Chrome --print-to-pdf)-->  PDF
```

### 1. 隔离环境装依赖

系统 Python 大概率是 PEP 668 "externally-managed-environment"，裸 `pip install` 会被拒绝。在 scratchpad 建一个一次性 venv：

```bash
python3 -m venv /path/to/scratchpad/venv_stats
/path/to/scratchpad/venv_stats/bin/pip install --quiet markdown pillow
```

`pillow` 只在需要截图核对多页渲染效果时才用（见第 4 步），只转 PDF 的话不需要。

### 2. Markdown → HTML，手动处理 checkbox

`python-markdown` 库**不认识 GFM 的任务列表语法**（`- [x]` / `- [ ]`），会把方括号原样当成文本渲染，很难看。必须在调用 `markdown.markdown()` **之前**用正则把 checkbox 换成不会被 markdown 解析器碰的占位符，转换完之后再把占位符换成真正的 HTML：

```python
import re, markdown

def checkbox_repl(m):
    indent, mark = m.group(1), m.group(2).strip()
    if mark.upper() == 'X':
        return f'{indent}- @@CHECKED@@ '
    elif mark == '✗':          # 项目里用来表示"拒绝/不采纳"的自定义标记
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

三态（已完成 / 未完成 / 拒绝）都能这样扩展——占位符 token 只要不含 markdown 特殊字符，能扛过一轮 `markdown.markdown()` 转换就行。

### 3. 踩过的坑：不要用 emoji 当 checkbox 图标

第一版直接把 `✅ / ☐ / ❌` 三个 emoji 字符写进 HTML 当 checkbox 视觉符号，图省事。结果 headless Chrome 的 PDF 渲染器**把三个 emoji 全部退化成同一个空心方框字形**，导致最终 PDF 里"已完成"、"未完成"、"被拒绝"三种状态**完全看不出区别**——这是靠下面第 4 步的视觉核查习惯才发现的，光看命令退出码和文件大小完全看不出问题。

正确做法：用原生 `<input type="checkbox" checked disabled>` / `<input type="checkbox" disabled>`，这是标准 HTML 元素，不依赖任何字体/emoji 支持，勾选态用 CSS `accent-color` 上色；"拒绝"这种三态里的第三态，不要指望第三个符号也能被区分，直接配一个文字标签（比如红色描边的 `REJECTED` span）。

对应的最小 CSS：

```css
input.cb { width:12px; height:12px; margin-right:6px; vertical-align:middle; accent-color:#2e7d32; }
input.cb-rejected { accent-color:#b03a2e; }
.rejected-tag { color:#b03a2e; font-weight:700; font-size:.78em; letter-spacing:.04em;
                margin-right:6px; border:1px solid #b03a2e; border-radius:3px; padding:0 4px; }
ul { list-style: none; }  /* checkbox 顶替了 bullet，不然会重复 */
```

页面外层包一层系统字体栈（`-apple-system, "Segoe UI", Helvetica, Arial`）、打印用的字号（正文约 10.5pt 比较合适，太大翻页太多），标题/横线/代码块按需上色即可，细节不重要。

### 4. HTML → PDF：headless Chrome

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-sandbox \
  --print-to-pdf="out.pdf" \
  --print-to-pdf-no-header --no-pdf-header-footer \
  "file:///absolute/path/to.html"
```

Mac 上 Chrome/Edge 通常已经装了，不需要额外安装任何东西。`file://` 必须是绝对路径。

### 5. 核心纪律：渲染完一定要"看一眼"再交付

不能只信退出码或文件字节数，必须实际截图看过再说完成——第 3 步的 emoji 坑就是这么抓出来的，不然会把一份三态完全分辨不出来的 PDF 当成成品交出去。两种截图手段，取决于要看第几页：

- **看第一页**（够用大部分场景，macOS 自带、零依赖）：
  ```bash
  qlmanage -t -s 1000 -o /output/dir file.pdf
  # 生成 /output/dir/file.pdf.png，用 Read 工具直接看
  ```
- **看任意/多页内容**：`qlmanage` 只出第一页缩略图，而这台机器上又没装 `pdftoppm`/poppler 去把 PDF 任意页转图。绕过的办法是**不转 PDF 本身，直接把源 HTML 用一个很高的窗口截全屏**（HTML 和最终 PDF 是同一份渲染结果，截 HTML 等价于看多页 PDF 拼起来的效果）：
  ```bash
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --headless --disable-gpu --no-sandbox \
    --window-size=900,9000 --screenshot="full.png" \
    "file:///absolute/path/to.html"
  ```
  窗口高度要给够（内容比窗口矮的话截图会有大片空白，比内容还矮会截断——先给一个明显够大的值比如 9000，再用下面的方法找真实内容边界）：
  ```python
  from PIL import Image
  import numpy as np
  arr = np.array(Image.open('full.png').convert('L'))
  last_content_row = np.where(arr.min(axis=1) < 250)[0].max()
  # 用这个位置裁剪出想核查的区域，比如结尾一段
  Image.open('full.png').crop((0, max(0, last_content_row-1200), arr.shape[1], last_content_row+30)).save('crop_end.png')
  ```

### 6. 交付位置

最终 PDF 存到源 `.md` 文件同一目录下（而不是只留在 scratchpad），当作项目的正式产出物。

## 相关

目前 `Academic_skills/` 下只有这一篇，直接挂在 [index.md](../index.md) 里；如果之后这个分类下页面多起来，参考 `concepts/CRA/` 的模式建一个总览页面做入口。
