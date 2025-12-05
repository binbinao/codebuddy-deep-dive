#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import platform
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import Color, black, white, HexColor
from reportlab.pdfgen import canvas

def html_to_pdf(html_file, pdf_file):
    """从HTML生成PDF - 推荐方法，中文支持更好"""
    try:
        from weasyprint import HTML, CSS
        from weasyprint.text.fonts import FontConfiguration
        
        # 创建字体配置
        font_config = FontConfiguration()
        
        # 添加自定义CSS
        custom_css = CSS(string='''
            @page {
                size: A4;
                margin: 2cm;
            }
            
            body {
                font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", 
                             "WenQuanYi Micro Hei", "Arial Unicode MS", sans-serif;
                line-height: 1.6;
                color: #333;
            }
            
            code, pre {
                font-family: "Monaco", "Menlo", "Courier New", monospace;
                background-color: #f5f5f5;
                padding: 2px 4px;
                border-radius: 3px;
            }
            
            pre {
                padding: 10px;
                overflow-x: auto;
            }
            
            h1, h2, h3, h4, h5, h6 {
                font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", 
                             "Arial Unicode MS", sans-serif;
                color: #2E86AB;
                page-break-after: avoid;
            }
            
            blockquote {
                border-left: 4px solid #2E86AB;
                padding-left: 15px;
                margin-left: 0;
                color: #666;
                font-style: italic;
            }
            
            table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 15pt;
                page-break-inside: avoid;
            }
            
            table th {
                background-color: #f0f0f0;
                color: #2E86AB;
                font-weight: bold;
                padding: 8pt;
                text-align: left;
                border: 1px solid #ddd;
            }
            
            table td {
                padding: 6pt;
                border: 1px solid #ddd;
            }
        ''', font_config=font_config)
        
        print(f"正在从 {html_file} 生成PDF...")
        HTML(filename=html_file).write_pdf(
            pdf_file, 
            stylesheets=[custom_css],
            font_config=font_config
        )
        
        print(f"✓ PDF已成功生成: {pdf_file}")
        return True
        
    except ImportError:
        print("✗ 未安装 weasyprint 库，请运行: pip install weasyprint")
        return False
    except Exception as e:
        print(f"✗ 生成PDF时出错: {e}")
        return False

