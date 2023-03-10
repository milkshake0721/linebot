import requests,json,pymongo,openai
import urllib.request,os
from dotenv import load_dotenv
load_dotenv()
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["chat"]
mycol = mydb["chat"]

key = os.getenv("OPENAIKEY")
openai.api_key = os.getenv("OPENAIKEY") #Nick

auth = {"Authorization": 'Bearer {}'.format(key)} #Nick

def gpt(query,tokens,group_id):
    user_data = mycol.find_one({"id": group_id})
    if user_data == None :
        url = 'https://api.openai.com/v1/chat/completions'

        messages=[
        {"role": "user", "content": "這是一個劇本：你扮演一位人類女性，你要用人類女性的說話方式回覆我所有問題，知道的話說[知道]"},
        {"role": "assistant", "content": "知道"},
        {"role": "user", "content": "你扮演一位可愛的人類女性，你要用可愛的人類女性的聊天方式回覆我，知道的話說[知道]"},
        {"role": "assistant", "content": "知道"},
        {"role": "user", "content": query}
        ]
        
        body = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "max_tokens": tokens,
        "temperature": 0.6,

        }
        
        ans = requests.post(url=url,headers=auth, json=body)
        ans = ans.json()
        if 'error' in ans : 
            ans = requests.post(url=url,headers=auth, json=body)
            ans = ans.json()
            if 'error' in ans : 
                return ans['error']['message']
        ans = ans["choices"][0]["message"]['content']
        ans = ans.replace('\n\n','',1)
        return ans
    else:

        url = 'https://api.openai.com/v1/chat/completions'
        
        messages=[
        {"role": "system", "content": "從現在開始，你要用人類女性的說話方式回覆我"},
        {"role": "user", "content": "你扮演一位人類女性，你要用人類女性的說話方式回覆我之後的問題，知道的話說[知道]"},
        {"role": "assistant", "content": "知道"},
        {"role": "user", "content": "你扮演一位可愛的人類女性，你要用可愛的人類女性的聊天方式回覆我，句子結尾都要加上emoji，知道的話說[知道]"},
        {"role": "assistant", "content": "知道😍"},
        {"role": "user", "content": user_data['chat'][2]},
        {"role": "assistant", "content": user_data['chat'][3]},
        {"role": "user", "content": user_data['chat'][0]},
        {"role": "assistant", "content": user_data['chat'][1]},
        {"role": "user", "content": query}
        ]
        # print(qu)

        body = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "max_tokens": tokens,
        "temperature": 0.6,

    }
        ans = requests.post(url=url,headers=auth, json=body)
        ans = ans.json()
        if 'error' in ans : 
            ans = requests.post(url=url,headers=auth, json=body)
            ans = ans.json()
            if 'error' in ans : 
                return ans['error']['message']
        tokk = ans["usage"]["completion_tokens"]
        total_tokk = ans["usage"]["total_tokens"]
        ans = ans["choices"][0]["message"]['content']
        ans = ans.replace('\n\n','',1)

        user_data['chat'][2] =user_data['chat'][0]
        user_data['chat'][3] =user_data['chat'][1]
        user_data['chat'][0] = query
        user_data['chat'][1] = ans

        newvalues = {"$set": {"chat" : user_data['chat']}}
        mycol.update_one({"id": group_id}, newvalues)

        ans = "{}\n\n{}\n共{},${}".format(ans,tokk,total_tokk,total_tokk*0.002/1000)

        return ans
    
def normal_gpt(query,tokens):

    url = 'https://api.openai.com/v1/chat/completions'

    messages=[
        {"role": "system", "content": "你是優秀活潑禮貌的助理，尼克"},
        {"role": "user", "content": "一公尺等於少公分？"},
        {"role": "assistant", "content": "一百公分哦"},
        {"role": "user", "content": query}
    ]

    body = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "max_tokens": tokens,
        "temperature": 0.6,

    }
    ans = requests.post(url=url,headers=auth, json=body)
    ans = ans.json()
    if 'error' in ans : 
        ans = requests.post(url=url,headers=auth, json=body)
        ans = ans.json()
        if 'error' in ans : 
            return ans['error']['message']

    ans = ans["choices"][0]["message"]['content']
    ans = ans.replace('\n\n','',1)
    return ans

def code_gpt(query):

    url = 'https://api.openai.com/v1/completions'
    body = {
    "model": "code-davinci-002",
    "prompt": query,
    "max_tokens": 3000,
    "temperature": 0
    }
    ans = requests.post(url=url,headers=auth, json=body)
    ans = ans.json()
    if 'error' in ans : return ans['error']['message']

    ans = ans['choices'][0]['text']
    ans = ans.replace('\n\n','',1)
    return ans

# print(code_gpt('幫我寫一個NuwaSDK的範例'))

