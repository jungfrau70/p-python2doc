# %load table.py

import pandas as pd
from pandas import Series, DataFrame
from pandas_ods_reader import read_ods

import altair as alt
import pandas as pd
import re  

def flatten_1d(input):
    new_list = []
    for i in input:
        for j in i:
            new_list.append(j)
    return new_list

def counter(df, regex):
    region_count = 0    
    regions = []
    
    for s in df['리전']:
        list = re.split(',|/|\|', s)
        regions.append(list)

    for s in flatten_1d(regions):
        for match in re.finditer(regex, s):
            region_count += 1    
            
    return region_count

def flatten_2d(data):
    regions = []
    regions_flatten = []
    regions_count = []  

    for s in data['리전']:
        list = re.split(',|/|\|', s)
        regions.append(list)

    region_list = []
    statuses_list = []
    for r, s in zip(regions, data['진행상태']):
        for item in r:
            region_list.append(item)
            statuses_list.append(s)          

    data = pd.DataFrame(zip(region_list, statuses_list))
    data.columns = ['리전', '진행상태']
    
    return data    

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
    elif '작업_Title' in df:
        # 
        df_filtered = df.loc[(df['월']==month) & (df['테넌트']== 'PRD')]
        pivotTable = pd.pivot_table(df_filtered[['리전','진행상태']], index = ['리전'], aggfunc = 'count').rename_axis('리전').reset_index()
        pivotTable.columns = ['리전', '합계']
        pivotTable.sort_values(by=['합계'], ascending=False, inplace=True)
        pivotTable.reset_index(drop=True, inplace=True)
        total = pivotTable["합계"].sum()
        pivotTable['비중'] = round((pivotTable['합계'] / total) * 100, 1) 
    elif '클러스터명' in df:
        # 자산관리 K8s
        df_filtered = df.loc[(df['월']==month) & (df['테넌트']== 'PRD')]
        pivotTable = pd.pivot_table(df_filtered[['리전', '클러스터명']], index = ['리전'], aggfunc = 'count').rename_axis('리전').reset_index()    
        pivotTable.columns = ['리전', '합계']
        pivotTable.sort_values(by=['합계'], ascending=False, inplace=True)
        pivotTable.reset_index(drop=True, inplace=True)
        total = pivotTable["합계"].sum()
        pivotTable['비중'] = round((pivotTable['합계'] / total) * 100, 1)
    elif '라이선스 종류' in df:
        # 집계
        df_filtered = df.loc[(df['월']==month) & (df['테넌트']== 'PRD')]
        pivotTable = pd.pivot_table(df_filtered[['리전', '라이선스 종류']], index = ['리전'], aggfunc = 'count').rename_axis('리전').reset_index()       
        pivotTable.columns = ['리전', '합계']
        pivotTable.sort_values(by=['합계'], ascending=False, inplace=True)
        pivotTable.reset_index(drop=True, inplace=True)
        total = pivotTable["합계"].sum()
        pivotTable['비중'] = round((pivotTable['합계'] / total) * 100, 1)    
    elif '성패' in df:
        # 백업관리 DB
        df_filtered = df.loc[(df['월']==month) & (df['테넌트']== 'PRD')]
        pivotTable = pd.pivot_table(df_filtered[['리전', '성패']], index = ['리전'], aggfunc = 'count').rename_axis('리전').reset_index()       
        pivotTable.columns = ['리전', '합계']
        pivotTable.sort_values(by=['합계'], ascending=False, inplace=True)
        pivotTable.reset_index(drop=True, inplace=True)
        total = pivotTable["합계"].sum()
        pivotTable['비중'] = round((pivotTable['합계'] / total) * 100, 1)        
    elif 'count' in df:
        # 집계
        df_filtered = df.loc[(df['월']==month) & (df['테넌트']== 'PRD')]
        pivotTable = pd.pivot_table(df_filtered[['리전', 'count']], index = ['리전'], aggfunc = 'sum').rename_axis('리전').reset_index() 
        pivotTable["합계"] = pivotTable.sum(axis=1)
        pivotTable.sort_values(by=['합계'], ascending=False, inplace=True)
        total = pivotTable["합계"].sum()
        pivotTable['비중'] = round((pivotTable['합계'] / total) * 100, 1)
    else:
        # 표준 데이터
        df_filtered = df.loc[(df['월']==month) & (df['테넌트']== 'PRD') & (df['진행상태']=='완료')]
        pivotTable = pd.pivot_table(df_filtered[['리전','진행상태']], index = ['리전'], aggfunc = 'count').rename_axis('리전').reset_index()
        pivotTable.columns = ['리전', '합계']
        pivotTable.sort_values(by=['합계'], ascending=False, inplace=True)
        pivotTable.reset_index(drop=True, inplace=True)
        total = pivotTable["합계"].sum()
        pivotTable['비중'] = round((pivotTable['합계'] / total) * 100, 1)

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


