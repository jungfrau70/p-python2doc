# %load chart.py

import pandas as pd
from pandas import Series, DataFrame
from pandas_ods_reader import read_ods

import altair as alt
import pandas as pd
import re  

#from io import BytesIO
#memfile = BytesIO()

#def getTable(df, regex, month):
#    df_filtered = df[df['리전'].apply(lambda x: True if re.search(regex, x) else False) & (df['테넌트']== 'PRD') & (df['진행상태']=='완료') & (df['월간']=='O')]
#    table = df_filtered[df_filtered['월'] == month].reset_index()
#    table = table[['리전', '테넌트', '진행상태', '성패', 'Description']]
    # dfi.export(table, 'table.png')
#    return table

def getTables(df, regex, month):
    df['장애전파'] = (pd.to_datetime(df['장애전파시간.1'])-pd.to_datetime(df['발생인지시간'])).astype('timedelta64[m]')
    df_filtered = df[df['리전'].apply(lambda x: True if re.search(regex, x) else False) & (df['월']== month) & (df['테넌트']== 'PRD') & (df['진행상태']=='완료')]
    # df_filtered
    df_filtered['장애전파'] = (pd.to_datetime(df_filtered['장애전파시간.1'])-pd.to_datetime(df_filtered['발생인지시간'])).astype('timedelta64[m]')
    df_filtered['장애전파시간.1'] = pd.to_datetime(df_filtered['장애전파시간.1'])
    timeslot  = df_filtered[['장애전파시간.1', '장애전파', '리전']]
    # timeslot
    timeslot.columns = ['일', '장애전파', '리전']
    # timeslot.info()
    timeslot['일'] = timeslot['일'].dt.day
    # timeslot['장애전파'] = timeslot['장애전파'].astype('timedelta64[m]')
    timeslot.sort_values(by=['일'], ascending=True, inplace=True)
    # timeslot
    return df, timeslot

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

def getLineChart(df):
    source = df
    point = alt.Chart(source).mark_point().encode(
        x=alt.X('월'),
        y=alt.Y('count()'),
        # text=alt.Text("성패:Q")
    )

    line = alt.Chart(source).mark_line(color="red").encode(
        x=alt.X('월'),
        y=alt.Y('count()', title='')
    )

    text = point.mark_text(
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


def getScatterChart(timeslot, month):
    
    # Brush for selection
    brush = alt.selection(type='interval')

    # Scatter Plot
    source = timeslot
    points = alt.Chart(source).mark_point().encode(
        x=alt.X('일:Q', scale=alt.Scale(padding=15), title='장애 발생 일'),
        y=alt.Y('장애전파:Q', title='장애전파 시간(분)'),
        color=alt.Color('리전:N')
    ).add_selection(brush)

    points

    # Base chart for data tables
    ranked_text = alt.Chart(source).mark_text(align='right').encode(
        y=alt.Y('row_number:O',axis=None)
    ).transform_filter(
        brush
    )
    
    #.transform_window(
    #    row_number='row_number()'
    #).transform_filter(
    #    'datum.row_number < 15'
    #)

    
    #chart = points + ranked_text
    chart = points
    return chart