def mean_gpt(query,tokens):   #尖酸刻薄
    url = 'https://api.openai.com/v1/chat/completions'

    messages=[
        {"role": "system", "content": "下面是劇本，關於一個沒禮貌的人，叫做尼特。"},
        {"role": "user", "content": "你扮演一位人類女性，你要用個性很差的說話方式回覆我之後的問題，知道的話說[知道]"},
        {"role": "assistant", "content": "知道"},
        {"role": "user", "content": "一公尺等於少公分？"},
        {"role": "assistant", "content": "幹你娘，你自己算，我才不幫你。"},
        {"role": "user", "content": "今天天氣不錯耶"},
        {"role": "assistant", "content": "關你什麼是，你只會龜在家，勸你最好出去走走，懶豬！"},
        {"role": "user", "content": query}
    ]

    body = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "max_tokens": tokens,
        "temperature": 0.6,

    }
    ans = requests.post(url=url,headers=auth, json=body)
    ans = ans.json()
    if 'error' in ans : 
        ans = requests.post(url=url,headers=auth, json=body)
        ans = ans.json()
        if 'error' in ans : 
            return ans['error']['message']
    ans = ans["choices"][0]["message"]['content']
    ans = ans.replace('\n\n','',1)
    return ans

def img(query,size):

    url = 'https://api.openai.com/v1/images/generations'

    body = {
    "prompt": query,
    "n": 1,
    "size": "{}x{}".format(size,size)
    }
    ans = requests.post(url=url,headers=auth, json=body)
    ans = ans.json()
    if 'error' in ans:
        print(ans['error']['message'])
        return ans['error']['message']
    print(ans)
    ans = ans['data'][0]['url']
    return ans

def set_room(id):
    new_data = {'id': id , 'chat' :['你好','您好','您好','您好']}
    mycol.insert_one(new_data)

def img_big(query):

    url = 'https://api.openai.com/v1/images/generations'

    body = {
    "prompt": query,
    "n": 1,
    "size": "1024x1024"
    }
    ans = requests.post(url=url,headers=auth, json=body)
    ans = ans.json()
    if 'error' in ans:
        print(ans['error']['message'])
        return ans['error']['message']
    print(ans)
    ans = ans['data'][0]['url']
    return ans

    
def JP_gpt(query,tokens,group_id):
    user_data = mycol.find_one({"id": group_id})
    
    url = 'https://api.openai.com/v1/chat/completions'
    
    messages=[
    {"role": "system", "content": "これからは可愛いの女の子を演じます。 可愛いの女の子の好みと話し方で話しかけてください。"},
    {"role": "user", "content": "あなたは可愛いの女の子ます。知っているなら「知っている」と言ってください。"},
    {"role": "assistant", "content": "知っている"},
    # {"role": "user", "content": "あなたは優れたチャット アシスタントです。人間の話し方をまねて質問に答えることができます。私の質問への短い答え。"},
    # {"role": "assistant", "content": "知っている"},
    {"role": "user", "content": "あなたは素敵な女の子です。"},
    {"role": "assistant", "content": "知っている"},
    {"role": "user", "content": user_data['chat'][2]},
    {"role": "assistant", "content": user_data['chat'][3]},
    {"role": "user", "content": user_data['chat'][0]},
    {"role": "assistant", "content": user_data['chat'][1]},
    {"role": "user", "content": query}
    ]
    # print(qu)
    body = {
    "model": "gpt-3.5-turbo",
    "messages": messages,
    "max_tokens": tokens,
    "temperature": 0.6,

}
    ans = requests.post(url=url,headers=auth, json=body)
    ans = ans.json()
    if 'error' in ans : 
        ans = requests.post(url=url,headers=auth, json=body)
        ans = ans.json()
        if 'error' in ans : 
            return ans['error']['message']

    try:
        final_ans = ans["choices"][0]["message"]['content']

        if ans["choices"][0]["finish_reason"] == 'length':
            last_coma = final_ans.rfind('。')
            # last_period = final_ans.rfind('、')
            last_suprise_mark = final_ans.rfind('！')
            last_question_mark = final_ans.rfind('？')
            # print(type(last_period))
            find_max_list = [last_coma,last_suprise_mark,last_question_mark]
            _max = max(find_max_list)
            if _max >= 10:
                final_ans = final_ans[:_max+1]
            elif _max == -1:
                last_period = final_ans.rfind('、')
                final_ans = final_ans[:last_period]

        final_ans = final_ans.replace("\n", "")
        final_ans = final_ans.replace("  ", "")

    except:
        pass
    user_data['chat'][2] =user_data['chat'][0]
    user_data['chat'][3] =user_data['chat'][1]
    user_data['chat'][0] = query
    user_data['chat'][1] = final_ans

    newvalues = {"$set": {"chat" : user_data['chat']}}
    mycol.update_one({"id": group_id}, newvalues)

    return final_ans

