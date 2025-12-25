# CODEBUDDY.md

This file provides guidance to CodeBuddy Code when working with code in this repository.

## Project Overview

This repository is a **Deep Learning Knowledge Base** containing:
- High-quality learning documents about neural networks, optimizers, and model compilation
- Professional visualization charts (30 PNG images total)
- Automated PDF generation system with perfect Chinese support
- Chart generation scripts for creating publication-quality figures

### Key Features
- ✅ Perfect Chinese font rendering in charts and PDFs
- ✅ Professional table formatting in generated PDFs
- ✅ Automated chart generation with unified styling
- ✅ 150 DPI high-resolution images
- ✅ Complete documentation with 9+ PDFs totaling 10+ MB

## Environment Setup

### Virtual Environment

All Python scripts in this project should be run within the virtual environment:

```bash
# Activate the virtual environment (macOS/Linux)
source venv/bin/activate

# If venv doesn't exist, create it
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install weasyprint playwright markdown reportlab matplotlib numpy scipy
playwright install chromium
```

### Required Dependencies

The project uses the following Python packages:
- `playwright` (1.56.0) - Browser automation for rendering HTML to PDF
- `weasyprint` - HTML/CSS to PDF conversion
- `markdown` (3.10) - Markdown to HTML conversion
- `reportlab` (4.4.5) - Direct PDF generation (legacy/backup)
- `matplotlib` (3.10.7) - Scientific plotting for activation function charts
- `numpy` (2.3.5) - Numerical computation
- `scipy` (1.16.3) - Scientific functions (e.g., erf for GELU)
- Standard libraries: `re`, `os`, `tempfile`, `subprocess`

## Common Commands

### Learning Documents

All core learning documents are located in the `docs/` directory:
- `docs/神经网络激活函数详解.md` + `.pdf` (4.5 MB)
- `docs/深度学习优化器详解.md` + `.pdf` (2.4 MB)
- `docs/模型编译优化指标详解.md` + `.pdf` (2.8 MB)
- `docs/模型编译优化指标速查表.md`

### PDF Generation

#### Generate Learning Document PDFs (Recommended)
```bash
source venv/bin/activate
python generate_learning_pdf.py docs/<markdown_file>.md
```
- Specialized for learning documents with proper formatting
- Perfect table rendering with professional styling
- Automatic image path resolution (relative to absolute)
- Handles Chinese fonts correctly
- Examples:
  ```bash
  python generate_learning_pdf.py docs/神经网络激活函数详解.md
  python generate_learning_pdf.py docs/深度学习优化器详解.md
  python generate_learning_pdf.py docs/模型编译优化指标详解.md
  ```

**Note**: Old PDF generation scripts have been archived to `archive/old_scripts/`
```bash
source venv/bin/activate
python generate_learning_pdf.py <markdown_file>
```
- Specialized for learning documents with proper title page formatting
- Handles first-page layout correctly (title + subtitle on same page)

### Chart Generation

#### Generate Activation Function Charts
```bash
source venv/bin/activate
python scripts/generate_activation_plots.py
```
- Generates 18 high-quality PNG charts for activation functions
- Output directory: `images/activation_functions/`
- Includes: sigmoid, tanh, ReLU, Leaky ReLU, ELU, GELU, Swish, Softmax
- Each function has: basic plot, plot with derivative, and comparison charts
- Charts are automatically referenced in Markdown and embedded in PDF

#### Generate Optimizer Charts
```bash
source venv/bin/activate
python scripts/generate_optimizer_plots.py
```
- Generates 6 high-quality PNG charts for optimizer explanations
- Output directory: `images/optimizers/`
- Includes: gradient descent visualization, optimizer path comparison, adaptive learning rate, convergence curves, momentum effect, feature radar
- Used in "深度学习优化器详解" document

#### Generate Model Metrics Charts
```bash
source venv/bin/activate
python scripts/generate_metrics_plots.py
```
- Generates 6 high-quality PNG charts for model compilation metrics
- Output directory: `images/model_metrics/`
- Includes: impossible triangle, latency comparison, optimization techniques, quantization comparison, throughput vs latency, scenario priorities
- Used in "模型编译优化指标详解" document

### Testing Commands

To verify the complete workflow:
```bash
source venv/bin/activate

# 1. Generate all charts
python scripts/generate_activation_plots.py
python scripts/generate_optimizer_plots.py
python scripts/generate_metrics_plots.py

# 2. Generate all PDFs
python generate_learning_pdf.py docs/神经网络激活函数详解.md
python generate_learning_pdf.py docs/深度学习优化器详解.md
python generate_learning_pdf.py docs/模型编译优化指标详解.md

# 3. Check output
ls -lh docs/*.pdf
ls -lh images/*/
```

## Code Architecture

### Project Structure

