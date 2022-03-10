from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, ImageSendMessage

from .defineWTD import wtd
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
                ans = wtd(ask)

                if '啪' in ask :
                    pa_list = ['https://i.imgur.com/E7SYgOa.jpeg','https://i.imgur.com/ah7Ubom.jpeg','https://i.imgur.com/EEA8c3n.jpg']
                    pa = random.choice(pa_list)
                    line_bot_api.reply_message(  # 回復圖片
                        event.reply_token,
                        ImageSendMessage(original_content_url = pa, preview_image_url = pa)
                    )
                else:
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=ans)
                    )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()