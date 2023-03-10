import requests,time
from bs4 import BeautifulSoup

def gate_io(coin):
    coin = coin.upper()
    # url = 'https://data.gateapi.io/api2/1/marketlist'
    url = 'https://data.gateapi.io/api2/1/ticker/' + coin + '_usdt'
    r = requests.get(url)
    sel = r.json()

    ans = coin + '/USDT\n| 現價 | ' + str(sel['last']) + ' (' + sel['percentChange'] + '%)' + '\n-------------------\n' + '| high24hr | ' + sel['high24hr'] + '\n|  low24hr | ' + sel['low24hr'] + '\n-------------------\nUSD volume in past 24 hours : '+ sel['baseVolume']
    return ans


def crypto(coin):
    
    coin = coin.upper()
    url_b = 'https://api.binance.com/api/v3/ticker/price?symbol='+ coin +'USDT'
    url24h = 'https://api.binance.com/api/v3/ticker/24hr?symbol='+ coin +'USDT' #/api/v3/klines
    urlk = 'https://data.binance.com/api/v3/klines?symbol=' + coin +'USDT&interval=1M'

    r = requests.get(url24h)
    # print(r.json()) 
    if r.json() == {'code': -1121, 'msg': 'Invalid symbol.'} :
        all = gate_io(coin)
        return all
    else:
        rk = requests.get(urlk)
        sellla = rk.json()
        big_one = 0
        small_one = 99999999
        for i in sellla:
            if float(i[2]) > big_one:big_one=float(i[2])
            if float(i[3]) < small_one:small_one=float(i[3])

        sel = r.json()
        # print (sel)
        name = sel['symbol']
        name = name.replace('USDT','')
        all = name + '\n| 現價 | ' + str(float(sel['lastPrice'])) + ' (' + str(round(float(sel['priceChangePercent']),2)) + '%)' + '\n-------------------\n' + '| 加加減減 | ' + str(round(float(sel['priceChange']),2)) +  '\n| 歷史高點 | ' + str(big_one) + '\n| 最高回落 | ' + str(round((-100*(1 - (round(float(sel['lastPrice']),2)/big_one))),2)) + ' %\n| 歷史低點 | ' + str(small_one) +  '\n-------------------\nUSD volume in past 24 hours : '+ str(round(float(sel['quoteVolume']),0)) 
        return all

def gasfee():
    url = 'https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken'
    r = requests.post(url)
    sel = r.json()['result']
    fee = '|平均| ' + str(int(sel['ProposeGasPrice'])) + '\n|最快| ' + str(int(sel['FastGasPrice'])) + '\n|最慢| ' + str(int(sel['SafeGasPrice']))
    return fee


def spot_margin(coin):
    # print (coin)
    coin = coin[2:]
    coin = coin.upper()
    coin = coin.split()
    # print(type(coin))
    url = 'http://ftx.com/api/spot_margin/lending_rates'
    r = requests.post(url)
    sel = r.json()['result']
    spot = None
    for i in range(len(sel)):
        if sel[i]['coin'] == coin[0] :
            spot = sel[i]
            # print(spot)
            break

    rate ='現在 '+ str(round((spot['previous']*24*365*100),2)) + '%\n下次 '+ str(round((spot['estimate']*24*365*100),2))+'%'
    # print(rate)
    return rate
# spot_margin('貸出 BNB')

def all_spot_margin():
    url = 'http://ftx.com/api/spot_margin/lending_rates'
    r = requests.post(url)
    sel = r.json()['result']
    find = ['USDT','USD','BTC','ETH','BNB']
    spot = {}
    # new_time = sel[0]['time']
    r = ''
    for i in range(len(sel)):
        for k in range(len(find)):
            if sel[i]['coin'] == find[k]:
                spot[find[k]] = sel[i]
                # print(find[k])
                ra = str(round(sel[i]['estimate']*24*365*100,1))
                # print(sel[i]['time'])
                r = r + '|'+ find[k] +'|\t' + ra + '%\n'

    return r


def crypto_greed():
    url = 'https://api.alternative.me/fng/'
    r = requests.get(url)
    dt = r.json()['data'][0]

    all = '貪婪恐慌\n|   ' + str(dt['value'])+'   | \n'+dt['value_classification']
    return all

def cryptoall():
    coin = ['BTCUSDT','ETHUSDT','BNBUSDT','SOLUSDT','FTTUSDT','GTUSDT','NEARUSDT']
    price = []
    url = 'https://api.binance.com/api/v3/ticker/price'
    r = requests.get(url).json()
    # print(r)
    for i in r:
        # print(i['symbol'])
        if i['symbol'] in coin:
            price.append(i)
    # print(price)
    all = ''
    for c in price:
        all += c['symbol'] + ' : ' + str(round(float(c['price']),2)) + '\n'
    
    all = all.replace('USDT','')
    # all = 'BTC : ' + price[0] + '\nETH : ' + price[1] + '\nBNB : ' + price[2] + '\nSOL : ' + price[3] + '\nFTT : ' + price[4] + '\nGT  : ' + price[5] + '\nNear: ' +price[6]
    return all
# print(cryptoall())
def usdt():
    try:
        max_url = 'https://max-api.maicoin.com/api/v2/tickers/usdttwd'
        r = requests.get(max_url)
        max = float(r.json()['last'])
    except:
        max = 9999
    try:
        bito_url = 'https://api.bitopro.com/v3/trades/usdt_twd'
        bito_r = requests.get(bito_url)
        # print(bito_r.json()['data'][0]['price'])
        bito = float(bito_r.json()['data'][0]['price'])
    except:
        bito = 9999
    try:
        ace_url = 'http://ace.io/polarisex/oapi/list/tradePrice'
        ace_r = requests.post(ace_url,timeout=15,headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15'})
        # print(ace_r.json())
        ace = float(ace_r.json()['USDT/TWD']['last_price'])
    except:
        ace = 9999
    ans = 'Ace | '+ str(round(ace,2))+ '\nBito | ' + str(round(bito,2)) + '\nMax | ' + str(round(max,2))

    all = ans
        

    return all

# print(crypto('btc'))