```
codebuddy-deep-dive/
├── docs/                           # Core learning documents
│   ├── 神经网络激活函数详解.md + .pdf (4.5 MB, 18 charts)
│   ├── 深度学习优化器详解.md + .pdf (2.4 MB, 6 charts)
│   ├── 模型编译优化指标详解.md + .pdf (2.8 MB, 6 charts)
│   └── 模型编译优化指标速查表.md
├── images/                        # High-quality charts
│   ├── activation_functions/     # 18 PNG images (~1.2 MB)
│   ├── optimizers/               # 6 PNG images (~751 KB)
│   └── model_metrics/            # 6 PNG images (~544 KB)
├── scripts/                       # Chart generation scripts
│   ├── generate_activation_plots.py
│   ├── generate_optimizer_plots.py
│   └── generate_metrics_plots.py
├── archive/                       # Archived/deprecated files
│   ├── old_scripts/               # Old PDF generation scripts
│   └── *.md                       # Temporary documentation
├── generate_learning_pdf.py       # Main PDF generation script
├── CODEBUDDY.md                   # This file
├── README.md                      # Project overview
├── LICENSE                        # MIT License
└── venv/                          # Python virtual environment
```

### PDF Generation Pipeline

The repository implements a multi-strategy PDF generation system:

```
┌─────────────────────────────────────────────────┐
│          PDF Generation System                   │
└─────────────────────────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          │                       │
      HTML Source           Markdown Source
          │                       │
          ├─ Mermaid?            └─> Markdown Library
          │                           │
     [Strategy A]                     └─> HTML + CSS
  Playwright + Chromium                   │
  (html_to_pdf_with_mermaid.py)      [Strategy B]
          │                          Playwright
          │                          (convert_to_pdf.py)
          │                               │
          └───────────────┬───────────────┘
                          │
                      PDF Output
                  (Perfect Chinese Support)
```

### Core Scripts

1. **convert_to_pdf.py** (Main Entry Point)
   - Intelligent routing based on available source files
   - Tries HTML→PDF first (with Mermaid support)
   - Falls back to Markdown→HTML→PDF
   - Contains both WeasyPrint and Playwright rendering logic
   - Lines 541-587: Main execution logic with fallback chain

2. **html_to_pdf_with_mermaid.py** (Recommended for HTML)
   - Preprocesses HTML to inject Mermaid rendering scripts
   - Uses Playwright + Chromium for accurate rendering
   - Lines 82-135: HTML preprocessing with Mermaid script injection
   - Lines 28-79: Playwright rendering with wait for Mermaid
   - Handles mermaid CDN imports and initialization

3. **html_to_pdf.py** (Basic HTML Conversion)
   - Uses WeasyPrint for HTML→PDF (no JavaScript support)
   - Good for static HTML without Mermaid
   - Custom CSS injection for Chinese fonts
   - Font fallback: PingFang SC → Hiragino Sans GB → Microsoft YaHei

4. **markdown_to_pdf_improved.py** (Markdown Pipeline)
   - Two-stage: Markdown→HTML→PDF
   - Uses Python `markdown` library with extensions
   - Playwright rendering (avoids ReportLab font issues)
   - Lines 221-449: Complete Markdown conversion pipeline

5. **generate_learning_pdf.py** (Learning Documents)
   - Specialized CSS for learning materials
   - Fixed first-page layout (title + subtitle together)
   - Chapter-based page breaks
   - See: PDF问题修复记录.md for CSS pagination details

### Font Handling Strategy

The codebase uses a sophisticated font registration system to ensure Chinese character support:

**Font Priority (macOS)**:
1. Arial Unicode MS - Most reliable, includes extensive CJK characters
2. PingFang SC (苹方) - macOS native Chinese font
3. STHeiti (华文黑体) - Alternative Chinese font
4. Hiragino Sans GB - Japanese font with Chinese support

**Implementation** (convert_to_pdf.py, lines 106-220):
- Handles TTC (TrueType Collection) fonts with `subfontIndex` parameter
- Cross-platform support (macOS, Windows, Linux)
- Graceful fallback if no Chinese fonts available

### Mermaid Rendering Technique

To render Mermaid diagrams in PDF:

1. **Detect Mermaid blocks**: Look for `class="mermaid"` in HTML
2. **Fix code block nesting**: Convert `<pre class="mermaid"><code>...</code></pre>` to `<pre class="mermaid">...</pre>`
3. **Inject Mermaid CDN**: Add ESM module import before `</head>`
4. **Initialize Mermaid**: Configure with Chinese font fallback
5. **Wait for rendering**: Use Playwright's `wait_for_selector()` and timeout
6. **Generate PDF**: Chromium's native PDF generation preserves rendered SVG

See: html_to_pdf_with_mermaid.py, lines 82-135 for full implementation.

## Known Issues & Solutions

### Issue: Chinese Characters Display as Black Dots
**Solution**: Use Playwright-based rendering (html_to_pdf_with_mermaid.py or convert_to_pdf.py), NOT pure ReportLab.

