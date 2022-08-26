from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, ImageSendMessage

from .defineWTD import wtd
from .crypto_get import crypto,gasfee,spot_margin,all_spot_margin,crypto_greed,usdt,cryptoall
from .stocksAPI import stockapi,currency,metal,get_greed_pic
from .do_excel import Nick_lmao_time,check_Nick_lmao_time
from .twstock import oil_price,eggprice,chickenprice,gweei
from .weather import ask_weather,weather_in_english
import random
 
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 
 
@csrf_exempt
def callback(request):
 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                try :
                    ask = event.message.text
                except:
                    break
                if ask == None :
                    break
                userid = event.source.user_id
                ask_type = event.source.type
                if ask_type == 'group':
                        group_id = event.source.group_id
                        print('\n\nRoomID : ',group_id)
                print(userid,'say',ask,'\n')
                imgurl_dict = {'安息吧': 'https://imgur.com/3ni4dLZ.jpg', 'GameFi_gg': 'https://imgur.com/tTANEnl.jpg', '我我也要': 'https://imgur.com/tm9o6TG.jpg', '安詳': 'https://imgur.com/1rRH53I.jpg', 'Crypto_gg': 'https://imgur.com/Z2p7HOh.jpg', '養我 拜託': 'https://imgur.com/AIe5Z5h.jpg', 'NFT_gg': 'https://imgur.com/2SBJ8nf.jpg', '你們說話啊': 'https://imgur.com/2XU9RKi.jpg', '偽娘': 'https://imgur.com/97lUJLO.jpg', '我有錢': 'https://imgur.com/Z1coA4X.jpg', '格局太小': 'https://imgur.com/1uqEueN.jpg', '男生才不會懷孕': 'https://imgur.com/08QcLGe.jpg', '偷嚕': 'https://imgur.com/Y1n2MrC.jpg', '快幫我': 'https://imgur.com/bri3fEZ.jpg', '抽獎我全要': 'https://imgur.com/TcbghMV.jpg', 'DeFi_gg': 'https://imgur.com/XxS2NKx.jpg', '小錢啦': 'https://imgur.com/LsHU0vY.jpg', '看戲': 'https://imgur.com/sZ7VuHU.jpg', '有bug不影響': 'https://imgur.com/wj0jSy4.jpg', '群友賺錢': 'https://imgur.com/OdDWtBq.jpg', 'dddd': 'https://imgur.com/LteluhE.jpg', '誇張喔': 'https://imgur.com/Y3qNhLK.jpg', '槍硬': 'https://imgur.com/CYynAR0.jpg', '弄死你們': 'https://imgur.com/Dn8AJUR.jpg', 'A9': 'https://imgur.com/zIMOe6v.jpg', '就是你啦': 'https://imgur.com/wfWULIp.jpg', '沒輸過': 'https://imgur.com/losMbzR.jpg', '正能量': 'https://imgur.com/kvPv9xX.jpg', 'a9': 'https://imgur.com/BMYhZEw.jpg', '不懂不要碰': 'https://imgur.com/dvIs4d3.jpg', '沒有，滾': 'https://imgur.com/cWZd3Hg.jpg', '獨色色': 'https://imgur.com/ihqqkvY.jpg', '愣': 'https://imgur.com/NNKuQEt.jpg', '你多長': 'https://imgur.com/zo5YkYQ.jpg', 'g8虧爛': 'https://imgur.com/ItXpW6a.jpg', '有輸過': 'https://imgur.com/60QYgJd.jpg', '大餅10w': 'https://imgur.com/9UiJukx.jpg', '仰望大佬': 'https://imgur.com/uCXmPYI.jpg', '好傷人': 'https://imgur.com/l93qEHE.jpg', '....': 'https://imgur.com/ApGIQa9.jpg', '我閉嘴': 'https://imgur.com/uXATqeD.jpg', '我的盤古': 'https://imgur.com/LYUxVCA.jpg', '不拉盤？': 'https://imgur.com/HjAOHS1.jpg', '!?': 'https://imgur.com/UpITfMs.jpg', '????': 'https://imgur.com/2uls8gi.jpg', '便宜啦': 'https://imgur.com/9xpIKr3.jpg','不想上班':'https://i.imgur.com/LOS5ZAC.png','昨天不是賠錢過': 'https://imgur.com/Bm20XC7.jpg', '召喚牛牛': 'https://imgur.com/YNaCUz5.jpg', '下輩子一起抄底': 'https://imgur.com/es9fr7O.jpg', '我是廢物': 'https://imgur.com/XISXl3F.jpg', '突然好難受': 'https://imgur.com/z6WgrUF.jpg', '我好餓啊': 'https://imgur.com/2dQ7rao.jpg', '目光呆滯': 'https://imgur.com/b3nwIkT.jpg', '要爆了': 'https://imgur.com/makcgQF.jpg', '你不是還有生命嗎': 'https://imgur.com/pUBqVG1.jpg', '轉帳中': 'https://imgur.com/4bIQyY8.jpg', '再也不梭了': 'https://imgur.com/9uBMqsi.jpg', '我好想贏': 'https://imgur.com/RWMF4BB.jpg', '美股用日幣計價': 'https://imgur.com/0MLxGSX.jpg', '噴了噴了': 'https://imgur.com/5Qec4jb.jpg', '錢錢飛了': 'https://imgur.com/lzlroVJ.jpg', 'First time?': 'https://imgur.com/9oOA1cn.jpg', '熊市做研究': 'https://imgur.com/x4z7429.jpg', '幣價動態清零': 'https://imgur.com/XrMOtXi.jpg', '退錢啊': 'https://imgur.com/Z5Hulrr.jpg', 'Q_Q': 'https://imgur.com/gK1Sv5Q.jpg', '下輩子當狗': 'https://imgur.com/0vi5ZEs.jpg', '新手賠錢': 'https://imgur.com/uNDjP8w.jpg', '哭啊': 'https://imgur.com/N0p7YpQ.jpg', '每一秒都在蒸發': 'https://imgur.com/OCa1swf.jpg', '盈利呢': 'https://imgur.com/NHRoXGl.jpg', ':l': 'https://imgur.com/9fFKdd5.jpg', '可4我沒錢': 'https://imgur.com/8L3lrQP.jpg', '握草': 'https://imgur.com/CuNJirz.jpg', 'v起來啊': 'https://imgur.com/5FeLG5u.jpg', 'wiwi995': 'https://imgur.com/veRPPCA.jpg', '99sol': 'https://imgur.com/DRyl5Zs.jpg', '\\|/': 'https://imgur.com/VUPJCcd.jpg', '沒了': 'https://imgur.com/X0T8vb7.jpg', '公園還有位子嗎': 'https://imgur.com/dfyjj8s.jpg', '<3': 'https://imgur.com/IgKGAIG.jpg', '給我都好': 'https://imgur.com/Rv3EqDV.jpg', '吐血': 'https://imgur.com/if7kIqf.jpg', '快抄底': 'https://imgur.com/NxOyJev.jpg', '被現實打醒': 'https://imgur.com/7h5cZ85.jpg', '跌下去虧死你': 'https://imgur.com/jTtcDyy.jpg', '我為什麼會在這裡': 'https://imgur.com/F6RzD2r.jpg', '還錢': 'https://imgur.com/uhCyUos.jpg', 'Q.Q': 'https://imgur.com/tMiuelC.jpg', '都沒了': 'https://imgur.com/9BUZdx5.jpg'}
                if ask in imgurl_dict:
                    url = imgurl_dict[ask]
                    line_bot_api.reply_message(  # 回復圖片
                        event.reply_token,
                        ImageSendMessage(original_content_url = url, preview_image_url = url)
                    )
                if '啪' in ask :
                    pa_list = ['https://i.imgur.com/E7SYgOa.jpeg','https://i.imgur.com/ah7Ubom.jpeg','https://i.imgur.com/EEA8c3n.jpg','https://imgur.com/X0T8vb7.jpg','https://imgur.com/9BUZdx5.jpg']
                    pa = random.choice(pa_list)
                    line_bot_api.reply_message(  # 回復圖片
                        event.reply_token,
                        ImageSendMessage(original_content_url = pa, preview_image_url = pa)
                    )
                if '笑死' in ask and userid == 'U0bdb890d03a5b755f3dbb67eafa74f5d' and ask != '尼克笑死幾次':
                    Nick_lmao_time()
                if ask == '尼克笑死幾次' :
                    com = check_Nick_lmao_time()
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=com)
                    )
                if ask == '指令列表':
                    ans = '《查股市》\n◇美股\n「us 指數/tsla/amzn…」\n「美股貪婪」\n◇台股\n「tw 加權/台積電/2330…」\n\n《查幣圈》\n「$ btc/eth…」\n「gas/gas fee/gasfee」\n「usdt匯率」\n「匯率」\n「貸出 btc/eth…」\n「放貸利率」\n「幣圈貪婪」\n\n《查鏈遊》\n「!lms」\n「!stepn」\n\n《查物價》\n「我要黃金」\n「蛋價」\n「豬價」\n「雞價」\n「油價」\n「房價」\n\n《天氣》\n「台北天氣」\n「台中下週天氣」\n\n《Meme》\n「啪」\n「分」\n「腳麻了」\n「我想學英文」\n「尼克笑死幾次」\n'
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=ans)
                    )
                if ask == '我想學英文' :
                    com = 'Let me speak 學英文來賺錢！\nhttps://www.rayskyinvest.com/64390/let-me-speak-lms'
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=com)
                    )
                if  ask == '孟霖啊' :
                    command_list = ['小雞雞怎麼了?','脖子出來','脖子還舒服嗎？','2030之前都單身吧','脊椎脊椎脊椎脊椎脊椎脊椎','2030🤔','小JJ','3mm','脊椎 x_x','喀嚓']
                    com = random.choice(command_list)
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=com)
                    )
                if  '我要嫖' in ask or ask == '我要半套' or ask == '我要全套':
                    command_list = ['👀','✂️🐔','🔪🐔','2000/1s','free','wow','15000/1d','ˊˇˋ','🧐','喀嚓','Nick很高興為您服務']
                    com = random.choice(command_list)
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=com)
                    )
                if  ask == '戒指' or ask == '振宇啊':
                    if group_id != 'C7e2649b69e0ab80f01262051a886d96d':
                        break
                    command_list = ['振宇?','振宇該買了吧','差不多了吧，振宇','可以刷下去了，振宇','該買給可潔囉','可傑在等你的戒指Ｒ','30萬而已，ok的啦','該結婚了吧，振宇']
                    com = random.choice(command_list)
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=com)
                    )
                if  ask == '香瓜' and userid == 'U1c1925ccd29c125ed845cc2db637f39b' :
                    # ans = 'Your ID is :' + userid + '💩'
                    # url = 'https://markets.money.cnn.com/Marketsdata/uploadhandler/z678f7d0azd283da5dca51434aad5398d0938eb5f4.png'
                    url = 'https://alternative.me/crypto/fear-and-greed-index.png'
                    line_bot_api.reply_message(  # 回復圖片
                        event.reply_token,
                        ImageSendMessage(original_content_url = url, preview_image_url = url)
                    )
                if ask == '梗圖列表':
                    ans = '安息\nGameFi_gg\n我我也要\n安詳\nCrypto_gg\n養我 拜託\nNFT_gg\n你們說話啊\n偽娘\n我有錢\n格局太小\n男生才不會懷孕\n偷嚕\n快幫我\n抽獎我全要\nDeFi_gg\n小錢啦\n看戲\n有bug不影響\n群友賺錢\ndddd\n誇張喔\n槍硬\n弄死你們\nA9\n就是你啦\n沒輸過\n正能量\na9\n不懂不要碰\n沒有，滾\n獨色色\n愣\n你多長\ng8虧爛\n有輸過\n大餅10w\n仰望大佬\n好傷人\n....\n我閉嘴\n我的盤古\n不拉盤？\n!?\n????\n便宜啦\n昨天不是賠錢過\n召喚牛牛\n下輩子一起抄底\n我是廢物\n突然好難受\n我好餓啊\n目光呆滯\n要爆了\n你不是還有生命嗎\n轉帳中\n再也不梭了\n我好想贏\n美股用日幣計價\n噴了噴了\n錢錢飛了\nFirst time?\n熊市做研究\n幣價動態清零\n退錢啊\nQ_Q\n下輩子當狗\n新手賠錢\n哭啊\n每一秒都在蒸發\n盈利呢\n:l\n可4我沒錢\n握草\nv起來啊\nwiwi995\n99sol\n\|/\n沒了\n公園還有位子嗎\n<3\n給我都好\n吐血\n快抄底\n被現實打醒\n跌下去虧死你\n我為什麼會在這裡\n還錢\nQ.Q\n都沒了'
                    line_bot_api.reply_message(  # 回復圖片
                        event.reply_token,
                        TextSendMessage(text = ans )
                    )
                if  '逢好帥' in ask or ask == '我好帥' or ask == '我好漂亮' or ask == '我好美' or '尼克好醜' in ask :
                    good_list = ['沒綽','對的','我也這麼認為','你多說幾次也不會有人反駁你','沒有錯','我贊同你的想法','您說得對','您最棒了']
                    if  userid == 'U0bdb890d03a5b755f3dbb67eafa74f5d' and ask != '尼克好醜' and ask != '逢好帥' :
                        good_list = ['笑死','屁','噁心死了','嘔嘔嘔嘔','你想太多了','Bullshit','夠囉','...','幽默','蛤?','我聽不見','3小','呵','你夠囉','媽媽說不能騙人','你好意思?','爛死了','好爛']
                    ans = random.choice(good_list)
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text = str(ans) )
                    )
                if ask == '蛋價':
                    egg = eggprice()
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=egg)
                    )
                if ask == '雞價':
                    chicken = chickenprice()
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=chicken)
                    )
                if  ask == 'Nick好帥' or ask == 'nick好帥' or  ask == '我是台中金城武' or ask == '我是金城武' or '跟金城武一樣' in ask or '我金城武' in ask or '尼克好帥' in ask :
                    bullshit_list = ['笑死','屁','噁心死了','嘔嘔嘔嘔','你想太多了','Bullshit','夠囉','...','幽默','蛤?','我聽不見','3小','呵','你夠囉','媽媽說不能騙人','你好意思?']
                    if '逢' in ask:
                        break
                    no = random.choice(bullshit_list)
                    line_bot_api.reply_message(  # 回復圖片
                        event.reply_token,
                        TextSendMessage(text=no)
                    )    
                if  ask == '並沒有' or ask == '不要瞎掰好嗎':
                    no_list = ['https://cdn2.ettoday.net/images/3420/d3420288.jpg','https://i.imgur.com/SzAHxWh.jpg','https://cdn2.ettoday.net/images/3420/3420289.jpg','https://i.imgur.com/k4IWCTYh.jpg']
                    no = random.choice(no_list)
                    line_bot_api.reply_message(  # 回復圖片
                        event.reply_token,
                        ImageSendMessage(original_content_url = no, preview_image_url = no)
                    )
                if ask == '請打到以下地址':
                    adress = 'SOL-Chain : thatismy.sol \nETH-Chain : thatismy.eth \nBNB-Chain : thatismy.bnb'
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=adress)
                    )
                if  ask == '分' :
                    no_list = ['https://i.imgur.com/fTPyUxt.jpeg','https://i.imgur.com/T6rpwPA.jpeg','https://i.imgur.com/WTLsPY4.jpeg']
                    no = random.choice(no_list)
                    line_bot_api.reply_message(  # 回復圖片 https://i.imgur.com/fm6G0G2.jpeg
                        event.reply_token,
                        ImageSendMessage(original_content_url = no, preview_image_url = no)
                    )
                if  ask == '乞丐超人' :
                    line_bot_api.reply_message(  # 回復圖片 
                        event.reply_token,
                        ImageSendMessage(original_content_url = 'https://i.imgur.com/fm6G0G2.jpeg', preview_image_url = 'https://i.imgur.com/fm6G0G2.jpeg')
                    )
                if  ask == 'gas' or ask == 'gas fee' or ask == 'gasfee':
                    ans = gasfee()
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=ans)
                    )
                if  ask == 'USDT 匯率' or ask == 'usdt匯率' or ask == 'USDT匯率'or ask == 'usdt 匯率' or ask == 'Usdt 匯率' or ask == 'Usdt匯率' and  userid != "Udeadbeefdeadbeefdeadbeefdeadbeef":
                    ans = usdt()
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=ans)
                    )
                if  ask[0:3] == '貸出 ' :
                    ans = spot_margin(ask)
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=ans)
                    )  
                if  ask[0:4] == '放貸利率' or ask[0:4] == '資金費率':
                    ans = all_spot_margin()
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=ans)
                    )  
                if ask == '腳麻了' :
                    url = 'https://i.imgur.com/fzUAf7h.jpeg'
                    line_bot_api.reply_message(  # 回復圖片
                        event.reply_token,
                        ImageSendMessage(original_content_url = url, preview_image_url = url)
                    )   
                if '美股貪婪' in ask :
                    ans = get_greed_pic()
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=ans)
                    )
                if '天氣'in ask and len(ask)<10:
                    ans = ask_weather(ask)
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=ans)
                    )
                    
                if '鮑魚' in ask and ask_type == 'group' :
                    if group_id == 'C28118069d07e5b9d2b1c7eb44bfd5121' or group_id == 'Cd847ab4f2bfd6886fe37bf194cb2d92c':
                        url = 'https://i.imgur.com/a0ezI7q.png'
                        #https://alternative.me/crypto/fear-and-greed-index.png
                        line_bot_api.reply_message(  # 回復圖片
                            event.reply_token,
                            ImageSendMessage(original_content_url = url, preview_image_url = url)
                        )
                if '幣圈貪婪' in ask :
                    url = 'https://alternative.me/crypto/fear-and-greed-index.png'
                    #https://alternative.me/crypto/fear-and-greed-index.png
                    ans = crypto_greed()
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=ans)
                    )
                if ask == '匯率' :
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=currency())
                    )    
                if ask == '我要黃金' :
                    ran = [0,1]
                    cho = random.choices(ran,weights=(90,10))
                    if cho[0] == 1:
                        poop = '💩'
                        line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=poop)
                        )
                    else:
                        line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=metal())
                        )
                if ask == '油價':
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=oil_price())
                        )
                if ask == '房價':
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text='很高 >w<')
                        )
                if ask == '幣價':
                    # ran = [0,1]
                    # a = ['還問啊？','很低啦','OuO?','QAQ','很低 別再問啦>w<','記得多看少動啦']
                    # cho = random.choices(ran,weights=(75,25))
                    # if cho == [0]:
                    ans = cryptoall()
                    # else:
                        # ans = random.choice(a)
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=ans)
                    )
                
                if ask[0:2] == '$ ':
                    ask = ask[2:]
                    ans = crypto(ask)
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=ans)
                    )
                if ask[0:2] == '櫃 ':
                    ask = ask[2:]
                    ans = gweei(ask)
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=ans)
                    )
                if ask[0:3] == 'av ' or ask[0:3] == 'Av ' or ask[0:3] == 'AV ':
                    ask = ask[3:]
                    ans = 'https://jable.tv/search/' + ask + '/'
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=ans)
                    )
                if ask[0:3] == 'tw ' or ask[0:3] == 'TW ' or ask[0:3] == 'Tw ':
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=wtd(ask))
                    )
                if ask[0:3] == 'us ' or ask[0:3] == 'US ' or ask[0:3] == 'Us ':
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=wtd(ask))
                    )
                if ask[:2] == 'w ':
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=weather_in_english(ask[2:]))
                    )
                else:
                    pass
        return HttpResponse()
    else:
        return HttpResponseBadRequest()