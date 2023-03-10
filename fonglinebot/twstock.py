import requests
import datetime
import yfinance as yf
import csv,urllib.request

def gweei(stockID):
    if stockID == 0 or stockID == '加權':
        link = 'http://mis.twse.com.tw/stock/api/getStockInfo.jsp?json=1&delay=0&ex_ch=otc_o00.tw'

    elif stockID[0] <= '9':
        link = 'http://mis.twse.com.tw/stock/api/getStockInfo.jsp?json=1&delay=0&ex_ch=otc_'+ str(stockID) +'.tw'
        pass
    else:
        with open('fonglinebot/gweei.csv', mode='r') as infile:
            reader = csv.reader(infile)
            with open('coors_new.csv', mode='w') as outfile:
                writer = csv.writer(outfile)
                mydict = {rows[2]:rows[1] for rows in reader}
        stockID = mydict[stockID]

        link = 'http://mis.twse.com.tw/stock/api/getStockInfo.jsp?json=1&delay=0&ex_ch=otc_'+ str(stockID) +'.tw'

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

# print(gweei('加權'))

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
        link = 'http://mis.twse.com.tw/stock/api/getStockInfo.jsp?json=1&delay=0&ex_ch=tse_t00.tw'

    elif stockID[0] <= '9':
        link = 'http://mis.twse.com.tw/stock/api/getStockInfo.jsp?json=1&delay=0&ex_ch=tse_'+ str(stockID) +'.tw'
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

def twexrate():
    ans = ''
    url = 'https://rate.bot.com.tw/xrt/flcsv/0/day'
    webpage = urllib.request.urlopen(url)
    data = csv.reader(webpage.read().decode('utf-8').splitlines())
    diction = {'USD':'美金','HKD':'港幣','GBP':'英鎊','AUD':'澳幣','CAD':'加大','SGD':'新幣','CHF':'法郎','JPY':'日幣','ZAR':'南非','SEK':'瑞典','NZD':'紐元','THB':'泰幣','PHP':'菲賓','IDR':'印尼','EUR':'歐元','KRW':'韓元','VND':'越盾','MYR':'馬來膜','CNY':'人民'}
    j=0
    for i in data:
        if i[3]=='0.00000':
            pass
        else:
            if j == 0:
                ans += '即期    買          賣\n'
                # print(i[0],i[3],i[13])
            if j!= 0 :
                ans += '{} : \t {}  {}\n'.format(diction[i[0]],i[3],i[13])
                # print(i[0],float(i[3]),float(i[13]))
        j+=1
    return ans
# print(oil_price())
# def makepretty(ans):
#     a = 0
# num = '富邦公司治理'
# a = gettwstock(num)
# print(eggprice())
# print (a)
# print(a['證券代號'] == num)
# print(a['證券名稱'])
# print(gettwstock('加權'))
# print(gettwstock(0))
