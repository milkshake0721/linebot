import requests
from bs4 import BeautifulSoup

def crypto(coin):
    url = 'http://ftx.com/api/markets/'+ coin +'/USD'
    # url = 'http://ftx.com/api/markets/ETH/USDT'
    url_history = 'http://ftx.com/api/markets/' + coin + '/USD/candles?resolution=2592000'
    r = requests.post(url)
    coin = coin.upper()
    if r.json()['success'] != True :
        all = gate_io(coin)
        return all
    else:
        sel = r.json()['result']
        # print (sel)
        '''
        {"success":true,"result":{"name":"ETH/USDT","enabled":true,"postOnly":false,"priceIncrement":0.1,"sizeIncrement":0.001,"minProvideSize":0.001,"last":2585.4,"bid":2585.6,"ask":2585.7,"price":2585.6,"type":"spot","baseCurrency":"ETH","quoteCurrency":"USDT","underlying":null,"restricted":false,"highLeverageFeeExempt":true,"largeOrderThreshold":5000.0,"change1h":-0.004887811261209252,"change24h":-0.06145413626628916,"changeBod":-0.05299783906530418,"quoteVolume24h":63523496.6902,"volumeUsd24h":63543617.12254165}}
        '''
        rh = requests.post(url_history)

        sel_h = rh.json()['result']
        history_high = 0
        history_low = sel_h[0]['low']
        for i in range(len(sel_h)):
            if sel_h[i]['high'] >  history_high:
                history_high = sel_h[i]['high']
            if sel_h[i]['low'] <  history_low:
                history_low = sel_h[i]['low']

        history_high2now = (float(sel['price']) - float(history_high)) / history_high *100

        all = sel['name'] + '\n| 現價 | ' + str(sel['price']) + ' (' + str(round(float(sel['change24h'])*100,2)) + '%)' + '\n-------------------\n' + '| 最高回落 | ' + str(round(float(history_high2now),3)) + '%\n| 一小變動 | ' + str(round(float(sel['change1h'])*100,3)) + '%\n| 歷史高點 | ' + str(round(float(history_high),3)) + '\n| 歷史低點 | ' + str(round(float(history_low),3)) +  '\n-------------------\nUSD volume in past 24 hours : '+ str(round(float(sel['volumeUsd24h']),0)) 
        return all


def gasfee():
    '''
    {"fast":390,"fastest":480,"safeLow":245,"average":290,"block_time":11,
    "blockNum":14362667,"speed":0.4876316436867856,"safeLowWait":10.3,"avgWait":1.1,"fastWait":0.5,"fastestWait":0.4,
    "gasPriceRange":{"4":183.3,"6":183.3,"8":183.3,"10":183.3,"20":183.3,"30":183.3,"40":183.3,"50":183.3,"60":183.3,"70":183.3,"80":183.3,"90":183.3,"100":183.3,"110":183.3,"120":183.3,"130":183.3,"140":183.3,"150":183.3,"160":183.3,"170":183.3,"180":183.3,"190":183.3,"200":183.3,"220":183.3,"240":11.7,"245":10.3,"260":8.3,"280":6.3,"290":1.1,"300":0.9,"320":0.8,"340":0.6,"360":0.5,"380":0.5,"390":0.5,"400":0.4,"420":0.4,"440":0.4,"460":0.4,"480":0.4}}
    '''
    url = 'http://ethgasstation.info/api/ethgasAPI.json?'
    r = requests.post(url)
    sel = r.json()
    fee = '|平均| ' + str(sel['average']/10) + '\n|最快| ' + str(sel['fastest']/10) + '\n|最慢| ' + str(sel['safeLow']/10)
    return fee

def spot_margin(coin):
    # print (coin)
    coin = coin[2:]
    coin = coin.upper()
    coin = coin.split()
    # print(type(coin))
    url = 'http://ftx.com/api/spot_margin/history'
    r = requests.post(url)
    sel = r.json()['result']
    spot = None
    for i in range(len(sel)):
        if sel[i]['coin'] == coin[0] :
            spot = sel[i]

    # print(spot['rate']*24*365*100)
    # rate = spot
    rate = str(round((spot['rate']*24*365*100),2)) + '%'
    print(rate)
    return rate

def all_spot_margin():
    url = 'http://ftx.com/api/spot_margin/history'
    r = requests.post(url)
    sel = r.json()['result']
    find = ['USDT','USD','BTC','ETH','BNB']
    spot = {}
    for i in range(len(sel)):
        for k in range(len(find)):
            if sel[i]['coin'] == find[k] :
                spot[find[k]] = sel[i]

    # rate = str(spot['rate']*24*365*100) + '%'
    # return rate
    rate = '|USDT|  ' + str(round(spot['USDT']['rate']*24*365*100,1)) + '%\n|USD  |  ' +str(round(spot['USD']['rate']*24*365*100,1)) +  '%\n|BTC  |  ' +str(round(spot['BTC']['rate']*24*365*100,1)) +  '%\n|ETH  |  ' + str(round(spot['ETH']['rate']*24*365*100,1)) +  '%\n|BNB  |  ' + str(round(spot['BNB']['rate']*24*365*100,1)) + '%'

    return rate

# spot_margin('貸出 Btc')
# all_spot_margin()

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

def crypto_greed():
    url = 'https://api.alternative.me/fng/'
    r = requests.get(url)
    dt = r.json()['data'][0]

    all = '貪婪恐慌\n|   ' + str(dt['value'])+'   | \n'+dt['value_classification']
    return all
