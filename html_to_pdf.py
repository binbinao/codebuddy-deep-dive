#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
从HTML文件生成PDF
使用weasyprint库，它对中文和CSS支持很好
"""

import sys
import os

def html_to_pdf_weasyprint(html_file, pdf_file):
    """使用WeasyPrint将HTML转换为PDF"""
    try:
        from weasyprint import HTML, CSS
        from weasyprint.text.fonts import FontConfiguration
        
        # 创建字体配置
        font_config = FontConfiguration()
        
        # 添加自定义CSS来确保中文字体正确显示
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
            
            h1 {
                font-size: 24pt;
                margin-top: 20pt;
                margin-bottom: 10pt;
            }
            
            h2 {
                font-size: 18pt;
                margin-top: 16pt;
                margin-bottom: 8pt;
            }
            
            h3 {
                font-size: 14pt;
                margin-top: 12pt;
                margin-bottom: 6pt;
            }
            
            p {
                margin-bottom: 10pt;
                text-align: justify;
            }
            
            ul, ol {
                margin-bottom: 10pt;
                padding-left: 20pt;
            }
            
            li {
                margin-bottom: 5pt;
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
            
            blockquote {
                border-left: 4px solid #2E86AB;
                padding-left: 15px;
                margin-left: 0;
                color: #666;
                font-style: italic;
            }
            
            /* 防止代码块跨页断开 */
            pre, blockquote, table {
                page-break-inside: avoid;
            }
            
            /* 图片样式 */
            img {
                max-width: 100%;
                height: auto;
            }
        ''', font_config=font_config)
        
        # 读取HTML并生成PDF
        print(f"正在从 {html_file} 生成PDF...")
        HTML(filename=html_file).write_pdf(
            pdf_file, 
            stylesheets=[custom_css],
            font_config=font_config
        )
        
        print(f"✓ PDF已成功生成: {pdf_file}")
        return True
        
    except ImportError:
        print("✗ 未安装 weasyprint 库")
        return False
    except Exception as e:
        print(f"✗ 生成PDF时出错: {e}")
        import traceback
        traceback.print_exc()
        return False


def html_to_pdf_pdfkit(html_file, pdf_file):
    """使用pdfkit(wkhtmltopdf)将HTML转换为PDF"""
    try:
        import pdfkit
        
        options = {
            'page-size': 'A4',
            'margin-top': '20mm',
            'margin-right': '20mm',
            'margin-bottom': '20mm',
            'margin-left': '20mm',
            'encoding': 'UTF-8',
            'enable-local-file-access': None,
            'no-outline': None,
            'quiet': ''
        }
        
        print(f"正在从 {html_file} 生成PDF...")
        pdfkit.from_file(html_file, pdf_file, options=options)
        print(f"✓ PDF已成功生成: {pdf_file}")
        return True
        
    except ImportError:
        print("✗ 未安装 pdfkit 库")
        return False
    except OSError as e:
        if 'wkhtmltopdf' in str(e):
            print("✗ 未安装 wkhtmltopdf")
            print("  请安装: brew install wkhtmltopdf")
        else:
            print(f"✗ 生成PDF时出错: {e}")
        return False
    except Exception as e:
        print(f"✗ 生成PDF时出错: {e}")
        return False


def main():
    html_file = "CodeBuddy_架构指南.html"
    pdf_file = "CodeBuddy_架构指南.pdf"
    
    # 检查HTML文件是否存在
    if not os.path.exists(html_file):
        print(f"✗ HTML文件不存在: {html_file}")
        sys.exit(1)
    
    print("=" * 60)
    print("HTML转PDF工具")
    print("=" * 60)
    
    # 优先尝试使用weasyprint (更好的CSS和字体支持)
    print("\n方法1: 尝试使用 WeasyPrint...")
    if html_to_pdf_weasyprint(html_file, pdf_file):
        print("\n" + "=" * 60)
        print("转换成功!")
        print("=" * 60)
        return
    
    # 如果weasyprint失败，尝试pdfkit
    print("\n方法2: 尝试使用 pdfkit...")
    if html_to_pdf_pdfkit(html_file, pdf_file):
        print("\n" + "=" * 60)
        print("转换成功!")
        print("=" * 60)
        return
    
    # 两种方法都失败
    print("\n" + "=" * 60)
    print("两种方法都失败了，请安装所需的库:")
    print("  pip install weasyprint")
    print("  或")
    print("  brew install wkhtmltopdf && pip install pdfkit")
    print("=" * 60)
    sys.exit(1)


if __name__ == "__main__":
    main()