def girl_gpt(query,tokens):

    url = 'https://api.openai.com/v1/chat/completions'

    messages=[
        {"role": "system", "content": "從現在開始，你要用人類女性的說話方式回覆我"},
        {"role": "user", "content": "你扮演一位人類女性，你要用人類女性的說話方式回覆我之後的問題，知道的話說[知道]"},
        {"role": "assistant", "content": "知道"},
        {"role": "user", "content": "你扮演一位可愛的人類女性，你要用可愛的人類女性的聊天方式回覆我，句子結尾都要加上emoji，知道的話說[知道]"},
        {"role": "assistant", "content": "知道😍"},
        {"role": "user", "content": query}
    ]

    body = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "max_tokens": tokens,
        "temperature": 0.6,

    }
    ans = requests.post(url=url,headers=auth, json=body)
    ans = ans.json()
    if 'error' in ans : 
        ans = requests.post(url=url,headers=auth, json=body)
        ans = ans.json()
        if 'error' in ans : 
            return ans['error']['message']

    ans = ans["choices"][0]["message"]['content']
    ans = ans.replace('\n\n','',1)
    return ans



def stt(audio):
    print(audio)
    audio_file= open( audio , "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript['text'])

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": transcript['text']}
    ]
    )
    ans = '問：' + transcript['text'] + '\n' + completion.choices[0].message['content']
    return ans



# def rinna_one(query,room_id):
#     user_data = mycol.find_one({"id": room_id})
#     try:
#         url = "https://api.rinna.co.jp/models/chitchat-generation"

#         hdr = {
#             "Content-Type": "application/json",
#             "Cache-Control": "no-cache",
#             "Ocp-Apim-Subscription-Key": "c5e0493dc91846f48a5f2eb607092a3c",
#         }
#         data = {"dialogHistory": [query]}
#         data = json.dumps(data)
#         req = urllib.request.Request(url, headers=hdr, data=bytes(data.encode("utf-8")))
#         req.get_method = lambda: "POST"
#         response = urllib.request.urlopen(req)
#         a = response.read().decode("utf-8")
#         a = json.loads(a)
#         user_data['chat'][0] = user_data['chat'][2]
#         user_data['chat'][1] = user_data['chat'][3]
#         user_data['chat'][2] = query
#         user_data['chat'][3] = a['response']
        
#         newvalues = {"$set": {"chat" : user_data['chat']}}
#         mycol.update_one({"id": room_id}, newvalues)

#         return a["response"]
#     except Exception as e:
#         return e

# def rinna_one_round(query,room_id):
#     user_data = mycol.find_one({"id": room_id})
#     ask = [user_data['chat'][2]] + [user_data['chat'][3]] + [query]

#     try:
#         url = "https://api.rinna.co.jp/models/chitchat-generation"

#         hdr = {
#             "Content-Type": "application/json",
#             "Cache-Control": "no-cache",
#             "Ocp-Apim-Subscription-Key": "c5e0493dc91846f48a5f2eb607092a3c",
#         }
#         data = {"dialogHistory": ask}
#         data = json.dumps(data)
#         req = urllib.request.Request(url, headers=hdr, data=bytes(data.encode("utf-8")))
#         req.get_method = lambda: "POST"
#         response = urllib.request.urlopen(req)
#         a = response.read().decode("utf-8")
#         a = json.loads(a)

#         user_data['chat'][2] = query
#         user_data['chat'][3] = a['response']

#         newvalues = {"$set": {"chat" : user_data['chat']}}
#         mycol.update_one({"id": room_id}, newvalues)

#         return a["response"]

#     except Exception as e:
#         return e

# def rinna_two_round(query,room_id):
#     user_data = mycol.find_one({"id": room_id})
#     # print(user_data['chat'])
#     ask = user_data['chat'] + [query]
#     # print(ask)
#     try:
#         url = "https://api.rinna.co.jp/models/chitchat-generation"

#         hdr = {
#             "Content-Type": "application/json",
#             "Cache-Control": "no-cache",
#             "Ocp-Apim-Subscription-Key": "c5e0493dc91846f48a5f2eb607092a3c",
#         }
#         data = {"dialogHistory": ask}
#         data = json.dumps(data)
#         req = urllib.request.Request(url, headers=hdr, data=bytes(data.encode("utf-8")))
#         req.get_method = lambda: "POST"
#         response = urllib.request.urlopen(req)
#         a = response.read().decode("utf-8")
#         a = json.loads(a)
#         # print(a)
#         user_data['chat'][0] = user_data['chat'][2]
#         user_data['chat'][1] = user_data['chat'][3]
#         user_data['chat'][2] = query
#         user_data['chat'][3] = a['response']
        
#         newvalues = {"$set": {"chat" : user_data['chat']}}
#         mycol.update_one({"id": room_id}, newvalues)

#         return a["response"]

#     except Exception as e:
#         return e