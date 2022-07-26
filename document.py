
import docx
import re  

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor, Inches
from docx.oxml.ns import qn
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

document = Document()
sections = document.sections

for section in sections:
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    
section = document.sections[0]

sectPr = section._sectPr
cols = sectPr.xpath('./w:cols')[0]
cols.set(qn('w:num'), '1')

def addSummaryTable(df, regex, month):
    
    if [ month != '누적' ]:
        df = df[df['월'] == month].reset_index()
    else:
        pass
    
    table = document.add_table(rows=1, cols=3, style="Table Grid")

    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = '월'
    hdr_cells[1].text = '진행상태'
    hdr_cells[2].text = '내용 상세'

    for ind in df.index:
        row_cells = table.add_row().cells
        row_cells[0].text = df['월'][ind]
        row_cells[1].text = df['진행상태'][ind]
        row_cells[2].text = df['Description'][ind]  

def addFailedTable(df, regex, month):
    
    if [ month != '누적' ]:
        df = df[df['월'] == month].reset_index()
    else:
        pass
    
    table = document.add_table(rows=1, cols=4, style="Table Grid")

    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = '날짜'
    hdr_cells[1].text = '진행상태'
    hdr_cells[2].text = '내용 상세'
    hdr_cells[3].text = '장애전파시간(분)'
    
    for ind in df.index:
        row_cells = table.add_row().cells
        row_cells[0].text = df['날짜'][ind]
        row_cells[1].text = df['장애 내용'][ind]
        row_cells[2].text = df['장애대응조치내용'][ind]  
        row_cells[3].text = '%0.1f' % df['장애전파'][ind]
