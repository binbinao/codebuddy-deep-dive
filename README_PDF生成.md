# PDF生成工具使用说明

## 概述

提供两种方式从文档生成PDF，**两种方式都完美支持中文**：
1. **HTML转PDF + Mermaid渲染**（推荐）- 支持Mermaid流程图，格式保留完整
2. **Markdown转PDF**（备用）- 智能转换为HTML再渲染，完美支持中文

## 推荐方案：从HTML生成PDF（支持Mermaid）

### 特点
✅ 完美支持中文（无黑点问题）
✅ 完美渲染Mermaid流程图
✅ 保留完整的HTML样式和格式
✅ 支持表格、代码块、引用等复杂格式
✅ 自动嵌入系统中文字体
✅ 支持CSS自定义样式
✅ 使用Playwright + Chromium渲染引擎

### 使用方法

```bash
# 1. 进入项目目录
cd /Users/duobinji/Documents/GitHub/codebuddy-deep-dive

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 运行转换脚本（自动使用HTML转PDF）
python convert_to_pdf.py
```

或者单独使用HTML转PDF脚本：

```bash
python html_to_pdf.py
```

### 安装依赖

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装所有必要的库
pip install weasyprint playwright markdown

# 安装Chromium浏览器（用于渲染）
playwright install chromium
```

## 备用方案：从Markdown生成PDF

### 特点
✅ **完美支持中文（已修复，无黑点问题）**
✅ 智能转换：Markdown → HTML → PDF
✅ 使用Playwright渲染，与HTML方案一致
✅ 支持所有Markdown语法
✅ 可以自定义PDF样式
✅ 自动处理表格、列表、代码块

### 技术方案
新版Markdown转PDF采用了与HTML转PDF相同的技术：
1. 使用Python的`markdown`库将MD转换为HTML
2. 添加美观的CSS样式
3. 使用Playwright + Chromium渲染为PDF
4. **完全避免了ReportLab的字体问题**

### 使用方法

```bash
# 删除或重命名HTML文件，让脚本使用Markdown模式
mv CodeBuddy_架构指南.html CodeBuddy_架构指南.html.bak
python convert_to_pdf.py

# 或者直接使用独立的改进版Markdown转PDF工具
python markdown_to_pdf_improved.py
```

## 文件说明

- `convert_to_pdf.py` - 主转换脚本（智能选择HTML或Markdown）
- `html_to_pdf.py` - 独立的HTML转PDF工具
- `CodeBuddy_架构指南.html` - 源HTML文件
- `CodeBuddy_架构指南.md` - 源Markdown文件
- `CodeBuddy_架构指南.pdf` - 生成的PDF文件

## 技术细节

### HTML转PDF技术栈
- **WeasyPrint**: 基于Python的HTML/CSS转PDF引擎
- **字体回退机制**: 自动使用系统中文字体（PingFang SC、Hiragino Sans GB等）
- **CSS样式**: 自定义样式确保排版美观

### 支持的中文字体（按优先级）
1. PingFang SC（苹方-简体中文）
2. Hiragino Sans GB（冬青黑体）
3. Microsoft YaHei（微软雅黑，Windows）
4. WenQuanYi Micro Hei（文泉驿微米黑，Linux）
5. Arial Unicode MS（包含大量Unicode字符）

## 常见问题

### Q: 生成的PDF有黑点？
A: 请使用HTML转PDF方式（推荐方案），它对中文支持最好。

### Q: WeasyPrint安装失败？
A: 确保使用Python 3.8+版本，并且系统安装了必要的依赖。

### Q: 如何自定义PDF样式？
A: 修改 `convert_to_pdf.py` 或 `html_to_pdf.py` 中的CSS样式字符串。

### Q: 生成的PDF文件过大？
A: 这是正常的，因为字体被完整嵌入以确保跨平台显示一致性。

## 输出示例

```
============================================================
使用HTML转PDF（推荐方法，中文支持更好）
============================================================
正在从 CodeBuddy_架构指南.html 生成PDF...
✓ PDF已成功生成: CodeBuddy_架构指南.pdf
```

## 性能对比

| 方案 | 文件大小 | 中文支持 | 格式保留 | 生成速度 |
|------|---------|---------|---------|---------|
| HTML转PDF | ~755KB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 快 |
| Markdown转PDF | ~165KB | ⭐⭐⭐ | ⭐⭐⭐⭐ | 较快 |

## 推荐工作流

```bash
# 第一次使用：设置环境
python3 -m venv venv
source venv/bin/activate
pip install weasyprint reportlab

# 日常使用：一键生成
source venv/bin/activate && python convert_to_pdf.py
```
