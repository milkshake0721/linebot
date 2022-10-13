#純粹計算Nick笑死次數

import datetime
import pygsheets

gc = pygsheets.authorize(service_file='LineBot.json')
sht = gc.open_by_url(
'https://docs.google.com/spreadsheets/d/1jmZpDVYvshyUN5JP1-YcqDYcwgcJR7aDsCpFIvzpbY0/'
)

tday = datetime.date.today()
wks_list = sht.worksheets()

def Nick_lmao_time():
    if str(sht.sheet1.cell('A2').value) != str(tday)  :
        sht.sheet1.cell('A2').value = str(tday)
        sht.sheet1.cell('C2').value = int(0)
    sht.sheet1.cell('C2').value = int(sht.sheet1.cell('C2').value) + 1
    sht.sheet1.cell('C3').value = int(sht.sheet1.cell('C3').value) + 1

def check_Nick_lmao_time():
    if str(sht.sheet1.cell('A2').value) != str(tday)  :
        sht.sheet1.cell('A2').value = str(tday)
        sht.sheet1.cell('C2').value = int(0)
    all = '今日笑死 : ' + str(sht.sheet1.cell('C2').value) + '次\n總共笑死 : ' + str(sht.sheet1.cell('C3').value) + '次'
    return all

