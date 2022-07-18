# %load chart.py

import pandas as pd
from pandas import Series, DataFrame
from pandas_ods_reader import read_ods

import altair as alt
import pandas as pd
import re  

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor, Inches
from docx.oxml.ns import qn
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import docx

from io import BytesIO
memfile = BytesIO()

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

def get_pivotTable(df):
    df_filtered = df.loc[(df['월']=='6월') & (df['테넌트']== 'PRD') & (df['진행상태']=='완료')]
    pTable = pd.pivot_table(df_filtered[['리전','진행상태']], index = ['리전'], aggfunc = 'count').rename_axis('리전').reset_index()
    # filtered.describe()
    pTable.columns = ['리전', '합계']
    pTable.sort_values(by=['합계'], ascending=False, inplace=True)
    pTable.reset_index(drop=True, inplace=True)
    total = pTable["합계"].sum()
    pTable['비중'] = round(pTable['합계'] / total, 2) * 100
    return pTable

def get_pivotTable_am(df):
    df_filtered = df.loc[(df['월']=='6월') & (df['테넌트']== 'PRD')]
    pTable = pd.pivot_table(df_filtered[['리전', 'DBMS', 'count']], index = ['리전'], aggfunc = 'sum').rename_axis('리전').reset_index()
    pTable.columns = ['리전', '합계']
    pTable.sort_values(by=['합계'], ascending=False, inplace=True)
    pTable.reset_index(drop=True, inplace=True)
    total = pTable["합계"].sum()
    pTable['비중'] = round((pTable['합계'] / total)*100, 1)
    return pTable

def get_barChart(source):
    bar = alt.Chart(source).mark_bar().encode(
        x=alt.X('리전'),
        y=alt.Y('합계:Q', title='')
    )
    text = bar.mark_text(
        size=12,
        color='black',
        dy = -10
    ).encode(
        text="label:N"
    ).transform_calculate(
        label = alt.datum.리전 + ": " + alt.datum.합계   + ", " + alt.datum.비중 +"%"
    )

    chart = (bar + text).properties(width=400, height=200)
    return chart

def get_pieChart(source):
    base = alt.Chart(source).encode(
        theta=alt.Theta("합계:Q", 
                        stack=True), 
        color=alt.Color("리전:N", legend=None)
    )

    pie = base.mark_arc(outerRadius=120)

    text = pie.mark_text(
        size=12,
        radius=160,        
        color='black'
    ).encode(
        text="label:N"
    ).transform_calculate(
        label = alt.datum.리전 + ": " + alt.datum.합계   + ", " + alt.datum.비중 +"%"
    )

    chart = (pie + text).properties(width=400, height=400)
    return chart

def get_lineChart(source):
    point = alt.Chart(source).mark_point().encode(
        x=alt.X('월'),
        y=alt.Y('count()'),
        # text=alt.Text("성패:Q")
    )

    line = alt.Chart(source).mark_line(color="red").encode(
        x=alt.X('월'),
        y=alt.Y('count()', title='')
    )

    text = bar.mark_text(
        size=12,
        align='center',
        baseline='line-top',
        color='black',
        dy=-20,
        fontSize=12,
    ).encode(
        text = 'count(성패):Q'
    )

    chart = (point + line + text).properties(width=400, height=200)
    return chart

def get_lineChart_am(source):
    point = alt.Chart(source).mark_point().encode(
        x=alt.X('월'),
        y=alt.Y('sum(count)'),
        # text=alt.Text("성패:Q")
    )

    line = alt.Chart(source).mark_line(color="red").encode(
        x=alt.X('월'),
        y=alt.Y('sum(count)', title='')
    )

    text = point.mark_text(
        size=12,
        align='center',
        baseline='line-top',
        color='black',
        dy=-20,
        fontSize=12,
    ).encode(
        text = 'sum(count):Q'
    )

    chart = (point + line + text).properties(width=400, height=200)
    return chart
