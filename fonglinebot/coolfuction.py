import json

def nick_counter():
    
    with open("fonglinebot/lmao.json") as f:
        p = json.load(f)
    print("name =", p["Nick"])

    p["Nick"] = int(p["Nick"]) + 1
    with open("fonglinebot/lmao.json", "w") as f:
        json.dump(p, f, indent = 4)

def ask_nick_lmao():
    f = open("fonglinebot/lmao.json",'r')
    p = json.load(f)
    return p['Nick']