### Issue: Mermaid Shows as Source Code
**Solution**: Use html_to_pdf_with_mermaid.py which injects Mermaid rendering scripts. Do NOT use html_to_pdf.py (WeasyPrint can't execute JavaScript).

### Issue: First Page Title Split Across Two Pages
**Solution**: Use generate_learning_pdf.py which has fixed CSS pagination rules. See PDF问题修复记录.md for details.

### Issue: Large PDF File Size
**Explanation**: This is expected. Playwright embeds full fonts for cross-platform compatibility. Typical sizes:
- HTML + Mermaid: ~1.9MB
- Markdown → PDF: ~986KB
- ReportLab direct: ~36KB (but has font issues)

## Development Workflow

### Adding New PDF Generation Features

1. For new rendering logic, extend convert_to_pdf.py
2. For new CSS styles, modify the CSS string templates
3. For new Markdown extensions, update the `markdown.Markdown()` configuration
4. Test with both HTML and Markdown sources
5. Verify Chinese character rendering and Mermaid diagrams

### Testing Strategy

```bash
# Test HTML with Mermaid
python html_to_pdf_with_mermaid.py

# Test Markdown conversion
mv CodeBuddy_架构指南.html CodeBuddy_架构指南.html.bak
python convert_to_pdf.py
mv CodeBuddy_架构指南.html.bak CodeBuddy_架构指南.html

# Test learning document formatting
python generate_learning_pdf.py 深度学习优化器详解.md
```

### File Organization

```
codebuddy-deep-dive/
├── venv/                              # Python virtual environment
├── scripts/                           # Utility scripts
│   └── generate_activation_plots.py   # Chart generation script
├── images/                            # Generated images
│   └── activation_functions/          # Activation function charts (18 PNG files)
├── convert_to_pdf.py                  # Smart PDF generator (main entry)
├── html_to_pdf_with_mermaid.py        # HTML+Mermaid renderer (recommended)
├── html_to_pdf.py                     # Basic HTML renderer (WeasyPrint)
├── markdown_to_pdf_improved.py        # Markdown→PDF pipeline
├── generate_learning_pdf.py           # Learning materials specialized
├── convert_with_weasyprint.py         # WeasyPrint utilities
├── CodeBuddy_架构指南.md              # Source: CodeBuddy architecture
├── CodeBuddy_架构指南.html            # Rendered HTML (with Mermaid)
├── CodeBuddy_架构指南.pdf             # Final PDF output
├── 神经网络激活函数详解.md            # Source: Activation functions
├── 深度学习优化器详解.md              # Source: DL optimizers
├── 模型编译优化指标详解.md            # Source: Model compilation
├── 图表生成方案.md                    # Chart generation strategy document
├── 图表使用指南.md                    # Chart usage guide
└── README_PDF生成.md                  # User documentation
```

## Technical Notes

### Why Playwright Over WeasyPrint?

- **JavaScript Support**: Mermaid requires JS execution
- **Font Handling**: Browser's automatic font fallback is more robust
- **Rendering Accuracy**: Chromium's rendering matches web preview exactly
- **Trade-off**: Larger file size, requires Chromium installation

### CSS Pagination Control

Key CSS properties for PDF page breaks:
- `page-break-before: avoid` - Don't break before element
- `page-break-after: avoid` - Don't break after element  
- `page-break-after: always` - Force break after element
- `page-break-inside: avoid` - Keep element together on one page

Use CSS selectors like `:first-of-type` and `:nth-of-type(n+2)` for precise control.

### Character Encoding

All scripts use UTF-8 encoding (`# -*- coding: utf-8 -*-`). When reading/writing files, always specify `encoding='utf-8'` to prevent encoding issues with Chinese characters.

## Documentation

Primary documentation files in this repository:
- **README_PDF生成.md**: User guide for PDF generation
- **PDF生成方案总结.md**: Technical comparison of approaches
- **PDF问题修复记录.md**: Fix history for pagination issues
- **CodeBuddy_架构指南.md**: Complete CodeBuddy Code architecture reference

## Best Practices

1. **Always activate venv** before running scripts
2. **Use html_to_pdf_with_mermaid.py** for best quality
3. **Test both HTML and Markdown sources** when modifying code
4. **Preserve UTF-8 encoding** in all text operations
5. **Use Playwright rendering** to avoid font issues
6. **Keep HTML sources** when available (better than regenerating from Markdown)
7. **Check Chromium installation** if Playwright fails: `playwright install chromium`

## Quick Reference

```bash
# Daily workflow
cd /Users/duobinji/Documents/GitHub/codebuddy-deep-dive
source venv/bin/activate
python convert_to_pdf.py

# Generate specific document
python generate_learning_pdf.py <input.md>

# Force Markdown conversion
rm CodeBuddy_架构指南.html
python convert_to_pdf.py

# Debug mode (see full error traces)
python -u html_to_pdf_with_mermaid.py
```