def register_chinese_fonts():
    """注册中文字体 - 使用subfontIndex参数处理TTC字体"""
    
    system = platform.system()
    
    if system == "Darwin":  # macOS
        # 定义字体系列 - 每个系列包含普通和粗体
        font_families = [
            # Arial Unicode MS (最可靠，包含大量中文字符)
            [
                {'path': '/Library/Fonts/Arial Unicode.ttf', 'name': 'ArialUnicode', 'subfontIndex': None},
                {'path': '/Library/Fonts/Arial Unicode.ttf', 'name': 'ArialUnicode-Bold', 'subfontIndex': None}
            ],
            # 苹方字体系列 (macOS推荐)
            [
                {'path': '/System/Library/Fonts/PingFang.ttc', 'name': 'PingFang', 'subfontIndex': 0},  # Regular
                {'path': '/System/Library/Fonts/PingFang.ttc', 'name': 'PingFang-Bold', 'subfontIndex': 2}  # Semibold
            ],
            # 华文黑体系列
            [
                {'path': '/System/Library/Fonts/STHeiti Medium.ttc', 'name': 'STHeiti', 'subfontIndex': 0},
                {'path': '/System/Library/Fonts/STHeiti Medium.ttc', 'name': 'STHeiti-Bold', 'subfontIndex': 1}
            ],
            # Hiragino Sans GB (也支持中文)
            [
                {'path': '/System/Library/Fonts/Hiragino Sans GB.ttc', 'name': 'HiraginoSansGB', 'subfontIndex': 0},
                {'path': '/System/Library/Fonts/Hiragino Sans GB.ttc', 'name': 'HiraginoSansGB-Bold', 'subfontIndex': 1}
            ],
        ]
        
        # 尝试注册字体系列
        for family in font_families:
            family_fonts = []
            family_failed = False
            
            for config in family:
                font_path = config['path']
                font_name = config['name']
                subfont_index = config['subfontIndex']
                
                if not os.path.exists(font_path):
                    family_failed = True
                    break
                    
                try:
                    if subfont_index is not None:
                        pdfmetrics.registerFont(TTFont(font_name, font_path, subfontIndex=subfont_index))
                    else:
                        pdfmetrics.registerFont(TTFont(font_name, font_path))
                    
                    print(f"✓ 成功注册字体: {font_name} (来自: {os.path.basename(font_path)})")
                    family_fonts.append(font_name)
                    
                except Exception as e:
                    print(f"✗ 注册字体失败 {font_name}: {e}")
                    family_failed = True
                    break
            
            # 如果该字体系列成功注册，返回
            if not family_failed and len(family_fonts) >= 1:
                if len(family_fonts) >= 2:
                    return family_fonts[0], family_fonts[1]
                else:
                    # 如果只有一个字体，用同一个字体作为粗体
                    return family_fonts[0], family_fonts[0]
    
    elif system == "Windows":
        # Windows系统字体
        windows_fonts = [
            ('C:/Windows/Fonts/msyh.ttc', 'MicrosoftYaHei', 0),  # 微软雅黑
            ('C:/Windows/Fonts/msyhbd.ttc', 'MicrosoftYaHei-Bold', 0),
            ('C:/Windows/Fonts/simhei.ttf', 'SimHei', None),  # 黑体
            ('C:/Windows/Fonts/simsun.ttc', 'SimSun', 0),  # 宋体
        ]
        
        for font_path, font_name, subfont_index in windows_fonts:
            if os.path.exists(font_path):
                try:
                    if subfont_index is not None:
                        pdfmetrics.registerFont(TTFont(font_name, font_path, subfontIndex=subfont_index))
                    else:
                        pdfmetrics.registerFont(TTFont(font_name, font_path))
                    print(f"✓ 成功注册字体: {font_name}")
                    return font_name, font_name
                except Exception as e:
                    print(f"✗ 注册字体失败 {font_name}: {e}")
    
    elif system == "Linux":
        # Linux系统字体
        linux_font_paths = [
            '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
            '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
        ]
        
        for font_path in linux_font_paths:
            if os.path.exists(font_path):
                try:
                    font_name = os.path.splitext(os.path.basename(font_path))[0]
                    if font_path.endswith('.ttc'):
                        pdfmetrics.registerFont(TTFont(font_name, font_path, subfontIndex=0))
                    else:
                        pdfmetrics.registerFont(TTFont(font_name, font_path))
                    print(f"✓ 成功注册字体: {font_name}")
                    return font_name, font_name
                except Exception as e:
                    print(f"✗ 注册字体失败: {e}")
    
    # 如果所有方法都失败，打印错误信息
    print("=" * 60)
    print("警告: 未能注册任何中文字体!")
    print("建议: 请安装支持中文的字体，或者指定字体路径")
    print("=" * 60)
    return 'Helvetica', 'Helvetica-Bold'

