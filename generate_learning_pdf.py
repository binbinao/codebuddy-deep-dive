#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
快速Markdown转PDF工具
专为学习文档设计，包含精美样式
"""

import sys
import os
import tempfile
from playwright.sync_api import sync_playwright
import markdown

def markdown_to_beautiful_pdf(md_file, pdf_file=None):
    """
    将Markdown文件转换为精美的PDF
    
    参数:
        md_file: Markdown文件路径
        pdf_file: PDF输出路径（可选，默认为md文件名.pdf）
    """
    
    # 确定输出文件名
    if pdf_file is None:
        pdf_file = md_file.replace('.md', '.pdf')
    
    print(f"正在读取: {md_file}")
    
    # 获取Markdown文件的目录（用于解析相对路径）
    md_dir = os.path.dirname(os.path.abspath(md_file))
    
    # 读取Markdown
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except FileNotFoundError:
        print(f"✗ 文件不存在: {md_file}")
        return False
    
    print("正在转换Markdown为HTML...")
    
    # 转换为HTML（支持代码高亮、表格、TOC等）
    md = markdown.Markdown(extensions=[
        'fenced_code',
        'tables', 
        'toc',
        'nl2br',
        'sane_lists',
        'codehilite',
        'attr_list'
    ])
    # 如果 md_content 中没有 [TOC]，自动在第一个 h1 之后添加
    if '[TOC]' not in md_content and '# ' in md_content:
        lines = md_content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('# '):
                lines.insert(i + 1, '\n[TOC]\n')
                break
        md_content = '\n'.join(lines)
    
    html_body = md.convert(md_content)
    
    # 修复图片路径：将相对路径转换为绝对路径
    import re
    def fix_image_path(match):
        img_tag = match.group(0)
        src_match = re.search(r'src="([^"]+)"', img_tag)
        if src_match:
            src = src_match.group(1)
            # 如果是相对路径，转换为绝对路径
            if not src.startswith(('http://', 'https://', 'file://', '/')):
                abs_path = os.path.join(md_dir, src)
                if os.path.exists(abs_path):
                    img_tag = img_tag.replace(f'src="{src}"', f'src="file://{abs_path}"')
                    print(f"  修复图片路径: {src} -> file://{abs_path}")
        return img_tag
    
    html_body = re.sub(r'<img[^>]+>', fix_image_path, html_body)
    
    # 精美的HTML模板
    html_template = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>学习文档</title>
    <style>
        @page {
            size: A4;
            margin: 2cm;
        }
        
        * {
            box-sizing: border-box;
        }
        
        body {
            font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", 
                         "WenQuanYi Micro Hei", "Arial Unicode MS", sans-serif;
            line-height: 1.8;
            color: #333;
            font-size: 14px;
            max-width: 100%;
        }
        
        /* 标题样式 - 渐变色系 */
        h1 {
            color: #2C3E50;
            font-size: 28px;
            text-align: center;
            border-bottom: 4px solid #3498DB;
            padding-bottom: 15px;
            margin: 30px 0 25px 0;
            page-break-after: avoid;
        }
        
        /* 第一个h1：首页标题，不换页 */
        h1:first-of-type {
            margin-top: 150px;
            margin-bottom: 50px;
            font-size: 42px;
            color: #2C3E50;
            border-bottom: none;
            page-break-before: avoid;
            page-break-after: avoid;
            padding-bottom: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        /* 目录样式 */
        .toc {
            background-color: #F8F9FA;
            padding: 25px;
            border-radius: 8px;
            margin: 40px 0;
            border-left: 5px solid #3498DB;
            page-break-after: always;
        }
        
        .toc ul {
            list-style-type: none;
            padding-left: 20px;
        }
        
        .toc li {
            margin-bottom: 8px;
        }
        
        .toc a {
            color: #2C3E50;
            text-decoration: none;
            border-bottom: 1px solid transparent;
        }
        
        .toc a:hover {
            color: #3498DB;
            border-bottom: 1px solid #3498DB;
        }
        
        /* 副标题（紧跟第一个h1的h2）：显示在首页 */
        h1:first-of-type + h2 {
            text-align: center;
            color: #7F8C8D;
            font-size: 20px;
            border: none;
            margin-top: 20px;
            margin-bottom: 150px;
            page-break-before: avoid;
            page-break-after: always;  /* 副标题之后换页 */
        }
        
        /* 第二个h1及以后才开始新页 */
        body > h1:nth-of-type(2),
        body > h1:nth-of-type(n+3) {
            page-break-before: always;
            margin-top: 0;
            padding-top: 20px;
        }
        
        h2 {
            color: #2980B9;
            font-size: 26px;
            border-bottom: 2px solid #ECF0F1;
            padding-bottom: 10px;
            margin-top: 40px;
            page-break-after: avoid;
        }
        
        h3 {
            color: #3498DB;
            font-size: 22px;
            margin-top: 30px;
            page-break-after: avoid;
        }
        
        h4 {
            color: #5DADE2;
            font-size: 18px;
            margin-top: 25px;
        }
        
        h5 {
            color: #85C1E9;
            font-size: 16px;
            margin-top: 20px;
        }
        
        /* 段落样式 */
        p {
            margin-bottom: 15px;
            text-align: justify;
            text-justify: inter-ideograph;
        }
        
        /* 代码样式 - 深色主题 */
        code {
            font-family: "Monaco", "Menlo", "Consolas", "Courier New", monospace;
            background-color: #F8F9FA;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.9em;
            color: #E74C3C;
            word-wrap: break-word;
        }
        
        pre {
            background: linear-gradient(135deg, #2C3E50 0%, #34495E 100%);
            color: #ECF0F1;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            border-left: 4px solid #3498DB;
            page-break-inside: avoid;
            font-size: 12px;
            line-height: 1.6;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        pre code {
            background-color: transparent;
            padding: 0;
            color: #ECF0F1;
            font-size: 1em;
        }
        
        /* 引用样式 - 渐变背景 */
        blockquote {
            border-left: 5px solid #3498DB;
            padding: 15px 20px;
            margin: 20px 0;
            background: linear-gradient(90deg, #EBF5FB 0%, #FFFFFF 100%);
            font-style: italic;
            border-radius: 0 8px 8px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        
        /* 表格样式 - 现代风格 */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            box-shadow: 0 2px 12px rgba(0,0,0,0.1);
            page-break-inside: avoid;
            border-radius: 8px;
            overflow: hidden;
        }
        
        table th {
            background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
            color: white;
            font-weight: bold;
            padding: 15px;
            text-align: left;
            border: none;
            font-size: 14px;
        }
        
        table td {
            padding: 12px 15px;
            border-bottom: 1px solid #ECF0F1;
            font-size: 13px;
        }
        
        table tr:nth-child(even) {
            background-color: #F8F9FA;
        }
        
        table tr:hover {
            background-color: #EBF5FB;
            transition: background-color 0.2s ease;
        }
        
        table tr:last-child td {
            border-bottom: none;
        }
        
        /* 列表样式 */
        ul, ol {
            margin-bottom: 20px;
            padding-left: 35px;
        }
        
        li {
            margin-bottom: 10px;
            line-height: 1.6;
        }
        
        ul li::marker {
            color: #3498DB;
            font-weight: bold;
        }
        
        ol li::marker {
            color: #E74C3C;
            font-weight: bold;
        }
        
        /* 分隔线 */
        hr {
            border: none;
            border-top: 3px solid #ECF0F1;
            margin: 50px 0;
            background: linear-gradient(90deg, transparent, #3498DB, transparent);
            height: 2px;
        }
        
        /* 链接样式 */
        a {
            color: #3498DB;
            text-decoration: none;
            border-bottom: 1px dotted #3498DB;
            transition: all 0.2s ease;
        }
        
        a:hover {
            color: #2980B9;
            border-bottom: 1px solid #2980B9;
        }
        
        /* 强调样式 */
        strong {
            color: #E74C3C;
            font-weight: bold;
        }
        
        em {
            color: #8E44AD;
            font-style: italic;
        }
        
        /* 图片样式 */
        img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin: 20px 0;
        }
        
        /* 打印优化 */
        @media print {
            body {
                max-width: 100%;
            }
            
            h1, h2, h3, h4, h5, h6 {
                page-break-after: avoid;
            }
            
            pre, blockquote, table, img {
                page-break-inside: avoid;
            }
            
            a {
                color: #3498DB;
                text-decoration: none;
            }
            
            /* 确保背景色打印出来 */
            * {
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }
        }
        
        /* 特殊徽章样式（可选） */
        .badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: bold;
            margin: 0 4px;
        }
        
        .badge-success {
            background-color: #27AE60;
            color: white;
        }
        
        .badge-warning {
            background-color: #F39C12;
            color: white;
        }
        
        .badge-info {
            background-color: #3498DB;
            color: white;
        }
    </style>
</head>
<body>
''' + html_body + '''
</body>
</html>'''
    
    # 创建临时HTML文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(html_template)
        temp_html = f.name
    
    print(f"临时HTML文件: {temp_html}")
    print("正在使用Playwright渲染PDF...")
    
    try:
        # 使用Playwright生成PDF
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(f'file://{os.path.abspath(temp_html)}')
            page.wait_for_load_state('networkidle')
            
            page.pdf(
                path=pdf_file,
                format='A4',
                margin={
                    'top': '2cm',
                    'right': '2cm',
                    'bottom': '2.5cm',
                    'left': '2cm'
                },
                print_background=True,
                display_header_footer=True,
                footer_template='''
                    <div style="font-size: 10px; color: #7F8C8D; width: 100%; text-align: center;">
                        第 <span class="pageNumber"></span> 页 / 共 <span class="totalPages"></span> 页
                    </div>
                '''
            )
            
            browser.close()
        
        # 清理临时文件
        os.unlink(temp_html)
        
        print("\n" + "=" * 60)
        print(f"✓ PDF生成成功: {pdf_file}")
        print("=" * 60)
        
        # 显示文件大小
        size_mb = os.path.getsize(pdf_file) / (1024 * 1024)
        print(f"文件大小: {size_mb:.2f} MB")
        
        return True
        
    except Exception as e:
        print(f"\n✗ 生成失败: {e}")
        import traceback
        traceback.print_exc()
        
        # 清理临时文件
        if os.path.exists(temp_html):
            os.unlink(temp_html)
        
        return False


def main():
    if len(sys.argv) < 2:
        print("用法: python generate_learning_pdf.py <markdown文件> [输出pdf文件]")
        print("\n示例:")
        print("  python generate_learning_pdf.py 深度学习优化器详解.md")
        print("  python generate_learning_pdf.py 学习笔记.md 输出.pdf")
        sys.exit(1)
    
    md_file = sys.argv[1]
    pdf_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    print("\n" + "=" * 60)
    print("Markdown转PDF工具 - 学习文档专用")
    print("=" * 60 + "\n")
    
    success = markdown_to_beautiful_pdf(md_file, pdf_file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
