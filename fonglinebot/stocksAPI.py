from genericpath import exists
from re import A
from aiohttp import request
import finnhub
import requests
import datetime
from bs4 import BeautifulSoup
import json,re
import fear_and_greed

def pay():
    url = "https://yahoo-finance97.p.rapidapi.com/stock-info"
    index_all = ['^GSPC','^DJI','^IXIC']
    an = []
    for i in index_all:
        payload = "symbol=" + i + '&period=1d'
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "X-RapidAPI-Key": "ece950ca5fmsh02f019c5d4464efp1afb3bjsndb9ae3b18724",
            "X-RapidAPI-Host": "yahoo-finance97.p.rapidapi.com"
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        a = response.json()['data']['regularMarketPrice']
        an.append(a)

    ans = 'S&P 500 {}\nDOW 30  {}\nNASDAQ  {}'.format(an[0],an[1],an[2])
    return ans

def stockapi(ID):
    if ID == '我要指數':
        all = pay()
    else:
        ID = ID.upper()
        datetime_dt = datetime.datetime.today()
        today = datetime_dt.strftime("%Y-%m-%d")
        oneday = datetime.timedelta(days=1)
        yesterday = datetime_dt - oneday
        tomarrow = datetime_dt + oneday
        yesterday = yesterday.strftime("%Y-%m-%d")
        tomarrow = tomarrow.strftime("%Y-%m-%d")
        finnhub_client = finnhub.Client(api_key="c8k6sqaad3i8fk1kn8ag")
        ans = finnhub_client.quote(ID)
        # print(ans)
        news = finnhub_client.company_news(ID, _from = yesterday , to = today)
        # print(news)
        if news == []:
            news = [{'headline':'','url':''}]
            news[0]['headline'] = 'N/A'
            news[0]['url'] = 'N/A'
        ans.pop('t')
        # all = news[0]['url']
        all = ID + ' ( ' +str(ans['dp']) + '% )\n現在價格 : ' + str(ans['c']) + '\n-------------------\n變動價格 : ' + str(ans['d']) + '\n今日最高 : ' + str(ans['h']) + '\n今日最低 : '+ str(ans['l']) + '\n開市價格 : '+ str(ans['o']) + '\n上次閉市 : '+ str(ans['pc']) + '\n-------------------\n新聞 : '+ news[0]['headline']+ '\n' + news[0]['url']
    return all

# print(stockapi('hl'))

def currency():
    finnhub_client = finnhub.Client(api_key="sandbox_c8k6qfaad3i8fk1kn7c0")
    _currency = finnhub_client.forex_rates(base = 'TWD')
    qu = _currency['quote']
    usd = str(round(1/qu['USD'],3))
    jpy = str(round(1/qu['JPY'],3))
    eur = str(round(1/qu['EUR'],3))
    rmb = str(round(1/qu['CNY'],3))
    aud = str(round(1/qu['AUD'],3))
    all = '美金 : ' + usd + '\n日幣 : '+ jpy +'\n歐元 : ' + eur + '\n人民幣:' + rmb  + '\n澳幣 : ' + aud
    # print('美金 : ' + usd + '\n日幣 : '+ jpy +'\n歐元 : ' + eur )
    return all
# print(currency())

def metal():
    url = 'https://api.metals.live/v1/spot'
    me = requests.get(url)
    met = ['gold','silver','platinum','palladium','']
    p = me.json()
    all = ''
    for i in range(len(p)):
        if met[i] in p[0]:
            try:
                gold = p[i]['gold']
                all += '黃金 : ' + str(gold)
            except:
                continue
        elif met[i] in p[1]:
            try:
                silver = p[i]['silver']
                all += '\n白銀 : ' + str(silver)
            except:
                continue
        elif met[i] in p[2]:
            try:
                platinum = p[i]['platinum']
                all += '\n白金 : ' + str(platinum)
            except:
                continue
        elif met[i] in p[3]:
            try:
                palladium = p[i]['palladium']
                all += '\n鈀鈀 : ' + str(palladium)
            except:
                continue

    # all = '黃金 : ' + str(gold) + '\n白銀 : ' + str(silver) + '\n白金 : ' + str(platinum) + '\n鈀鈀 : ' + str(palladium)
    return all

def get_greed_pic():
    pic_url = fear_and_greed.get()

    all = all = '貪婪恐慌\n|   ' + str(pic_url[0])+'   | \n'+pic_url[1]

    return all

# print(get_greed_pic())


# print(stockapi('我要指數'))
# pay('CL=F')
# pay('CL=F')