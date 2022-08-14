
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

# def getStackedHBarChart(source):
#     bar = alt.Chart(source).mark_bar().encode(
#         x=alt.X('count(리전):Q', stack='zero', title=''),         
#         y=alt.Y('진행상태:O'),        
#         color=alt.Color('리전:N') #, legend=None)   
#     )
#     text1 = alt.Chart(source).mark_text(dx=0, dy=3, color='black').encode(
#         x=alt.X('진행상태:O'),        
#         y=alt.Y('count(리전):Q', stack='zero', title=''), 
#         color=alt.Color('리전:N'), # legend=None)   
#         text = alt.Text('count(리전):Q', format='d')
#         # text = alt.Text('sum(count):Q', format='d')        
#     ) 
#     chart = (bar + text1).properties(width=360, height=360)
#     return chart


def getStackedHBarChart(source):
    bar = alt.Chart(source).mark_bar().encode(
        x=alt.X('count(리전):Q', stack='zero', title=''),         
        y=alt.Y('진행상태:O', sort='ascending'),  
        # order=alt.Order("count(리전):Q", sort='descending'),
        color=alt.Color('리전:N') #, legend=None)   
    )
    
    text1 = alt.Chart(source).mark_text(dx=-20, dy=0, color='black').encode(
        x=alt.X('count(리전):Q', stack='zero', sort='ascending'),        
        y=alt.Y('진행상태:N', sort='ascending'),        
        detail=alt.Color("리전:N"),
        text = alt.Text('count(리전):Q', format='d') #, sort='descending')
    )
    
    text2 = alt.Chart(source).mark_text(dx=10, dy=-3, color='black').encode(
        x=alt.X('count(리전):Q', stack='zero', title=''),         
        y=alt.Y('진행상태:N'),        
        # order=alt.Order("count(리전):Q", sort='descending'),
        # color=alt.Color('리전:N'), # legend=None)   
        text = alt.Text('count(리전):Q', format='d')
        # text = alt.Text('sum(count):Q', format='d')        
    ) 
    
    chart = (bar + text1 + text2).properties(width=360, height=360)
    return chart

def getStackedHBarChart1(source):
    bar = alt.Chart(source).mark_bar().encode(
        x=alt.X('sum(count):Q', stack='zero', title=''),
        y=alt.Y('월:N'),
        color=alt.Color("유형:N") #, legend=None)   
    )
    line = alt.Chart(source).mark_line(color="red").encode(
        x=alt.X('sum(count):Q', title=''),
        y=alt.Y('월:N', title='월별 추세')
    )
    text1 = alt.Chart(source).mark_text(dx=0, dy=3, color='black').encode(
        x=alt.X('sum(count):Q', stack='zero'),
        y=alt.Y('월:N'),
        detail=alt.Color("유형:N"),
        text = alt.Text('sum(count):Q', format='d')
    )
    text2 = line.mark_text(dx=20, dy=0, color='red').encode(
        x=alt.X('sum(count):Q'),
        y=alt.Y('월:N'),
        text = alt.Text('sum(count):Q', format='d')
    )    
    chart = (bar + line + text1 + text2).properties(width=360, height=360)
    return chart


def getStackedVBarChart1(source):
    bar = alt.Chart(source).mark_bar().encode(
        x=alt.X('월:N', stack='zero', title=''),
        y=alt.Y('sum(count):Q'),
        color=alt.Color("유형:N") #, legend=None)   
    )
    line = alt.Chart(source).mark_line(color="red").encode(
        x=alt.X('월:N', title=''),
        y=alt.Y('sum(count):Q', title='월별 추세')
    )
    text1 = alt.Chart(source).mark_text(dx=-20, dy=0, color='black').encode(
        x=alt.X('월:N'),        
        y=alt.Y('sum(count):Q', stack='zero'),     
        detail=alt.Color("유형:N"),
        text = alt.Text('sum(count):Q', format='d')
    )
    text2 = line.mark_text(dx=0, dy=-15, color='red').encode(
        x=alt.X('월:N'),        
        y=alt.Y('sum(count):Q'),
        text = alt.Text('sum(count):Q', format='d')
    )        
    chart = (bar + line + text1 + text2).properties(width=360, height=360)
    return chart    

    
def getBarChart1(source):
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