def getPivotTable_security(df, month):
   
    # 표준 데이터
    df_filtered = df.loc[(df['월']==month) & (df['테넌트']== 'PRD') ]
    # df_filtered = df.loc[(df['월']==month) & (df['테넌트']== 'PRD') & (df['진행상태']=='완료')]
    
    pivotTable = pd.pivot_table(df_filtered[['리전','진행상태']], index = ['리전'], aggfunc = 'count').rename_axis('리전').reset_index()
    pivotTable.columns = ['리전', '합계']
    pivotTable.sort_values(by=['합계'], ascending=False, inplace=True)
    pivotTable.reset_index(drop=True, inplace=True)
    total = pivotTable["합계"].sum()
    pivotTable['비중'] = round((pivotTable['합계'] / total) * 100, 1)

    return pivotTable, total

def getPivotTable_event(df_filtered, month, region_list):

    #pivotTable = pd.pivot_table(df_filtered[['리전','진행상태']], index = ['리전','진행상태'], aggfunc = 'count').rename_axis('리전').reset_index()
    pivotTable = pd.pivot_table(df_filtered[['진행상태','리전','월간']], index = ['진행상태','리전'], aggfunc = 'count').rename_axis(['진행상태','리전']).reset_index()
    pivotTable.columns = ['진행상태','리전', '합계']
    
    pivot = pivotFlatten_2c(pivotTable, region_list)
    
    pivot.sort_values(by=['합계'], ascending=False, inplace=True)
    pivot.reset_index(drop=True, inplace=True)
    total = pivot["합계"].sum()
    pivot['비중'] = round((pivot['합계'] / total) * 100, 1)

    return df_filtered, pivot, total

def pivotFlatten_2c(pivotTable, region_list):
    regions = []
    counts = []
    statuses = []
    region_flatten = []
    status_flatten = []
    countByRegion = []
    completed_countByRegion = []
    incompleted_countByRegion = []

    for index, row in pivotTable.iterrows():
        list = re.split(',|/|\|', row['리전'])
        regions.append(list)
        counts.append(row['합계'])
        statuses.append(row['진행상태'])
    for (c, r, s) in zip(counts, regions, statuses):
        for j in r:
            region_flatten.append(j * c)
            status_flatten.append(s)
            
    for r in region_list:
        regex = r
        region_count = 0
        for s in region_flatten:
            for match in re.finditer(regex, s):
                region_count += 1
        countByRegion.append(region_count)
        
    for r in region_list:
        regex = r
        complete_count = 0
        incomplete_count = 0
        for rf, sf in zip(region_flatten, status_flatten):
            for match in re.finditer(regex, rf):
                for match in re.finditer("완료", sf):
                    complete_count += 1
                for match in re.finditer("진행중", sf):
                    incomplete_count += 1
        completed_countByRegion.append(complete_count)
        incompleted_countByRegion.append(incomplete_count)
        
    pivot = pd.DataFrame((zip(region_list, countByRegion, completed_countByRegion, incompleted_countByRegion )), columns=['리전', '합계', '완료', '미완료'])       
    
    return pivot       
    
    
def pivotFlatten(pivotTable, region_list):
    regions = []
    counts = []
    pivot_flatten = []
    countByRegion = []
    complete_countByRegion = []
    incomplete_countByRegion = []
    
    for index, row in pivotTable.iterrows():
        list = re.split(',|/|\|', row['리전'])
        regions.append(list)
        counts.append(row['합계'])

    for (c, r) in zip(counts, regions):
        for j in r:
            pivot_flatten.append(j * c)

    for r in region_list:
        regex = r
        region_count = 0
        for s in pivot_flatten:
            for match in re.finditer(regex, s):
                region_count += 1
        countByRegion.append(region_count)

    for r in region_list:
        regex = r
        complete_count = 0
        incomplete_count = 0
        for s in pivotTable['진행상태']:
            if s == '완료':
                complete_count += 1
            else:
                incomplete_count += 1
        complete_countByRegion.append(complete_count)
        incomplete_countByRegion.append(incomplete_count)
        
    pivot = pd.DataFrame((zip(region_list, countByRegion, complete_count, incomplete_count )), columns=['리전', '합계', '완료', '미완료'])
    return pivot    

def getPivotTable_capacity(df, month):
   
    # 표준 데이터
    df_filtered = df.loc[(df['월']==month) & (df['테넌트']== 'PRD') ]
    # df_filtered = df.loc[(df['월']==month) & (df['테넌트']== 'PRD') & (df['진행상태']=='완료')]
    
    pivotTable = pd.pivot_table(df_filtered[['리전','카테고리']], index = ['리전'], aggfunc = 'count').rename_axis('리전').reset_index()
    pivotTable.columns = ['리전', '합계']
    pivotTable.sort_values(by=['합계'], ascending=False, inplace=True)
    pivotTable.reset_index(drop=True, inplace=True)
    total = pivotTable["합계"].sum()
    pivotTable['비중'] = round((pivotTable['합계'] / total) * 100, 1)

    return pivotTable, total

