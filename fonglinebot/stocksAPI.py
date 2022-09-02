import finnhub
import requests
import datetime
import fear_and_greed
import yfinance as yf
from apikey import STOCKAPIKEY,CURRENCYKEY

def pay():
    index_all = ['^GSPC','^DJI','^IXIC']
    an = []
    for i in index_all:
        ticker = yf.Ticker(i)
        a = ticker.info['regularMarketPrice']
        an.append(a)

    ans = 'S&P  : {}\nDOW  : {}\nNAS  : {}'.format(an[0],an[1],an[2])
    return ans
# print(pay())

def pay_oil():
    index_all = ['CL=F','BZ=F']
    an = []
    for i in index_all:
        ticker = yf.Ticker(i)
        a = ticker.info['regularMarketPrice']
        an.append(a)

    ans = '原油 : {}\n布倫特原油 : {}'.format(an[0],an[1])
    return ans
# print(pay_oil())

def stockapi(ID):
    if ID == '指數':
        all = pay()
    elif ID == '油':
        all = pay_oil()
    else:
        ID = ID.upper()
        datetime_dt = datetime.datetime.today()
        today = datetime_dt.strftime("%Y-%m-%d")
        oneday = datetime.timedelta(days=1)
        yesterday = datetime_dt - oneday
        tomarrow = datetime_dt + oneday
        yesterday = yesterday.strftime("%Y-%m-%d")
        tomarrow = tomarrow.strftime("%Y-%m-%d")
        finnhub_client = finnhub.Client(api_key=STOCKAPIKEY)
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
    finnhub_client = finnhub.Client(api_key=CURRENCYKEY)
    _currency = finnhub_client.forex_rates(base = 'TWD')
    qu = _currency['quote']
    usd = str(round(1/qu['USD'],3))
    jpy = str(round(1/qu['JPY'],3))
    eur = str(round(1/qu['EUR'],3))
    rmb = str(round(1/qu['CNY'],3))
    aud = str(round(1/qu['AUD'],3))
    all = '美金 : ' + usd + '\n日幣 : '+ jpy +'\n歐元 : ' + eur + '\n人民幣:' + rmb  + '\n澳幣 : ' + aud

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

    return all

def get_greed_pic():
    pic_url = fear_and_greed.get()

    all = all = '貪婪恐慌\n|   ' + str(pic_url[0])+'   | \n'+pic_url[1]

    return all

# print(get_greed_pic())
# print(stockapi('我要油'))