def markdown_to_pdf(markdown_file, pdf_file):
    """
    将Markdown文件转换为PDF
    新方案: Markdown -> HTML -> PDF (使用Playwright渲染)
    这样可以完美支持中文，避免字体问题
    """
    import tempfile
    import subprocess
    
    print("=" * 60)
    print("Markdown转PDF方案: MD -> HTML -> PDF")
    print("=" * 60)
    
    try:
        # 方案1: 使用markdown库 + 自定义HTML模板
        try:
            import markdown
            from markdown.extensions import fenced_code, tables, toc
            
            print("步骤1: 读取Markdown文件...")
            with open(markdown_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            print("步骤2: 转换Markdown为HTML...")
            # 配置Markdown扩展
            md = markdown.Markdown(extensions=[
                'fenced_code',
                'tables',
                'toc',
                'nl2br',
                'sane_lists'
            ])
            html_body = md.convert(md_content)
            
            # 创建完整的HTML文档
            html_template = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>CodeBuddy Code 架构指南</title>
    <style>
        body {{
            font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", 
                         "WenQuanYi Micro Hei", "Arial Unicode MS", sans-serif;
            line-height: 1.8;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", 
                         "Arial Unicode MS", sans-serif;
            color: #2E86AB;
            margin-top: 24px;
            margin-bottom: 16px;
        }}
        
        h1 {{ font-size: 28px; border-bottom: 2px solid #2E86AB; padding-bottom: 10px; }}
        h2 {{ font-size: 24px; border-bottom: 1px solid #ddd; padding-bottom: 8px; }}
        h3 {{ font-size: 20px; }}
        h4 {{ font-size: 18px; }}
        
        p {{
            margin-bottom: 12px;
            text-align: justify;
        }}
        
        code {{
            font-family: "Monaco", "Menlo", "Courier New", monospace;
            background-color: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.9em;
        }}
        
        pre {{
            background-color: #f5f5f5;
            padding: 16px;
            border-radius: 6px;
            overflow-x: auto;
            border: 1px solid #ddd;
        }}
        
        pre code {{
            background-color: transparent;
            padding: 0;
            font-size: 0.85em;
            line-height: 1.5;
        }}
        
        blockquote {{
            border-left: 4px solid #2E86AB;
            padding-left: 16px;
            margin-left: 0;
            color: #666;
            font-style: italic;
            background-color: #f9f9f9;
            padding: 10px 16px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        
        table th {{
            background-color: #f0f0f0;
            color: #2E86AB;
            font-weight: bold;
            padding: 10px;
            text-align: left;
            border: 1px solid #ddd;
        }}
        
        table td {{
            padding: 8px;
            border: 1px solid #ddd;
        }}
        
        table tr:nth-child(even) {{
            background-color: #fafafa;
        }}
        
        ul, ol {{
            margin-bottom: 16px;
            padding-left: 30px;
        }}
        
        li {{
            margin-bottom: 8px;
        }}
        
        hr {{
            border: none;
            border-top: 2px solid #eee;
            margin: 24px 0;
        }}
        
        a {{
            color: #2E86AB;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        img {{
            max-width: 100%;
            height: auto;
        }}
        
        /* 打印优化 */
        @media print {{
            body {{
                max-width: 100%;
            }}
            h1, h2, h3 {{
                page-break-after: avoid;
            }}
            pre, blockquote, table {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
{body}
</body>
</html>'''
            
            html_content = html_template.format(body=html_body)
            
            # 创建临时HTML文件
            temp_html = tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.html',
                delete=False,
                encoding='utf-8'
            )
            temp_html.write(html_content)
            temp_html.close()
            
            print(f"步骤3: 临时HTML文件创建: {temp_html.name}")
            
            # 使用Playwright渲染为PDF
            print("步骤4: 使用Playwright渲染为PDF...")
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(f'file://{os.path.abspath(temp_html.name)}')
                page.wait_for_load_state('networkidle')
                
                page.pdf(
                    path=pdf_file,
                    format='A4',
                    margin={
                        'top': '2cm',
                        'right': '2cm',
                        'bottom': '2cm',
                        'left': '2cm'
                    },
                    print_background=True
                )
                
                browser.close()
            
            # 清理临时文件
            os.unlink(temp_html.name)
            
            print(f"✓ PDF已成功生成: {pdf_file}")
            return True
            
        except ImportError as e:
            print(f"✗ 缺少必要的库: {e}")
            print("请安装: pip install markdown playwright")
            print("然后运行: playwright install chromium")
            return False
            
    except Exception as e:
        print(f"✗ 转换失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def html_to_pdf(html_file, pdf_file):
    """从HTML生成PDF - 推荐方法，中文支持更好"""
    try:
        from weasyprint import HTML, CSS
        from weasyprint.text.fonts import FontConfiguration
        
        # 创建字体配置
        font_config = FontConfiguration()
        
        # 添加自定义CSS
        custom_css = CSS(string='''
            @page {
                size: A4;
                margin: 2cm;
            }
            
            body {
                font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", 
                             "WenQuanYi Micro Hei", "Arial Unicode MS", sans-serif;
                line-height: 1.6;
                color: #333;
            }
            
            code, pre {
                font-family: "Monaco", "Menlo", "Courier New", monospace;
                background-color: #f5f5f5;
                padding: 2px 4px;
                border-radius: 3px;
            }
            
            pre {
                padding: 10px;
                overflow-x: auto;
            }
            
            h1, h2, h3, h4, h5, h6 {
                font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", 
                             "Arial Unicode MS", sans-serif;
                color: #2E86AB;
                page-break-after: avoid;
            }
            
            blockquote {
                border-left: 4px solid #2E86AB;
                padding-left: 15px;
                margin-left: 0;
                color: #666;
                font-style: italic;
            }
            
            table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 15pt;
                page-break-inside: avoid;
            }
            
            table th {
                background-color: #f0f0f0;
                color: #2E86AB;
                font-weight: bold;
                padding: 8pt;
                text-align: left;
                border: 1px solid #ddd;
            }
            
            table td {
                padding: 6pt;
                border: 1px solid #ddd;
            }
        ''', font_config=font_config)
        
        print(f"正在从 {html_file} 生成PDF...")
        HTML(filename=html_file).write_pdf(
            pdf_file, 
            stylesheets=[custom_css],
            font_config=font_config
        )
        
        print(f"✓ PDF已成功生成: {pdf_file}")
        return True
        
    except ImportError:
        print("✗ 未安装 weasyprint 库，请运行: pip install weasyprint")
        return False
    except Exception as e:
        print(f"✗ 生成PDF时出错: {e}")
        return False


if __name__ == "__main__":
    import sys
    import subprocess
    
    # 首先尝试使用支持Mermaid的版本（推荐）
    html_file = "CodeBuddy_架构指南.html"
    pdf_file = "CodeBuddy_架构指南.pdf"
    
    if os.path.exists(html_file):
        print("=" * 60)
        print("检测到HTML文件，使用支持Mermaid的渲染方式")
        print("=" * 60)
        
        # 尝试调用html_to_pdf_with_mermaid.py
        try:
            result = subprocess.run(
                [sys.executable, "html_to_pdf_with_mermaid.py"],
                capture_output=False,
                timeout=120
            )
            if result.returncode == 0:
                sys.exit(0)
            else:
                print("\n⚠️ Mermaid渲染失败，尝试使用基础HTML转PDF...")
        except FileNotFoundError:
            print("\n⚠️ 未找到html_to_pdf_with_mermaid.py，使用基础HTML转PDF...")
        except Exception as e:
            print(f"\n⚠️ Mermaid渲染出错: {e}")
            print("尝试使用基础HTML转PDF...")
        
        # 回退到基础HTML转PDF
        print("=" * 60)
        print("使用基础HTML转PDF（不支持Mermaid动态渲染）")
        print("=" * 60)
        if html_to_pdf(html_file, pdf_file):
            sys.exit(0)
    
    # 如果HTML不存在，使用Markdown转PDF
    markdown_file = "CodeBuddy_架构指南.md"
    if os.path.exists(markdown_file):
        print("=" * 60)
        print("使用Markdown转PDF（备用方法）")
        print("=" * 60)
        markdown_to_pdf(markdown_file, pdf_file)
    else:
        print("✗ 找不到源文件: " + html_file + " 或 " + markdown_file)
        sys.exit(1)