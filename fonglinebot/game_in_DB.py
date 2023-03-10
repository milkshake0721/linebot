import json, pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["DnD"]
mycol = mydb["DnD"]


# with open("user_info.json", "r", encoding="utf-8") as f:
#     data = json.load(f)
#     for i in data["data"]:
#         print(i)            #{'id': 'U0bdb890d03a5b755f3dbb67eafa74f5d', 'name': '尼克', 'gold': 6, 'silver': 62, 'mine': 1}

# mycol.insert_one(i)

# x = mycol.find()
# print(x)
# newvalues = {"$set": {"city": "蘇爾德村"}}
# mycol.update_one({}, newvalues)
def add_city():
    all_user = mycol.find()
    for i in all_user:
        # if '俗頭' in i and i['俗頭'] >= 10:
        #     newvalues = {"$set": { "金幣" : i['金幣']+100}}
        #     mycol.update_one(i, newvalues)
        if i['title'] in  ['劍士','小混混','見習法師','農夫']:
            newvalues = {"$set": {  "change_title" : 2}}
            mycol.update_one(i, newvalues)
        
        if i['title'] in  ['狂劍士','大劍士','魔導士','法師','盜賊','大地主']:
            newvalues = {"$set": {  "change_title" : 3}}
            mycol.update_one(i, newvalues)
        
        if i['title'] in  ['劍豪','聖劍士','黑魔導士','大法師','暗夜盜賊','領主']:
            newvalues = {"$set": {  "change_title" : 4}}
            mycol.update_one(i, newvalues)


        if i['title'] in  ['劍魔','皇家聖劍士','混沌魔導士','皇家法師','暗月神偷','大公']:
            newvalues = {"$set": {  "change_title" : 5}}
            mycol.update_one(i, newvalues)
add_city()