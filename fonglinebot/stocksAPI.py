import finnhub
import requests
import datetime
import fear_and_greed
import yfinance as yf
import os 
from dotenv import load_dotenv
load_dotenv()

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
        finnhub_client = finnhub.Client(api_key=os.getenv("STOCKAPIKEY"))
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
    url = 'https://production.dataviz.cnn.io/index/fearandgreed/graphdata'
    greed = requests.get(
        url,
        headers={
                "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15"
                }
            )
    # print(greed.json())
    score = str(round(greed.json()['fear_and_greed']['score'],2))
    rating = str(greed.json()['fear_and_greed']['rating'])
    oneweek = str(greed.json()['fear_and_greed']['previous_1_week'])
    onemounth = str(round(greed.json()['fear_and_greed']['previous_1_month'],2))
    sp500 = str(greed.json()['market_momentum_sp500']['data'][-1]['y'])
    sp500_m = str(round(greed.json()['market_momentum_sp500']['score'],2))
    sp500_rating = str(greed.json()['market_momentum_sp500']['rating'])
    put_call_options_s = str(round(greed.json()['put_call_options']['score'],2))
    put_call_options_r = str(greed.json()['put_call_options']['rating'])
    all = ('貪婪恐慌\n|   ' + score +'   | \n' + rating + '\n一週前 : ' + oneweek + 
           '\n一個月前 : ' + onemounth + '\n\nsp500 : {}\n    {},{} \n'.format(sp500,sp500_rating,sp500_m) + 
            '\n看漲期權 : {},{}'.format(put_call_options_r,put_call_options_s)+
            '\n避險需求 : {},{}'.format(str(greed.json()['safe_haven_demand']['rating']),str(round(greed.json()['safe_haven_demand']['score'],2)))+
            '\n垃圾債需求 : {},{}'.format(str(greed.json()['junk_bond_demand']['rating']),str(round(greed.json()['junk_bond_demand']['score'],2)))
            )

    return all

# print(get_greed_pic())
# print(stockapi('我要油'))