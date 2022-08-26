# -*- coding: UTF-8 -*-
import requests


week = ["這週", "本周", "下週", "這周", "下周", "本週"]
loc = [
    "臺北市",
    "新北市",
    "桃園市",
    "臺中市",
    "臺南市",
    "高雄市",
    "新竹縣",
    "苗栗縣",
    "彰化縣",
    "南投縣",
    "雲林縣",
    "嘉義縣",
    "屏東縣",
    "宜蘭縣",
    "花蓮縣",
    "臺東縣",
    "澎湖縣",
    "金門縣",
    "連江縣",
    "基隆市",
    "新竹市",
    "嘉義市",
]

def if_two_words(place):
    for i in loc:
        if place in i:return i
    

def get_36h_weather(place):
    if not place:return
    # CWB-EC9FB2AA-AEB7-48B6-8816-4993A9543232
    weather, rain, tem, ci, temM = [], [], [], [], []
    a = place + "\n"

    url = (
        "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-EC9FB2AA-AEB7-48B6-8816-4993A9543232&locationName="
        + place
    )
    r_weather = requests.get(url)
    raw = r_weather.json()["records"]["location"]
    if raw == []:
        return
    raw = raw[0]["weatherElement"]

    startTime = (
        raw[0]["time"][0]["startTime"],
        raw[0]["time"][1]["startTime"],
        raw[0]["time"][2]["startTime"],
        raw[0]["time"][2]["endTime"],
    )

    for i in raw:
        if i["elementName"] == "Wx":
            weather.append(i["time"][0]["parameter"]["parameterName"])
            weather.append(i["time"][1]["parameter"]["parameterName"])
            weather.append(i["time"][2]["parameter"]["parameterName"])
        if i["elementName"] == "PoP":
            rain.append(i["time"][0]["parameter"]["parameterName"])
            rain.append(i["time"][1]["parameter"]["parameterName"])
            rain.append(i["time"][2]["parameter"]["parameterName"])
        if i["elementName"] == "MinT":
            tem.append(i["time"][0]["parameter"]["parameterName"])
            tem.append(i["time"][1]["parameter"]["parameterName"])
            tem.append(i["time"][2]["parameter"]["parameterName"])
        if i["elementName"] == "CI":
            ci.append(i["time"][0]["parameter"]["parameterName"])
            ci.append(i["time"][1]["parameter"]["parameterName"])
            ci.append(i["time"][2]["parameter"]["parameterName"])
        if i["elementName"] == "MaxT":
            temM.append(i["time"][0]["parameter"]["parameterName"])
            temM.append(i["time"][1]["parameter"]["parameterName"])
            temM.append(i["time"][2]["parameter"]["parameterName"])

    for i in range(3):
        a += "{}\n\n氣溫{}~{}\n降雨機率是{}%\n\n{}\n{}\n\n".format(
            startTime[i], tem[i], temM[i], rain[i], weather[i], ci[i]
        )

    return a


def week_weather(place):

    ans = place+'\n'
    detal = ''
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-091?Authorization=CWB-EC9FB2AA-AEB7-48B6-8816-4993A9543232"+'&elementName=WeatherDescription'
    r_weather = requests.get(url)
    raw = r_weather.json()['records']['locations'][0]['location']
    for i in raw:
        if i['locationName'] == place:
            detal = i['weatherElement'][0]['time']
            for k in detal:
                ans += k['startTime']+'\n'+k['elementValue'][0]['value']+'\n\n'
            return(ans)
    pass


def ask_weather(place):
    if "明年" in place:
        return "假賽"
    place = place.replace("天氣", "")
    place = place.replace("台", "臺")
    if place == "臺北縣":
        return "改叫新北市了啦，老人"
    elif ("週" or "周") in place:
        for i in week:
            place = place.replace(i, "")
        place = if_two_words(place)
        return week_weather(place)
    # elif place in weather_station_list:
    #     ans = station(place)
    else:
        place = if_two_words(place)
        ans = get_36h_weather(place)
        return ans

# print(ask_weather("台北天氣"))

# url = (
#         "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-017?Authorization=CWB-EC9FB2AA-AEB7-48B6-8816-4993A9543232"
#     )
# r_weather = requests.get(url)
# raw = r_weather.json()
# print(raw)
def weather_in_english(query):
    # This is the core of our weather query URL
    try:
        days = int(query[query.find(' '):])
        if days > 14:
            days = 7
    except:
        days = 1
    query = query[:query.find(' ')]
    BaseURL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'

    ApiKey='82W8W5QY9JMFUHV9AKHLTN792'
    #UnitGroup sets the units of the output - us or metric
    UnitGroup ='metric'

    #Location for the weather data
    Location = query
    StartDate = ''
    EndDate=''
    ContentType="json"
    #include sections
    #values include days,hours,current,alerts
    Include="days"
    # print('')
    # print(' - Requesting weather : ')
    #basic query including location
    ApiQuery=BaseURL + Location

    #append the start and end date if present
    if (len(StartDate)):
        ApiQuery+="/"+StartDate
        if (len(EndDate)):
            ApiQuery+="/"+EndDate
    #Url is completed. Now add query parameters (could be passed as GET or POST)
    ApiQuery+="?"
    #append each parameter as necessary
    if (len(UnitGroup)):
        ApiQuery+="&unitGroup="+UnitGroup
    if (len(ContentType)):
        ApiQuery+="&contentType="+ContentType
    if (len(Include)):
        ApiQuery+="&include="+Include
    ApiQuery+="&key="+ApiKey
    r_weather = requests.get(ApiQuery).json()
    all = '{}\n\n'.format(r_weather['resolvedAddress'])
    if days == 1:
        for i in range(days):
            all += '{}\n\n'.format(r_weather['days'][i]['datetime'])
            all += '氣溫{}~{}度\n'.format(r_weather['days'][i]['tempmax'],r_weather['days'][i]['tempmin'])
            all += '體感{}~{}度\n\n'.format(r_weather['days'][i]['feelslikemax'],r_weather['days'][i]['feelslikemin'])
            all += '日出時間{}\n日落時間{}\n'.format(r_weather['days'][i]['sunrise'],r_weather['days'][i]['sunset'])
            all += '{}，降雨機率{}%\n'.format(r_weather['days'][i]['conditions'],r_weather['days'][i]['precipprob'])
            all += '{}\n'.format(r_weather['days'][i]['description'])
    else:
        for i in range(days):
            all += '{}\n\n'.format(r_weather['days'][i]['datetime'])
            all += '氣溫{}~{}度\n'.format(r_weather['days'][i]['tempmax'],r_weather['days'][i]['tempmin'])
            all += '體感{}~{}度\n\n'.format(r_weather['days'][i]['feelslikemax'],r_weather['days'][i]['feelslikemin'])
            all += '{}，降雨機率{}%\n'.format(r_weather['days'][i]['conditions'],r_weather['days'][i]['precipprob'])
            all += '\n'
    # print(datetime)
    # all = '{}\n'.format(r_weather['resolvedAddress'] )

    # print(all)
    return all
# bb = 'w Tokyo '
# print(bb[:2])
# print(weather_in_english(bb[2:]))