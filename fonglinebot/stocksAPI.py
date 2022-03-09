import finnhub
import pprint

'''
{'c': 824.4,
 'd': 19.82,
 'dp': 2.4634,
 'h': 849.99,
 'l': 782.17,
 'o': 795.53,
 'pc': 804.58,
 't': 1646773204}
 '''

def stockapi(ID):
    ID = ID.upper()
    finnhub_client = finnhub.Client(api_key="c8k6sqaad3i8fk1kn8ag")
    ans = finnhub_client.quote(ID)
    ans.pop('t')
    all = '個股代號 : ' + ID + '\n現在價格 : ' + str(ans['c']) + '\n變動價格 : ' + str(ans['d']) + '\n變動趴數 : ' + str(ans['dp']) + '\n今日最高 : ' + str(ans['h']) + '\n今日最低 : '+ str(ans['l']) + '\n開市價格 : '+ str(ans['o']) + '\n上次閉市 : '+ str(ans['pc'])
    return all
