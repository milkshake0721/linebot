import json, random, pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["DnD"]
mycol = mydb["DnD"]

def version():
    return "V.0.2.5b"

def work_minus(id,num):
    user_data = mycol.find_one({"id": id})
    user_data['work'] -= num
    newvalues = {"$set":{'work' : user_data['work']}}
    mycol.update_one({"id": id}, newvalues)

def check_work_times(id,num):
    user_data = mycol.find_one({"id": id})
    if user_data['work'] >= num:return True
    else : return False

def add_user(id, name):
    is_id_exit = mycol.find_one({"id": id})
    is_name_exit = mycol.find_one({"name": name})

    if is_id_exit:  # 檢查 玩家/姓名 是否存在
        return "U had already login as {}".format(is_id_exit["name"])
    if is_name_exit :
        return "Name {} had been used".format(name)

    _id = open("id.txt", "+a")
    _id.write("{},{}\n".format(id, name))
    _id.close

    new_data = {"id" : id , "name": name ,"LV" : 0 , "title" : "村民" , "金幣" : 0 , "銀幣" : 0, "mine": 0 , "work" : 10 , "bank" : {"金幣" : 0 , "銀幣" : 0} , "city" : "蘇爾德村",'been_rob' : {},'you_rob' : {}}
    mycol.insert_one(new_data)

    return "歡迎 {} 的加入\n詳細規則可以輸入/指令 or /規則查看".format(name)

# print(add_user('U1c1925ccd29c125ed845cc2db637f39b','逢'))
# print(add_user('U0bdb890d03a5b755f3dbb67eafa74f5d','尼克'))

