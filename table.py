# %load chart.py

import pandas as pd
from pandas import Series, DataFrame
from pandas_ods_reader import read_ods

import altair as alt
import pandas as pd
import re  


def getTables(df, regex, month):
    df['장애전파'] = (pd.to_datetime(df['장애전파시간.1'])-pd.to_datetime(df['발생인지시간'])).astype('timedelta64[m]')
    df_filtered = df[df['리전'].apply(lambda x: True if re.search(regex, x) else False) & (df['테넌트']== 'PRD') & (df['진행상태']=='완료')]
    
    # df_filtered
    df_filtered['장애전파'] = (pd.to_datetime(df_filtered['장애전파시간.1'])-pd.to_datetime(df_filtered['발생인지시간'])).astype('timedelta64[m]')
    df_filtered['장애전파시간.1'] = pd.to_datetime(df_filtered['장애전파시간.1'])
    
    # timeslot
    timeslot = df_filtered[df_filtered['월']== month]
    timeslot  = timeslot[['장애전파시간.1', '장애전파', '리전']]
    timeslot.columns = ['일', '장애전파', '리전']
    
    timeslot['일'] = timeslot['일'].dt.day
    # timeslot['장애전파'] = timeslot['장애전파'].astype('timedelta64[m]')
    timeslot.sort_values(by=['일'], ascending=True, inplace=True)
    # timeslot
    return df_filtered, timeslot

def getPivotTable(df, month):
    
    if '자원유형' in df:
        df_filtered = df.loc[(df['월']==month) & (df['테넌트']== 'PRD') & (df['진행상태']=='완료')]
        pivotTable = pd.pivot_table(df_filtered[['리전','진행상태']], index = ['리전'], aggfunc = 'count').rename_axis('리전').reset_index()
        pivotTable.columns = ['리전', '합계']
        pivotTable.sort_values(by=['합계'], ascending=False, inplace=True)
        pivotTable.reset_index(drop=True, inplace=True)
        total = pivotTable["합계"].sum()
        pivotTable['비중'] = round((pivotTable['합계'] / total) * 100, 1)        
    elif 'k8s클러스터명' in df:
        df_filtered = df.loc[(df['월']==month) & (df['테넌트']== 'PRD')]
        pivotTable = pd.pivot_table(df_filtered[['리전', 'k8s클러스터명']], index = ['리전'], aggfunc = 'count').rename_axis('리전').reset_index()    
        pivotTable.columns = ['리전', '합계']
        pivotTable.sort_values(by=['합계'], ascending=False, inplace=True)
        pivotTable.reset_index(drop=True, inplace=True)
        total = pivotTable["합계"].sum()
        pivotTable['비중'] = round((pivotTable['합계'] / total) * 100, 1)       
    elif 'count' in df:
        df_filtered = df.loc[(df['월']==month) & (df['테넌트']== 'PRD')]
        pivotTable = pd.pivot_table(df_filtered[['리전', 'count']], index = ['리전'], aggfunc = 'sum').rename_axis('리전').reset_index() 
        pivotTable["합계"] = pivotTable.sum(axis=1)
        pivotTable.sort_values(by=['합계'], ascending=False, inplace=True)
        total = pivotTable["합계"].sum()
        pivotTable['비중'] = round((pivotTable['합계'] / total) * 100, 1)
    else:
        pivotTable, total = None, None

    # elif 'DBType' in df:
    #     df_filtered = df.loc[(df['월']==month) & (df['테넌트']== 'PRD')]
    #     pivotTable = pd.pivot_table(df_filtered[['리전', 'DBType']], index = ['리전'], aggfunc = 'count').rename_axis('리전').reset_index()                
    # elif 'DBMS유형' in df:
    #     # 자산관리 DB
    #     df_filtered = df.loc[(df['월']==month) & (df['테넌트']== 'PRD')]
    #     pivotTable = pd.pivot_table(df_filtered[['리전', 'DBMS유형', 'count']], index = ['리전'], aggfunc = 'sum').rename_axis('리전').reset_index()        
    # elif 'count' in df:
    #     df_filtered = df.loc[(df['월']==month) & (df['테넌트']== 'PRD')]
    #     pivotTable = pd.pivot_table(df_filtered[['리전', 'count']], index = ['리전'], aggfunc = 'sum').rename_axis('리전').reset_index() 
        
    # else:
    #     df_filtered = df.loc[(df['월']==month) & (df['테넌트']== 'PRD') & (df['진행상태']=='완료')]
    #     pivotTable = pd.pivot_table(df_filtered[['리전','진행상태']], index = ['리전'], aggfunc = 'count').rename_axis('리전').reset_index()
        
    # filtered.describe()
    # print(pivotTable)
    # pivotTable.columns = ['리전', '합계']
    # pivotTable.sort_values(by=['합계'], ascending=False, inplace=True)
    # pivotTable.reset_index(drop=True, inplace=True)
    # total = pivotTable["합계"].sum()
    # pivotTable['비중'] = round((pivotTable['합계'] / total) * 100, 1)
    return pivotTable, total


def getPivotTable2(df, month):
    # 집계 데이터
    if 'count' in df:
        df_filtered = df.loc[(df['월']==month) & (df['테넌트']== 'PRD')]
        pivotTable = pd.pivot_table(df_filtered[['리전', '유형', 'count']], values = 'count', index = ["유형"], columns = ["리전"], aggfunc = 'sum')
        pivotTable["합계"] = pivotTable.sum(axis=1)
    else:
        pivotTable, total = None, None
        
    pivotTable.sort_values(by=['합계'], ascending=False, inplace=True)
    total = pivotTable["합계"].sum()
    pivotTable['비중'] = round((pivotTable['합계'] / total) * 100, 1)
    return pivotTable, total
