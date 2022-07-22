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

def getPivotTable(df):
    
    if '자원유형' in df:
        df_filtered = df.loc[(df['월']=='6월') & (df['테넌트']== 'PRD') & (df['진행상태']=='완료')]
        pivotTable = pd.pivot_table(df_filtered[['리전','진행상태']], index = ['리전'], aggfunc = 'count').rename_axis('리전').reset_index()
    elif 'DBType' in df:
        df_filtered = df.loc[(df['월']=='6월') & (df['테넌트']== 'PRD')]
        pivotTable = pd.pivot_table(df_filtered[['리전', 'DBType']], index = ['리전'], aggfunc = 'count').rename_axis('리전').reset_index()                
    elif 'DBMS' in df:
        df_filtered = df.loc[(df['월']=='6월') & (df['테넌트']== 'PRD')]
        pivotTable = pd.pivot_table(df_filtered[['리전', 'DBMS', 'count']], index = ['리전'], aggfunc = 'sum').rename_axis('리전').reset_index()        
    elif 'count' in df:
        df_filtered = df.loc[(df['월']=='6월') & (df['테넌트']== 'PRD')]
        pivotTable = pd.pivot_table(df_filtered[['리전', 'count']], index = ['리전'], aggfunc = 'sum').rename_axis('리전').reset_index() 
    elif 'k8s클러스터명' in df:
        df_filtered = df.loc[(df['월']=='6월') & (df['테넌트']== 'PRD')]
        pivotTable = pd.pivot_table(df_filtered[['리전', 'k8s클러스터명']], index = ['리전'], aggfunc = 'count').rename_axis('리전').reset_index()           
    else:
        df_filtered = df.loc[(df['월']=='6월') & (df['테넌트']== 'PRD') & (df['진행상태']=='완료')]
        pivotTable = pd.pivot_table(df_filtered[['리전','진행상태']], index = ['리전'], aggfunc = 'count').rename_axis('리전').reset_index()
        
    # filtered.describe()
    # print(pivotTable)
    pivotTable.columns = ['리전', '합계']
    pivotTable.sort_values(by=['합계'], ascending=False, inplace=True)
    pivotTable.reset_index(drop=True, inplace=True)
    total = pivotTable["합계"].sum()
    pivotTable['비중'] = round(pivotTable['합계'] / total, 2) * 100
    return pivotTable, total

def getBarChart(source):
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

def getPieChart(source):
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

def getLineChart(source):
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

def getLineChart_am(source):
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

def getPointChart(source):
    # Scatter Plot
    points = alt.Chart(source).mark_point().encode(
        x='일:Q',
        y='소요시간:Q',
       # color=alt.condition(brush, '일:O', alt.value('grey'))
    ) #.add_selection(brush)

    chart = points
    return chart    
