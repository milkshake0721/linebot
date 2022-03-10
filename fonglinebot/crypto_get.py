import requests

def crypto(coin):
    url = 'http://ftx.com/api/markets/'+ coin +'/USD'
    # url = 'http://ftx.com/api/markets/ETH/USDT'
    url_history = 'http://ftx.com/api/markets/' + coin + '/USD/candles?resolution=2592000'
    r = requests.post(url)
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

    all = sel['name'] + '\n| 現價 | ' + str(sel['price']) + ' (' + str(round(float(sel['change24h'])*100,2)) + '%)' + '\n-------------------\n\n' + '最高回落 | ' + str(round(float(history_high2now),3)) + '%\n1小時變動 | ' + str(round(float(sel['change1h'])*100,3)) + '%\n\n歷史高點 | ' + str(round(float(history_high),3)) + '\n歷史低點 | ' + str(round(float(history_low),3)) +  '\n\n-------------------\n\nUSD volume in past 24 hours : '+ str(round(float(sel['volumeUsd24h']),0)) 

    return all
