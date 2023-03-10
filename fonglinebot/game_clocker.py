import schedule,time
import json, random, pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["DnD"]
mycol = mydb["DnD"]


def mine_to_0():
    all_user = mycol.find()
    for i in all_user:
        if 'mine' in i:
            newvalues = {"$set": {"mine": 0}}
            mycol.update_one(i, newvalues)

def work_to_10():
    all_user = mycol.find()
    for i in all_user:
        # print(i['id'])
        if 'work' in i:
            newvalues = {"$set": {"work": 10}}
            if i['title'] in ['劍士','狂劍士','大劍士','混沌魔導士','暗月神偷']: newvalues = {"$set": {"work": 12}}
            if i['title'] in ['黑魔導士','暗夜盜賊']: newvalues = {"$set": {"work": 11}}
            if i['title'] in ['劍豪','劍魔']: newvalues = {"$set": {"work": 13}}
            if i['title'] in ['聖劍士', '皇家聖劍士']: newvalues = {"$set": {"work": 14}}
            mycol.update_one({'id':i['id']}, newvalues)      

def bank_rate():  
    all_user = mycol.find()
    for i in all_user:
        if 'bank' in i:
            items = i['bank']
            if items!=[]:
                for item in items.keys():
                    items[item] = round(items[item]*1.0022,2)
                newvalues = {"$set": {"bank": items}}
                # print(newvalues)
                mycol.update_one({'id':i['id']}, newvalues)    

def day_skill_to_0(): 
    all_user = mycol.find()
    for i in all_user:
        if 'rob' in i:
            newvalues = {"$set": {"rob": 0}}
            mycol.update_one(i, newvalues)
        if 'rent' in i :
            newvalues = {"$set": {"rent": 0}}
            mycol.update_one(i, newvalues)
        if 'tax' in i:
            newvalues = {"$set": {"tax": 0}}
            mycol.update_one(i, newvalues)

work_to_10()

schedule.every().day.at("00:30").do(mine_to_0)
schedule.every().day.at("01:00").do(bank_rate)
schedule.every().day.at("00:00").do(day_skill_to_0)
schedule.every().hour.at("00:00").do(work_to_10)

while True:
    schedule.run_pending()
    time.sleep(0.1)