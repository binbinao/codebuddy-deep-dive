#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
改进的Markdown转PDF工具
解决字体黑点问题的方案：使用多字体回退机制
"""

import re
import os
import sys
import platform
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import registerFontFamily

def register_unicode_fonts():
    """
    注册多个Unicode字体，建立字体回退机制
    返回: (主字体名, 粗体字体名, 等宽字体名)
    """
    
    system = platform.system()
    registered_fonts = []
    
    print("\n" + "=" * 60)
    print("正在注册字体...")
    print("=" * 60)
    
    if system == "Darwin":  # macOS
        # 定义多个字体选项（按优先级）
        font_options = [
            # Arial Unicode MS - 最全面的Unicode支持
            {
                'regular': '/Library/Fonts/Arial Unicode.ttf',
                'bold': '/Library/Fonts/Arial Unicode.ttf',
                'mono': '/Library/Fonts/Arial Unicode.ttf',
                'name': 'ArialUnicode'
            },
            # 苹方字体
            {
                'regular': ('/System/Library/Fonts/PingFang.ttc', 0),
                'bold': ('/System/Library/Fonts/PingFang.ttc', 2),
                'mono': '/Library/Fonts/Monaco.ttf',
                'name': 'PingFang'
            },
            # 华文黑体
            {
                'regular': ('/System/Library/Fonts/STHeiti Medium.ttc', 0),
                'bold': ('/System/Library/Fonts/STHeiti Medium.ttc', 1),
                'mono': '/System/Library/Fonts/Monaco.ttf',
                'name': 'STHeiti'
            },
        ]
        
        for font_config in font_options:
            try:
                font_name = font_config['name']
                
                # 注册常规字体
                regular_font = font_config['regular']
                if isinstance(regular_font, tuple):
                    path, index = regular_font
                    if os.path.exists(path):
                        pdfmetrics.registerFont(TTFont(font_name, path, subfontIndex=index))
                else:
                    if os.path.exists(regular_font):
                        pdfmetrics.registerFont(TTFont(font_name, regular_font))
                
                # 注册粗体字体
                bold_font = font_config['bold']
                if isinstance(bold_font, tuple):
                    path, index = bold_font
                    if os.path.exists(path):
                        pdfmetrics.registerFont(TTFont(f"{font_name}-Bold", path, subfontIndex=index))
                else:
                    if os.path.exists(bold_font):
                        pdfmetrics.registerFont(TTFont(f"{font_name}-Bold", bold_font))
                
                # 注册等宽字体（代码用）
                mono_font = font_config.get('mono', '/Library/Fonts/Courier New.ttf')
                if isinstance(mono_font, str) and os.path.exists(mono_font):
                    try:
                        pdfmetrics.registerFont(TTFont(f"{font_name}-Mono", mono_font))
                    except:
                        # 如果等宽字体失败，使用常规字体
                        pass
                
                print(f"✓ 成功注册字体系列: {font_name}")
                return font_name, f"{font_name}-Bold", 'Courier'
                
            except Exception as e:
                print(f"✗ 注册 {font_config['name']} 失败: {e}")
                continue
    
    elif system == "Windows":
        # Windows字体
        try:
            # 微软雅黑
            msyh_path = 'C:/Windows/Fonts/msyh.ttc'
            if os.path.exists(msyh_path):
                pdfmetrics.registerFont(TTFont('MSYH', msyh_path, subfontIndex=0))
                pdfmetrics.registerFont(TTFont('MSYH-Bold', msyh_path, subfontIndex=1))
                print("✓ 成功注册字体: 微软雅黑")
                return 'MSYH', 'MSYH-Bold', 'Courier'
        except Exception as e:
            print(f"✗ 注册微软雅黑失败: {e}")
    
    elif system == "Linux":
        # Linux字体
        try:
            # 文泉驿微米黑
            wqy_path = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'
            if os.path.exists(wqy_path):
                pdfmetrics.registerFont(TTFont('WQY', wqy_path, subfontIndex=0))
                pdfmetrics.registerFont(TTFont('WQY-Bold', wqy_path, subfontIndex=0))
                print("✓ 成功注册字体: 文泉驿微米黑")
                return 'WQY', 'WQY-Bold', 'Courier'
        except Exception as e:
            print(f"✗ 注册文泉驿失败: {e}")
    
    print("⚠️  警告: 使用默认字体，可能无法显示所有中文字符")
    return 'Helvetica', 'Helvetica-Bold', 'Courier'


def clean_text_for_pdf(text):
    """
    清理文本，移除或替换可能导致显示问题的字符
    """
    # 替换特殊字符
    replacements = {
        '→': '->',
        '←': '<-',
        '↑': '^',
        '↓': 'v',
        '✓': 'v',
        '✗': 'x',
        '•': '*',
        '—': '-',
        '–': '-',
        '"': '"',
        '"': '"',
        ''': "'",
        ''': "'",
        '…': '...',
        '　': ' ',  # 全角空格
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text


def safe_paragraph(text, style):
    """
    创建安全的段落对象，处理可能的编码问题
    """
    try:
        # 清理文本
        cleaned_text = clean_text_for_pdf(text)
        return Paragraph(cleaned_text, style)
    except Exception as e:
        # 如果失败，尝试只使用ASCII可打印字符
        print(f"⚠️  段落创建警告: {str(e)[:50]}")
        ascii_text = ''.join(c if ord(c) < 128 else '?' for c in text)
        return Paragraph(ascii_text, style)


def markdown_to_pdf_improved(markdown_file, pdf_file):
    """
    改进的Markdown转PDF转换器
    """
    
    # 注册字体
    font_name, bold_font_name, mono_font_name = register_unicode_fonts()
    
    print(f"\n使用字体:")
    print(f"  - 普通: {font_name}")
    print(f"  - 粗体: {bold_font_name}")
    print(f"  - 代码: {mono_font_name}")
    print()
    
    # 读取Markdown文件
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 创建PDF文档
    doc = SimpleDocTemplate(
        pdf_file, 
        pagesize=A4,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch
    )
    
    # 获取样式
    styles = getSampleStyleSheet()
    
    # 自定义样式
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=14,
        alignment=TA_CENTER,
        textColor=HexColor('#2E86AB'),
        fontName=bold_font_name,
        leading=26
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=10,
        spaceBefore=14,
        textColor=HexColor('#2E86AB'),
        fontName=bold_font_name,
        leading=22,
        keepWithNext=True
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=8,
        spaceBefore=12,
        textColor=HexColor('#2E86AB'),
        fontName=bold_font_name,
        leading=20,
        keepWithNext=True
    )
    
    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=6,
        spaceBefore=10,
        textColor=HexColor('#2E86AB'),
        fontName=bold_font_name,
        leading=18,
        keepWithNext=True
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        fontName=font_name,
        leading=16
    )
    
    code_style = ParagraphStyle(
        'CustomCode',
        parent=styles['Code'],
        fontSize=9,
        spaceAfter=8,
        spaceBefore=4,
        fontName=mono_font_name,
        backColor=HexColor('#F5F5F5'),
        leftIndent=20,
        rightIndent=20,
        leading=13
    )
    
    list_style = ParagraphStyle(
        'CustomList',
        parent=normal_style,
        leftIndent=20,
        bulletIndent=10,
        spaceAfter=4
    )
    
    # 处理Markdown内容
    story = []
    
    # 添加封面
    story.append(Spacer(1, 1.5*inch))
    story.append(safe_paragraph("CodeBuddy Code", title_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(safe_paragraph("产品架构与快速上手指南", heading1_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(safe_paragraph("完整架构文档", normal_style))
    story.append(PageBreak())
    
    # 按行处理
    lines = content.split('\n')
    in_code_block = False
    code_content = []
    in_table = False
    table_data = []
    skip_toc = True  # 跳过目录
    
    for i, line in enumerate(lines):
        # 跳过开头的目录部分
        if skip_toc:
            if line.strip().startswith('## ') and '简介' in line:
                skip_toc = False
            else:
                continue
        
        # 处理代码块
        if line.strip().startswith('```'):
            if in_code_block:
                # 结束代码块
                if code_content:
                    code_text = '\n'.join(code_content)
                    # 清理代码文本
                    code_text = clean_text_for_pdf(code_text)
                    # 使用Preformatted而不是Paragraph来保持格式
                    try:
                        story.append(Preformatted(code_text, code_style))
                    except:
                        # 如果失败，使用简单段落
                        story.append(safe_paragraph(code_text.replace('\n', '<br/>'), code_style))
                    story.append(Spacer(1, 0.15*inch))
                code_content = []
                in_code_block = False
            else:
                # 开始代码块
                in_code_block = True
            continue
        
        if in_code_block:
            code_content.append(line)
            continue
        
        # 处理表格
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                in_table = True
                table_data = []
            
            # 处理表格行
            row = [cell.strip() for cell in line.split('|') if cell.strip()]
            if row:
                # 跳过表头分隔符
                if all(cell.replace('-', '').replace(':', '').strip() == '' for cell in row):
                    continue
                # 清理每个单元格
                row = [clean_text_for_pdf(cell) for cell in row]
                table_data.append(row)
            continue
        else:
            # 表格结束
            if in_table and table_data:
                try:
                    table = Table(table_data, repeatRows=1)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#f0f0f0')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#2E86AB')),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), bold_font_name),
                        ('FONTNAME', (0, 1), (-1, -1), font_name),
                        ('FONTSIZE', (0, 0), (-1, -1), 9),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                        ('TOPPADDING', (0, 0), (-1, -1), 6),
                        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ]))
                    story.append(table)
                    story.append(Spacer(1, 0.2*inch))
                except Exception as e:
                    print(f"⚠️  表格创建警告: {e}")
                in_table = False
                table_data = []
        
        # 处理标题
        if line.startswith('# ') and not line.startswith('## '):
            text = clean_text_for_pdf(line[2:].strip())
            story.append(safe_paragraph(text, title_style))
            story.append(Spacer(1, 0.2*inch))
        elif line.startswith('## '):
            text = clean_text_for_pdf(line[3:].strip())
            story.append(safe_paragraph(text, heading1_style))
            story.append(Spacer(1, 0.15*inch))
        elif line.startswith('### '):
            text = clean_text_for_pdf(line[4:].strip())
            story.append(safe_paragraph(text, heading2_style))
            story.append(Spacer(1, 0.1*inch))
        elif line.startswith('#### '):
            text = clean_text_for_pdf(line[5:].strip())
            story.append(safe_paragraph(text, heading3_style))
            story.append(Spacer(1, 0.08*inch))
        # 处理分隔线
        elif line.strip() == '---':
            story.append(Spacer(1, 0.2*inch))
        # 处理空行
        elif line.strip() == '':
            story.append(Spacer(1, 0.08*inch))
        # 处理普通文本
        else:
            # 清理文本
            processed_line = clean_text_for_pdf(line)
            
            # 基本的Markdown处理
            processed_line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', processed_line)
            processed_line = re.sub(r'\*(.*?)\*', r'<i>\1</i>', processed_line)
            processed_line = re.sub(r'`(.*?)`', r'<font face="Courier">\1</font>', processed_line)
            processed_line = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'<u>\1</u>', processed_line)
            
            # 处理列表项
            if line.strip().startswith('- ') or line.strip().startswith('* '):
                processed_line = f"• {processed_line[2:]}"
                story.append(safe_paragraph(processed_line, list_style))
            elif re.match(r'^\d+\.\s', line.strip()):
                story.append(safe_paragraph(processed_line, list_style))
            else:
                story.append(safe_paragraph(processed_line, normal_style))
    
    # 构建PDF
    print("正在生成PDF...")
    try:
        doc.build(story)
        print(f"\n{'='*60}")
        print(f"✓ PDF已成功生成: {pdf_file}")
        print(f"{'='*60}\n")
        return True
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"✗ PDF生成失败: {e}")
        print(f"{'='*60}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    markdown_file = "CodeBuddy_架构指南.md"
    pdf_file = "CodeBuddy_架构指南_from_md.pdf"
    
    if not os.path.exists(markdown_file):
        print(f"✗ Markdown文件不存在: {markdown_file}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("改进的Markdown转PDF工具")
    print("=" * 60)
    
    success = markdown_to_pdf_improved(markdown_file, pdf_file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
