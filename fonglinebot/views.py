from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, ImageSendMessage

from .defineWTD import wtd
from .crypto_get import crypto,gasfee,spot_margin,all_spot_margin,crypto_greed
from .stocksAPI import stockapi,currency,metal,get_greed_pic
from .do_excel import Nick_lmao_time,check_Nick_lmao_time
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
                userid = event.source.user_id
                ask_type = event.source.type
                if ask_type == 'group':
                        group_id = event.source.group_id
                        print('\n\nRoomID : ',group_id)
                print(userid,'say',ask,'\n')
                if ask == None :
                    break
                if '啪' in ask :
                    pa_list = ['https://i.imgur.com/E7SYgOa.jpeg','https://i.imgur.com/ah7Ubom.jpeg','https://i.imgur.com/EEA8c3n.jpg']
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
                if  ask == '孟霖啊' :
                    command_list = ['小雞雞怎麼了?','脖子出來','脖子還舒服嗎？','2030之前都單身吧','脊椎脊椎脊椎脊椎脊椎脊椎']
                    com = random.choice(command_list)
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=com)
                    )
                if  ask == '戒指' :
                    if group_id != 'C7e2649b69e0ab80f01262051a886d96d':
                        break
                    command_list = ['振宇?','振宇該買了吧','差不多了吧，振宇','可以刷下去了，振宇','該買給可潔囉']
                    com = random.choice(command_list)
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=com)
                    )
                if  ask == '香瓜' and userid == 'U1c1925ccd29c125ed845cc2db637f39b' :
                    # ans = 'Your ID is :' + userid + '💩'
                    url = 'https://markets.money.cnn.com/Marketsdata/uploadhandler/z678f7d0azd283da5dca51434aad5398d0938eb5f4.png'
                    #https://alternative.me/crypto/fear-and-greed-index.png
                    line_bot_api.reply_message(  # 回復圖片
                        event.reply_token,
                        ImageSendMessage(original_content_url = url, preview_image_url = url)
                    )
                    # line_bot_api.reply_message(  # 回復訊息文字
                    #     event.reply_token,
                    #     TextSendMessage(text = str(ans) )
                    # )
                if  '逢好帥' in ask or ask == '我好帥' or '尼克好醜' in ask :
                    good_list = ['沒綽','對的','我也這麼認為','你多說幾次也不會有人反駁你','沒有錯','我贊同你的想法']
                    if  userid == 'U0bdb890d03a5b755f3dbb67eafa74f5d' and ask != '尼克好醜'  :
                        good_list = ['笑死','屁','噁心死了','嘔嘔嘔嘔','你想太多了','Bullshit','夠囉','...','幽默','蛤?','我聽不見','3小','呵','你夠囉','媽媽說不能騙人','你好意思?']
                    ans = random.choice(good_list)
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text = str(ans) )
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
                if  ask == '分' :
                    no_list = ['https://i.imgur.com/fTPyUxt.jpeg','https://i.imgur.com/T6rpwPA.jpeg','https://i.imgur.com/WTLsPY4.jpeg']
                    no = random.choice(no_list)
                    line_bot_api.reply_message(  # 回復圖片
                        event.reply_token,
                        ImageSendMessage(original_content_url = no, preview_image_url = no)
                    )
                if  ask == 'gas' or ask == 'gas fee' or ask == 'gasfee':
                    ans = gasfee()
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
                if  ask[0:4] == '放貸利率' :
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
                    url = get_greed_pic()
                    line_bot_api.reply_message(  # 回復圖片
                        event.reply_token,
                        ImageSendMessage(original_content_url = url, preview_image_url = url)
                    )
                if '鮑魚' in ask and ask_type == 'group' :
                    if group_id == 'C3ab802df2f56bf2cb65206d0c7192699' or group_id == 'Cd847ab4f2bfd6886fe37bf194cb2d92c':
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
                if ask[0:2] == '$ ':
                    ask = ask[2:]
                    ans = crypto(ask)
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
                else:
                    pass
        return HttpResponse()
    else:
        return HttpResponseBadRequest()