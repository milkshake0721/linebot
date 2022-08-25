import requests
import pandas as pd
import numpy as np
import datetime
from bs4 import BeautifulSoup
import re
import json
import csv

def pay(query):
    url = "https://yahoo-finance97.p.rapidapi.com/stock-info"

    payload = "symbol=" + query + '&period=1d'
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "ece950ca5fmsh02f019c5d4464efp1afb3bjsndb9ae3b18724",
        "X-RapidAPI-Host": "yahoo-finance97.p.rapidapi.com"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    a = response.json()
    # print(a)
    return a['data']['regularMarketPrice']

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
    if stockID == 0 or stockID == '加權':
        return pay('^TWII')

    elif stockID[0] <= '9':
        pass
    else:
        with open('fonglinebot/stocks.csv', mode='r') as infile:
            reader = csv.reader(infile)
            with open('coors_new.csv', mode='w') as outfile:
                writer = csv.writer(outfile)
                mydict = {rows[1]:rows[0] for rows in reader}
        stockID = mydict[stockID]

    link = 'http://mis.twse.com.tw/stock/api/getStockInfo.jsp?json=1&delay=0&ex_ch=tse_'+ str(stockID) +'.tw'
    # link = 'http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_2330.tw&json=1&delay=0'
    # print(link)
    r = requests.post(link)
    sel = r.json()['msgArray'][0]
    if sel['z'] == '-' :
        now = now = sel['a'][:6]
    else:
        now = sel['z']
    change = (float(now)) - (float(sel['o']))
    change = round(change, 2)
    change_p = (float(now) - float(sel['o'])) / float(sel['o']) * 100
    change_p = round(change_p, 2)
    all = stockID + '  \n'+ sel['n'] + '\n' + str(round(float(now),2)) + ' (' + str(change_p) + '%)' + '\n===================\n' + '開盤價格 : '+ str(round(float(sel['o']),2)) + '\n===================' + '\n價格變動 : ' + str(change) + '\n昨日收盤 : '+ str(round(float(sel['y']),2)) + '\n今日最高 : ' + str(round(float(sel['h']),2)) + '\n今日最低 : '+ str(round(float(sel['l']),2)) + '\n==================='
    return all    

'''
<型別名稱>汽柴油零售</型別名稱>
    <產品編號>113F 1209800</產品編號>
    <產品名稱>98無鉛汽油</產品名稱>
    <包裝>散裝</包裝>
    <銷售對象>一般自用客戶 </銷售對象>
    <交貨地點>中油自營站</交貨地點>
    <計價單位>元/ 公升</計價單位>
    <參考牌價>34.7</參考牌價>
    <營業稅>5%</營業稅>
    <貨物稅>內含</貨物稅>
    <牌價生效時間>20220328</牌價生效時間>
'''
def oil_price():
    url = 'http://vipmbr.cpc.com.tw/CPCSTN/ListPriceWebService.asmx/getCPCMainProdListPrice_XML'
    r = requests.post(url)
    tx = r.text
    oil_name = {}
    oil_98_h = tx.find('<產品名稱>')+6
    oil_98_e = tx.find('</產品名稱>')
    price_h = tx.find('<參考牌價>')+6
    price_e = tx.find('</參考牌價>')
    for i in range(5): 
        name = tx[oil_98_h:oil_98_e]
        price = tx[price_h:price_e]
        oil_name[name] = price
        oil_98_h = tx.find('<產品名稱>',oil_98_e)+6
        oil_98_e = tx.find('</產品名稱>',oil_98_h)
        price_h = tx.find('<參考牌價>',price_e)+6
        price_e = tx.find('</參考牌價>',price_h)
    all = '98無鉛汽油 |' + oil_name['98無鉛汽油'] + '元' + '\n95無鉛汽油 |' + oil_name['95無鉛汽油'] + '元' + '\n92無鉛汽油 |' + oil_name['92無鉛汽油'] + '元' + '\n99柴柴汽油 |' + oil_name['超級柴油'] + '元' + '\n58酒精汽油 |' + oil_name['酒精汽油'] + '元'

    return all

def eggprice():
    # /api/v1/PoultryTransType_BoiledChicken_Eggs?Start_time=交易日期(起)&Start_time=交易日期(起)&End_time=交易日期(迄)&Start_time=交易日期(起)&End_time=交易日期(迄)
    url = 'https://data.coa.gov.tw/api/v1/PoultryTransType_BoiledChicken_Eggs'
    #'/api/v1/PoultryTransType_BoiledChicken_Eggs'
    r = requests.get(url)
    egg = r.json()['Data'][0]['egg_TaijinPrice']
    return egg + ' 元/台斤'

'''
 "RS": "OK",
  "Data": [
    {
      "TransDate": "2022/03/29",
      "LunarCalendar": "廿七",
      "RedFeather_N": "41.0",
      "RedFeather_C": "42.0",
      "RedFeather_S": "-",
      "BlackFeather_S_M": "46.0",
      "BlackFeather_S_F": "46.0"
    }
'''

def chickenprice():
    url = 'https://data.coa.gov.tw/api/v1/PoultryTransType_BoiledChicken_Eggs'
    url_to_chicken = 'https://data.coa.gov.tw/api/v1/PoultryTransType_Chicken'
    r = requests.get(url)
    r_to = requests.get(url_to_chicken)
    w_chicken = r.json()['Data'][0]['Store_KP_TaijinPrice']
    r_chicken = r_to.json()['Data'][0]['RedFeather_N']
    b_chicken = r_to.json()['Data'][0]['BlackFeather_S_F']

    all = '一般白雞 ' + w_chicken + ' 元/台斤\n紅羽土雞 ' + r_chicken + ' 元/台斤\n黑羽土雞 ' + b_chicken + ' 元/台斤'
    return all
# print(oil_price())
# def makepretty(ans):
#     a = 0
# num = '富邦公司治理'
# a = gettwstock(num)
# print(eggprice())
# print (a)
# print(a['證券代號'] == num)
# print(a['證券名稱'])
# print(gettwstock('2330'))
# print(gettwstock(0))
