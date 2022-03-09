import requests
import pandas as pd
import numpy as np
import datetime

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
    # 下載證交所資料 ------
    link = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL?response=open_data'
    data = pd.read_csv(link)

    # ['證券代號', '證券名稱', '成交股數', '成交金額', '開盤價',
    #  '最高價', '最低價', '收盤價', '漲跌價差', '成交筆數']
    data.columns =  ['證券代號', '證券名稱', '成交股數', '成交金額', '開盤價',
    '最高價', '最低價', '收盤價', '漲跌價差', '成交筆數']  
    # 標註今日日期
    data['日期'] = date_get_today()
    stock_num = str(stockID)
    cols = data.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    data = data[cols]
    # 除了證券代號外，其他欄位都是str，且部份資料中有''
    data = data.replace('', np.nan, regex=True)
    ans = (data.loc[(data['證券代號'] == stock_num)])
    ans = ans.set_index('日期')
    # ans = ans.drop(ans.columns[[0]], axis=1)
    return ans.T     # T表示行列互換

# def makepretty(ans):
#     a = 0
# num = '2330'
# a = gettwstock(num)

# print (a)
# print(a['證券代號'] == num)
# print(a['證券名稱'])