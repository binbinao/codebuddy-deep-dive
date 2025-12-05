#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
从HTML生成PDF，支持Mermaid图表渲染
使用Playwright + mermaid-cli或直接使用Chrome headless
"""

import sys
import os
import re
import subprocess
import tempfile
from pathlib import Path

def check_mermaid_cli():
    """检查是否安装了mermaid-cli"""
    try:
        result = subprocess.run(['mmdc', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def render_html_with_playwright(html_file, output_pdf):
    """使用Playwright渲染HTML（包括Mermaid）并生成PDF"""
    try:
        from playwright.sync_api import sync_playwright
        
        print("正在使用Playwright渲染HTML（包括Mermaid图表）...")
        
        with sync_playwright() as p:
            # 启动浏览器
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # 加载HTML文件
            html_path = Path(html_file).absolute()
            page.goto(f'file://{html_path}')
            
            # 等待Mermaid图表渲染完成
            # 检查页面是否有Mermaid元素
            try:
                page.wait_for_selector('.mermaid', timeout=5000)
                # 等待额外时间确保渲染完成
                page.wait_for_timeout(2000)
                print("✓ Mermaid图表渲染完成")
            except:
                print("ℹ 未检测到Mermaid图表或渲染超时")
            
            # 生成PDF
            page.pdf(
                path=output_pdf,
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
            
        print(f"✓ PDF已成功生成: {output_pdf}")
        return True
        
    except ImportError:
        print("✗ 未安装 playwright")
        return False
    except Exception as e:
        print(f"✗ 渲染失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def preprocess_html_for_mermaid(html_file):
    """预处理HTML，添加Mermaid渲染脚本"""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 检查是否已经包含Mermaid脚本
    if 'mermaid.min.js' in html_content or 'mermaid.initialize' in html_content:
        print("ℹ HTML已包含Mermaid脚本")
        return html_file
    
    # 检查是否有Mermaid代码块
    if 'class="mermaid"' not in html_content and '<pre class="mermaid">' not in html_content:
        print("ℹ HTML中没有Mermaid图表")
        return html_file
    
    print("正在为HTML添加Mermaid渲染支持...")
    
    # 修复Mermaid代码块格式：<pre class="mermaid"><code>...</code></pre> -> <pre class="mermaid">...</pre>
    html_content = re.sub(
        r'<pre class="mermaid"><code>(.*?)</code></pre>',
        r'<pre class="mermaid">\1</pre>',
        html_content,
        flags=re.DOTALL
    )
    
    # 添加Mermaid脚本（在</head>之前）
    mermaid_script = '''
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({ 
      startOnLoad: true,
      theme: 'default',
      securityLevel: 'loose',
      fontFamily: 'PingFang SC, Hiragino Sans GB, Microsoft YaHei, Arial'
    });
  </script>
'''
    
    html_content = html_content.replace('</head>', mermaid_script + '</head>')
    
    # 创建临时HTML文件
    temp_html = tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.html',
        delete=False,
        encoding='utf-8'
    )
    temp_html.write(html_content)
    temp_html.close()
    
    print(f"✓ 已创建包含Mermaid支持的临时HTML: {temp_html.name}")
    
    return temp_html.name


def html_to_pdf_with_mermaid(html_file, pdf_file):
    """主函数：处理Mermaid并生成PDF"""
    
    # 预处理HTML，添加Mermaid渲染脚本
    processed_html = preprocess_html_for_mermaid(html_file)
    
    # 使用Playwright渲染
    success = render_html_with_playwright(processed_html, pdf_file)
    
    # 清理临时文件
    if processed_html != html_file:
        try:
            os.unlink(processed_html)
            print("✓ 已清理临时文件")
        except:
            pass
    
    return success


def main():
    html_file = "CodeBuddy_架构指南.html"
    pdf_file = "CodeBuddy_架构指南.pdf"
    
    # 检查HTML文件是否存在
    if not os.path.exists(html_file):
        print(f"✗ HTML文件不存在: {html_file}")
        sys.exit(1)
    
    print("=" * 60)
    print("HTML转PDF工具（支持Mermaid图表）")
    print("=" * 60)
    print()
    
    # 转换
    if html_to_pdf_with_mermaid(html_file, pdf_file):
        print()
        print("=" * 60)
        print("转换成功!")
        print(f"输出文件: {pdf_file}")
        print("=" * 60)
        sys.exit(0)
    else:
        print()
        print("=" * 60)
        print("转换失败!")
        print()
        print("请安装依赖:")
        print("  pip install playwright")
        print("  playwright install chromium")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
