#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

def markdown_to_html(markdown_content):
    """将Markdown转换为HTML"""
    
    # 基本的Markdown到HTML转换
    html_content = markdown_content
    
    # 处理标题
    html_content = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    
    # 处理粗体
    html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_content)
    
    # 处理斜体
    html_content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html_content)
    
    # 处理代码块
    html_content = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', html_content, flags=re.DOTALL)
    
    # 处理行内代码
    html_content = re.sub(r'`(.*?)`', r'<code>\1</code>', html_content)
    
    # 处理列表
    html_content = re.sub(r'^\s*- (.*?)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'(<li>.*</li>)', r'<ul>\1</ul>', html_content, flags=re.DOTALL)
    
    # 处理链接
    html_content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html_content)
    
    # 处理段落
    lines = html_content.split('\n')
    processed_lines = []
    current_paragraph = []
    
    for line in lines:
        if line.strip() == '':
            if current_paragraph:
                processed_lines.append('<p>' + ' '.join(current_paragraph) + '</p>')
                current_paragraph = []
            processed_lines.append('')
        elif line.startswith('<') and line.endswith('>'):
            if current_paragraph:
                processed_lines.append('<p>' + ' '.join(current_paragraph) + '</p>')
                current_paragraph = []
            processed_lines.append(line)
        else:
            current_paragraph.append(line)
    
    if current_paragraph:
        processed_lines.append('<p>' + ' '.join(current_paragraph) + '</p>')
    
    html_content = '\n'.join(processed_lines)
    
    return html_content

def create_pdf_from_html(html_content, pdf_file):
    """从HTML创建PDF"""
    
    # 完整的HTML文档
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>CodeBuddy Code 产品架构与快速上手指南</title>
        <style>
            @page {{
                size: A4;
                margin: 2cm;
                @top-center {{
                    content: "CodeBuddy Code 架构指南";
                    font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
                    font-size: 12px;
                    color: #666;
                }}
                @bottom-center {{
                    content: "第 " counter(page) " 页";
                    font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
                    font-size: 10px;
                    color: #666;
                }}
            }}
            
            body {{
                font-family: "PingFang SC", "Microsoft YaHei", "SimHei", sans-serif;
                font-size: 12px;
                line-height: 1.6;
                color: #333;
                margin: 0;
                padding: 0;
            }}
            
            h1 {{
                font-size: 24px;
                color: #2E86AB;
                text-align: center;
                margin: 30px 0 20px 0;
                border-bottom: 2px solid #2E86AB;
                padding-bottom: 10px;
            }}
            
            h2 {{
                font-size: 20px;
                color: #2E86AB;
                margin: 25px 0 15px 0;
                border-left: 4px solid #2E86AB;
                padding-left: 10px;
            }}
            
            h3 {{
                font-size: 16px;
                color: #2E86AB;
                margin: 20px 0 10px 0;
            }}
            
            p {{
                margin: 10px 0;
                text-align: justify;
            }}
            
            ul, ol {{
                margin: 10px 0 10px 20px;
            }}
            
            li {{
                margin: 5px 0;
            }}
            
            code {{
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 3px;
                padding: 2px 4px;
                font-family: "Courier New", monospace;
                font-size: 11px;
            }}
            
            pre {{
                background-color: #f8f8f8;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 15px;
                margin: 15px 0;
                overflow-x: auto;
                font-family: "Courier New", monospace;
                font-size: 11px;
                line-height: 1.4;
            }}
            
            pre code {{
                background: none;
                border: none;
                padding: 0;
            }}
            
            strong {{
                color: #2E86AB;
                font-weight: bold;
            }}
            
            em {{
                font-style: italic;
                color: #666;
            }}
            
            a {{
                color: #2E86AB;
                text-decoration: none;
            }}
            
            a:hover {{
                text-decoration: underline;
            }}
            
            .header {{
                text-align: center;
                margin: 50px 0;
            }}
            
            .title {{
                font-size: 28px;
                color: #2E86AB;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            
            .subtitle {{
                font-size: 16px;
                color: #666;
                margin-top: 0;
            }}
            
            .separator {{
                border-top: 1px solid #ddd;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="title">CodeBuddy Code</div>
            <div class="subtitle">产品架构与快速上手指南</div>
        </div>
        
        {html_content}
        
        <div class="separator"></div>
        <p style="text-align: center; color: #666; font-size: 10px;">
            文档生成时间: 2024年12月5日 | CodeBuddy Code 架构指南
        </p>
    </body>
    </html>
    """
    
    # 创建字体配置
    font_config = FontConfiguration()
    
    # 创建PDF
    html = HTML(string=full_html)
    
    # 生成PDF
    html.write_pdf(pdf_file, font_config=font_config)
    
    print(f"PDF已成功生成: {pdf_file}")

def main():
    """主函数"""
    
    # 读取Markdown文件
    with open("CodeBuddy_架构指南.md", 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # 转换为HTML
    html_content = markdown_to_html(markdown_content)
    
    # 创建PDF
    pdf_file = "CodeBuddy_架构指南_weasyprint.pdf"
    create_pdf_from_html(html_content, pdf_file)
    
    print(f"\n转换完成！")
    print(f"输入文件: CodeBuddy_架构指南.md")
    print(f"输出文件: {pdf_file}")

if __name__ == "__main__":
    main()