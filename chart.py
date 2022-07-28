
import pandas as pd
from pandas import Series, DataFrame
from pandas_ods_reader import read_ods

import altair as alt
import pandas as pd
import re  

def hanfont():
    font = "맑은고딕"
    
    return {
        "config" : {
             "axis": {
                  "fontSize": 12,                
                  "font": font,
                  "anchor": "start", # equivalent of left-aligned.
                  "fontColor": "#000000"
             }
        }
    }
    

def getBarChart(source):
    bar = alt.Chart(source).mark_bar().encode(
        x=alt.X('리전'),
        y=alt.Y('count()', title=''),
        color=alt.Color("리전:N", legend=None)
    )
    text = bar.mark_text(
        align='center', # align='left',
        baseline='middle',
        dx=7  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='count():Q'
    )

    chart = (bar + text).properties(width=360, height=360)
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

    chart = (pie + text).properties(width=360, height=360)
    return chart

def getPieChart2(source):
    base = alt.Chart(source).encode(
        theta=alt.Theta("합계:Q", 
                        stack=True), 
        color=alt.Color("DBMS유형:N", legend=None)
    )

    pie = base.mark_arc(outerRadius=120)

    text = pie.mark_text(
        size=12,
        radius=160,        
        color='black'
    ).encode(
        text="label:N"
    ).transform_calculate(
        label = alt.datum.DBMS유형 + ": " + alt.datum.합계   + ", " + alt.datum.비중 +"%"
    )

    chart = (pie + text).properties(width=360, height=360)
    return chart

def getLineChart(df, month):
    source = df
    point = alt.Chart(source).mark_point().encode(
        x=alt.X('월', scale=alt.Scale(padding=15), title='월별 추세'),
        y=alt.Y('count()', title='발생 건수'),
        color=alt.Color('리전:N')
    )

    line = alt.Chart(source).mark_line(color="red").encode(
        x=alt.X('월', title='월별 추세'),
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

    chart = (point + line + text).properties(width=360, height=200)
    return chart

def getLineChart2(df, month):
    source = df    
    point = alt.Chart(source).mark_point().encode(
        x=alt.X('월', scale=alt.Scale(padding=15), title='월별 추세'),
        y=alt.Y('sum(count)', title='수량'),
        # text=alt.Text("성패:Q")
    )

    line = alt.Chart(source).mark_line(color="red").encode(
        x=alt.X('월', title='월별 추세'),
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

    chart = (point + line + text).properties(width=360, height=200)
    return chart


def getScatterChart(timeslot, month):
    
    # Brush for selection
    brush = alt.selection(type='interval')

    # Scatter Plot
    source = timeslot
    points = alt.Chart(source).mark_point().encode(
        x=alt.X('일:Q', scale=alt.Scale(padding=15), title='장애 발생 일'),
        y=alt.Y('장애전파:Q', title='장애전파 소요시간(분)'),
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
    chart = (points).properties(width=360, height=200)

    return chart