def user_profile(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"

    return "{}: {} (lv{})\n  體:{}\n  -位於[{}]".format(user_data['title'],user_data['name'],user_data['LV'],user_data['work'],user_data['city'])

def check_wallet(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    return "金幣：{}枚\n銀幣：{}枚".format(user_data['金幣'],user_data['銀幣'])

def change_user_name(id,name):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if 'change_name' not in user_data:
        return '請先找到魔法少年瞭解規則'
    name = name.replace(' ','')
    if name == '':
        return "請輸入正確的名稱"
    if mycol.find_one({"name": name}): return "名稱已被使用"
    if user_data['change_name'] == 1 :
        if user_data['銀幣'] < 1000:return '更名需要1000銀幣，而你只有{}枚QAQ'.format(user_data['銀幣'])
        newvalues = {
                "$set": {
                    "name" : name,
                    "銀幣" : user_data['銀幣']-1000,
                    "change_name" : 0
                }
            }
        mycol.update_one({"id": id}, newvalues)
        return "Hi {}".format(name)
    else:
        return '請先找到魔法少年瞭解規則'
    
def magic_boy(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['city'] == '蘇爾德村':
        if 'change_name' not in user_data:
            newvalues = {
                    "$set": {
                        "change_name" : 1
                    }
                }
            mycol.update_one({"id": id}, newvalues)
            return "魔法少黏-[甲修]:\n\nHi~{}\n我聽說如果要換名字\n只要輸入\n/更名 名字\n再加上1000銀幣就可以了!!\n但是聽說好像只能換一次".format(user_data['name'])
        if user_data['change_name'] == 1:
            ans_list = ["魔法少黏-[甲修]:\n\n聽說換名字\n只要輸入\n/更名 名字\n再加上1000銀幣就可以了\n","魔法少黏-[甲修]:\n\n    你的名字是{}嗎w?\n".format(user_data['name']),"魔法少黏-[甲修]:\n\n    很高興認識身為{}的{}\n".format(user_data['title'],user_data['name'])]
            ans = random.choice(ans_list)
            return ans
        if user_data['change_name'] == 0:
            ans_list = ["魔法少黏-[甲修]:\n\n名字一生只能換一次呦\n","魔法少黏-[甲修]:\n\n    你的名字是{}嗎w?\n".format(user_data['name']),"魔法少黏-[甲修]:\n\n    很高興認識身為{}的{}\n".format(user_data['title'],user_data['name']),'魔法少黏-[甲修]:\n\n    你換過名字了嗎？\n    {}啊～\n    是個好名字呢'.format(user_data['name'])]
            ans = random.choice(ans_list)
            return ans
    
# print(change_user_name('U1c1925ccd29c125ed845cc2db637f39b','逢'))
# print(magic_boy('U1c1925ccd29c125ed845cc2db637f39b'))

def working(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if check_work_times(id,1):
        work_minus(id,1)
        if user_data['city'] == '蘇爾德村':
            銀幣 = random.randint(12, 30) * user_data['LV'] # 隨機產生礦物
            if random.randint(1,10) == 8:
                newvalues = {
                    "$set": {
                        "銀幣": 銀幣 + user_data["銀幣"],
                        "金幣": 2 + user_data["金幣"]
                    }
                }
                mycol.update_one({"id": id}, newvalues)
                return "打工賺到了{}枚銀幣\n老闆看你認真，多給你2枚金幣".format(銀幣)

            else:  # 更新數量
                newvalues = {
                    "$set": {
                        "銀幣": 銀幣 + user_data["銀幣"],
                    }
                }
                mycol.update_one({"id": id}, newvalues)
                return "打工賺到了{}枚銀幣".format(銀幣)
        elif user_data['city'] == '萊克爾村':
            銀幣 = random.randint(20, 35) * user_data['LV'] # 隨機產生礦物
            if random.randint(1,8) == 4:
                newvalues = {
                    "$set": {
                        "銀幣": 銀幣 + user_data["銀幣"],
                        "金幣": 2 + user_data["金幣"]
                    }
                }
                mycol.update_one({"id": id}, newvalues)
                return "陪阿姨逛街賺到了{}枚銀幣\n阿姨看你可愛，多給你2枚金幣".format(銀幣)

            else:  # 更新數量
                newvalues = {
                    "$set": {
                        "銀幣": 銀幣 + user_data["銀幣"],
                    }
                }
                mycol.update_one({"id": id}, newvalues)
                return "陪阿姨逛街賺到了{}枚銀幣".format(銀幣)
        elif user_data['city'] == '阿拉瑪村':
            銀幣 = random.randint(28, 35) * user_data['LV'] # 隨機產生礦物
            if random.randint(1,8) == 4:
                newvalues = {
                    "$set": {
                        "銀幣": 銀幣 + user_data["銀幣"],
                        "金幣": 2 + user_data["金幣"]
                    }
                }
                mycol.update_one({"id": id}, newvalues)
                return "陪肌肉猛男逛街賺到了{}枚銀幣\n肌肉猛男看你可愛，多給你2枚金幣".format(銀幣)

            else:  # 更新數量
                newvalues = {
                    "$set": {
                        "銀幣": 銀幣 + user_data["銀幣"],
                    }
                }
                mycol.update_one({"id": id}, newvalues)
                return "陪肌肉猛男逛街賺到了{}枚銀幣".format(銀幣)
        elif user_data['city'] == '莫爾茲村':
            銀幣 = random.randint(30, 40) * user_data['LV'] # 隨機產生礦物
            if random.randint(1,8) == 4:
                newvalues = {
                    "$set": {"銀幣": 銀幣 + user_data["銀幣"],"金幣": 2 + user_data["金幣"]}}
                mycol.update_one({"id": id}, newvalues)
                return "當船夫賺到了{}枚銀幣\n肌肉猛男看你可愛，多給你2枚金幣".format(銀幣)

            else:  # 更新數量
                newvalues = {"$set": {"銀幣": 銀幣 + user_data["銀幣"]}}
                mycol.update_one({"id": id}, newvalues)
                return "當船夫賺到了{}枚銀幣".format(銀幣)
        elif user_data['city'] == '布爾維天空城':
            銀幣 = random.randint(30, 40) * user_data['LV'] # 隨機產生礦物
            if random.randint(1,8) == 4:
                newvalues = {
                    "$set": {"銀幣": 銀幣 + user_data["銀幣"],"金幣": 2 + user_data["金幣"]}}
                mycol.update_one({"id": id}, newvalues)
                return "當天空快遞賺到了{}枚銀幣\n老闆看你可愛，多給你2枚金幣".format(銀幣)
            else:  # 更新數量
                newvalues = {"$set": {"銀幣": 銀幣 + user_data["銀幣"]}}
                mycol.update_one({"id": id}, newvalues)
                return "當天空快遞賺到了{}枚銀幣".format(銀幣)
        elif user_data['city'] == '王城' and user_data['王城']>20:
            銀幣 = random.randint(50, 80) * user_data['LV'] # 隨機產生礦物
            if random.randint(1,8) == 4:
                newvalues = {
                    "$set": {"銀幣": 銀幣 + user_data["銀幣"],"金幣": 7 + user_data["金幣"]}}
                mycol.update_one({"id": id}, newvalues)
                return "當天空快遞賺到了{}枚銀幣\n老闆看你可愛，多給你7枚金幣".format(銀幣)
            else:  # 更新數量
                newvalues = {"$set": {"銀幣": 銀幣 + user_data["銀幣"]}}
                mycol.update_one({"id": id}, newvalues)
                return "當天空快遞賺到了{}枚銀幣".format(銀幣)
        elif user_data['city'] == '王城' and user_data['王城']==20:
            return "找村長先唄"

    else:
        return "已耗盡體力，請等下個小時再回來吧"

# print(working("U0bdb890d03a5b755f3dbb67eafa74f5d"))
def investigation(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['city'] == '蘇爾德村':
        if '2023_new_year_priest' in user_data and user_data['2023_new_year_priest']==1:
            if '劍玉' not in user_data:
                newvalues = {"$set" : { '劍玉' : 1 }}
            else : newvalues = {"$set" : { '劍玉' : 1 + user_data['劍玉'] }}
            mycol.update_one(user_data, newvalues)
            return "獲得 劍玉*1\n\n拿給祭司吧～"
    if user_data['city'] == '翠綠森林':
        if '翠綠森林的現況' not in user_data : 
            newvalues = {"$set" : { '翠綠森林的現況' : 1 }}
            mycol.update_one(user_data, newvalues)
            return "獲得 翠綠森林的現況*1\n請回 萊克爾村 找村長報告吧"
        elif user_data['翠綠森林的現況'] == 0 : return "你覺得{}很舒適".format(user_data['city'])
        else : 
            newvalues = {"$set" : { '翠綠森林的現況' : 1 + user_data['翠綠森林的現況'] }}
            mycol.update_one(user_data, newvalues)
            return "獲得 翠綠森林的現況*1\n請回 萊克爾村 找村長報告吧"
    elif user_data['city'] == '阿拉瑪村的地下城':
        if check_work_times(id,2):
            work_minus(id,2)
            how_much = random.choices([1,2,3,4],weights=[8,3,3,1])
            if user_data['title'] in ['法師','魔導士','大法師']:
                how_much = random.choices([1,2,3,4],weights=[7,3,3,1])
            if user_data['title'] in ['黑魔導士']:
                how_much = random.choices([1,2,3,4],weights=[5,3,3,2])
            how_much = how_much[0]
            now_coin = user_data['銀幣']
            if how_much ==1:
                coin = 20 * 5 * user_data['LV']
                sing = '[事件]\n遇到一些不尋常的怪物，並戰勝了它們。'
                if user_data['title'] in ['劍豪','狂劍士','大劍士']:
                    coin= int(coin * 1.3)
                if user_data['title'] in ['聖劍士']:
                    coin= int(coin * 1.7)
            if how_much ==2:
                coin = 28 * 5 * user_data['LV']
                sing = '遇到地下城中的幽靈和幽靈使者，你跟他們聊天勝歡，他們給你一些靈用錢。'
            if how_much ==3:
                if '水球術' not in user_data : return "[事件]\n發現地下城中的寶庫，但由於沒有[水球術]，打不開寶庫"
                coin = 50 * 5 * user_data['LV']
                sing = '[事件]\n發現地下城裡的神秘寶藏，並用[水球術]開啟鎖住的寶庫。'
            if how_much ==4:
                coin = 35 * 5 * user_data['LV']
                if '可樂果' in user_data and user_data['可樂果'] > 0:
                    coin = coin * 4
                    newvalues = {"$set": { '可樂果' : user_data['可樂果'] - 1}}
                    mycol.update_one({"id": id}, newvalues)
                    sing = '[事件]\n遇到地下城裡的邪惡勢力\n你把你的可樂果給他們，他們覺得很開心\n決定給你很多銀幣'
                elif '壽司' not in user_data or user_data['壽司'] == 0:
                    loss = min(now_coin,coin)
                    newvalues = {"$set": { '銀幣' : now_coin - loss}}
                    mycol.update_one({"id": id}, newvalues)
                    return '[事件]\n遇到地下城裡的邪惡勢力\n你被狠狠的打了一頓\n也被搶走了{}枚銀幣'.format(loss)
                elif user_data['壽司'] > 0 :
                    newvalues = {"$set": { '壽司' : user_data['壽司'] - 1}}
                    mycol.update_one({"id": id}, newvalues)
                    sing = '[事件]\n遇到地下城裡的邪惡勢力\n你把你的壽司給他們，他們覺得很開心\n決定給你一些銀幣'
            
            if user_data['title'] in ['法師','魔導士']:
                coin = int(coin * 1.1)
            if '水怪' in user_data:
                if user_data['水怪'] == 1:
                    get_or_not = random.randint(1,3)
                    if get_or_not == 1:
                        sing += '\n\n另外也找到了1個 [阿拉瑪村地下城的齒輪] 共{}個'.format(user_data['阿拉瑪村地下城的齒輪'] + 1)
                        newvalues = {"$set": { '阿拉瑪村地下城的齒輪' : user_data['阿拉瑪村地下城的齒輪'] + 1 }}
                        mycol.update_one({"id": id}, newvalues)
            if user_data['title'] in ['劍豪','劍魔'] and how_much!=3:
                if random.randint(1,3) == 1:
                    coin*=2
                    sing+="\n\n觸發-[血刃]"
            newvalues = {"$set": { '銀幣' : coin + now_coin }}
            if how_much == 3:newvalues = {"$set": { '銀幣' : coin + now_coin ,'金幣': user_data['金幣'] + 2}}
            mycol.update_one({"id": id}, newvalues)
            if how_much == 3:return '{}\n\n獲得{}枚銀幣,2枚金幣'.format(sing,coin)
            return '{}\n\n獲得{}枚銀幣\n剩餘{}體'.format(sing,coin,user_data['work']-2)
        else:
            return "調查地下城需要2體力呦，您的體力貌似不夠"
    if user_data['city'] == '王城':
        if check_work_times(id,1):
            if user_data['王城'] == 1 :
                newvalues = {"$set": { '王城' : 2 }}
                mycol.update_one({"id": id}, newvalues)
                return "您到了王城的大門口\n這邊的重力非比尋常...\n走起路來都很吃力...\n\n您前面有三道看起來歷史悠久的大門\n看得出來跟 阿拉瑪村的地下城 是同個年代的產物\n1.有著香蕉形狀鎖孔的大門\n2.有著魚排形狀鎖孔的大門\n3.有著壽司形狀鎖孔的大門\n您想先打開哪個呢？\n\n請輸入/王城 1"
            if user_data['王城'] == 2 :
                return "您到了王城的大門口\n這邊的重力非比尋常...\n走起路來都很吃力...\n\n您前面有三道看起來歷史悠久的大門\n看得出來跟 阿拉瑪村的地下城 是同個年代的產物\n1.有著香蕉形狀鎖孔的大門\n2.有著魚排形狀鎖孔的大門\n3.有著壽司形狀鎖孔的大門\n您想先打開哪個呢？\n\n請輸入/王城 1"
            if user_data['王城'] == 3 :
                newvalues = {"$set": { '王城' : 4 }}
                mycol.update_one({"id": id}, newvalues)
                return "剛剛的騷動引來了一大批士兵\n\n您要怎麼做?\n\n1.大步向前走\n2.大步向後走\n\n請輸入/王城 1"
            if user_data['王城'] == 4 :
                return "剛剛的騷動引來了一大批士兵\n\n您要怎麼做?\n\n1.大步向前走\n2.大步向後走\n\n請輸入/王城 1"
            if user_data['王城'] == 9 :
                return '在你面前的是一棟大城堡以及一間小屋子\n\n您要往哪兒走?\n\n1.大城堡\n2.小屋子\n\n請輸入/王城 1'
            if user_data['王城'] == 10:
                newvalues = {"$set": { '王城' : 11 }}
                mycol.update_one({"id": id}, newvalues)
                return "王廚的姊姊 -花花:\n嘿!你是誰?\n你怎麼會在這裡?\n看你的穿著是剛剛逃獄出來的吧\n不想被抓的話就用10w銀幣來買我的 廚師衣服\n不然的話等等警衛就要來囉\n\n1.買啦 哪次不買\n2.假賽 警衛來我就扁他\n\n/花花 1"
            if user_data['王城'] == 11:
                return "王廚的姊姊 -花花:\n看你的穿著是剛剛逃獄出來的吧\n不想被抓的話就用10w銀幣來買我的 廚師衣服\n不然的話等等警衛就要來囉\n\n1.買啦 哪次不買\n2.假賽 警衛來我就扁他\n\n/花花 1"
            if user_data['王城'] == 12:
                newvalues = {"$set": { '王城' : 13 }}
                mycol.update_one({"id": id}, newvalues)
                return "王廚的姊姊 -花花:\n你有聽到二樓的聲音嗎?\n上去幫我瞧瞧吧\n上面不應該有那種怪怪的聲音的\n好像有人在上面一樣\n\n你到了二樓\n/調查"
            if user_data['王城'] == 13:
                newvalues = {"$set": { '王城' : 14 }}
                mycol.update_one({"id": id}, newvalues)
                return "[王城廚房的二樓]\n\n二樓空蕩蕩的\n看過去一整片烏漆媽黑，沒有電燈\n只有從樓梯滲出 一樓的微弱光線\n隱隱約約看到一個巫毒娃娃在屋子的正中間\n它裝飾著鮮豔的衣服，臉部則是用紅色和黑色的絲織編織出來的\n眼睛上有一個小紅珠子。巫毒娃娃面對著一個小祭壇，上面放著一些蠟燭和祭品，四周環繞著一些青蛙的獸骨。可以感受到一股陰森的氣氛\n房間的角落有個人在喃喃自語，好像是在念某種咒\n忽然你眼前一黑...\n\n/調查"
            if user_data['王城'] == 14:
                newvalues = {"$set": { '王城' : 15 }}
                mycol.update_one({"id": id}, newvalues)
                return "王城的某處 - XX :\n\n嘿 醒過來!\n\n(你迷糊地醒了過來)\n\n/調查"
            if user_data['王城'] == 15:
                newvalues = {"$set": { '王城' : 16 }}
                mycol.update_one({"id": id}, newvalues)
                return "二王子 - 艾文 :\n\n我先自我介紹一下\n我是二王子 艾文\n你可以當作什麼都沒看到嗎？\n那是我為了篡位而做的，假如你就此當作沒看到的話\n之後等我上了王位必會重賞你的\n\n/調查"
            if user_data['王城'] == 16:
                newvalues = {"$set": { '王城' : 17 }}
                mycol.update_one({"id": id}, newvalues)
                return "二王子 - 艾文 :\n\n我剛剛跟花花說過了\n你是我的秘書\n所以你等等也要跟我去見國王\n希望你不要亂說話\n\n/調查"
            if user_data['王城'] == 17:
                newvalues = {"$set": { '王城' : 18 }}
                mycol.update_one({"id": id}, newvalues)
                return " - (到了王城的辦公室) - \n\n艾文 :\n\n(報告報告....)\n\n/調查"
            if user_data['王城'] == 18:
                newvalues = {"$set": { '王城' : 19 }}
                mycol.update_one({"id": id}, newvalues)
                return "王 - 凱薩約翰 :\n  旁邊的秘書\n  我好像沒怎麼看過你\n  你有東西要報告嗎？\n\n1.我家巷口的大腸麵線超好吃\n2.報告！北爛二王子正在籌備篡位的事宜，被我發現的時候還把我敲暈......\n\n/王城 1"
        else:
            return "您沒體力走不動了"
    if user_data['city'] == '王城的監獄':   
        if check_work_times(id,1):     
            if user_data['王城'] == 5 :
                newvalues = {"$set": { '王城' : 6 }}
                mycol.update_one({"id": id}, newvalues)
                return "你在空蕩蕩的監獄\n\n您要怎麼做?\n\n1.四處瞧瞧\n2.調皮\n\n請輸入/王城 1"
            if user_data['王城'] == 6 :
                return "你在空蕩蕩的監獄\n\n您要怎麼做?\n\n1.四處瞧瞧\n2.調皮\n\n請輸入/王城 1"
            if user_data['王城'] == 7 :
                return "你隱約看到門上有一組數字按鍵\n好像可以讓你按一樣\n\n/打密碼 1234 \n -(這邊當然是輸入你的密碼，不太可能是1234就是了)\n\n提示 前幾句有顯示出的4位數字"
            if user_data['王城'] == 8 :
                newvalues = {"$set": { '王城' : 9 , 'city' : '王城' }}
                mycol.update_one({"id": id}, newvalues)
                return "你躲過了所有獄卒的監視，離開了監獄\n在你面前的是一棟大城堡以及一間小屋子\n\n您要往哪兒走?\n\n1.大城堡\n2.小屋子\n\n請輸入/王城 1"
        else:
            return "您沒體力走不動了"

        return
    else:
        return "你覺得{}很舒適".format(user_data['city'])

def search(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['LV']==0:return '請找村長'
    if check_work_times(id,1):
        work_minus(id,1)
        if user_data['city'] == '蘇爾德村':
            slime = random.randint(20, 50) * (user_data['LV']) # 隨機產生礦物
            bigslime = random.randint(30, 60) * (user_data['LV'])
            monkey = random.randint(80, 100) * (user_data['LV'])
            if user_data['title'] in ['小混混','盜賊']:
                slime = int(slime*1.2)
                bigslime = int(bigslime*1.2)
                monkey = int(monkey*1.2)

            if user_data['LV'] >= 20 :
                slime = int(slime*0.3)
                bigslime = int(bigslime*0.3)
                monkey = int(monkey*0.3)

            meet = (random.choices([slime,bigslime,monkey],weights=[8,2,1]))
            if user_data['LV']>=20 and '萊克爾村' not in user_data and ((user_data['金幣']+user_data['bank']['金幣'])<100):
                meet = (random.choices([slime,bigslime,monkey],weights=[7,5,3]))
            if user_data['title'] == '見習法師':
                meet = (random.choices([slime,bigslime,monkey],weights=[7,3,2]))
            if user_data['title'] in ['法師','魔導士']:
                meet = (random.choices([slime,bigslime,monkey],weights=[5,4,3]))
            
            if int(meet[0]) == slime:
                if user_data["LV"] >=5:
                    win_weight = 8
                    loss_weight = 2
                    if user_data['title'] == '劍士':
                        win_weight +=1
                        loss_weight -= 1
                    if user_data['title'] in ['狂劍士','大劍士']:
                        win_weight +=1.1
                        loss_weight -= 1.1
                    win_or_loss = random.choices(['win','loss'],weights=[win_weight,loss_weight])
                    if win_or_loss[0] == 'loss': return "[事件]\n遇到-屎萊姆\n\n你打輸了\n你掉落{}枚眼淚".format(slime)
                elif user_data["LV"] < 5:
                    win_weight = 7
                    loss_weight = 3
                    if user_data['title'] == '劍士':
                        win_weight +=1
                        loss_weight -= 1
                    if user_data['title'] in ['狂劍士','大劍士']:
                        win_weight +=1.1
                        loss_weight -= 1.1
                    win_or_loss = random.choices(['win','loss'],weights=[win_weight,loss_weight])
                    if win_or_loss[0] == 'loss': return "[事件]\n遇到-屎萊姆\n\n你打輸了\n妳掉落{}枚眼淚".format(slime)
                newvalues = {
                    "$set": {
                        "銀幣": slime + user_data["銀幣"]
                    }
                }
                mycol.update_one({"id": id}, newvalues)
                return "[事件]\n遇到-屎萊姆\n\n擊殺掉了\n它掉落{}枚銀幣".format(slime)
            elif int(meet[0]) == monkey:
                if '可樂果' in user_data:
                    if user_data['可樂果']>0:
                        newvalues = {"$set": {"銀幣" : user_data["銀幣"] + monkey*10 , "可樂果" : user_data['可樂果'] -1 }}
                        mycol.update_one({"id": id}, newvalues)
                        return "[事件]\n你遇到了生氣的猴子，妳給牠吃可樂果\n猴子很開心，決定要報答你他剛找到的銀山\n山上有{}枚銀幣".format(monkey*10)
                if '香蕉' not in user_data or user_data['香蕉'] == 0:
                    monkey = min(monkey,user_data['銀幣'])
                    newvalues = {"$set": {"銀幣" : user_data["銀幣"] - monkey}}
                    mycol.update_one({"id": id}, newvalues)
                    return "[事件]\n你遇到了生氣的猴子，被打了一頓\n支付醫療費{}枚銀幣".format(monkey)
                else:
                    newvalues = {"$set": {"銀幣" : user_data["銀幣"] + monkey , "香蕉" : user_data["香蕉"] - 1}}
                    mycol.update_one({"id": id}, newvalues)
                    return "[事件]\n你遇到了生氣的猴子，妳給牠一隻香蕉\n猴子很開心，決定要報答你他剛找到的寶箱\n裡面有{}枚銀幣".format(monkey)
            else:  # 更新數量
                newvalues = {
                    "$set": {
                        "銀幣" : bigslime + user_data["銀幣"],
                        "金幣" : 1 + user_data["金幣"]
                    }
                }
                if user_data['LV']>=20 and '萊克爾村' not in user_data and ((user_data['金幣']+user_data['bank']['金幣'])<100):
                    newvalues = {
                    "$set": {"銀幣" : bigslime + user_data["銀幣"],"金幣" : 8 + user_data["金幣"]}}
                    mycol.update_one({"id": id}, newvalues)
                    return "[事件]\n遇到-大屎萊姆\n\n擊殺掉了\n它掉落{}枚銀幣以及8枚金幣".format(bigslime)
                mycol.update_one({"id": id}, newvalues)
                return "[事件]\n遇到-大屎萊姆\n\n擊殺掉了\n它掉落{}枚銀幣以及1枚金幣".format(bigslime)
        if user_data['city'] == '萊克爾村':
            slime = random.randint(15, 40) * (user_data['LV']) # 隨機產生礦物
            bigslime = random.randint(30, 55) * (user_data['LV'])
            hippo = random.randint(100, 120) * (user_data['LV'])
            if user_data['LV'] >=35:
                slime =int(slime*0.4)
                bigslime = int(bigslime*0.4)
                hippo = int(hippo*0.4)
            if user_data['title'] in ['小混混','盜賊']:
                slime = int(slime*1.2)
                bigslime = int(bigslime*1.2)
                hippo = int(hippo*1.2)
            meet = (random.choices([slime,bigslime,hippo],weights=[8,2,1]))
            if user_data['title'] == '見習法師':
                meet = (random.choices([slime,bigslime,hippo],weights=[7,3,2]))
            if user_data['title'] in ['法師','魔導士']:
                meet = (random.choices([slime,bigslime,hippo],weights=[4,6,2.2]))
            if int(meet[0]) == slime:
                if user_data["LV"] >=5:
                    win_weight = 8
                    loss_weight = 2
                    if user_data['title'] == '劍士':
                        win_weight +=1
                        loss_weight -= 1
                    if user_data['title'] in ['狂劍士','大劍士']:
                        win_weight +=1.1
                        loss_weight -= 1.1
                    if user_data['title'] in ['劍豪','聖劍士']:
                        win_weight +=1.2
                        loss_weight -= 1.2
                    win_or_loss = random.choices(['win','loss'],weights=[win_weight,loss_weight])
                    if win_or_loss[0] == 'loss': return "[事件]\n遇到-萊姆酒\n\n你乾了\n覺得微醺"
                newvalues = {"$set": {"銀幣": slime + user_data["銀幣"]}}
                mycol.update_one({"id": id}, newvalues)
                return "[事件]\n遇到-綠萊姆\n\n擊殺掉了\n它掉落{}枚銀幣".format(slime)
            elif int(meet[0]) == hippo:
                if '可樂果' in user_data:
                    if user_data['可樂果']>0:
                        newvalues = {"$set": {"銀幣" : user_data["銀幣"] + hippo*5 , "可樂果" : user_data['可樂果'] -1 ,"金幣" : 4 + user_data["金幣"]}}
                        mycol.update_one({"id": id}, newvalues)
                        return "[事件]\n你遇到了生氣的河馬，妳給牠吃可樂果\n河馬很開心，決定要報答你他剛找到的銀山\n山上有{}枚銀幣以及4枚金幣".format(hippo*5)
                if '蘋果' not in user_data or user_data['蘋果'] == 0:
                    hippo = min(hippo,user_data['銀幣'])
                    newvalues = {"$set": {"銀幣" : user_data["銀幣"] - hippo}}
                    mycol.update_one({"id": id}, newvalues)
                    return "[事件]\n你遇到了生氣的河馬，被打了一頓\n支付醫療費{}枚銀幣".format(hippo)
                else:
                    newvalues = {"$set": {"銀幣" : user_data["銀幣"] + hippo , "蘋果" : user_data["蘋果"] - 1}}
                    mycol.update_one({"id": id}, newvalues)
                    return "[事件]\n你遇到了生氣的河馬，妳給牠一顆蘋果\n河馬很開心，決定要報答你他剛找到的寶箱\n裡面有{}枚銀幣".format(hippo)
            else:  # 更新數量
                if user_data['LV']>=33 and '阿拉瑪村' not in user_data and ((user_data['金幣']+user_data['bank']['金幣'])<150):
                    newvalues = {
                    "$set": {"銀幣" : bigslime + user_data["銀幣"],"金幣" : 20 + user_data["金幣"]}}
                    mycol.update_one({"id": id}, newvalues)
                    return "[事件]\n遇到-辣萊姆\n\n擊殺掉了\n它掉落{}枚銀幣以及20枚金幣".format(bigslime)
                newvalues = {
                    "$set": {
                        "銀幣" : bigslime + user_data["銀幣"],
                        "金幣" : 2 + user_data["金幣"]
                    }
                }
                mycol.update_one({"id": id}, newvalues)
                return "[事件]\n遇到-辣萊姆\n\n擊殺掉了\n它掉落{}枚銀幣以及2枚金幣".format(bigslime)
        if user_data['city'] == '阿拉瑪村':
            newvalues = {"$set": {"work" : user_data["work"]}}
            mycol.update_one({"id": id}, newvalues)
            return "阿拉瑪村-村長 知紗子:\n\n 我們村落沒有什麼怪呦，建議到[阿拉瑪村的地下城]去[調查]"
        if user_data['city'] == '碎石洞窟':
            slime = random.randint(15, 40) * (user_data['LV']) # 隨機產生礦物
            bigslime = random.randint(30, 55) * (user_data['LV'])
            hippo = random.randint(100, 120) * (user_data['LV'])
            if user_data['title'] in ['小混混','盜賊']:
                slime = int(slime*1.2)
                bigslime = int(bigslime*1.2)
                hippo = int(hippo*1.2)
            meet = (random.choices([slime,bigslime,hippo],weights=[8,2,1]))
            if user_data['title'] in ['法師','魔導士','大法師']:
                meet = (random.choices([slime,bigslime,hippo],weights=[6.5,4,2.2]))
            if user_data['title'] in ['黑魔導士']:
                meet = (random.choices([slime,bigslime,hippo],weights=[6,4.3,2.5]))
            blood = 0
            if user_data['title'] in ['劍豪','劍魔'] :
                if random.randint(1,3) == 1:
                    blood = 1
            if int(meet[0]) == slime:
                if user_data["LV"] >=5:
                    win_weight = 8
                    loss_weight = 2
                    if user_data['title'] in ['狂劍士','大劍士']:
                        win_weight +=1.1
                        loss_weight -= 1.1
                    win_or_loss = random.choices(['win','loss'],weights=[win_weight,loss_weight])
                    if win_or_loss[0] == 'loss': return "[事件]\n遇到-烤碑\n\n你覺得燙\n起了水泡"
                if blood == 1:
                    newvalues = {"$set": {"銀幣": slime*2 + user_data["銀幣"]}}
                    mycol.update_one({"id": id}, newvalues)
                    return "[事件]\n遇到-可碑\n\n觸發 -[血刃]\n它掉落{}枚銀幣".format(slime)
                newvalues = {"$set": {"銀幣": slime + user_data["銀幣"]}}
                mycol.update_one({"id": id}, newvalues)
                return "[事件]\n遇到-可碑\n\n擊殺掉了\n它掉落{}枚銀幣".format(slime)
            elif int(meet[0]) == hippo:
                if '可樂果' in user_data:
                    if user_data['可樂果']>0:
                        newvalues = {"$set": {"銀幣" : user_data["銀幣"] + hippo*3 , "可樂果" : user_data['可樂果'] -1 }}
                        mycol.update_one({"id": id}, newvalues)
                        return "[事件]\n你遇到了生氣的俗碑，妳給牠吃可樂果\n俗碑很開心，決定要報答你他剛找到的銀山\n山上有{}枚銀幣".format(hippo*3)
                if '蘋果' not in user_data or user_data['蘋果'] == 0:
                    hippo = min(hippo,user_data['銀幣'])
                    newvalues = {"$set": {"銀幣" : user_data["銀幣"] - hippo}}
                    mycol.update_one({"id": id}, newvalues)
                    return "[事件]\n你遇到了生氣的俗碑，被敲了{}枚銀幣".format(hippo)
                else:
                    newvalues = {"$set": {"銀幣" : user_data["銀幣"] + hippo , "蘋果" : user_data["蘋果"] - 1}}
                    mycol.update_one({"id": id}, newvalues)
                    return "[事件]\n你遇到了生氣的俗碑，妳給牠一顆蘋果\n俗碑很開心，決定要報答你他剛找到的寶箱\n裡面有{}枚銀幣".format(hippo)
            else:  # 更新數量
                newvalues = {
                    "$set": {
                        "銀幣" : bigslime + user_data["銀幣"],
                        "金幣" : 2 + user_data["金幣"],
                        "俗頭" : 1 + user_data["俗頭"]
                    }
                }
                mycol.update_one({"id": id}, newvalues)
                return "[事件]\n遇到-馬克碑\n\n擊殺掉了\n它掉落{}枚銀幣,2枚金幣以及1張俗頭\n共{}張".format(bigslime,1 + user_data["俗頭"])
        if user_data['city'] == '莫爾茲村':
            if '獨木粥' not in user_data:
                return "您沒有獨木粥，無法到在此行動"
            if '水怪' not in user_data or user_data['水怪']==0:
                newvalues = {"$set": {"work" : user_data["work"] }}
                mycol.update_one({"id": id}, newvalues)
                return "有水怪在湖泊中游泳，在夜晚發出詭異的叫聲，讓人不寒而慄，附近的原生生態都被破壞了\n請找村長暸解狀況"
            slime = random.randint(15, 40) * (user_data['LV']) # 隨機產生礦物
            bigslime = random.randint(30, 55) * (user_data['LV'])
            hippo = random.randint(100, 120) * (user_data['LV'])
            if user_data['title'] in ['小混混','盜賊']:
                slime = int(slime*1.2)
                bigslime = int(bigslime*1.2)
                hippo = int(hippo*1.2)
            if user_data['title'] == '暗夜盜賊':
                slime = int(slime*1.35)
                bigslime = int(bigslime*1.35)
                hippo = int(hippo*1.35)
            meet = (random.choices([slime,bigslime,hippo],weights=[8,2,1]))
            if user_data['title'] in ['大法師','魔導士']:
                meet = (random.choices([slime,bigslime,hippo],weights=[5,4,2.2]))
            if user_data['title'] in ['黑魔導士','皇家法師']:
                meet = (random.choices([slime,bigslime,hippo],weights=[5,4.2,2.5]))
            if int(meet[0]) == slime:
                if user_data["LV"] >=5:
                    win_weight = 8
                    loss_weight = 2
                    if user_data['title'] in ['劍魔']:
                        win_weight += 2
                        loss_weight -= 1.5
                    if user_data['title'] in ['劍豪','聖劍士','皇家聖劍士']:
                        win_weight +=1.3
                        loss_weight -= 1.3
                    win_or_loss = random.choices(['win','loss'],weights=[win_weight,loss_weight])
                    if win_or_loss[0] == 'loss': return "[事件]\n遇到-青呱\n\n你打輸了\n你掉落{}枚眼淚".format(slime)
                newvalues = {"$set": {"銀幣": slime + user_data["銀幣"]}}
                mycol.update_one({"id": id}, newvalues)
                return "[事件]\n遇到-青呱\n\n擊殺掉了\n它掉落{}枚銀幣".format(slime)
            elif int(meet[0]) == hippo:
                if '可樂果' in user_data:
                    if user_data['可樂果']>0:
                        newvalues = {"$set": {"銀幣" : user_data["銀幣"] + hippo*3 , "可樂果" : user_data['可樂果'] -1 }}
                        mycol.update_one({"id": id}, newvalues)
                        return "[事件]\n你遇到了生氣的滑鼠，妳給牠吃可樂果\n滑鼠很開心，決定要報答你他剛找到的銀山\n山上有{}枚銀幣".format(hippo*3)
                if '螺絲' not in user_data or user_data['螺絲'] == 0:
                    hippo = min(hippo,user_data['銀幣'])
                    newvalues = {"$set": {"銀幣" : user_data["銀幣"] - hippo}}
                    mycol.update_one({"id": id}, newvalues)
                    return "[事件]\n你遇到了生氣的滑鼠，被打了一頓\n支付醫療費{}枚銀幣".format(hippo)
                else:
                    newvalues = {"$set": {"銀幣" : user_data["銀幣"] + hippo , "螺絲" : user_data["螺絲"] - 1}}
                    mycol.update_one({"id": id}, newvalues)
                    return "[事件]\n你遇到了生氣的滑鼠，妳給牠一株螺絲\n滑鼠很開心，決定要報答你他剛找到的寶箱\n裡面有{}枚銀幣".format(hippo)
            else:  # 更新數量
                newvalues = {
                    "$set": {
                        "銀幣" : bigslime + user_data["銀幣"],
                        "金幣" : 3 + user_data["金幣"]
                    }
                }
                mycol.update_one({"id": id}, newvalues)
                return "[事件]\n遇到-地呱\n\n擊殺掉了\n它掉落{}枚銀幣以及3枚金幣".format(bigslime)
        if user_data['city'] == '布爾維天空城':
            if '飛行靴' not in user_data:
                return "您沒有飛行靴，無法在此行動"
            slime = random.randint(15, 40) * (user_data['LV']) # 隨機產生礦物
            bigslime = random.randint(30, 55) * (user_data['LV'])
            hippo = random.randint(100, 120) * (user_data['LV'])
            if user_data['title'] in ['暗夜盜賊','暗月神偷']:
                slime = int(slime*1.35)
                bigslime = int(bigslime*1.35)
                hippo = int(hippo*1.35)
            meet = (random.choices([slime,bigslime,hippo],weights=[8,2,1]))
            if user_data['title'] in ['大法師','魔導士']:
                meet = (random.choices([slime,bigslime,hippo],weights=[5,4,2.2]))
            if user_data['title'] in ['黑魔導士','皇家法師']:
                meet = (random.choices([slime,bigslime,hippo],weights=[5,4.2,2.5]))
            blood = 0
            if user_data['title'] == '劍豪' :
                if random.randint(1,3) == 1:
                    blood = 1
            if user_data['title'] == '劍魔' :
                if random.randint(1,2) == 1:
                    blood = 1
            if int(meet[0]) == slime:
                if user_data["LV"] >=5:
                    win_weight = 8
                    loss_weight = 2
                    if user_data['title'] in ['劍魔']:
                        win_weight += 2
                        loss_weight -= 1.5
                    if user_data['title'] in ['劍豪','聖劍士','皇家聖劍士']:
                        win_weight +=1.3
                        loss_weight -= 1.3
                    win_or_loss = random.choices(['win','loss'],weights=[win_weight,loss_weight])
                    if win_or_loss[0] == 'loss': return "[事件]\n遇到-餛飩甲蟲\n\n你打輸了\n你掉落{}枚眼淚".format(slime)
                if blood == 1:
                    newvalues = {"$set": {"銀幣": slime*2 + user_data["銀幣"]}}
                    mycol.update_one({"id": id}, newvalues)
                    return "[事件]\n遇到-可碑\n\n觸發 -[血刃]\n它掉落{}枚銀幣".format(slime)
                newvalues = {"$set": {"銀幣": slime + user_data["銀幣"]}}
                mycol.update_one({"id": id}, newvalues)
                return "[事件]\n遇到-餛飩甲蟲\n\n擊殺掉了\n它掉落{}枚銀幣".format(slime)
            elif int(meet[0]) == hippo:
                if '可樂果' in user_data:
                    if user_data['可樂果']>0:
                        newvalues = {"$set": {"銀幣" : user_data["銀幣"] + hippo*5 , "可樂果" : user_data['可樂果'] -1 }}
                        mycol.update_one({"id": id}, newvalues)
                        return "[事件]\n你遇到了生氣的彩蕉飛魚，妳給牠吃可樂果\n彩蕉飛魚很開心，決定要報答你他剛找到的銀水\n一杯裡面有{}枚銀幣".format(hippo*5)
            
                if '魚排' in user_data and user_data['魚排'] > 0:
                    hippo = min(hippo*2,user_data['銀幣'])
                    newvalues = {"$set": {"銀幣" : user_data["銀幣"] - hippo , '魚排' : 0}}
                    mycol.update_one({"id": id}, newvalues)
                    return "[事件]\n你遇到了生氣的彩蕉飛魚\n你拿出魚排給他吃\n謝謝你讓他更生氣了\n他直接把你所有魚排打掉，順便爆打你一頓\n-被摸走{}枚銀幣".format(hippo)
                if '草莓' not in user_data or user_data['草莓'] == 0:
                    hippo = min(hippo,user_data['銀幣'])
                    newvalues = {"$set": {"銀幣" : user_data["銀幣"] - hippo}}
                    mycol.update_one({"id": id}, newvalues)
                    return "[事件]\n你遇到了生氣的彩蕉飛魚，你被打了一頓\n也被摸走{}枚銀幣".format(hippo)
                
                else:
                    newvalues = {"$set": {"銀幣" : user_data["銀幣"] + hippo , "草莓" : user_data["草莓"] - 1}}
                    mycol.update_one({"id": id}, newvalues)
                    return "[事件]\n你遇到了生氣的彩蕉飛魚，妳給牠一株草莓\n彩蕉飛魚很開心，決定要報答你他剛找到的寶箱\n裡面有{}枚銀幣".format(hippo)
            else:  # 更新數量
                newvalues = {
                    "$set": {
                        "銀幣" : bigslime + user_data["銀幣"],
                        "金幣" : 3 + user_data["金幣"],
                        "絢彩之羽" : 1 + user_data["絢彩之羽"]
                    }
                }
                mycol.update_one({"id": id}, newvalues)
                return "[事件]\n遇到-香瓜鳥\n\n擊殺掉了\n它掉落{}枚銀幣以及3枚金幣\n外帶一根絢彩之羽".format(bigslime)
        else:
            newvalues = {"$set": {"work" : user_data["work"] }}
            mycol.update_one({"id": id}, newvalues)
            return "{}好像沒有魔物呦".format(user_data['city'])
    else:
        return "已耗盡體力，請等下個小時再回來吧"

# print(search("U1c1925ccd29c125ed845cc2db637f39b"))

def make_love(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['city'] in ['王城','王城的監獄']:
        return "受王城所影響，暫時失去能力"
    if check_work_times(id,4):
        if user_data['銀幣'] < 20 * user_data['LV'] : return "你只有{}枚,這行為需要{}枚銀幣".format(user_data['銀幣'],20 * user_data['LV'])
        work_minus(id,4)
        faith = random.randint(1, 10) # 隨機產生礦物
        if faith == 10:
            newvalues = {
                "$set": {
                    "銀幣": 1000 * user_data['LV'] + user_data["銀幣"],
                }
            }
            mycol.update_one({"id": id}, newvalues)
            return "您的夥伴很滿意，他/她/它給您{}枚銀幣".format(1000)
        elif faith > 6:
            newvalues = {
                "$set": {
                    "銀幣": 100 * user_data['LV'] + user_data["銀幣"],
                }
            }
            mycol.update_one({"id": id}, newvalues)
            return "您的夥伴很滿意，他/她/它給您{}枚銀幣".format(100)
        elif faith >= 2:
            newvalues = {
                "$set": {
                    "銀幣": user_data["銀幣"] - 20 * user_data['LV'],
                }
            }
            mycol.update_one({"id": id}, newvalues)
            return "您的很滿意的花了{}枚銀幣".format(20 * user_data['LV'])
        elif faith == 1:
            steal = 200 * user_data['LV']
            if user_data["銀幣"] < 200 * user_data['LV']:
                steal = user_data["銀幣"]
            newvalues = {
                "$set": {
                    "銀幣": user_data["銀幣"] - steal,
                }
            }
            mycol.update_one({"id": id}, newvalues)
            return "你被仙人跳了，損失{}枚銀幣，你剩下{}枚".format(200,user_data["銀幣"] - steal)
        
    else:
        return "一小時有體力上限，請等下個小時再回來吧\n這行為需要4體力"
    
# print(make_love("U1c1925ccd29c125ed845cc2db637f39b"))

def mining(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    # print(user_data)
    if user_data['city'] in ['王城','王城的監獄']:
        return "受王城所影響，暫時失去能力"
    金幣 = random.randint(2, 5)  # 隨機產生礦物
    銀幣 = random.randint(100, 300)
    if "金幣" in user_data:  # 更新數量
        if user_data["mine"] == 1:
            return "過陣子再來吧！\n一天一次呦~"
        else:
            if user_data['LV']>=60 and '莫爾茲村' not in user_data: #共需要350
                if '獨木粥' not in user_data:
                    金幣=80
                if user_data['bank']['金幣'] + user_data['金幣'] <= 350:
                    金幣=350 - int(user_data['bank']['金幣'] + user_data['金幣'])-5
            newvalues = {
                "$set": {
                    "mine": 1,
                    "銀幣": 銀幣 + user_data["銀幣"],
                    "金幣": 金幣 + user_data["金幣"],
                }
            }
            mycol.update_one({"id": id}, newvalues)
            return "挖到{}個金幣以及{}個銀幣".format(金幣, 銀幣)
    else:
        newvalues = {"$set": {"mine": 1, "銀幣": 銀幣, "金幣": 金幣}}
        # print(newvalues)
        mycol.update_one({"id": id}, newvalues)

        return "挖到{}個金幣以及{}個銀幣".format(金幣, 銀幣)

# print(mining("U0bdb890d03a5b755f3dbb67eafa74f5d"))

def gambling_rules(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    else:
        return "輸入\n/比大小 5 \n 用5塊擲兩顆骰子 跟機器人比大小\n 贏的拿5塊，如果兩顆骰子一樣的話就可以拿雙倍\n 輸的話5塊就沒了\n\n"

# print(gambling_rules("U0bdb890d03a5b755f3dbb67eafa74f5d"))

def big_or_small(id,amount):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['city'] in ['王城','王城的監獄']:
        return "受王城所影響，暫時失去能力"
    if check_work_times(id,1):
        if user_data['銀幣'] < amount : return "你只有{}枚".format(user_data['銀幣'])
        work_minus(id,1)
        user_data['銀幣'] = user_data['銀幣']-amount

        pc_random_1 = random.randint(2, 6)
        pc_random_2 = random.randint(2, 6)
        gamer_random_1 = random.randint(1, 6)
        gamer_random_2 = random.randint(1, 6)

        if gamer_random_1+gamer_random_2 > pc_random_1+pc_random_2: 
            amount = amount*2
            newvalues = {"$set": {"銀幣": user_data['銀幣'] + amount}}
            mycol.update_one({"id": id}, newvalues)
            return "你擲到的骰子點數為({},{})\n機器人的點數為({},{})\n恭喜獲得{}枚銀幣!".format(gamer_random_1,gamer_random_2,pc_random_1,pc_random_2,amount)
        elif gamer_random_1+gamer_random_2 == pc_random_1+pc_random_2: 
            return "你擲到的骰子點數為({},{})\n機器人的點數為({},{})\n啥都沒花生".format(gamer_random_1,gamer_random_2,pc_random_1,pc_random_2)
        else:
            amount = 0
            newvalues = {"$set": {"銀幣": user_data['銀幣']}}
            mycol.update_one({"id": id}, newvalues)
            return "你擲到的骰子點數為({},{})\n機器人的點數為({},{})\n恭喜獲得一場空ˊˇˋ".format(gamer_random_1,gamer_random_2,pc_random_1,pc_random_2)
    else:
        return "已耗盡體力，請等下個小時再回來吧"

# print(big_or_small("U1c1925ccd29c125ed845cc2db637f39b",3))

def put_in_bank(id,cmd):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['city'] in ['王城','王城的監獄']: return "王城的系統不支援SWIFT匯款"
    if '銀' in cmd:
        item = '銀幣'
        a = cmd.replace('幣','')
        a = a.replace('銀','')
        amount = int(a)
    if '金' in cmd:
        item = '金幣'
        a = cmd.replace('幣','')
        a = a.replace('金','')
        amount = int(a)
    if '銀' not in cmd and '金' not in cmd:
        item = '銀幣'
        amount = int(cmd)
    if item != '金幣' and item !='銀幣':return '請放到你的倉庫，銀行不收{}'.format(item)
    if user_data[item] < amount:return "你的{}不夠哦，你只有{}個".format(item,user_data[item])
    else:
        if item not in user_data['bank']:
            now = user_data[item] 
            newvalues = {"$set":{item : now - amount}}
            mycol.update_one({"id": id}, newvalues)

            user_data['bank'][item] = amount
            newvalues = {"$set":{'bank' : user_data['bank']}}
            mycol.update_one({"id": id}, newvalues)

            return "將{}枚{}放入銀行".format(amount,item)

        else:
            newvalues = {"$set" : { item : user_data[item]-amount }}
            mycol.update_one(user_data, newvalues)

            user_data['bank'][item] = amount + user_data['bank'][item]
            newvalues = {"$set":{'bank' : user_data['bank']}}
            mycol.update_one({"id": id}, newvalues)

            return "將{}枚{}放入銀行\n銀行有{}枚\n身上有{}枚".format(amount,item,user_data['bank'][item],user_data[item]-amount)

# print(put_in_bank('U1c1925ccd29c125ed845cc2db637f39b','香蕉',1))

def pull_out_bank(id,cmd):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['city'] in ['王城','王城的監獄']: return "王城的系統不支援SWIFT匯款"
    if '銀' in cmd:
        item = '銀幣'
        a = cmd.replace('幣','')
        a = a.replace('銀','')
        print(a)
        amount = int(a)
    if '金' in cmd:
        item = '金幣'
        a = cmd.replace('幣','')
        a = a.replace('金','')
        amount = int(a)
    if '銀' not in cmd and '金' not in cmd:
        item = '銀幣'
        amount = int(cmd)
    if item != '金幣' and item !='銀幣':return '銀行裡沒有{}...'.format(item)
    else:
        if item not in user_data['bank']:
            return "你的銀行內沒有{}".format(item)
        else:
            bank_amount = user_data['bank'][item]
            if bank_amount < amount:return "你銀行的{}不夠哦，你只有{}枚".format(item,bank_amount)

            newvalues = {"$set" : { item : user_data[item] + amount }}
            mycol.update_one(user_data, newvalues)

            user_data['bank'][item] = bank_amount - amount
            newvalues = {"$set":{'bank' : user_data['bank']}}
            mycol.update_one({"id": id}, newvalues)

            return "取出{}枚{}\n銀行有{}枚\n身上有{}枚".format(amount,item,bank_amount - amount,user_data[item] + amount)

def leader(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['city'] == '蘇爾德村':
        if user_data['LV'] == 0:
            newvalues = {
                    "$set": {
                        "LV" : 1
                    }
                }
            mycol.update_one({"id": id}, newvalues)
            return "蘇爾德村-村長:\n\nHi~{}\n我是蘇爾德村的村長 索倫\n如果想要升等\n請找祭司幫您升等哦~\n告訴他是我請你去找他就行了".format(user_data['name'])
        if user_data['LV'] < 5:
            return "蘇爾德村-村長 索倫:\n\nHi~{}\n當你五等的時候\n可以來找我選擇職業呦".format(user_data['name'])
        if user_data['LV']>=5 and 'change_title' not in user_data:
            newvalues = {
                    "$set": {
                        "change_title" : 1
                    }
                }
            mycol.update_one({"id": id}, newvalues)
            return "蘇爾德村-村長 索倫:\n\n最近過得如何{}\n天啊！沒想到你已經五等了！\n\n想轉職了嗎？\n總共有4種職業可以選呦\n1.劍士\n  鬥士(被動技能)\n   -打怪勝率+10%\n    -體力+2\n\n2.見習法師\n  冥想(主動技能)\n   -想想可樂果\n\n3.小混混\n  偷竊(主動技能)\n   -每天可以偷別人一次\n    不一定成功就是\n\n4.農夫\n  農夫\n\n想轉職的話請輸入\n\n/轉職 劍士\n".format(user_data['name'])
        else :
            ans_list = ["蘇爾德村-村長 索倫:\n\n    Hi~{} 最近過得如何呀？\n".format(user_data['name']),"蘇爾德村-村長 索倫:\n\n    探險的還順利嗎0.0?\n","蘇爾德村-村長 索倫:\n\n    不知道為什麼，我老婆蓮娜總是哭哭啼啼的\n","蘇爾德村-村長 索倫:\n\n    一切都還順利嗎?\n","蘇爾德村-村長 索倫:\n\n    你可以戰勝挑戰！\n","蘇爾德村-村長 索倫:\n\n    你是最棒的！\n"]
            if 'liannaQQ' in user_data and user_data['liannaQQ'] == 10:
                ans_list = ["蘇爾德村-村長 索倫:\n\n    Hi~{} 最近過得如何呀？\n".format(user_data['name']),"蘇爾德村-村長 索倫:\n\n    探險的還順利嗎0.0?\n","蘇爾德村-村長 索倫:\n\n    不知道為什麼，我老婆不見了\n","蘇爾德村-村長 索倫:\n\n    一切都還順利嗎?\n","蘇爾德村-村長 索倫:\n\n    你可以戰勝挑戰！\n","蘇爾德村-村長 索倫:\n\n    你是最棒的！\n"]
            ans = random.choice(ans_list)
            return ans
    if user_data['city'] == '萊克爾村':
        if "翠綠森林" not in user_data:
            return "萊克爾村-村長 克里西斯:\n\n  您好，我是村長 克里西斯\n  歡迎來到萊克爾村\n  我們村莊旁邊的[翠綠森林]最近遭魔物盤據\n  希望{}大人能前去[調查]一下\n 並回來告訴我那邊的情況\n\n-傳送去[翠綠森林]並[調查]".format(user_data['title'])
        if '翠綠森林的現況' in user_data and user_data['翠綠森林的現況'] != 0:
            if user_data['翠綠森林的現況'] == 1:
                newvalues = {"$set":{'銀幣' : user_data['銀幣'] + 1000 , '翠綠森林的現況' : 0}}
                mycol.update_one({"id": id}, newvalues)
                return "萊克爾村-村長 克里西斯:\n\n  謝謝您的幫忙！\n  我們會盡快派兵去消滅他們的\n  這1000枚銀幣不成敬意，收下吧"
            else:
                newvalues = {"$set":{'金幣' : user_data['金幣'] + 10 , '翠綠森林的現況' : 0}}
                mycol.update_one({"id": id}, newvalues)
                return "萊克爾村-村長 克里西斯:\n\n  感謝您的幫忙！\n  您竟然調查的那麼仔細\n這10枚金幣就請收下吧"
        if '女巫' not in user_data:
            return "萊克爾村-村長 克里西斯:\n\n  您有遇到翠綠森林的女巫嗎?\n  她好像對法術略知一二\n  有空可以找她聊聊\n"
        if user_data['LV'] < 25:
            return "萊克爾村-村長 克里西斯:\n\nHi~{}\n當你25等的時候\n可以來找我選擇職業呦~".format(user_data['name'])
        if user_data['LV'] >= 25 and user_data['title'] != '村民' and user_data['change_title'] == 1 :
            newvalues = {
                    "$set": {
                        "change_title" : 2
                    }
                }
            mycol.update_one({"id": id}, newvalues)
            if user_data['title'] == '劍士':
                advice = '身為劍士的你，有兩條路能走~,\n\n狂劍士\n大劍士\n\n基本上這兩個職業沒什麼差別，因為目前作者沒時間多做，給兩個選擇讓你感覺有選擇一樣 :p\n\n所有能力小幅提升'
            if user_data['title'] == '見習法師':
                advice = '身為見習法師的你，有兩條路能走~,\n\n法師\n魔導士\n\n基本上這兩個職業沒什麼差別，因為目前作者沒時間多做，下一轉應該會做出差異  吧 :p\n\n冥想所消耗體力減少2'
            if user_data['title'] == '小混混':
                advice = '身為小混混的你，可以轉成\n盜賊\n\n所有能力將小幅提升'
            if user_data['title'] == '農夫':
                advice = '\n耕耘萬里田，收穫歡樂真。\n種種苦難裏，終有果決顯。\n久雨新秋晚，霜降迎秋寒。\n茂葉萬種翠，收割滿院間。\n夜夜澆灌苦，朝朝收禾穀。\n穩健耕者身，榮耀收穫時。\n\n耕者有其田\n您擁有一大片土地\n -/收租\n\n/轉職 大地主\n'
            return "萊克爾村-村長 克里西斯:\n\n最近過得如何{}\n天啊！沒想到你已經25等了！\n\n可以轉職了呦~\n{}".format(user_data['name'],advice)
        if '永恆之森' not in user_data and '水球術'in user_data:
            newvalues = {"$set": {"女巫" : 5 }}
            mycol.update_one({"id": id}, newvalues)
            return "萊克爾村-村長 克里西斯:\n\n  對了，您去過[永恆之森]了嗎？ \n  蒂拉芙·林茵好像對那座森林很有興趣\n  找時間跟她聊聊吧\n"
        return "萊克爾村-村長 克里西斯:\n\n  您好，我是村長 克里西斯\n  歡迎來到萊克爾村～\n  我們村莊的環境不錯喔\n  歡迎來玩～"
    if user_data['city'] == '阿拉瑪村':
        if '火球術' in user_data and '阿拉瑪村的地下城' not in user_data:
            return "阿拉瑪村-村長 知紗子:\n\n  您好，我是村長 知紗子\n  歡迎來到阿拉瑪村\n  什麼!?你會火球術!!\n  是這樣的 我們村莊有一個古老的地下城\n  必須要使用火球術才能將大門打開\n  如果您能幫忙打開大門\n  我們會很感謝您的\n\n請在[阿拉瑪村]使用[火球術]".format(user_data['title'])
        if '火球術' not in user_data:
            return "阿拉瑪村-村長 知紗子:\n\n  您好，我是村長 知紗子\n  歡迎來到阿拉瑪村\n  原來你不會[火球術]呀...\n  是這樣的 我們村莊有一個古老的地下城\n  必須要使用火球術才能將大門打開\n  如果您能幫忙打開大門\n  我們會很感謝您的\n"
        if '地下城的門' not in user_data:
            if '俗頭' not in user_data :
                newvalues = {"$set": {"俗頭" : 0 ,'碎石洞窟' : 0}}
                mycol.update_one({"id": id}, newvalues)
                return "阿拉瑪村-村長 知紗子:\n\n  地下城是打開了...\n  但是這個門整個被你燒壞...\n  現在古堡內的生物時不時就會出來\n  影響到我們的生活\n  現在需要做一個大門\n  需要請你幫忙拿10張俗頭給我，謝謝\n  請你到我們村莊附近的[碎石洞窟]\n  那邊的馬克碑有機會會掉落俗頭\n  來吧，這是[碎石洞窟]的傳送卡  \n  再麻煩了\n\n/傳送 碎石洞窟"
            if user_data['俗頭'] <10:
                return "阿拉瑪村-村長 知紗子:\n\n  有10張俗頭給我了嗎？\n  請到我們村莊附近的[碎石洞窟]\n  那邊的馬克碑有機會會掉落俗頭哦~\n"
            elif user_data['俗頭']>=10:
                newvalues = {"$set": {"地下城的門" : 1 ,"銀幣": 150000 + user_data['銀幣'],'金幣' : user_data['金幣'] + 200}}
                mycol.update_one({"id": id}, newvalues)
                return "阿拉瑪村-村長 知紗子:\n\n  謝謝您～\n  我們的村莊這下總算安全了～\n  這是一點酬勞，謝謝你的幫助～\n  另外，60等時記得來找我哦～\n\n-銀幣150000\n-金幣200"
        if user_data['LV'] < 60:
            return "阿拉瑪村-村長 知紗子:\n\nHi~{}\n當你60等的時候\n可以來找我選擇職業呦~".format(user_data['name'])
        if user_data['LV'] >= 60 and user_data['change_title'] == 3:
            if user_data['title'] == '狂劍士':
                advice = '身為狂劍士的你，將升成 劍豪\n  血刃(被動技能)\n  -爆擊機率提升\n  體力+1\n其他能力小幅提升\n/轉職 劍豪\n'
            if user_data['title'] == '大劍士':
                advice = '身為大劍士的你，將升成 聖劍士\n  英勇(被動技能)\n  -遇見不死魔物掉落提升\n  體力+2\n其他能力小幅提升\n/轉職 聖劍士'
            if user_data['title'] == '魔導士':
                advice = '身為魔導士的你，將升成 黑魔導士\n  夜火 (被動技能)\n  -特殊調查 觸發率大幅提升\n  體力+1\n/轉職 黑魔導士'
            if user_data['title'] == '法師':
                advice = '身為法師的你，將升成 大法師\n  沈穩(被動技能)\n  -冥想所消耗體力減少4\n/轉職 大法師'
            if user_data['title'] == '盜賊':
                advice = '身為盜賊的你，可以轉成 暗夜盜賊\n  能力有加成～\n  體力+1\n/轉職 暗夜盜賊'
            if user_data['title'] == '大地主':
                advice = '親愛的大地主，您深受百姓愛戴，國王封給你一塊屬於你的領地\n\n -/收稅\n\n/轉職 領主\n'
            return "阿拉瑪村-村長 知紗子:\n\n最近過得如何{}\n天啊！沒想到你已經60等了！\n\n可以轉職了呦~\n\n{}".format(user_data['name'],advice)
        else:
            return "阿拉瑪村-村長 知紗子:\n\n  歡迎來到阿拉瑪村\n  歡迎在我們村逛逛~"
    if user_data['city'] == '莫爾茲村':
        if '獨木粥' not in user_data:
            return "您沒有獨木粥，無法到達村長的辦公室"
        if '水怪' not in user_data:
            newvalues = {"$set": {"水怪" : 0}}
            mycol.update_one({"id": id}, newvalues)
            return "莫爾茲村-村長 弗里曼:\n\n您好我是這個村的村長 弗里曼\n身為{}的您，請務必幫我們這個忙\n\n原本我們村是一個非常安靜的小村莊。村民們自給自足，生活著平凡又幸福的日子。\n然而，有一天，村民們發現我們的湖被一種古怪的水怪所打擾，這個水怪是一種極其可怕的怪物，它喜歡吃著村民們的藥草和稻米，同時也把村民們的湖泊搞得一團糟QQ\n\n後來我們發現他最愛吃藥草！\n希望你能給我一些藥草，一部分要拯救我們的傷兵，一部分要引走水怪\n\n總共需要10張藥草".format(user_data['title'])
        if '藥草' not in user_data or user_data['藥草'] < 10 and user_data['水怪'] == 0:
            return "莫爾茲村-村長 弗里曼:\n\n可以請您帶10張 藥草 給我嗎🥺? 謝謝~!!"
        if user_data['藥草'] >= 10 and user_data['水怪'] == 0:
            newvalues = {"$set": {"水怪" : 1 , '藥草' : user_data['藥草'] - 10 ,'阿拉瑪村地下城的齒輪' : 0}}
            mycol.update_one({"id": id}, newvalues)
            return "莫爾茲村-村長 弗里曼:\n\n謝謝您！\n我們終於有救了😍"
        if user_data['水怪'] == 1 and '阿拉瑪村地下城的齒輪' not in user_data:
            return "莫爾茲村-村長 弗里曼:\n\n謝謝您！水怪終於引走了\n為了防止他回來，我們正在修復一個古代機關，以前防止水怪闖進來的\n但是發現少了五個零件\n可以請您幫忙找給我們嗎？\n\n這是前人留下的訊息:\n紅日沉沒 日落西山\n英雄前往 阿拉瑪村\n藏匿齒輪 發掘秘密\n抵禦水怪 守護平安\n\n尋找齒輪 勇敢挑戰\n開啟機關 解除魔障\n千錘百鍊 把鋼鐵改\n英雄豪情 天下無雙\n"
        if user_data['水怪'] == 1 and user_data['阿拉瑪村地下城的齒輪'] < 5:
            return "莫爾茲村-村長 弗里曼:\n\n水怪終於引走了\n為了防止他回來，我們正在修復一個古代機關，以前防止水怪闖進來的\n但是發現少了五個零件\n可以請您幫忙找給我們嗎？\n\n這是前人留下的訊息:\n紅日沉沒 日落西山\n英雄前往 阿拉瑪村\n藏匿齒輪 發掘秘密\n抵禦水怪 守護平安\n\n尋找齒輪 勇敢挑戰\n開啟機關 解除魔障\n千錘百鍊 把鋼鐵改\n英雄豪情 天下無雙\n"
        if user_data['水怪'] == 1 and user_data['阿拉瑪村地下城的齒輪'] >= 5:
            newvalues = {"$set": {"水怪" : 2 , '阿拉瑪村地下城的齒輪' : user_data['阿拉瑪村地下城的齒輪'] - 5 , '金幣' : user_data['金幣'] +200 , '銀幣': user_data['銀幣']+150000}}
            mycol.update_one({"id": id}, newvalues)
            return "莫爾茲村-村長 弗里曼:\n\n謝謝您的幫助，我們的城鎮終於恢復原本的秩序了😍!!\n這點心意收下唄\n\n-200金\n-15w銀"
        if user_data['LV'] < 90:
            return "莫爾茲村-村長 弗里曼:\n\nHi~{}大人\n當你90等的時候\n可以來找我選擇職業呦~".format(user_data['name'])
        if user_data['LV'] >= 90 and user_data['change_title'] == 4:
            if user_data['title'] == '劍豪':
                advice = '身為劍豪的你，將升成 劍魔\n  無懼(被動技能)\n  -勝率大幅提升\n其他能力小幅提升\n/轉職 劍魔\n'
            if user_data['title'] == '聖劍士':
                advice = '身為聖劍士的你，將升成 皇家聖劍士\n  聖劍(被動技能)\n  -遇見不死魔物掉落提升\n  體力+1\n其他能力小幅提升\n/轉職 皇家聖劍士\n'
            if user_data['title'] == '黑魔導士':
                advice = '身為魔導士的你，將升成 混沌魔導士\n  闇 (被動技能)\n  -調查成功率大幅提升\n體力+1\n/轉職 混沌魔導士\n'
            if user_data['title'] == '大法師':
                advice = '身為大法師的你，將升成 皇家法師\n  聖光(被動技能)\n  -冥想所消耗體力減少5\n/轉職 皇家法師'
            if user_data['title'] == '暗夜盜賊':
                advice = '身為暗夜盜賊的你，可以轉成 暗月神偷\n能力有加成～\n/轉職 暗月神偷'
            if user_data['title'] == '領主':
                advice = '親愛的領主，您深受百姓愛戴，國王賜給您一個大公的職位\n\n -/收稅\n\n/轉職 大公\n'
            return "莫爾茲村-村長 弗里曼:\n\n最近過得如何{}\n天啊！沒想到你已經90等了！\n\n可以轉職了呦~\n\n{}".format(user_data['name'],advice)
        return "莫爾茲村-村長 弗里曼:\n\n  又是一個和平的日子呀～"
    if user_data['city'] == '布爾維天空城':
        if '飛行靴' not in user_data:
            return "您沒有飛行靴，無法到達村長的辦公室"
        if user_data['布爾維天空城'] == 1:
            newvalues = {"$set": {"布爾維天空城" : 2}}
            mycol.update_one({"id": id}, newvalues)
            return "布爾維天空城-守衛 尤里:\n\n  歡迎來到布爾維天空城~\n  我是城的守衛 尤里\n  我們主人 卡羅琳 在睡覺，請稍後再來訪\n  謝謝"
        if user_data['布爾維天空城'] == 2:
            newvalues = {"$set": {"布爾維天空城" : 3}}
            mycol.update_one({"id": id}, newvalues)
            return "布爾維天空城-守衛 尤里:\n\n  我們主人 卡羅琳 還在睡覺ㄟ，晚點再來訪啦\n  抱歉"
        if user_data['布爾維天空城'] == 3:
            newvalues = {"$set": {"布爾維天空城" : 4}}
            mycol.update_one({"id": id}, newvalues)
            return "尤里:\n\n  真的很..\n\nxx:\n尤里～你有看到卡羅琳大人嗎？\n我到處都找不到她\n\n尤里:\n\n  歐，{}大人，這位是瑪莎..我們的管家 瑪莎\n\n管家 瑪莎:  \n  歐歐 {}您好\n  我們大人一定又在翠綠森林找林茵聊天...\n  可以請您幫忙請她回來嗎？\n  我暫時忙到有點抽不開身🫠\n  謝謝".format(user_data['name'],user_data['name'])
        if user_data['布爾維天空城'] == 4:
            return "管家 瑪莎:  \n  我們大人一定又在翠綠森林找林茵聊天...\n  可以請您幫忙請她回來嗎？\n  我暫時忙到有點抽不開身🫠\n  謝謝".format(user_data['name'],user_data['name'])
        if user_data['布爾維天空城'] == 5:
            newvalues = {"$set": {"布爾維天空城" : 6}}
            mycol.update_one({"id": id}, newvalues)
            return "布爾維天空城-郡主 卡羅琳:\n\n  謝謝你找我回來\n  不然瑪莎真的會累死😅\n\n  啊! 都忘記自我介紹了\n  歡迎來到布爾維天空城~\n  我是卡羅琳～\n"
        if user_data['布爾維天空城'] == 6:
            newvalues = {"$set": {"布爾維天空城" : 7 , '絢彩之羽' : 0}}
            mycol.update_one({"id": id}, newvalues)
            return "布爾維天空城-郡主 卡羅琳:\n\n  最近我們城飛來了一群不速之客，想請您幫忙把他們趕走\n  另外他們會掉落[絢彩之羽]\n  幫我收集10個唄 {}大人🥺\n\n/打怪".format(user_data['title'])
        if user_data['布爾維天空城'] == 7 and user_data['絢彩之羽']<10:
            return "布爾維天空城-郡主 卡羅琳:\n\n  那群不速之客會掉落[絢彩之羽]\n  幫我收集10個唄 {}大人🥺".format(user_data['title'])
        if user_data['布爾維天空城'] == 7 and user_data['絢彩之羽']>=10:
            newvalues = {"$set": {"布爾維天空城" : 8 , '絢彩之羽' : user_data['絢彩之羽'] - 10}}
            mycol.update_one({"id": id}, newvalues)
            return "布爾維天空城-郡主 卡羅琳:\n\n  謝謝尼～\n  這樣我就可以做絢彩羽衣了❤️".format(user_data['title'])
        if user_data['布爾維天空城'] == 8 :
            newvalues = {"$set": {"布爾維天空城" : 9 , '絢彩羽衣' : 1}}
            mycol.update_one({"id": id}, newvalues)
            return "布爾維ˇ=城-郡主 卡羅-:\n\n  開玩笑的啦 >w<\n  怎麼可能只做我的~\n  來，這是你的～\n\n- 絢彩羽衣*1"
        if user_data['布爾維天空城'] == 9 :
            a=0
            sig = ""
            if '氧氣' in user_data:
                a=1
                sig += " 氧氣"
            if '香香的空氣' in user_data:
                a=1
                sig += " 香香的空氣"
            if '臭臭的空氣' in user_data:
                a=1
                sig += " 臭臭的空氣"
            if '稀薄的空氣' in user_data:
                a=1
                sig += " 稀薄的空氣"
            if '空氣' in user_data:
                a=1
                sig += " 空氣"
            if a == 1:
                newvalues = {"$set": {"布爾維天空城" : 10}}
                mycol.update_one({"id": id}, newvalues)
                return "3爾d+空城-郡主 卡^琳:\n\n快收進背包吧...\n\n咦！你包包裡面怎麼有{}的發票XD \n你被當成盤子啦🤣\n不過這樣看您銀幣也是蠻多的，哈哈哈哈\n".format(sig)
            else:
                newvalues = {"$set": {"布爾維天空城" : 10}}
                mycol.update_one({"id": id}, newvalues)
                return "b爾3天空*-郡主 /羅琳:\n\n快收進背包吧...\n\n咦 你怎麼有 藥草 俗頭\n  那是 阿拉瑪村地下城的齒輪嗎！這很稀有誒😲\n看樣子您也去過真多地方～\n不知道你玩得開不開心\n"
        if user_data['布爾維天空城'] == 10 :
            newvalues = {"$set": {"布爾維天空城" : 11}}
            mycol.update_one({"id": id}, newvalues)
            return "b爾3天空*-郡z /FL:\n\n好啦~\n講了一對廢話:P\n也不知道你有沒有認真在看我們對話\n\n劇情到這也告一個段落了...\n"
        if user_data['布爾維天空城'] == 11 :
            newvalues = {"$set": {"布爾維天空城" : 12}}
            mycol.update_one({"id": id}, newvalues)
            return "作者 -逢:\n\n最後也謝謝你願意玩到這邊XD\n也請到這邊留個回饋:https://forms.gle/sKqhTxpUKSqURNrr7\n我先繼續修Bug了 \n88~\n\n  - 終(暫時)\n"
        if user_data['布爾維天空城'] == 12 :
            newvalues = {"$set": {"布爾維天空城" : 13}}
            mycol.update_one({"id": id}, newvalues)
            return "布爾維天空城-郡主 卡羅琳:\n\n  嗯...\n  剛剛是哪招\n"
        if user_data['布爾維天空城'] ==13:
            return "布爾維天空城-郡主 卡羅琳:\n\n  哈囉~😅\n  歡迎在我的城內逛逛呦~\n  我應該一直都會在哦！"
    if user_data['city'] == '王城' and user_data['王城'] == 20:
        if user_data['叛亂'] == 0:
            newvalues = {"$set": {"王城" : 21 }}
            mycol.update_one({"id": id}, newvalues)
            return "王:\n\n  歡迎光臨王城\n謝謝你之前告訴我關於二王子的事情\n讓我能在最壞情況發生之前做準備\n現在王城中分兩派勢力\n一派是我們國王軍\n另一派是二王子的叛軍\n我們預計每週日會發兵攻打他們\n希望您能支援我們\n有任何問題在找[大臣]唄\n"
        if user_data['叛亂'] == 1:
            newvalues = {"$set": {"王城" : 21 }}
            mycol.update_one({"id": id}, newvalues)
            return "二王子:\n\n  歡迎光臨王城\n謝謝你之前舉發我的事情\n讓我能成功發起突襲\n現在王城中分兩派勢力\n一派是我們叛軍\n另一派是國王的國王軍\n我們預計每週日會發兵攻打他們\n希望您能支援我們\n有任何問題在找我的[大臣]唄\n"
    else:
        return "此區無村長"
    
# print(leader('U1c1925ccd29c125ed845cc2db637f39b'))
def lianna(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['city'] == '蘇爾德村' and user_data['title']!='村民':
        if 'liannaQQ' not in user_data:
            newvalues = {"$set": {"liannaQQ" : 1 }}
            mycol.update_one({"id": id}, newvalues)
            return "蘇爾德村-村長夫人 蓮娜:\n\n    嗚嗚嗚...\n"
        if user_data['liannaQQ'] != 10:
            newvalues = {"$set": {"liannaQQ" : 1 + user_data['liannaQQ'] }}
            mycol.update_one({"id": id}, newvalues)
            return "蘇爾德村-村長夫人 蓮娜:\n\n    嗚嗚嗚..\n"
        if user_data['liannaQQ'] == 10:
            return "蘇爾德村-村長夫人 蓮娜:\n\n    謝謝{}願意關心我🥹，也陪我度過一個美麗的夜晚\n我們必須私奔。我們的愛情不能被拘束，我們必須獨自面對所有的困難，堅守我們的愛情。就算未來充滿艱辛，我們都會堅持到最後，因為我們對彼此的愛是真誠的。\n    我聽說商人有在賣萊克爾村的傳送卡\n    我們一起過去吧".format(user_data['name'])
    if user_data['city'] == '萊克爾村' and user_data['liannaQQ'] == 10 :
        return "你的老婆 蓮娜:\n\n  {},我們一起在 萊克爾村 逛逛吧".format(user_data['name'])

def seller(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['LV'] < 5:
        newvalues = {"$set": {"buy_ability" : 1 }}
        mycol.update_one({"id": id}, newvalues)
        return "蘇爾德村-商人 泰瑞爾:\n\n    Hi~伙計\n    我是這個村的商人\n    我有些好東西你要不參考看看\n    1.香蕉 1銀\n    2.空氣 100銀\n    輸入/泰瑞爾 1 (編號)來進行購買"
    if user_data['LV'] >= 5 and user_data['city'] == '蘇爾德村':
        newvalues = {"$set": {"buy_ability" : 1 }}
        mycol.update_one({"id": id}, newvalues)
        return "蘇爾德村-商人 泰瑞爾:\n\n    Hi~伙計\n    我是這個村的商人\n    我有些好東西你要不參考看看\n    1.香蕉 1銀\n    2.空氣 100銀\n    3.萊克爾村-傳送卡 100金\n    輸入/泰瑞爾 1 (編號)來進行購買\n"
    if user_data['city'] == '萊克爾村':
        return "萊克爾村-商人 莉法:\n\n    Hi~伙計\n    我是這個村的商人\n    我有些好東西你要不參考看看\n    1.蘋果 1銀\n    2.稀薄的空氣 500銀\n    3.阿拉瑪村-傳送卡 150金\n    4.翠綠森林-傳送卡 15金\n    輸入/莉法 1 (編號)來進行購買\n"
    if user_data['city'] == '阿拉瑪村':
        return "阿拉瑪村-商人 吉斯:\n\n    Hi~伙計\n    我是這個村的商人\n    我有些好東西你要不參考看看\n    1.壽司 10銀\n    2.臭臭的空氣 5000銀\n    3.莫爾茲村-傳送卡 300金\n    4.阿拉瑪村的地下城-傳送卡 1500金\n    5.獨木粥  50金\n    輸入/吉斯 1 (編號)來進行購買\n"
    if user_data['city'] == '莫爾茲村':
        return "莫爾茲村-商人 布魯:\n\n    Hi~伙計\n    我是這個村的商人\n    我有些好東西你要不參考看看\n    1.螺絲 100銀\n    2.香香的空氣 50000銀\n    3.布爾維天空城-傳送卡 150金\n    4.飛行靴  100金\n    輸入/布魯 1 (編號)來進行購買\n"
    if user_data['city'] == '布爾維天空城' and '魚排' not in user_data:
        return "布爾維天空城-商人 芬克斯:\n\n    Hi~夥伴\n    我是這個城的商人\n    我有些好東西你要不參考看看\n    1.魚排 1000銀\n    2.氧氣 80000銀\n    3.王城-傳送卡 3500金\n    輸入/芬克斯 1 (編號)來進行購買\n"
    if user_data['city'] == '布爾維天空城' and user_data['布爾維天空城']>=11:
        return "布爾維天空城-商人 芬克斯:\n\n    Hi~夥伴\n    我是這個城的商人\n    我有些好東西你要不參考看看\n    1.魚排 1000銀\n    2.氧氣 80000銀\n    3.王城-傳送卡 \n    4.草莓  1000銀\n    輸入/芬克斯 1 (編號)來進行購買\n"
    if user_data['city'] == '布爾維天空城':
        return "布爾維天空城-商人 芬克斯:\n\n    Hi~夥伴\n    我是這個城的商人\n    我有些好東西你要不參考看看\n    1.魚排 1000銀\n    2.氧氣 80000銀\n    3.王城-傳送卡 3500金\n    4.草莓  1000銀\n    輸入/芬克斯 1 (編號)來進行購買\n"
    if user_data['city'] in ['王城','王城的監獄']:
        if user_data['王城']>20:
            if user_data['叛亂']==1:    #叛亂
                return '叛軍商人-魯修:\n\n    Hey~同伴\n    有想買的商品嗎?\n   '
            if user_data['叛亂']==0:    #反叛
                return '王城商人-貝卡:\n\n    Hey~同伴\n    有想買的商品嗎?\n   '
        return "王廚的姊姊 -花花:\n\n    你誰？\n"
    else:
        return "此區域沒有商人"

def seller_1(id,cmd):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if 'buy_ability' not in user_data:return "請先找商人"
    if user_data['city'] == '蘇爾德村':
        if cmd == 3 :
            if user_data['LV'] <5:return
            if user_data['金幣'] < 100:return "金幣不夠喔，你只有{}枚".format(user_data['金幣'])
            else:
                newvalues = {
                    "$set": {
                        "萊克爾村": 1,
                        "蘇爾德村": 1,
                        "金幣": user_data["金幣"] - 100
                    }
                }
                mycol.update_one({"id": id}, newvalues)
                return "獲得 萊克爾村 的傳送卡\n\n -輸入 /傳送 萊克爾村"
        if cmd == 1 :
            if user_data['銀幣'] < 1:return "銀幣不夠喔，你只有{}枚".format(user_data['銀幣'])
            elif '香蕉' not in user_data:
                newvalues = {"$set": {"香蕉" : 1 ,"銀幣": user_data["銀幣"] - 1}}
                mycol.update_one({"id": id}, newvalues)
                return "購入一根香蕉"
            else:
                newvalues = {"$set": {"香蕉" : user_data["香蕉"] + 1 ,"銀幣": user_data["銀幣"] - 1}}
                mycol.update_one({"id": id}, newvalues)
                return "購入一根香蕉，共{}根".format(user_data["香蕉"] + 1)
        if cmd == 2 :
            if user_data['銀幣'] < 100:return "銀幣不夠喔，你只有{}枚".format(user_data['銀幣'])
            else:
                newvalues = {"$set": {"空氣" : 1 ,"銀幣": user_data["銀幣"] - 100}}
                mycol.update_one({"id": id}, newvalues)
                return "購入一袋空氣，但響應環保，不提供塑膠袋"
    else:
        return "泰瑞爾並不在{}，請去 蘇爾德村 找他".format(user_data['city'])

def seller_2(id,cmd):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['city'] == '萊克爾村':
        if cmd == 1 :
            if user_data['銀幣'] < 1:return "銀幣不夠喔，你只有{}枚".format(user_data['銀幣'])
            elif '蘋果' not in user_data:
                newvalues = {"$set": {"蘋果" : 1 ,"銀幣": user_data["銀幣"] - 1}}
                mycol.update_one({"id": id}, newvalues)
                return "購入一根蘋果"
            else:
                newvalues = {"$set": {"蘋果" : user_data["蘋果"] + 1 ,"銀幣": user_data["銀幣"] - 1}}
                mycol.update_one({"id": id}, newvalues)
                return "購入一根蘋果，共{}根".format(user_data["蘋果"] + 1)
        if cmd == 2 :
            if user_data['銀幣'] < 500:return "銀幣不夠喔，你只有{}枚".format(user_data['銀幣'])
            else:
                newvalues = {"$set": {"稀薄的空氣" : 1 ,"銀幣": user_data["銀幣"] - 500}}
                mycol.update_one({"id": id}, newvalues)
                return "購入一袋稀薄的空氣，但響應環保，不提供塑膠袋"
        if cmd == 3 :
            if user_data['LV'] <10:return
            if user_data['金幣'] < 150:return "金幣不夠喔，你只有{}枚".format(user_data['金幣'])
            else:
                newvalues = {
                    "$set": {
                        "阿拉瑪村": 1,
                        "金幣": user_data["金幣"] - 150
                    }
                }
                mycol.update_one({"id": id}, newvalues)
                return "獲得 阿拉瑪村 的傳送卡"
        if cmd == 4 :
            if user_data['LV'] <10:return
            if user_data['金幣'] < 15:return "金幣不夠喔，你只有{}枚".format(user_data['金幣'])
            else:
                newvalues = {
                    "$set": {
                        "翠綠森林": 1,
                        "金幣": user_data["金幣"] - 15
                    }
                }
                mycol.update_one({"id": id}, newvalues)
                return "獲得 翠綠森林 的傳送卡"
    else:
        return "莉法並不在{}，請去 萊克爾村 找他".format(user_data['city'])

def seller_3(id,cmd):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['city'] == '阿拉瑪村':
        if cmd == 1 :
            if user_data['銀幣'] < 10:return "銀幣不夠喔，你只有{}枚".format(user_data['銀幣'])
            elif '壽司' not in user_data:
                newvalues = {"$set": {"壽司" : 1 ,"銀幣": user_data["銀幣"] - 10}}
                mycol.update_one({"id": id}, newvalues)
                return "購入一杯壽司"
            else:
                newvalues = {"$set": {"壽司" : user_data["壽司"] + 1 ,"銀幣": user_data["銀幣"] - 10}}
                mycol.update_one({"id": id}, newvalues)
                return "購入一杯壽司，共{}杯".format(user_data["壽司"] + 1)
        if cmd == 2 :
            if user_data['銀幣'] < 5000:return "銀幣不夠喔，你只有{}枚".format(user_data['銀幣'])
            else:
                newvalues = {"$set": {"臭臭的空氣" : 1 ,"銀幣": user_data["銀幣"] - 5000}}
                mycol.update_one({"id": id}, newvalues)
                return "購入一袋臭臭的空氣，但響應環保，不提供塑膠袋"
        if cmd == 3 :
            if user_data['LV'] <60 : return "建議60等之後再來哦"
            if user_data['金幣'] < 300 : return "金幣不夠喔，你只有{}枚".format(user_data['金幣'])
            elif '莫爾茲村' not in user_data:
                newvalues = {
                    "$set": {
                        "莫爾茲村": 1,
                        "金幣": user_data["金幣"] - 300
                    }
                }
                mycol.update_one({"id": id}, newvalues)
                return "獲得 莫爾茲村 的傳送卡"
            else : return '一人限一張哦'
        if cmd == 4 :
            if user_data['LV'] <10:return
            if user_data['金幣'] < 1500:return "金幣不夠喔，你只有{}枚".format(user_data['金幣'])
            else:
                newvalues = {
                    "$set": {
                        "阿拉瑪村的地下城": 1,
                        "金幣": user_data["金幣"] - 1500
                    }
                }
                mycol.update_one({"id": id}, newvalues)
                return "獲得 阿拉瑪村的地下城 的傳送卡"
        if cmd == 5:
            if user_data['LV'] <10:return
            if user_data['金幣'] < 50:return "金幣不夠喔，你只有{}枚".format(user_data['金幣'])
            else:
                newvalues = {
                    "$set": {
                        "獨木粥": 1,
                        "金幣": user_data["金幣"] - 50
                    }
                }
                mycol.update_one({"id": id}, newvalues)
                return "獲得 獨木粥"
    else:
        return "吉斯並不在{}，請去 阿拉瑪村 找他".format(user_data['city'])

def seller_4(id,cmd):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['city'] == '莫爾茲村':
        if cmd == 1 :
            if user_data['銀幣'] < 100:return "銀幣不夠喔，你只有{}枚".format(user_data['銀幣'])
            elif '螺絲' not in user_data:
                newvalues = {"$set": {"螺絲" : 1 ,"銀幣": user_data["銀幣"] - 100}}
                mycol.update_one({"id": id}, newvalues)
                return "購入一株螺絲"
            else:
                newvalues = {"$set": {"螺絲" : user_data["螺絲"] + 1 ,"銀幣": user_data["銀幣"] - 100}}
                mycol.update_one({"id": id}, newvalues)
                return "購入一株螺絲，共{}株".format(user_data["螺絲"] + 1)
        if cmd == 2 :
            if user_data['銀幣'] < 50000:return "銀幣不夠喔，你只有{}枚".format(user_data['銀幣'])
            else:
                newvalues = {"$set": {"臭臭的空氣" : 1 ,"銀幣": user_data["銀幣"] - 50000}}
                mycol.update_one({"id": id}, newvalues)
                return "購入一袋臭臭的空氣，但響應環保，不提供塑膠袋"
        if cmd == 3 :
            if user_data['LV'] <60 : return "建議60等之後再來哦"
            if user_data['金幣'] < 150 : return "金幣不夠喔，你只有{}枚".format(user_data['金幣'])
            elif "布爾維天空城" not in user_data:
                newvalues = {
                    "$set": {
                        "布爾維天空城": 1,
                        "金幣": user_data["金幣"] - 150
                    }
                }
                mycol.update_one({"id": id}, newvalues)
                return "獲得 布爾維天空城 的傳送卡"
            else : return "你已經持有此傳送卡了"
        if cmd == 4 :
            if user_data['金幣'] < 100:return "金幣不夠喔，你只有{}枚".format(user_data['金幣'])
            else:
                newvalues = {
                    "$set": {
                        "飛行靴": 1,
                        "金幣": user_data["金幣"] - 100
                    }
                }
                mycol.update_one({"id": id}, newvalues)
                return "獲得 飛行靴 \n(有了它之後能在布爾維天空城自由行走)\n"
        
    else:
        return "吉斯並不在{}，請去 莫爾茲村 找他".format(user_data['city'])

def seller_5(id,cmd):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['city'] == '布爾維天空城':
        if cmd == 1 :
            if user_data['銀幣'] < 100:return "銀幣不夠喔，你只有{}枚".format(user_data['銀幣'])
            elif '魚排' not in user_data:
                newvalues = {"$set": {"魚排" : 1 ,"銀幣": user_data["銀幣"] - 1000}}
                mycol.update_one({"id": id}, newvalues)
                return "購入魚排"
            else:
                newvalues = {"$set": {"魚排" : user_data["魚排"] + 1 ,"銀幣": user_data["銀幣"] - 1000}}
                mycol.update_one({"id": id}, newvalues)
                return "購入一株魚排，共{}株".format(user_data["魚排"] + 1)
        if cmd == 2 :
            if user_data['銀幣'] < 80000:return "銀幣不夠喔，你只有{}枚".format(user_data['銀幣'])
            else:
                newvalues = {"$set": {"氧氣" : 1 ,"銀幣": user_data["銀幣"] - 80000}}
                mycol.update_one({"id": id}, newvalues)
                return "購入一袋氧氣，但響應環保，不提供塑膠袋"
        if cmd == 3 :
            if user_data['布爾維天空城']<11:
                return "先找村長吧"
            elif '王城' not in user_data :
                newvalues = {"$set": {"王城" : 0 }}
                mycol.update_one({"id": id}, newvalues)
                return "布爾維天空城-商人 芬克斯:\n\n    聽說通往王城的傳送門好像開啟了\n\n    但有很多方便的技能在那邊都不能用 例如 傳送 存款 等等...\n    準備好之後可以找黑市的萊特聊解一下\n    他可能會直接帶去出發\n\n/萊特"
            else:
                return  "布爾維天空城-商人 芬克斯:\n\n    想去王城要找萊特哦\n\n/萊特\n"
        if cmd == 4 :
            if '魚排' not in user_data or user_data['魚排']!= 0: return "嗯？"
            if user_data['銀幣'] < 1000:return "銀幣不夠喔，你只有{}枚".format(user_data['銀幣'])
            if '草莓' not in user_data :
                newvalues = {
                    "$set": {
                        "草莓": 1,
                        "銀幣": user_data["銀幣"] - 1000
                    }
                }
                mycol.update_one({"id": id}, newvalues)
                return "獲得 草莓*1"
            else:
                newvalues = {"$set": {"草莓" : user_data["草莓"] + 1 ,"銀幣": user_data["銀幣"] - 1000}}
                mycol.update_one({"id": id}, newvalues)
                return "購入一條草莓，共{}條".format(user_data["草莓"] + 1)
        
    else:
        return "芬克斯並不在{}，請去 布爾維天空城 找他".format(user_data['city'])

def witch(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['city'] == '翠綠森林':
        if "女巫" not in user_data :
            if '見習法師' in user_data['title']:
                newvalues = {"$set": {"女巫" : 1 ,'火球術' : 1 , '水球術' : 1}}
                mycol.update_one({"id": id}, newvalues)
                return "翠綠森林-女巫 蒂拉芙·林茵:\n\n    Hi~小伙\n    我是這座森林的女巫-蒂拉芙·林茵，初次見面\n    聽旁邊村長說你想學點魔法\n    咦～！你也是法師嗎？\n    來教你兩招好了～\n    1.火球術 2.水球術\n\n  已經學會 [火球術] 及 [水球術]\n    另外還賣點藥草，說不定您哪天用得上\n    3.藥草 10000銀\n\n輸入/蒂拉芙·林茵 3"
            else:
                newvalues = {"$set": {"女巫" : 1 }}
                mycol.update_one({"id": id}, newvalues)
                return "翠綠森林-女巫 蒂拉芙·林茵:\n\n    Hi~小伙\n    我是這座森林的女巫-蒂拉芙·林茵，初次見面\n    聽旁邊村長說你想學點魔法\n   我這邊有兩個課程，你可以參考看看\n    1.火球術\n    2.水球術\n\n    各需要花10體力，以及30000銀幣來學習\n    另外還賣點藥草，說不定您哪天用得上\n    3.藥草 10000銀\n\n輸入/蒂拉芙·林茵 1"
        if user_data['女巫'] < 5:
            ans_list = ['翠綠森林-女巫 蒂拉芙·林茵:\n\n    我這邊有兩個課程，你可以參考看看\n    1.火球術\n    2.水球術\n\n    各需要花10體力，以及30000銀幣來學習\n    另外還賣點藥草，說不定您哪天用得上\n    3.藥草 10000銀\n\n輸入/蒂拉芙·林茵 1','翠綠森林-女巫 蒂拉芙·林茵:\n\n    我的森林不錯吧～？\n']
            ans = random.choice(ans_list)
            newvalues = {"$set": {"女巫" : user_data['女巫'] + 1 }}
            mycol.update_one({"id": id}, newvalues)
            if user_data['女巫'] == 4:ans = '翠綠森林-女巫 蒂拉芙·林茵:\n\n    嗯...'
            return ans
        if '水球術' not in user_data:
            ans_list = ['翠綠森林-女巫 蒂拉芙·林茵:\n\n    我這邊有兩個課程，你可以參考看看\n    1.火球術\n    2.水球術\n\n    各需要花10體力，以及30000銀幣來學習\n    另外還賣點藥草，說不定您哪天用得上\n    3.藥草 10000銀\n\n輸入/蒂拉芙·林茵 1','翠綠森林-女巫 蒂拉芙·林茵:\n\n    我的森林不錯吧～？\n']
            ans = random.choice(ans_list)
            return ans
        if '永恆之森' not in user_data and '水球術' in user_data:
            newvalues = {"$set": {"永恆之森" : 1 ,'拍照' : 0 }}
            mycol.update_one({"id": id}, newvalues)
            return "翠綠森林-女巫 蒂拉芙·林茵:\n\n    對了，你對[永恆之森]熟悉嗎？\n    我暫時抽不開身，想請你去記錄一下\n    想請你拍幾張照回來讓我放進我的研究報告，我上次忘記拍了😅\n    等你呦～\n\n請前往[永恆之森]\n並[拍照](-2體)"
        if '永恆之森' in user_data and user_data['拍照'] < 10 and '水球術' in user_data:
            return "翠綠森林-女巫 蒂拉芙·林茵:\n\n  看來你懂如何拍照了\n  請幫我到[永恆之森]拍大約10張照片給我～\n\n請前往[永恆之森]\n並[拍照]"
        if user_data['永恆之森'] ==1 and user_data['拍照'] >= 10 and '水球術' in user_data:
            newvalues = {"$set": {"銀幣" : 100000 + user_data['銀幣'] , '永恆之森' : 2}}
            mycol.update_one({"id": id}, newvalues)
            return "翠綠森林-女巫 蒂拉芙·林茵:\n\n  哇！\n  拍照技術不錯呦\n  這樣我就能發表論文了!!\n  十分感謝你！\n  這點銀幣就當作是謝禮吧～\n\n-獲得10w銀幣"
        if "布爾維天空城" in user_data and user_data['布爾維天空城']==4:
            newvalues = {"$set": {'布爾維天空城' : 5}}
            mycol.update_one({"id": id}, newvalues)
            return "翠綠森林-女巫 蒂拉芙·林茵:\n\n  哎呀！這不是 {}大人嗎\n  我正在跟天空城的 卡羅琳 聊天呢～\n\n\n布爾維天空城-郡主 卡羅琳:\n  哈囉～初次見面\n\n如此如此\n(...)\n這般這般\n\n\n布爾維天空城-郡主 卡羅琳:\n  哦哦～\n  抱歉啦林茵，看樣子瑪莎那邊需要我幫忙\n  必須要先回去了😅\n\n蒂拉芙·林茵:\n\n  好勒～下次見囉～  \n\n/傳送 布爾維天空城".format(user_data['title'])
        if "布爾維天空城" in user_data and user_data['布爾維天空城']==5:
            return "翠綠森林-女巫 蒂拉芙·林茵:\n\n  您不跟上去嗎OuO?\n"
        else:
            ans_list = ['翠綠森林-女巫 蒂拉芙·林茵:\n\n    我這邊有兩個課程，你可以參考看看\n    1.火球術\n    2.水球術\n\n    各需要花10體力，以及30000銀幣來學習\n    另外還賣點藥草，說不定您哪天用得上\n    3.藥草 10000銀\n\n輸入/蒂拉芙·林茵 1','翠綠森林-女巫 蒂拉芙·林茵:\n\n    我的森林不錯吧～？\n']
            ans = random.choice(ans_list)
            return ans
    else:
        return "{}沒有女巫".format(user_data['city'])

def teacher_1(id,cmd):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['city'] == '翠綠森林':
        if cmd == 1:cmd='火球術'
        if cmd == 2:cmd='水球術'
        if cmd in ['火球術','水球術']:
            if cmd in user_data : return "您之前就學會{}了".format(cmd)
            if user_data['銀幣'] >= 30000 and user_data['work'] >= 10 :
                newvalues = {"$set": {cmd : 1 ,'銀幣' : user_data['銀幣'] - 30000 }}
                mycol.update_one({"id": id}, newvalues)
                work_minus(id,10)
                return "恭喜！  已學會{}".format(cmd)
            else:
                return "學習{}需要30000枚銀幣跟10體力呦".format(cmd)
        if cmd ==3:
            if user_data['銀幣'] < 10000:return "銀幣不夠喔，你只有{}枚".format(user_data['銀幣'])
            elif '藥草' not in user_data:
                newvalues = {"$set": {"藥草" : 1 ,"銀幣": user_data["銀幣"] - 10000}}
                mycol.update_one({"id": id}, newvalues)
                return "購入一包藥草"
            else:
                newvalues = {"$set": {"藥草" : user_data["藥草"] + 1 ,"銀幣": user_data["銀幣"] - 10000}}
                mycol.update_one({"id": id}, newvalues)
                return "購入一包藥草，共{}包".format(user_data["藥草"] + 1)
    else:
        return "蒂拉芙·林茵並不在{},她在翠綠森林".format(user_data['city'])


def skill_1(id,cmd):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"

    if cmd not in user_data : return '您並未學會該技能'
    if user_data['work'] < 10: return '您體力小於10不夠施放{}'.format(cmd)
    if user_data['city'] in ['蘇爾德村','萊克爾村','莫爾茲村','布爾維天空城']:
        newvalues = {"$set": { 'work' : 0 }}
        mycol.update_one({"id": id}, newvalues)
        return "你在{}內施放{},被當地守衛隊關禁閉,將在下個小時放人".format(user_data['city'],cmd)
    elif user_data['city'] == '翠綠森林':
        return "翠綠森林-女巫 蒂拉芙·林茵:\n\n    !!!!\n    喂喂喂！！\n    請不要在我的森林施展這種法術好嗎!\n    聽說 阿拉瑪村 的村長急需這方面的人才\n    說不定你能助他一臂之力\n"
    elif user_data['city'] == '阿拉瑪村' :
        if '阿拉瑪村的地下城' not in user_data and cmd == '火球術':
            newvalues = {"$set": { '阿拉瑪村的地下城' : 1 }}
            mycol.update_one({"id": id}, newvalues)
            return "阿拉瑪村-村長 知紗子:\n\n  非常感謝您！\n  這是地下城的傳送卡，之後歡迎來[調查]哦\n\n/傳送 阿拉瑪村的地下城"
        else:
            return "阿拉瑪村-村長 知紗子:\n\n  非常感謝您！\n  地下城的門已經開囉，不要在村內放法術了"
    elif user_data['city'] == '王城' and cmd == '火球術':
        if '王城' in user_data:
            if user_data['王城'] == 2:
                work_minus(id,10)
                newvalues = {"$set": { '王城' : 3 }}
                mycol.update_one({"id": id}, newvalues)
                return "你把三個門都炸了\n但你發現這只是個障眼法\n\n請繼續/調查"
            if user_data['王城'] == 4:
                work_minus(id,10)
                pw = random.randint(1000,9999)
                newvalues = {"$set": { '王城' : 5 , 'pw': pw , 'city' : '王城的監獄'}}
                mycol.update_one({"id": id}, newvalues)
                return "王城的法師回贈你\n    {}球\n輕輕鬆鬆就把你抓起來\n\n您的所在位置[王城的監獄]\n/調查".format(pw)
            else:
                return "城內的魔素量不足以讓你使出火球術"
    elif user_data['city'] == '王城的監獄':
        police_hit(id)
        return "你被獄卒打了一頓"

def pet_sys(id,cmd,job):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"


def lv_list(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    all = mycol.find()
    all.sort('LV',-1)
    ans = ''
    j = 0
    for i in all:
        try:
            j+=1
            if '叛亂' in i and i['叛亂'] == 1:
                ans += str(j) + ". 🗡" + "[{}] ".format(i['title']) + i['name'] + " : lv " + str(i['LV']) + "\n"
            elif '叛亂' in i and i['叛亂'] == 0:
                ans += str(j) + ". ⚜️" + "[{}] ".format(i['title']) + i['name'] + " : lv " + str(i['LV']) + "\n"
            else:
                ans += str(j) + ".  " + "[{}] ".format(i['title']) + i['name'] + " : lv " + str(i['LV']) + "\n"
        except:
            pass
        if j ==11:return ans
    return ans

def all_lv_list(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    all = mycol.find()
    all.sort('LV',-1)
    ans = ''
    j = 0
    for i in all:
        try:
            j+=1
            if '叛亂' in i and i['叛亂'] == 1:
                ans += str(j) + ". 🗡" + "[{}] ".format(i['title']) + i['name'] + " : lv " + str(i['LV']) + "\n"
            elif '叛亂' in i and i['叛亂'] == 0:
                ans += str(j) + ". ⚜️" + "[{}] ".format(i['title']) + i['name'] + " : lv " + str(i['LV']) + "\n"
            else:
                ans += str(j) + ".  " + "[{}] ".format(i['title']) + i['name'] + " : lv " + str(i['LV']) + "\n"
        except:
            pass
    return ans
# print(lv_list('U1c1925ccd29c125ed845cc2db637f39b'))

def new_year_event2023(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if '2023_new_year_priest' not in user_data:
        return "請到 蘇爾德村 找祭司呦"
    elif user_data['2023_new_year_priest'] ==2:
        userLV = user_data['LV']
        amount = max(50000,random.randint(1000,userLV*1800))
        newvalues = {"$set": {"2023_new_year_priest" : 4 , '銀幣' : amount + user_data['銀幣'] , '金幣' : 50 + user_data['金幣']}}
        mycol.update_one({"id": id}, newvalues)
        return "恭喜獲得{}枚銀幣\n以及50枚金幣～！".format(amount)
    elif user_data['2023_new_year_priest'] ==3:     #少一點
        userLV = user_data['LV']
        amount = max(30000,random.randint(1000,userLV*1100))
        newvalues = {"$set": {"2023_new_year_priest" : 4 , '銀幣' : amount + user_data['銀幣'] , '金幣' : 20 + user_data['金幣']}}
        mycol.update_one({"id": id}, newvalues)
        return "恭喜獲得{}枚銀幣\n以及20枚金幣～！".format(amount)
    elif user_data['2023_new_year_priest'] ==4:
        return "您領過囉ˊˇˋ\n新年快樂~~\n\n分享給其他還沒領過的朋友唄\n活動到 1/3唄\n有任何問題再請聯絡me\nhttps://forms.gle/FyEdn248iedpaDEt7"
    return

def priest(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['city'] == '蘇爾德村':
        if user_data['LV'] == 0:
            return "你誰？"
        if user_data['LV'] > 0 and "change_LV" not in user_data:
            newvalues = {
                    "$set": {
                        "change_LV" : 1
                    }
                }
            mycol.update_one({"id": id}, newvalues)
            return "蘇爾德村-祭司 波卡斯:\n\n    Hi! 我是蘇爾德村的祭司-波卡斯\n    你就是{}對吧\n    村長剛剛有交代\n    我要教你如何升等\n\n    每升等一次都要銀幣\n    一等升到兩等需要1000枚\n    指令是 /升等".format(user_data['name'])
        if '2023_new_year_priest' not in user_data:         #2023新年任務
            newvalues = {"$set": {"2023_new_year_priest" : 1}}
            mycol.update_one({"id": id}, newvalues)
            return "蘇爾德村-祭司 波卡斯:\n\n新年快樂呀～\n我是今年負責裝扮城市的祭司\n新年的一年到了\n想請您幫我找一些佈置用的道具~\n\n此處[調查]"
        if '劍玉' not in user_data and user_data['2023_new_year_priest'] ==1:
            return "蘇爾德村-祭司 波卡斯:\n\n請您幫我找一些佈置用的道具\n\n此處[調查]"
        if '劍玉' in user_data and '2023_new_year_priest' in user_data and user_data['2023_new_year_priest'] ==1:
            if user_data['劍玉']>=5:
                newvalues = {"$set": {"2023_new_year_priest" : 2 , '劍玉' : 0}}
                mycol.update_one({"id": id}, newvalues)
                return "蘇爾德村-祭司 波卡斯:\n\n你也找到太多劍玉了吧🤣\n謝謝你啦～\n來，這是新年禮包\n祝您在2023事事順利～\n\n輸入 /2023 來開起禮包\n迎接新的一年～\n"
            elif user_data['劍玉']>0:
                newvalues = {"$set": {"2023_new_year_priest" : 3 , '劍玉' : 0}}
                mycol.update_one({"id": id}, newvalues)
                return "蘇爾德村-祭司 波卡斯:\n\n謝謝您拿劍玉給我～\n來，這是新年禮包\n祝您在2023事事順利～ \n\n輸入 /2023 來開禮包\n迎接新的一年～\n"
        else:
            return "蘇爾德村-祭司 波卡斯:\n\n    Hi! 我是蘇爾德村的祭司 波卡斯\n    每升等一次都要銀幣\n    一等升到兩等需要1000枚\n    指令是 /升等".format(user_data['name'])
    if user_data['city'] == '萊克爾村':
        if 'pet_priest' not in user_data:
            newvalues = {"$set": {"pet_priest" : 1}}
            mycol.update_one({"id": id}, newvalues)
            return "萊克爾村-祭司 拉克:\n\nHey~ 我是萊克爾村的祭司 拉克\n\n{},你喜歡小動物嗎？\n像一般的 狗 貓 馬 天竺鼠...?".format(user_data['name'])
        if user_data['pet_priest'] == 1:
            newvalues = {"$set": {"pet_priest" : 2}}
            if '翠綠森林的現況' in user_data and user_data['翠綠森林的現況'] != 0:
                return "萊克爾村-祭司 拉克:\n\n勞贖?"
            if '翠綠森林的現況' not in user_data:
                return "萊克爾村-祭司 拉克:\n\n勞贖?"
            mycol.update_one({"id": id}, newvalues)
            return "萊克爾村-祭司 拉克:\n\n勞贖?"
        if user_data['pet_priest'] == 2:
            newvalues = {"$set": {"pet_priest" : 3}}
            mycol.update_one({"id": id}, newvalues)
            return "萊克爾村-祭司 拉克:\n\n好啦 不開玩笑\n看來您也已經調查過 翠綠森林 了\n也看到許多可愛的小動物對吧\n森林的魔素量很高，根本是牠們活動的天堂\n有些特別親近人的還可能變成人類的同伴\n有時間的話，不仿去走走\n說不定能找到優秀的伙伴\n這村有流傳一首童謠\n說不定能給你些想法:\n\n犬有著無窮的體力\n珍惜可以給你帶來幸福的動物\n羊擁有更好的運氣\n因為他們會給你更多更好的機會\n囓可以讓倍量收穫\n不一樣的動物帶來不一樣的環境\n不及貍奴讓你擁有更多更好生活\n\n到森林 -/走走"
    
    else:
        return "這邊沒有祭司呦"

def walk_pet(id,cmd):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if cmd != '' : cmd = int(cmd)
    if user_data['city'] == '翠綠森林':
        if 'pet_priest' in user_data and user_data['pet_priest'] == 3:
            newvalues = {"$set": {"pet_priest" : 4}}
            mycol.update_one({"id": id}, newvalues)
            return "走了走"
        if 'pet_priest' in user_data and user_data['pet_priest'] == 4:
            newvalues = {"$set": {"pet_priest" : 5}}
            mycol.update_one({"id": id}, newvalues)
            return "走了又走"
        if 'pet_priest' in user_data and user_data['pet_priest'] == 5:
            newvalues = {"$set": {"pet_priest" : 6}}
            mycol.update_one({"id": id}, newvalues)
            return "你發現了三隻長相奇特的小動物跟在你後面...\n\n1.長得像羊的狗\n2.長得像獅子的羊\n3.長得跟魚一樣的天竺鼠 \n\n/走走 1"
    if user_data['city'] == '永恆之森':
        if 'pet_priest' in user_data and user_data['pet_priest'] == 6:
            newvalues = {"$set": {"pet_priest" : 7}}
            mycol.update_one({"id": id}, newvalues)
            return "走了走..."
        if 'pet_priest' in user_data and user_data['pet_priest'] == 7:
            newvalues = {"$set": {"pet_priest" : 8}}
            mycol.update_one({"id": id}, newvalues)
            return "你在陰暗處看到了一隻黑貓 \n 4.黑貓\n\n/走走 4"

    if 'pet_priest' in user_data and user_data['pet_priest'] == 6:
        if cmd == 1:
            newvalues = {"$set": {"長得像羊的狗" : 1 , "pet_priest" : 9 , 'pet':"長得像羊的狗"}}
            mycol.update_one({"id": id}, newvalues)
            return "獲得夥伴 [長得像羊的狗]"
        if cmd == 2:
            newvalues = {"$set": {"長得像獅子的羊" : 1, "pet_priest" : 9 ,'pet':'長得像獅子的羊'}}
            mycol.update_one({"id": id}, newvalues)
            return "獲得夥伴 [長得像獅子的羊]"
        if cmd == 3:
            newvalues = {"$set": {"長得跟魚一樣的天竺鼠" : 1, "pet_priest" : 9 , 'pet':'長得跟魚一樣的天竺鼠'}}
            mycol.update_one({"id": id}, newvalues)
            return "獲得夥伴 [長得跟魚一樣的天竺鼠]"
    if 'pet_priest' in user_data and user_data['pet_priest'] == 8:
        if cmd == 1:
            newvalues = {"$set": {"長得像羊的狗" : 1 , "pet_priest" : 9 , 'pet':"長得像羊的狗"}}
            mycol.update_one({"id": id}, newvalues)
            return "獲得夥伴 [長得像羊的狗]"
        if cmd == 2:
            newvalues = {"$set": {"長得像獅子的羊" : 1, "pet_priest" : 9 ,'pet':'長得像獅子的羊'}}
            mycol.update_one({"id": id}, newvalues)
            return "獲得夥伴 [長得像獅子的羊]"
        if cmd == 3:
            newvalues = {"$set": {"長得跟魚一樣的天竺鼠" : 1, "pet_priest" : 9 , 'pet':'長得跟魚一樣的天竺鼠'}}
            mycol.update_one({"id": id}, newvalues)
            return "獲得夥伴 [長得跟魚一樣的天竺鼠]"
        if cmd == 4:
            newvalues = {"$set": {"黑貓" : 1, "pet_priest" : 9 , 'pet':'黑貓'}}
            mycol.update_one({"id": id}, newvalues)
            return "獲得夥伴 [黑貓]"
    if 'pet_priest' in user_data and user_data['pet_priest'] == 9:
        return "你覺得你的{}很可愛".format(user_data['pet'])
    
def change_title(id,title):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['city'] == '蘇爾德村':
        if user_data['LV'] == 0:
            return "想轉職的話，請找村長為您說明"
        if 'change_title' not in user_data:
            return "想轉職的話，請找村長為您說明"
        if user_data['LV']>=5 and user_data['change_title']==1:
            title = title.replace(" ","")
            if title not in ['劍士','小混混','見習法師','農夫']:return "請輸入正確的職業"
            newvalues = {
                    "$set": {
                        "title" : title,
                        "change_title" : 2
                    }
                }
            mycol.update_one({"id": id}, newvalues)
            return '恭喜{}成為{}'.format(user_data['name'],title)
        elif user_data['change_title'] == 2:
            return "您已踏上神聖的{}之路，休想半途而廢".format(user_data['title'])
    if user_data['city'] == '萊克爾村':
        if 'change_title' not in user_data:
            return "想轉職的話，請找蘇爾德村村長為您說明"
        if user_data['change_title']==2 :
            if user_data['title'] == '劍士':
                if title not in ['狂劍士','大劍士']:
                    return "您是劍士，只能升成 狂劍士 或 大劍士"
                else:
                    newvalues = {"$set": { "title" : title , "change_title" : 3}}
                    mycol.update_one({"id": id}, newvalues)
                    return '恭喜{}成為{}'.format(user_data['name'],title)
            if user_data['title'] == '見習法師':
                if title not in ['魔導士','法師']:
                    return "您是見習法師，只能升成 魔導士 或 法師"
                else:
                    newvalues = {"$set": { "title" : title , "change_title" : 3}}
                    mycol.update_one({"id": id}, newvalues)
                    return '恭喜{}成為{}'.format(user_data['name'],title)
            if user_data['title'] == '小混混':
                if title != '盜賊':
                    return "您是小混混，只能升成 盜賊"
                else:
                    newvalues = {"$set": { "title" : title , "change_title" : 3}}
                    mycol.update_one({"id": id}, newvalues)
                    return '恭喜{}成為{}'.format(user_data['name'],title)
            if user_data['title'] == '農夫':
                if title != '大地主':
                    return "您是農夫，只能升成 大地主"
                else:
                    newvalues = {"$set": { "title" : title , "change_title" : 3}}
                    mycol.update_one({"id": id}, newvalues)
                    return '恭喜{}成為{}'.format(user_data['name'],title)
        else:
            if user_data['title'] == '村民':return "請先找 蘇爾德村 村長"  
            return "請找村長為您說明"
    if user_data['city'] == '阿拉瑪村':
        if 'change_title' not in user_data:
            return "想轉職的話，請找蘇爾德村村長為您說明"
        if user_data['change_title'] == 3 :
            if user_data['title'] == '狂劍士':
                if title != '劍豪':
                    return "您是狂劍士，只能升成 劍豪"
                else:
                    newvalues = {"$set": { "title" : title , "change_title" : 4}}
                    mycol.update_one({"id": id}, newvalues)
                    return '恭喜{}成為{}'.format(user_data['name'],title)
            if user_data['title'] == '大劍士':
                if title != '聖劍士':
                    return "您是大劍士，只能升成 聖劍士"
                else:
                    newvalues = {"$set": { "title" : title , "change_title" : 4}}
                    mycol.update_one({"id": id}, newvalues)
                    return '恭喜{}成為{}'.format(user_data['name'],title)
            if user_data['title'] == '魔導士':
                if title != '黑魔導士':
                    return "您是魔導士，只能升成 黑魔導士"
                else:
                    newvalues = {"$set": { "title" : title , "change_title" : 4}}
                    mycol.update_one({"id": id}, newvalues)
                    return '恭喜{}成為{}'.format(user_data['name'],title)
            if user_data['title'] == '法師':
                if title != '大法師':
                    return "您是法師，只能升成 大法師"
                else:
                    newvalues = {"$set": { "title" : title , "change_title" : 4}}
                    mycol.update_one({"id": id}, newvalues)
                    return '恭喜{}成為{}'.format(user_data['name'],title)
            if user_data['title'] == '盜賊':
                if title != '暗夜盜賊':
                    return "您是盜賊，只能升成 暗夜盜賊"
                else:
                    newvalues = {"$set": { "title" : title , "change_title" : 4}}
                    mycol.update_one({"id": id}, newvalues)
                    return '恭喜{}成為{}'.format(user_data['name'],title)
            if user_data['title'] == '大地主':
                if title != '領主':
                    return "您是大地主，只能升成 領主"
                else:
                    newvalues = {"$set": { "title" : title , "change_title" : 4}}
                    mycol.update_one({"id": id}, newvalues)
                    return '恭喜{}成為{}'.format(user_data['name'],title)

    if user_data['city'] == '莫爾茲村':
        if 'change_title' not in user_data:
            return "想轉職的話，請找蘇爾德村村長為您說明"   
        if user_data['change_title'] == 4 and user_data['LV'] >=90:
            if user_data['title'] == '劍豪':
                if title != '劍魔':
                    return "您是劍豪，只能升成 劍魔"
                else:
                    newvalues = {"$set": { "title" : title , "change_title" : 5}}
                    mycol.update_one({"id": id}, newvalues)
                    return '恭喜{}成為{}'.format(user_data['name'],title)
            if user_data['title'] == '聖劍士':
                if title != '皇家聖劍士':
                    return "您是聖劍士，只能升成 皇家聖劍士"
                else:
                    newvalues = {"$set": { "title" : title , "change_title" : 5}}
                    mycol.update_one({"id": id}, newvalues)
                    return '恭喜{}成為{}'.format(user_data['name'],title)
            if user_data['title'] == '黑魔導士':
                if title != '混沌魔導士':
                    return "您是黑魔導士，只能升成 混沌魔導士"
                else:
                    newvalues = {"$set": { "title" : title , "change_title" : 5}}
                    mycol.update_one({"id": id}, newvalues)
                    return '恭喜{}成為{}'.format(user_data['name'],title)
            if user_data['title'] == '大法師':
                if title != '皇家法師':
                    return "您是大法師，只能升成 皇家法師"
                else:
                    newvalues = {"$set": { "title" : title , "change_title" : 5}}
                    mycol.update_one({"id": id}, newvalues)
                    return '恭喜{}成為{}'.format(user_data['name'],title)
            if user_data['title'] == '暗夜盜賊':
                if title != '暗月神偷':
                    return "您是暗夜盜賊，只能升成 暗月神偷"
                else:
                    newvalues = {"$set": { "title" : title , "change_title" : 5}}
                    mycol.update_one({"id": id}, newvalues)
                    return '恭喜{}成為{}'.format(user_data['name'],title)
            if user_data['title'] == '領主':
                if title != '大公':
                    return "您是領主，只能升成 大公"
                else:
                    newvalues = {"$set": { "title" : title , "change_title" : 5}}
                    mycol.update_one({"id": id}, newvalues)
                    return '恭喜{}成為{}'.format(user_data['name'],title)
        
    else:
        return "請前往村作進行轉職的動作"

def farm(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['title'] not in ['農夫','大地主']:
        return "你不是農夫，沒有田地"
    if user_data['city'] in ['王城','王城的監獄']:
        return "受王城所影響，暫時失去能力"
    if check_work_times(id,5):
        how_much = random.randint(1,6)
        now_coin = user_data['銀幣']
        work_minus(id,5)
        if how_much ==1:
            coin = 40 * 5 * user_data['LV']
            sing = '農夫勤勞耕種田\n收穫喜悅滿心間\n汗水流淌滋潤土\n收穫堆積滿山巒\n'
        if how_much ==2:
            coin = 45 * 5 * user_data['LV']
            sing = '農耕萬家節，蒼蠅滿田野。\n芒草金黃熟，禾稼收場晚。\n日日驅蟲賊，煩憂無窮期。\n收穫百萬穗，農家歡樂時。'
        if how_much ==3:
            coin = 50 * 5 * user_data['LV']
            sing = '芒種當風臨，農耕歡樂時\n正當此時正，種籽播撒開\n山風吹拂至，雨露滋潤著\n農夫勤懇力，收穫繁豐致'
        if how_much ==4:
            coin = 55 * 5 * user_data['LV']
            sing = '收割芒種穀，收获滿滿時\n禾稼應時完，穀粒收取來\n穀倉滿滿豐，農夫歡樂喜\n農耕豐收多，喜悅普天下'
        if how_much ==5:
            coin = 90 * 5 * user_data['LV']
            sing = '農耕收莊稼，黃金滿堆堆\n農家勤耕勞，懷抱豐收福\n農夫履深溝，耕耘一片肥\n犁耙搗拌土，收割滿園黍\n汗流塗滿身，收穫百倍喜\n良禾芒芒收，歡樂陣陣歌\n農耕歡樂事，收穫歡喜日'
        if how_much ==6:
            coin = 30 * random.randint(1,6) * user_data['LV']
            sing = '歲月易逝忽已秋，台風吹散芒草黃\n搖搖欲墜收稻梗，收割欠收苦無養\n落葉滿地枯草乾，空空虛虛無稻穗\n夜夜憂慮白髮添，孤單慘淡虛度年'
        if user_data['title'] == '大地主':
            coin = int(coin * 1.1)
        newvalues = {"$set": { '銀幣' : coin + now_coin }}
        mycol.update_one({"id": id}, newvalues)

        return '{}\n\n稻作收入{}枚銀幣'.format(sing,coin)
    else:
        return "體力不足，下不了農田\n需要5體力"

def recive_rent(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['title'] not in ['大地主']:
        return "你不是地主，無法收租"
    if user_data['city'] in ['王城','王城的監獄']:
        return "受王城所影響，暫時失去能力"
    if 'rent' not in user_data and user_data['title'] == '大地主':
        newvalues = {"$set": { '金幣' : 10 + user_data['金幣'] , 'rent' : 1 }}
        mycol.update_one({"id": id}, newvalues)
        return '收10枚金幣幣，共{}枚'.format(10 + user_data['金幣'])
    elif user_data['rent'] == 0 and user_data['title'] == '大地主':
        newvalues = {"$set": { '金幣' : 10 + user_data['金幣'] , 'rent' : 1 }}
        mycol.update_one({"id": id}, newvalues)
        return '收10枚金幣幣，共{}枚'.format(10 + user_data['金幣'])
    else:
        return "一天一次呦"

def recive_tax(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['title'] not in ['領主','大公']:
        return "你不是領主，無法收稅"
    if user_data['city'] in ['王城','王城的監獄']:
        return "受王城所影響，暫時失去能力"
    if 'tax' not in user_data and user_data['title'] == '領主':
        newvalues = {"$set": { '金幣' : 20 + user_data['金幣'],'銀幣' : 30000 + user_data['銀幣'] , 'tax' : 1 }}
        mycol.update_one({"id": id}, newvalues)
        return '收20枚金幣，共{}枚\n3w枚銀幣，共{}枚'.format(12 + user_data['金幣'],30000 + user_data['銀幣'] )
    elif user_data['tax'] == 0 and user_data['title'] == '領主':
        newvalues = {"$set": { '金幣' : 16 + user_data['金幣'] ,'銀幣' : 30000 + user_data['銀幣'], 'tax' : 1 }}
        mycol.update_one({"id": id}, newvalues)
        return '收16枚金幣幣，共{}枚\n3w枚銀幣，共{}枚'.format(16 + user_data['金幣'],30000 + user_data['銀幣'] )
    elif user_data['tax'] == 0 and user_data['title'] == '大公':
        newvalues = {"$set": { '金幣' : 24 + user_data['金幣'] ,'銀幣' : 60000 + user_data['銀幣'], 'tax' : 1 }}
        mycol.update_one({"id": id}, newvalues)
        return '收24枚金幣幣，共{}枚\n6w枚銀幣，共{}枚'.format(24 + user_data['金幣'],60000 + user_data['銀幣'] )
    else:
        return "一天一次呦"

def lv_up(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if 'change_LV' in user_data:
        need_coin = (user_data['LV']-1)*800 + 1000
        if user_data['LV'] >= 130:
            need_coin = (user_data['LV']-1)*1600 + 1000
        if user_data['LV'] >= 140:
            need_coin = (user_data['LV']-1)*1800 + 1000
        if user_data['LV'] >= 145:
            need_coin = (user_data['LV']-1)*2300 + 1000
        if user_data['LV'] >= 155:
            need_coin = (user_data['LV']-1)*3300 + 1000
        if user_data['LV'] >= 160:
            need_coin = (user_data['LV']-1)*4100 + 1000
        if user_data['銀幣'] < need_coin:
            return "升到下個等級需要{}枚銀幣,而你只有{}枚".format(need_coin,user_data['銀幣'])
        if user_data['銀幣'] >= need_coin:
            newvalues = {
                    "$set": {
                        "銀幣" : user_data['銀幣'] - need_coin,
                        "LV" : user_data['LV'] +1
                    }
                }
            mycol.update_one({"id": id}, newvalues)
            return "升等啦～恭喜升成{}等".format(user_data['LV'] +1)
    else:
        if user_data['LV']==0:
            return "找村長"
        if user_data['LV']>0:
            return "找祭司"

# print(lv_up('U1c1925ccd29c125ed845cc2db637f39b'))
def meditation(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['title'] not in ['見習法師','法師','魔導士','黑魔導士','大法師','混沌魔導士','皇家法師']:
        return "您並不是法師，你是{}".format(user_data['title'])
    if user_data['title'] == '見習法師': 
        aaa = check_work_times(id,10)
        dis = 10
    if user_data['title'] in ['法師','魔導士','黑魔導士']: 
        aaa = check_work_times(id,8)
        dis = 8
    if user_data['title'] in ['大法師','混沌魔導士','皇家法師']: 
        aaa = check_work_times(id,6)
        dis = 6
    if user_data['title'] in ['皇家法師']: 
        aaa = check_work_times(id,6)
        dis = 5
    if aaa:
        if "可樂果" not in user_data:
            newvalues = {"$set": {"可樂果" : 1}}
            mycol.update_one({"id": id}, newvalues)
            work_minus(id,dis)
            return "獲得一包可樂果，損失{}體力".format(dis)
        else:
            newvalues = {"$set": {"可樂果" : 1 + user_data['可樂果']}}
            mycol.update_one({"id": id}, newvalues)
            work_minus(id,dis)
            return "獲得一包可樂果，損失{}體力".format(dis)
    else:
        return "此行為需要{}體力，過陣子再來吧！".format(dis)

def rob_log(id,person,silver):
    user_data = mycol.find_one({"id": id})
    qq_person = mycol.find_one({"name": person})

    you_rob = user_data['you_rob']
    if qq_person['id'] not in you_rob:
        you_rob[qq_person['id']] = silver
    else:
        you_rob[qq_person['id']] += silver
    newvalues = {"$set": {'you_rob' : you_rob}}    
    mycol.update_one({"id": id}, newvalues)
    
    been_rob = qq_person['been_rob']
    if user_data['id'] not in been_rob:
        been_rob[user_data['id']] = silver
    else:
        been_rob[user_data['id']] += silver
    robvalues = {"$set": {'been_rob' : been_rob}}    
    mycol.update_one({"name": person}, robvalues)

    return

def rob(id,person):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['title'] not in  ['小混混','盜賊','暗夜盜賊','暗月神偷']:
        return "您並不是小混混，你是{}".format(user_data['title'])
    if user_data['city'] in ['王城','王城的監獄']:return "王城無法呦"
    qq_person = mycol.find_one({"name": person})
    if qq_person == None:
        return "此人不存在"
    if qq_person['city'] != user_data['city']: return "你們不在同一個村莊"
    
    if 'rob' not in user_data:
        qq_silver = qq_person['銀幣']
        rob_amount = random.randint(0, qq_silver)
        rob_amount = min(rob_amount,user_data['LV']*987)
        newvalues = {"$set": {"銀幣": rob_amount + user_data['銀幣'] , "rob" : 1}}
        qqvalues = {"$set": {"銀幣": qq_person['銀幣'] - rob_amount}}
        mycol.update_one({"id": id}, newvalues)
        mycol.update_one({"name": person}, qqvalues)
        rob_log(id,person,rob_amount)
        return "你偷了{} {}枚銀幣，他剩下{}枚".format(person,rob_amount,qq_person['銀幣'] - rob_amount)
    if user_data["rob"] == 1:return "您今天壞壞過囉"
    else:
        win = 0
        if user_data['title'] == '小混混':
            meet = (random.choices([0,1],weights=[4,6]))
            win = int(meet[0])
        if user_data['title'] == '盜賊':
            meet = (random.choices([0,1],weights=[3,7]))
            win = int(meet[0])
        if user_data['title'] == '暗夜盜賊':
            meet = (random.choices([0,1],weights=[2,8]))
            win = int(meet[0])
        if user_data['title'] == '暗月神偷':
            meet = (random.choices([0,1],weights=[1,9]))
            win = int(meet[0])
        if win == 1:
            qq_silver = qq_person['銀幣']
            rob_amount = random.randint(0, qq_silver)
            rob_amount = min(rob_amount,user_data['LV']*987)
            if user_data['LV']>120:
                rob_amount = min(rob_amount,user_data['LV']*4567)
            newvalues = {"$set": {"銀幣": rob_amount + user_data['銀幣'] , "rob" : 1}}
            qqvalues = {"$set": {"銀幣": qq_person['銀幣'] - rob_amount}}
            mycol.update_one({"id": id}, newvalues)
            mycol.update_one({"name": person}, qqvalues)
            rob_log(id,person,rob_amount)
            return "你偷了{} {}枚銀幣，他剩下{}枚".format(person,rob_amount,qq_person['銀幣'] - rob_amount)
        else:
            newvalues = {"$set": {"work": 0, "rob" : 1}}
            mycol.update_one({"id": id}, newvalues)
            return "你被警察抓到了，體力暫且歸零"

def bank_info(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    coin = user_data['bank']
    ans = ""
    for i in coin:
        ans += '{}:{}枚\n'.format(i,coin[i])
    return ans

def portal(id,place):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if place not in ['蘇爾德村','萊克爾村','阿拉瑪村','莫爾茲村','布爾維天空城','碎石洞窟','翠綠森林','永恆之森','阿拉瑪村的地下城']:return 
    if place not in user_data:return "您還沒有此地的傳送卡，請找特定商人購買"
    if user_data['city'] in ['王城','王城的監獄']:
        return "此道具受王城所影響，暫時失去能力"
    else:
        newvalues = {"$set": {"city": place}}
        mycol.update_one({"id": id}, newvalues)
        if place == '莫爾茲村':
            return "你傳送到了 莫爾茲村\n  -美麗的水都\n  (需要搭獨木粥才能移動)"
        if place == '布爾維天空城':
            return "你傳送到了 布爾維天空城\n  -莊麗的天空城\n  (需要飛行靴才能移動)"
        if place in ['蘇爾德村','萊克爾村','阿拉瑪村','莫爾茲村']:
            return "你傳送到了{}\n\n-找村長 : /村長\n".format(place)

        else:
            return "你傳送到了{}~".format(place)

def skill(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['title'] == '村民':
        return "請先轉職，村民是沒有技能的"
    elif user_data['title'] == '劍士':
        return "鬥士(被動技能)\n   -打怪勝率+10%\n    -體力+2"
    elif user_data['title'] == '見習法師':
        return "冥想(主動技能)\n   -想想可樂果\n每次冥想可以得到1顆可樂果\n在探險或打怪時很有用"
    elif user_data['title'] == '小混混':
        return "偷竊(主動技能)\n   -每天可以偷別人一次\n    不一定成功就是\n輸入/偷 Nick"

def black(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['title'] not in  ['領主','大公']:
        return "您不是領主"
    if user_data['city'] in ['王城','王城的監獄']:return "王城無法呦"
    else:
        if check_work_times(id,5):
            how_much = random.randint(1,6)
            now_coin = user_data['銀幣']
            work_minus(id,5)
            if how_much ==1:
                coin = 40 * 5 * user_data['LV']
                sing = '黃河向東流\n榨取農夫汗\n主宰空虛壓\n棉花拾遺芽\n沉思折磨心\n慘淡苦哀歌\n月花盡風起\n萬裏煙雲湧'
            if how_much ==2:
                coin = 45 * 5 * user_data['LV']
                sing = '金錢可使勞工苦\n苦心種植棉花田\n黃昏淒風吹著涼\n憐憫落日苦苦看'
            if how_much ==3:
                coin = 50 * 5 * user_data['LV']
                sing = '棉花滿園紅，苦難苦憤澣\n領主權威宏，壓榨勞工血'
            if how_much ==4:
                coin = 55 * 5 * user_data['LV']
                sing = '明月照草坪，聲聲穿工衣\n青雲掩萬里，歡笑滿心扉'
            if how_much ==5:
                coin = 70 * 5 * user_data['LV']
                sing = '門前路漫青草，慣把棉花採來\n汗流滿面憔悴，為貴主種福田'
            if how_much ==6:
                coin = 130 * 5 * user_data['LV']
                sing = '枝上柳絮聲細，風裡棉花飛絮\n滿園花開春暖，領主樂勞工苦'
            
            newvalues = {"$set": { '銀幣' : coin + now_coin }}
            mycol.update_one({"id": id}, newvalues)

            return '{}\n\n收入{}枚銀幣'.format(sing,coin)
        else:
            return "咖啡因藥過量了"

def camera(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if '拍照'not in user_data:
        return "您尚未取得相機"
    else:
        if user_data['city'] == '永恆之森':
            if check_work_times(id,2):
                work_minus(id,2)
                newvalues = {"$set": { '拍照' : 1 + user_data['拍照'] }}
                mycol.update_one({"id": id}, newvalues)
                return "拍了一張 永恆之森 的照片"
            else:
                return "拍照需要兩體力呦"
        if user_data['city'] == '王城':
            if check_work_times(id,2):
                work_minus(id,2)
                if '王城照片' not in user_data:
                    newvalues = {"$set": { '王城照片' : 1 }}
                    mycol.update_one({"id": id}, newvalues)
                    return "拍了一張 王城 的照片"
                else:
                    newvalues = {"$set": { '王城照片' : 1 + user_data['王城照片'] }}
                    mycol.update_one({"id": id}, newvalues)
                    return "拍了一張 王城 的照片"
            else:
                return "拍照需要兩體力呦"
        if user_data['city'] == '王城的監獄':
            if check_work_times(id,2):
                work_minus(id,2)
                if '王城的監獄的照片' not in user_data:
                    newvalues = {"$set": { '王城的監獄的照片' : 1 }}
                    mycol.update_one({"id": id}, newvalues)
                    return "拍了一張 王城的監獄的照片 的照片"
                else:
                    newvalues = {"$set": { '王城的監獄的照片' : 1 + user_data['王城的監獄的照片'] }}
                    mycol.update_one({"id": id}, newvalues)
                    return "拍了一張 王城的監獄的照片 的照片"
            else:
                return "拍照需要兩體力呦"
        else:
            return "附近的魔素量好像無法驅動相機"

def bag(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    inside = "{}的背包\n\n".format(user_data['name'])
    for i in ['萊克爾村','蘇爾德村','翠綠森林','阿拉瑪村','阿拉瑪村的地下城','碎石洞窟','莫爾茲村','永恆之森','布爾維天空城']:
        if i in user_data:
            inside += " {} -傳送卡 \n".format(i,user_data[i])
    inside += "\n"
    for i in ['香蕉','翠綠森林的現況','可樂果','蘋果','壽司','獨木粥','藥草','阿拉瑪村地下城的齒輪','螺絲','拍照','俗頭','草莓','絢彩之羽','絢彩羽衣']:
        if i in user_data:
            if user_data[i]==0:continue
            a = i
            if i == '拍照':
                a = '照片'
            inside += "  {} : {} \n".format(a,user_data[i])
    return inside

def unlink(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    

def find_where(id,qq_user):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['title'] not in  ['暗月神偷','暗夜盜賊','盜賊']:
        return "您職業不合哦"
    qq_user_data = mycol.find_one({"name": qq_user})
    if qq_user_data == None:
        return "沒有叫做{}的玩家".format(qq_user)
    else:
        return "{} 現在位於:\n{}\n\n錢包裡面有\n{}枚銀幣\n\n等你來偷呦 >w<".format(qq_user,qq_user_data['city'],qq_user_data['銀幣'])

def who_steal_my_money(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    sin = ''
    for i in user_data['been_rob']:
        sin += '{} 共偷了你 {}銀\n'.format(mycol.find_one({"id": i})['name'],user_data['been_rob'][i])
    return sin

def who_i_steal_most(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['title'] not in  ['小混混','盜賊','暗夜盜賊','暗月神偷']:
        return "你屬於被動的那一方"
    sin = '你偷了:\n'
    for i in user_data['you_rob']:
        sin += '{} {}銀'.format(mycol.find_one({"id": i})['name'],user_data['you_rob'][i])
    return sin

def black_market(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['city'] == '布爾維天空城':
        if '王城' not in user_data:return "黑市攤商-萊特:\n\n  嗯？\n"
        if user_data['王城'] >= 20: 
            if user_data['叛亂']==1:    #叛軍
                doordata = mycol.find_one({"id": '叛軍'})
                if doordata['open']!= 1:
                    return "黑市攤商-萊特:\n\n  王城內動蕩不安，叛軍所使用的傳送門被破壞了\n  暫時無法通行\n  我們需要{}張俗頭來修復\n\n/俗頭".format(doordata['俗頭'])
                else:
                    newvalues = {"$set": { 'city' : '王城'}}
                    mycol.update_one({"id": id}, newvalues)
                    return "傳送至王城"
            if user_data['叛亂']==0:    #反叛軍
                doordata = mycol.find_one({"id": '國王軍'})
                if doordata['open']!= 1:
                    return "黑市攤商-萊特:\n\n  王城內動蕩不安，國王軍所使用的傳送門被破壞了\n  暫時無法通行\n  我們需要{}張俗頭來修復\n\n/俗頭".format(doordata['俗頭'])
                else:
                    newvalues = {"$set": { 'city' : '王城'}}
                    mycol.update_one({"id": id}, newvalues)
                    return "傳送至王城"
        if user_data['王城'] == 0 : 
            newvalues = {"$set": { 'city' : '王城' , '王城' :1}}
            if user_data['香蕉'] == 0:
                newvalues = {"$set": { 'city' : '王城' , '王城' :1 ,'香蕉' : 3}}
            mycol.update_one({"id": id}, newvalues)
            return "黑市攤商-萊特:\n\n聽說你對王城有興趣\n我可以讓你上去\n但王城上的人能力都非比尋常\n小心為上，順走\n\n-你傳送到的 王城-\n\n/調查" 
        if user_data['王城'] == 2 : 
            newvalues = {"$set": { 'city' : '王城' , '王城' :1}}
            mycol.update_one({"id": id}, newvalues)
            return "黑市攤商-萊特:\n\n你怎麼回來了@@\n我可以讓你再上去一次\n準備好需要的物資\n小心為上，順走\n\n-你傳送到的 王城-\n\n/調查"


def castle_move(id,cmd):    # 王城 1
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    cmd = int(cmd)
    if check_work_times(id,1):
        if user_data['city'] == '王城':
            if user_data['王城'] == 2:
                if cmd == 1:
                    if user_data['香蕉']>0:
                        work_minus(id,1)
                        newvalues = {"$set": { '香蕉' : 0 , 'work' : 0 , 'city' : '布爾維天空城'}}
                        mycol.update_one({"id": id}, newvalues)
                        return '你把你所有的香蕉放進去，但你太用力了\n香蕉都爛得跟泥一樣\n看樣子這門是廢了\n路過的衛兵看到後很生氣\n你花所有體力把門清乾淨\n最後你被遣返到[布爾維天空城]'
                    else:
                        return '你翻了翻身上，沒有香蕉'
                if cmd == 2:
                    if user_data['魚排']>0:
                        work_minus(id,1)
                        newvalues = {"$set": { '魚排' : 0 , 'work' : 0 , 'city' : '布爾維天空城'}}
                        mycol.update_one({"id": id}, newvalues)
                        police_hit(id)
                        return '你把你所有的魚排放進去\n你被路過的彩蕉飛魚發現\n想當然耳\n你被超級暴打一頓\n回到了[布爾維天空城]療傷'
                    else:
                        return '你翻了翻身上，沒有魚排'
                if cmd == 3:
                    if user_data['壽司']>0:
                        work_minus(id,1)
                        newvalues = {"$set": { '壽司' : 0 , 'work' : 0 , 'city' : '布爾維天空城'}}
                        mycol.update_one({"id": id}, newvalues)
                        return '你把你所有的壽司放進去了\n但飯粒大多黏在洞口下不去\n你覺得不要浪費就把飯粒都吃完了\n\n結果你拉肚子拉到虛脫\n你回到[布爾維天空城]休息\n沒體力了...'
                    else:
                        return '你翻了翻身上，沒有壽司'
            if user_data['王城'] == 4:
                if cmd == 1 :
                    work_minus(id,1)
                    pw = random.randint(1000,9999)
                    newvalues = {"$set": { '王城' : 5 , 'pw': pw , 'city' : '王城的監獄'}}
                    mycol.update_one({"id": id}, newvalues)
                    return "你踩到了捏爛的香蕉滑了\n\n {} \n\n公尺遠\n士兵們衝上來把你抓起來\n\n您的所在位置[王城的監獄]\n[調查]".format(pw)
                if cmd == 2 :
                    work_minus(id,1)
                    pw = random.randint(1000,9999)
                    newvalues = {"$set": { '王城' : 5 , 'pw': pw , 'city' : '王城的監獄'}}
                    mycol.update_one({"id": id}, newvalues)
                    return "你踩到了散落一地的魚排滑了\n\n {} \n\n公尺遠\n士兵們衝上來把你抓起來\n\n您的所在位置[王城的監獄]\n[調查]".format(pw)
                return
            if user_data['王城'] == 9:
                if cmd == 1:    #大城堡
                    work_minus(id,1)
                    newvalues = {"$set": { '王城' : 10 }}
                    mycol.update_one({"id": id}, newvalues)
                    return "映入眼簾的是王城的廚房\n\n[調查]"
                if cmd == 2:
                    work_minus(id,1)
                    newvalues = {"$set": { '王城' : 10 ,'火鍋料' : 1}}
                    mycol.update_one({"id": id}, newvalues)
                    return "你找到了一件 火鍋料 看起來很好吃\n你離開了小屋子\n\n走進了大城堡\n\n映入眼簾的是王城的廚房\n\n[調查]"
            if user_data['王城'] == 19:
                if cmd == 1 :           #支持叛亂
                    newvalues = {"$set": { '王城' : 20 ,'叛亂' : 1 ,'金幣' : user_data['金幣']+1000 , '銀幣' : 1000000 + user_data['銀幣'] , 'city' : '布爾維天空城'}}
                    mycol.update_one({"id": id}, newvalues)
                    return "王 - 凱薩約翰 :\n\n  OK\n  那你可以下去了\n\n(離開會議廳後)\n\n二王子 - 艾文 :\n  我不清楚你怎麼過來的\n但接下來我要開始我的計畫了\n  王城將會動盪起來\n  你先回你該回的地方吧\n  之後會需要你的幫忙的\n  另外，謝謝你沒跟父王打小報告\n  這點錢你先收著\n  等我稱王之後不會少給你的\n\n-1000金\n-100w銀\n您被傳送回 布爾維天空城"
                if cmd == 2 :           #不支持叛亂
                    newvalues = {"$set": { '王城' : 20 ,'叛亂' : 0 ,'金幣' : user_data['金幣']+1000 , '銀幣' : 1000000 + user_data['銀幣'] , 'city' : '布爾維天空城'}}
                    mycol.update_one({"id": id}, newvalues)
                    return "王 - 凱薩約翰 :\n\n  !?\n  艾文 這是怎麼回事？！\n\n二王子 - 艾文 :\n  父王，別聽他胡說！\n\n王 - 凱薩約翰 :\n\n  沒事，我會自己查明清楚的\n  {}謝謝你的告知\n  但假如你騙我的話...\n  總之之後可能還會見面\n  到時候會需要你幫助\n  這點見面禮你收下吧\n\n-1000金\n-100w銀\n您被傳送回 布爾維天空城".format(user_data['name'])
        elif user_data['city'] == '王城的監獄':
            if user_data['王城'] == 5:
                return "身處監獄的你，該調查一下"
            if user_data['王城'] == 6 :
                if cmd == 1:
                    work_minus(id,1)
                    newvalues = {"$set": { '王城' : 7 }}
                    mycol.update_one({"id": id}, newvalues)
                    return "你的房間有\n一個馬桶、一張床以及一個洗手台\n窗戶小小一個，取代鐵欄杆的是魔法屏障\n環境昏昏暗暗的\n冰冷厚重的大門，也只留一個送餐的小洞\n你隱約看到門上有一組數字按鍵\n好像可以讓你按一樣\n\n/打密碼 1234 \n -(這邊當然是輸入你的密碼不太可能是1234就是了)"
                if cmd == 2 :
                    work_minus(id,1)
                    if '在王城監獄唱歌' not in user_data:
                        newvalues = {"$set": { '在王城監獄唱歌' : 1 }}
                    elif user_data['在王城監獄唱歌'] < 5:
                        newvalues = {"$set": { '在王城監獄唱歌' : 1 + user_data['在王城監獄唱歌'] }}
                    else:
                        police_hit(id)
                        return "獄卒嫌你太吵，把你打了一頓"
                    mycol.update_one({"id": id}, newvalues)
                    do_list = ['你在王城的監獄高聲歡唱，旁邊的獄友都為你歡呼','你在王城的監獄跳熱舞，獄友也為你喝采','你在王城的監獄裸奔，獄友笑到肚子痛']
                    pa = random.choice(do_list)
                    return pa
        else:
            return "你不在王城哦"
    else:return "體力不足哦，王城每個行動需要一體力"

def police_hit(id):
    user_data = mycol.find_one({"id": id})
    if '在王城被打了一頓' not in user_data:
        newvalues = {"$set": { '在王城被打了一頓' : 1 }}
    else:
        newvalues = {"$set": { '在王城被打了一頓' : 1 + user_data['在王城被打了一頓'] }}
    mycol.update_one({"id": id}, newvalues)
    
def pass_word_in_wc(id,cmd):        #打密碼
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    cmd = int(cmd)
    if user_data['city'] == '王城的監獄' and user_data['王城']==7:
        if cmd == user_data['pw']:
            newvalues = {"$set": { '王城' : 8 }}
            mycol.update_one({"id": id}, newvalues)
            return "牢房的門打開了\n\n請繼續/調查"
        else:
            return "密碼錯誤"

def stone(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if '叛亂' in user_data and user_data['叛亂'] == 0:
        king_data = mycol.find_one({"id": '國王軍'})
        user_stone = user_data['俗頭']
        king_stone = king_data['俗頭']

        if king_stone-user_stone>=0:
            king_newvalues = {"$set": { '俗頭' : king_stone - user_stone }}
            user_newvalues = {"$set": { '俗頭' : 0 }}
            mycol.update_one({"id": id}, user_newvalues)
            mycol.update_one({"id": '國王軍'}, king_newvalues)
            return "您捐獻了{}張\n還需{}張俗頭".format(user_stone,king_stone - user_stone)

        elif king_stone-user_stone<0:
            king_newvalues = {"$set": { '俗頭' : 0 , 'open' : 1}}
            user_newvalues = {"$set": { '俗頭' : user_stone - king_stone }}
            mycol.update_one({"id": id}, user_newvalues)
            mycol.update_one({"id": '國王軍'}, king_newvalues)
            return "謝謝您..\n通往王城的門修好了!!"

    elif '叛亂' in user_data and user_data['叛亂'] == 1:
        pan_data = mycol.find_one({"id": '叛軍'})
        user_stone = user_data['俗頭']
        pan_stone = pan_data['俗頭']

        if pan_stone-user_stone>=0:
            pan_newvalues = {"$set": { '俗頭' : pan_stone - user_stone }}
            user_newvalues = {"$set": { '俗頭' : 0 }}
            mycol.update_one({"id": id}, user_newvalues)
            mycol.update_one({"id": '叛軍'}, pan_newvalues)
            return "您捐獻了{}張\n還需{}張俗頭".format(user_stone,pan_stone - user_stone)

        elif pan_stone-user_stone<0:
            pan_newvalues = {"$set": { '俗頭' : 0 , 'open' : 1}}
            user_newvalues = {"$set": { '俗頭' : user_stone - pan_stone }}
            mycol.update_one({"id": id}, user_newvalues)
            mycol.update_one({"id": '叛軍'}, pan_newvalues)
            return "謝謝您..\n通往王城的門修好了!!"
    else:
        return "您不隸屬任何軍團"

def flower(id,cmd):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['city'] == '王城':
        if user_data['王城'] == 11:
            if cmd == 1 :
                if user_data['銀幣'] < 100000:return "銀幣不夠喔，你只有{}枚".format(user_data['銀幣'])
                else:
                    newvalues = {"$set": {"廚師衣服" :  1 ,"銀幣": user_data["銀幣"] - 100000 , '王城' : 12}}
                    mycol.update_one({"id": id}, newvalues)
                    return "購入一碗 廚師衣服 \n\n/調查"
            if cmd == 2 :
                if 'kick_out_of_castle' in user_data:
                    newvalues = {"$set": { '王城' : 2 , 'city' : '布爾維天空城' ,'kick_out_of_castle' : 1 + user_data['kick_out_of_castle']}}
                else:
                    newvalues = {"$set": { '王城' : 2 , 'city' : '布爾維天空城' ,'kick_out_of_castle' : 1}}
                mycol.update_one({"id": id}, newvalues)
                return "理所當然的\n來了一群警衛\n也如你所想的\n你被驅逐出境了...\n\n被遣返到[布爾維天空城]"

def pan_team_list(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    else:
        all = mycol.find()
        all.sort('LV',-1)
        ans = ''
        j = 0
        for i in all:
            if '叛亂' in i and i['叛亂'] == 1:
                j+=1
                ans += str(j) + ". 🗡" + "[{}] ".format(i['title']) + i['name'] + " : lv " + str(i['LV']) + "\n"
        return ans

def king_team_list(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    else:
        all = mycol.find()
        all.sort('LV',-1)
        ans = ''
        j = 0
        for i in all:
            if '叛亂' in i and i['叛亂'] == 0:
                j+=1
                ans += str(j) + ". ⚜️" + "[{}] ".format(i['title']) + i['name'] + " : lv " + str(i['LV']) + "\n"
        return ans
        
def minister(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if user_data['city'] == '王城':
        if user_data['王城']>20:
            if user_data['叛亂']==1:
                pan_data =  mycol.find_one({"id": '叛軍'})
                return "叛軍大臣-席斯\n\nHi 我是輔佐二王子的席斯\n謝謝你加入我們陣營\n我們現在在招兵\n假如您願意幫忙的話我們會十分感激您的\n到時候打勝仗所拿到的索賠會分您的\n\n一位士兵需要50金幣\n目前叛軍共有{}位\n\nBTW通往天空成的大電梯也建立好了\n專門給你們外來客用的\n\n回天空城:/回家\n招兵:/士兵 1(數字為數量)".format(pan_data['士兵'])
            if user_data['叛亂']==0:
                king_data =  mycol.find_one({"id": '國王軍'})
                return "國王軍大臣-迪斯\n\nHi 我是輔佐王的迪斯\n謝謝你加入我們陣營\n我們現在在招兵\n假如您願意幫忙的話我們會十分感激您的\n到時候打勝仗所拿到的索賠會分您的\n\n一位士兵需要50金幣\n目前國王軍共有{}位\n\nBTW通往天空成的大電梯也建立好了\n專門給你們外來客用的\n\n回天空城:/回家\n招兵:/士兵 1(數字為數量)".format(king_data['士兵'])

def soldier(id,cmd):        #士兵
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if cmd == '':
        cmd = 1
    else:cmd = int(cmd)
    user_gold = user_data['金幣']
    if (cmd*50) <= user_gold:
        if user_data['叛亂']==1:
            newvalues = {"$set": { '金幣' : user_gold-(cmd*50) }}
            pan_data =  mycol.find_one({"id": '叛軍'})
            if pan_data['open'] == 0: return

            if id in pan_data['donate_list']['士兵']:
                pan_data['donate_list']['士兵'][id] += cmd
            else:
                pan_data['donate_list']['士兵'][id] = cmd

            pan_newvalues = {"$set": { '士兵' : cmd + pan_data['士兵'] ,'donate_list' : pan_data['donate_list']}}
            mycol.update_one({"id": '叛軍'}, pan_newvalues)
            mycol.update_one({"id": id}, newvalues)

            return "[叛軍]\n士兵數 : {} 球\n\n您剩餘{}枚金幣".format(cmd + pan_data['士兵'],user_gold-(cmd*50))

        elif user_data['叛亂']==0:
            newvalues = {"$set": { '金幣' : user_gold-(cmd*50) }}
            king_data =  mycol.find_one({"id": '國王軍'})
            if king_data['open'] == 0: return

            if id in king_data['donate_list']['士兵']:
                king_data['donate_list']['士兵'][id] += cmd
            else:
                king_data['donate_list']['士兵'][id] = cmd

            king_newvalues = {"$set": { '士兵' : cmd + king_data['士兵'] , 'donate_list' : king_data['donate_list'] }}
            mycol.update_one({"id": '國王軍'}, king_newvalues)
            mycol.update_one({"id": id}, newvalues)

            return "[國王軍]\n士兵數 : {} 球\n\n您剩餘{}枚金幣".format(cmd + king_data['士兵'],user_gold-(cmd*50))
        else:
            return "您不屬於任一軍團"
    else:
        return "你只有{}枚金幣".format(user_gold)

def home(id):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    if '布爾維天空城' in user_data :
        newvalues = {"$set": { 'city' : '布爾維天空城' }}
        mycol.update_one({"id": id}, newvalues)
        return '傳送至布爾維天空城'

def donate_gold(id,amount):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    amount = amount.replace(" ",'')
    amount = int(amount)

    if user_data['金幣']>=amount:
        if user_data['叛亂']==0:
            team = mycol.find_one({"id": '國王軍'})

            newvalues = {"$set": { '金幣' : user_data['金幣'] - amount }}

            if id in team['donate_list']['金幣']:
                team['donate_list']['金幣'][id] += amount
            else:
                team['donate_list']['金幣'][id] = amount

            pan_newvalues = {"$set": { '金幣' : team['金幣'] + amount ,'donate_list' : team['donate_list']}}
            
            mycol.update_one({"id": '國王軍'}, pan_newvalues)
            mycol.update_one({"id": id}, newvalues)

            return "國王軍共有{}枚金幣\n您有{}枚".format(team['金幣']+ amount,user_data['金幣']- amount)

        elif user_data['叛亂']==1:
            team = mycol.find_one({"id": '叛軍'})

            newvalues = {"$set": { '金幣' : user_data['金幣'] - amount }}

            if id in team['donate_list']['金幣']:
                team['donate_list']['金幣'][id] += amount
            else:
                team['donate_list']['金幣'][id] = amount

            pan_newvalues = {"$set": { '金幣' : team['金幣'] + amount ,'donate_list' : team['donate_list']}}
            
            mycol.update_one({"id": '叛軍'}, pan_newvalues)
            mycol.update_one({"id": id}, newvalues)

            return "叛軍共有{}枚金幣\n您有{}枚".format(team['金幣']+ amount,user_data['金幣']- amount)
    else:
        return "您只有{}枚哦".format(user_data['金幣'])

def donate_silver(id,amount):
    user_data = mycol.find_one({"id": id})
    if user_data == None:
        return "您還未加入遊戲\n請輸入  \n/加入 你的名字\n來加入遊戲"
    amount = amount.replace(" ",'')
    amount = int(amount)

    if user_data['銀幣']>=amount:
        if user_data['叛亂']==0:
            team = mycol.find_one({"id": '國王軍'})

            newvalues = {"$set": { '銀幣' : user_data['銀幣'] - amount }}

            if id in team['donate_list']['銀幣']:
                team['donate_list']['銀幣'][id] += amount
            else:
                team['donate_list']['銀幣'][id] = amount

            pan_newvalues = {"$set": { '銀幣' : team['銀幣'] + amount ,'donate_list' : team['donate_list']}}
            
            mycol.update_one({"id": '國王軍'}, pan_newvalues)
            mycol.update_one({"id": id}, newvalues)

            return "國王軍共有{}枚銀幣\n您有{}枚".format(team['銀幣']+ amount,user_data['銀幣']- amount)

        elif user_data['叛亂']==1:
            team = mycol.find_one({"id": '叛軍'})

            newvalues = {"$set": { '銀幣' : user_data['銀幣'] - amount }}

            if id in team['donate_list']['銀幣']:
                team['donate_list']['銀幣'][id] += amount
            else:
                team['donate_list']['銀幣'][id] = amount

            pan_newvalues = {"$set": { '銀幣' : team['銀幣'] + amount ,'donate_list' : team['donate_list']}}
            
            mycol.update_one({"id": '叛軍'}, pan_newvalues)
            mycol.update_one({"id": id}, newvalues)

            return "叛軍共有{}枚銀幣\n您有{}枚".format(team['銀幣']+ amount,user_data['銀幣']- amount)
    else:
        return "您只有{}枚哦".format(user_data['銀幣'])
