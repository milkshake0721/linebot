from tkinter import END
import requests
import pandas as pd
import numpy as np
import datetime
from bs4 import BeautifulSoup
import soupsieve
import json
import csv

def conv_to_list(obj):
    '''
    將物件轉換為list
    '''
    if not isinstance(obj, list) :
        results = [obj]
    else:
        results = obj
    return results


def df_conv_col_type(df, cols, to, ignore=False):
    '''
    一次轉換多個欄位的dtype
    '''
    cols = conv_to_list(cols)
    for i in range(len(cols)):
        if ignore :
            try:
                df[cols[i]] = df[cols[i]].astype(to)
            except:
                print('df_conv_col_type - ' + cols[i] + '轉換錯誤')
                continue
        else:
            df[cols[i]] = df[cols[i]].astype(to)
    return df


def date_get_today(with_time=False):
    '''
    取得今日日期，並指定為台北時區
    '''
    import pytz
    central = pytz.timezone('Asia/Taipei')
    
    if with_time == True:
        now = datetime.datetime.now(central)
    else:
        now = datetime.datetime.now(central).date()
    return now


def gettwstock(stockID):
    if stockID[0] <= '9':
        pass
    else:
        with open('fonglinebot/stocks.csv', mode='r') as infile:
            reader = csv.reader(infile)
            with open('coors_new.csv', mode='w') as outfile:
                writer = csv.writer(outfile)
                mydict = {rows[1]:rows[0] for rows in reader}
        stockID = mydict[stockID]

    link = 'http://mis.twse.com.tw/stock/api/getStockInfo.jsp?json=1&delay=0&ex_ch=tse_'+ stockID +'.tw'
    # link = 'http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_2330.tw&json=1&delay=0'
    # print(link)
    r = requests.post(link)
    sel = r.json()['msgArray'][0]
    change = float(sel['z']) - float(sel['o'])
    change = round(change, 2)
    change_p = (float(sel['z']) - float(sel['o'])) / float(sel['o']) * 100
    change_p = round(change_p, 2)
    all = stockID + '  \n'+ sel['n'] + '\n\n' + str(round(float(sel['z']),2)) + ' (' + str(change_p) + '%)' + '\n\n===================\n' + '開盤價格 : '+ str(round(float(sel['o']),2)) + '\n===================' + '\n\n價格變動 : ' + str(change) + '\n昨日收盤 : '+ str(round(float(sel['y']),2)) + '\n今日最高 : ' + str(round(float(sel['h']),2)) + '\n今日最低 : '+ str(round(float(sel['l']),2)) + '\n\n===================\n '

    print(all)
    return     # T表示行列互換

# def makepretty(ans):
#     a = 0
# num = '富邦公司治理'
# a = gettwstock(num)

# print (a)
# print(a['證券代號'] == num)
# print(a['證券名稱'])

gettwstock('富邦公司治理')
