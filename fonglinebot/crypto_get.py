import requests,time
from bs4 import BeautifulSoup

def gate_io(coin):
    '''
    {"quoteVolume":"34916.269532841","baseVolume":"89291720.559167","highestBid":"2594.45","high24hr":"2604.56","last":"2594.45",
    "lowestAsk":"2594.46","elapsed":"4ms","result":"true","low24hr":"2493.34","percentChange":"0.57"}
    '''
    coin = coin.upper()
    # url = 'https://data.gateapi.io/api2/1/marketlist'
    url = 'https://data.gateapi.io/api2/1/ticker/' + coin + '_usdt'
    r = requests.get(url)
    sel = r.json()

    ans = coin + '/USDT\n| 現價 | ' + str(sel['last']) + ' (' + sel['percentChange'] + '%)' + '\n-------------------\n' + '| high24hr | ' + sel['high24hr'] + '\n|  low24hr | ' + sel['low24hr'] + '\n-------------------\nUSD volume in past 24 hours : '+ sel['baseVolume']
    return ans


def crypto(coin):
    url = 'http://ftx.com/api/markets/'+ coin +'/USD'
    # url = 'http://ftx.com/api/markets/ETH/USDT'
    url_history = 'http://ftx.com/api/markets/' + coin + '/USD/candles?resolution=2592000'
    r = requests.post(url)
    coin = coin.upper()
    # print(r.json())
    if r.json()['success'] != True or r.json()['result']['price'] == None :
        all = gate_io(coin)
        return all
    else:
        sel = r.json()['result']
        # print (sel)
        '''
        {"success":true,"result":{"name":"ETH/USDT","enabled":true,"postOnly":false,"priceIncrement":0.1,"sizeIncrement":0.001,"minProvideSize":0.001,"last":2585.4,"bid":2585.6,"ask":2585.7,"price":2585.6,"type":"spot","baseCurrency":"ETH","quoteCurrency":"USDT","underlying":null,"restricted":false,"highLeverageFeeExempt":true,"largeOrderThreshold":5000.0,"change1h":-0.004887811261209252,"change24h":-0.06145413626628916,"changeBod":-0.05299783906530418,"quoteVolume24h":63523496.6902,"volumeUsd24h":63543617.12254165}}
        {'success': True, 'result': {'name': 'NEAR/USD', 'enabled': True, 'postOnly': True, 'priceIncrement': 0.001, 'sizeIncrement': 0.1, 'minProvideSize': 0.1, 'last': None, 'bid': 16.224, 'ask': 17.552, 'price': None, 'type': 'spot', 'baseCurrency': 'NEAR', 'quoteCurrency': 'USD', 'underlying': None, 'restricted': False, 'highLeverageFeeExempt': True, 'largeOrderThreshold': 5000.0, 'change1h': 0.0, 'change24h': 0.0, 'changeBod': 0.0, 'quoteVolume24h': 0.0, 'volumeUsd24h': 0.0, 'priceHigh24h': 0.0, 'priceLow24h': 0.0}}
        '''
        rh = requests.post(url_history)

        sel_h = rh.json()['result']
        history_high = 0
        try:
            history_low = sel_h[0]['low']
            for i in range(len(sel_h)):
                if sel_h[i]['high'] >  history_high:
                    history_high = sel_h[i]['high']
                if sel_h[i]['low'] <  history_low:
                    history_low = sel_h[i]['low']
            history_high2now = (float(sel['price']) - float(history_high)) / history_high *100
        except:
            history_low = 0
            history_high2now = 0

        all = sel['name'] + '\n| 現價 | ' + str(sel['price']) + ' (' + str(round(float(sel['change24h'])*100,2)) + '%)' + '\n-------------------\n' + '| 最高回落 | ' + str(round(float(history_high2now),3)) + '%\n| 一小變動 | ' + str(round(float(sel['change1h'])*100,3)) + '%\n| 歷史高點 | ' + str(round(float(history_high),3)) + '\n| 歷史低點 | ' + str(round(float(history_low),3)) +  '\n-------------------\nUSD volume in past 24 hours : '+ str(round(float(sel['volumeUsd24h']),0)) 
        return all

def gasfee():
    '''
    {"fast":390,"fastest":480,"safeLow":245,"average":290,"block_time":11,
    "blockNum":14362667,"speed":0.4876316436867856,"safeLowWait":10.3,"avgWait":1.1,"fastWait":0.5,"fastestWait":0.4,
    "gasPriceRange":{"4":183.3,"6":183.3,"8":183.3,"10":183.3,"20":183.3,"30":183.3,"40":183.3,"50":183.3,"60":183.3,"70":183.3,"80":183.3,"90":183.3,"100":183.3,"110":183.3,"120":183.3,"130":183.3,"140":183.3,"150":183.3,"160":183.3,"170":183.3,"180":183.3,"190":183.3,"200":183.3,"220":183.3,"240":11.7,"245":10.3,"260":8.3,"280":6.3,"290":1.1,"300":0.9,"320":0.8,"340":0.6,"360":0.5,"380":0.5,"390":0.5,"400":0.4,"420":0.4,"440":0.4,"460":0.4,"480":0.4}}
    '''
    # url = 'http://ethgasstation.info/api/ethgasAPI.json?'
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
    # print(r)
    # rate = '|USDT|  ' + str(round(spot['USDT']['rate']*24*365*100,1)) + '%\n|USD  |  ' +str(round(spot['USD']['rate']*24*365*100,1)) +  '%\n|BTC  |  ' +str(round(spot['BTC']['rate']*24*365*100,1)) +  '%\n|ETH  |  ' + str(round(spot['ETH']['rate']*24*365*100,1)) +  '%\n|BNB  |  ' + str(round(spot['BNB']['rate']*24*365*100,1)) + '%'

    return r


def crypto_greed():
    url = 'https://api.alternative.me/fng/'
    r = requests.get(url)
    dt = r.json()['data'][0]

    all = '貪婪恐慌\n|   ' + str(dt['value'])+'   | \n'+dt['value_classification']
    return all

def cryptoall():
    coin = ['btc','eth','bnb','sol','ftt','gt','near']
    price = []
    for c in coin :
        url = 'http://ftx.com/api/markets/'+ c +'/USD'
        r = requests.post(url)
        sel = str(r.json()['result']['price'])
        price.append(sel)
    all = 'BTC : ' + price[0] + '\nETH : ' + price[1] + '\nBNB : ' + price[2] + '\nSOL : ' + price[3] + '\nFTT : ' + price[4] + '\nGT  : ' + price[5] + '\nNear: ' +price[6]
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

    ans = 'Bito | ' + str(round(bito,2)) + '\nMax | ' + str(round(max,2))

    all = ans
        

    return all

def usdt_ace():
    try:
        ace_url = 'http://ace.io/polarisex/oapi/list/tradePrice'
        ace_r = requests.post(ace_url,timeout=20,headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15'})
        # print(ace_r.json())
        ace = float(ace_r.json()['USDT/TWD']['last_price'])
    except:
        ace = 9999
    ans = 'Ace | '+ str(round(ace,2))

    all = ans
        
    return all


print(usdt_ace())