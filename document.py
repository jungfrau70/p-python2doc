
import docx
import re  

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor, Inches
from docx.oxml.ns import qn, nsdecls
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
    hdr_cells[0].text = '리전'
    hdr_cells[1].text = '진행상태'
    hdr_cells[2].text = '내용 상세'

    for ind in df.index:
        row_cells = table.add_row().cells
        row_cells[0].text = df['리전'][ind]
        row_cells[1].text = df['진행상태'][ind]
        row_cells[2].text = df['작업내용'][ind]  


def addTable3(df, regex, month):
    
    if [ month != '누적' ]:
        df = df[df['월'] == month].reset_index()
    else:
        pass
    
    table = document.add_table(rows=1, cols=3, style="Table Grid")

    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = '리전'
    hdr_cells[1].text = '진행상태'
    hdr_cells[2].text = '제목'

    for ind in df.index:
        row_cells = table.add_row().cells
        row_cells[0].text = df['리전'][ind]
        row_cells[1].text = df['진행상태'][ind]
        row_cells[2].text = df['제목'][ind] 

        
def addTable4(df, regex, month):
    
    if [ month != '누적' ]:
        df = df[df['월'] == month].reset_index()
    else:
        pass
    
    table = document.add_table(rows=1, cols=4, style="Table Grid")

    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = '리전'
    hdr_cells[1].text = '진행상태'
    hdr_cells[2].text = '제목'
    hdr_cells[3].text = '작업내용'    

    for ind in df.index:
        row_cells = table.add_row().cells
        row_cells[0].text = df['리전'][ind]
        row_cells[1].text = df['진행상태'][ind]
        row_cells[2].text = df['제목'][ind]
        row_cells[3].text = df['작업내용'][ind]  
        

def addPivot2Table(df):
    
    table = document.add_table(rows=1, cols=9, style="Table Grid")
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = '유형'
    hdr_cells[1].text = 'KR'
    hdr_cells[2].text = 'NA'
    hdr_cells[3].text = 'EU'    
    hdr_cells[4].text = 'CN'
    hdr_cells[5].text = 'SG'
    hdr_cells[6].text = 'RU'
    hdr_cells[7].text = '합계' 
    hdr_cells[8].text = '비중' 

    # DBMS유형	CN	EU	KR	NA	RU	SG	합계	비중
    
    for ind in df.index:
        row_cells = table.add_row().cells
        row_cells[0].text = df['유형'][ind]
        row_cells[1].text = '%0.1f' % df['KR'][ind]
        row_cells[2].text = '%0.1f' % df['NA'][ind]
        row_cells[3].text = '%0.1f' % df['EU'][ind]  
        row_cells[4].text = '%0.1f' % df['CN'][ind]
        row_cells[5].text = '%0.1f' % df['SG'][ind]
        row_cells[6].text = '%0.1f' % df['RU'][ind]
        row_cells[7].text = '%0.1f' % df['합계'][ind]  
        row_cells[8].text = '%0.1f' % df['비중'][ind]  
        
def addFailedTable(df, regex, month):
    
    if [ month != '누적' ]:
        df = df[df['월'] == month].reset_index()
    else:
        pass
    
    table = document.add_table(rows=1, cols=5, style="Table Grid")

    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = '날짜'
    hdr_cells[1].text = '진행상태'
    hdr_cells[2].text = '진행상태'    
    hdr_cells[3].text = '작업내용'
    hdr_cells[4].text = '장애전파시간(분)'
    
    for ind in df.index:
        row_cells = table.add_row().cells
        row_cells[0].text = df['날짜'][ind]
        row_cells[1].text = df['진행상태'][ind]
        row_cells[2].text = df['장애내용'][ind]
        row_cells[3].text = df['조치내용'][ind]  
        row_cells[4].text = '%0.1f' % df['장애전파소요시간'][ind]
            
