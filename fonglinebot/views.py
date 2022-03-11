from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, ImageSendMessage

from .defineWTD import wtd
from .crypto_get import crypto,gasfee
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
                ask = event.message.text
                person = event.message.id
                if '啪' in ask :
                    pa_list = ['https://i.imgur.com/E7SYgOa.jpeg','https://i.imgur.com/ah7Ubom.jpeg','https://i.imgur.com/EEA8c3n.jpg']
                    pa = random.choice(pa_list)
                    line_bot_api.reply_message(  # 回復圖片
                        event.reply_token,
                        ImageSendMessage(original_content_url = pa, preview_image_url = pa)
                    )
                if  ask == '孟霖啊' :
                    command_list = ['小雞雞怎麼了?','脖子出來','脖子還舒服嗎？','2030之前都單身吧']
                    com = random.choice(command_list)
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=com)
                    )
                if  ask == '香瓜'  :
                    profile = line_bot_api.get_profile('<user_id>')
                    print(profile)
                    ans = 'Your ID is :' + profile
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text = ans )
                    )
                    
                if  ask == '並沒有' :
                    no_list = ['https://cdn2.ettoday.net/images/3420/d3420288.jpg','https://i.imgur.com/SzAHxWh.jpg','https://cdn2.ettoday.net/images/3420/3420289.jpg','https://i.imgur.com/k4IWCTYh.jpg']
                    no = random.choice(no_list)
                    line_bot_api.reply_message(  # 回復圖片
                        event.reply_token,
                        ImageSendMessage(original_content_url = no, preview_image_url = no)
                    )
                if  ask == '分' :
                    no_list = ['https://i.imgur.com/24BomXy.jpeg']
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
                if '美股貪婪' in ask :
                    url = 'https://markets.money.cnn.com/Marketsdata/Api/Chart/FearGreedHistoricalImage?chartType=AvgPtileModel'
                    line_bot_api.reply_message(  # 回復圖片
                        event.reply_token,
                        ImageSendMessage(original_content_url = url, preview_image_url = url)
                    )
                if '幣圈貪婪' in ask :
                    url = 'https://alternative.me/crypto/fear-and-greed-index.png'
                    #https://alternative.me/crypto/fear-and-greed-index.png
                    line_bot_api.reply_message(  # 回復圖片
                        event.reply_token,
                        ImageSendMessage(original_content_url = url, preview_image_url = url)
                    )
                if ask[0:2] == '$ ':
                    ask = ask[2:]
                    ans = crypto(ask)
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