def getBarChart1s(source, month):
    
    bar = alt.Chart(source).mark_bar().encode(
        x=alt.X('유형:N'),
        y=alt.Y('sum(count)', title=''),
        color=alt.Color("유형:N", legend=None)
    )
    text = bar.mark_text(
        align='center', # align='left',
        baseline='middle',
        dx=7  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='sum(count):Q'
    )

    chart = (bar + text).properties(width=360, height=360)
    return chart

def getBarChart2(source, month):
    bar = alt.Chart(source).mark_bar().encode(
        x=alt.X('월'),
        y=alt.Y('count()', title=''),
        color=alt.Color("성패:N", legend=None)
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


def getBarChart2s(source, month):
    
    bar = alt.Chart(source).mark_bar().encode(
        x=alt.X('월:N'),
        y=alt.Y('sum(count)', title=''),
        color=alt.Color("유형:N", legend=None)
    )
    text = bar.mark_text(
        align='left', # align='center',
        baseline='top', # baseline='middle',
        dx=7  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='sum(count):Q'
    )

    chart = (bar + text).properties(width=360, height=360)
    return chart

def getBarChart3s(source, month):
    
    bar = alt.Chart(source).mark_bar().encode(
        x=alt.X('유형:N'),
        y=alt.Y('sum(count)', title=''),
        color=alt.Color("유형:N", legend=None)
    )
    text = bar.mark_text(
        align='center', # align='left',
        baseline='middle',
        dx=7  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='sum(count):Q'
    )

    chart = (bar + text).properties(width=360, height=360)
    return chart

def getPieChart(source):
    base = alt.Chart(source).encode(
        theta=alt.Theta("합계:Q", stack=True), 
        color=alt.Color("리전:N", legend=None),
        order=alt.Order("합계:Q", sort='descending')
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
        theta=alt.Theta("합계:Q", stack=True), 
        color=alt.Color("DBMS유형:N", legend=None),
        order=alt.Order("합계:Q", sort='descending')
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

def getLineChart2(df, month):
    source = df
    point = alt.Chart(source).mark_point().encode(
        x=alt.X('월', scale=alt.Scale(padding=15), title='월별 추세'),
        y=alt.Y('count()', title='발생 건수')
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

def getLineChart2s(df, month):
    source = df    
    point = alt.Chart(source).mark_point().encode(
        x=alt.X('월', scale=alt.Scale(padding=15), title='월별 추세'),
        y=alt.Y('sum(count)', title='수량'),
        text=alt.Text("성패:N")
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

def getLineChart3(df, month):
    source = df
    point = alt.Chart(source).mark_point().encode(
        x=alt.X('월', scale=alt.Scale(padding=15), title='월별 추세'),
        y=alt.Y('count()', title='발생 건수'),
        color=alt.Color('성패:N')
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

def getBarChart4s(source, month):
    
    bar = alt.Chart(source).mark_bar().encode(
        x=alt.X('라이선스 종류:N', title=['유형별 라이선스 수']),
        y=alt.Y('count(라이선스 종류)', title=''),
        color=alt.Color("유형:N", legend=None)
    )
    text = bar.mark_text(
        align='left', # align='center',
        baseline='top', # baseline='middle',
        dx=7  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='count(라이선스 종류):Q'
    )
    text2 = bar.mark_text(
        size=12,
        align='center',
        baseline='line-top',
        color='black',
        dy=-20,
        fontSize=12,
    ).encode(
        text = 'count(라이선스 종류):Q'
    )	

    chart = (bar + text + text2).properties(width=360, height=360)
    return chart



def getLineChart4s(df, month):
    source = df    
    point = alt.Chart(source).mark_point().encode(
        x=alt.X('월', scale=alt.Scale(padding=15), title='월별 추세'),
        y=alt.Y('count(라이선스 종류)', title='수량'),
        text=alt.Text("라이선스 종류:N")
    )

    line = alt.Chart(source).mark_line(color="red").encode(
        x=alt.X('월', title='월별 추세'),
        y=alt.Y('count(라이선스 종류)', title='')
    )

    text = point.mark_text(
        size=12,
        align='center',
        baseline='line-top',
        color='black',
        dy=-20,
        fontSize=12,
    ).encode(
        text = 'count(라이선스 종류):Q'
    )

    chart = (point + line + text).properties(width=360, height=200)
    return chart
