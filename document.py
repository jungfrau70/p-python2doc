
import docx
import re  

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor, Inches
from docx.oxml.ns import qn
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

document = Document()
sections = document.sections
from docx import Document
from docx.shared import Inches

document = Document()

for section in sections:
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    
section = document.sections[0]

sectPr = section._sectPr
cols = sectPr.xpath('./w:cols')[0]
cols.set(qn('w:num'), '1')

#import dataframe_image as dfi

def writeTable(df, regex, month):
    
    df = df[df['리전'].apply(lambda x: True if re.search(regex, x) else False) & (df['테넌트']== 'PRD') & (df['월간']=='O')]

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
        
