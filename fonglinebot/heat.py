from fuzzywuzzy import fuzz

c_ = open("fonglinebot/heatlist.txt", "r", encoding="utf-8")
hot_ = open('fonglinebot/hot.txt', "r", encoding="utf-8")

mylist = hot_.read().splitlines()
name_of_food = []
for i in mylist:
    a = i.split('\t')
    name_of_food .append(a[0])

read_c_=eval(c_.read())

def ask_heat(que):
    max_point = 0
    ans = ''
    possible = []
    finall_ans = ''

    for i in name_of_food:
        now_point = fuzz.partial_ratio(que, i)
        if now_point == 100:
            possible.append(i)
        max_point = max(now_point,max_point)
        if max_point==now_point:
            ans = i
            # if now_point == 100:break
    if ans not in possible:possible.append(ans)

    if len(possible) < 5 :
        for i in range(len(possible)):
            if i  == len(possible)-1:
                finall_ans += read_c_[possible[i]][:-1]
            else:
                finall_ans += read_c_[possible[i]] + '\n'
    else:
        race_list = [0,0]
        for i in possible:
            now_point = fuzz.token_sort_ratio(que,i)
            # print(i,now_point)
            if race_list[0] < now_point:
                race_list = [0,0]
                race_list[0] = now_point
                race_list[1] =i
            elif race_list[0] == now_point:
                race_list.append(i)


        for i in range(len(race_list)):
            if i == 0:continue
            if i == len(race_list)-1:
                finall_ans += read_c_[race_list[i]][:-1]
            else:
                finall_ans += read_c_[race_list[i]] + '\n'
    return finall_ans

# print(ask_heat('牛排'))