# import fonglinebot.game as g
import game as g
import random

def check_cmd(id,cmd):
    if cmd == 'v':
        return g.version()
    if cmd[0:3] == '加入 ':
        name = cmd[3:]
        return g.add_user(id,name)
    if cmd == '打工':
        return g.working(id)
    if cmd == '挖礦':
        return g.mining(id)
    if cmd == '敦倫':
        return g.make_love(id)
    if cmd =='錢包':
        return g.check_wallet(id)
    if cmd == '我':
        return g.user_profile(id)
    if cmd == '魔法少年':
        return g.magic_boy(id)
    if cmd == '村長':
        return g.leader(id)
    if cmd == '祭司':
        return g.priest(id)
    if cmd == '我的銀行':
        return g.bank_info(id)
    if cmd == '升等':
        return g.lv_up(id)
    if cmd == '耕田':
        return g.farm(id)
    if cmd == '收租':
        return g.recive_rent(id)
    if cmd == '收稅':
        return g.recive_tax(id)
    if cmd == '拍照':
        return g.camera(id)
    if cmd == '俗頭':
        return g.stone(id)
    if cmd == '叛軍':
        return g.pan_team_list(id)
    if cmd == '國王軍':
        return g.king_team_list(id)
    if cmd == '喝紅茶':
        return g.black(id)
    if cmd == '國王排名':
        return g.lv_list(id)
    if cmd == '所有排名':
        return g.all_lv_list(id)
    if cmd == '商人':
        return g.seller(id)
    if cmd == '調查':
        return g.investigation(id)
    if cmd == '蓮娜':
        return g.lianna(id)
    if cmd == '萊特':
        return g.black_market(id)
    if cmd == '打怪':
        return g.search(id)
    if cmd == '冥想':
        return g.meditation(id)
    if cmd == '大臣':
        return g.minister(id)
    if cmd == '女巫':
        return g.witch(id)
    if cmd == '1221':
        return g.unlink(id)
    if cmd == '2023':           #新年
        return g.new_year_event2023(id)
    if cmd == '背包':
        return g.bag(id)
    if cmd == '火球術':
        return g.skill_1(id,'火球術')
    if cmd == '水球術':
        return g.skill_1(id,'水球術')
    if cmd == '是誰在偷偷摸摸':
        return g.who_steal_my_money(id)
    if cmd == '偷偷摸摸':
        return g.who_i_steal_most(id)
    if cmd[0] == '找':
        person = cmd[1:]
        person = person.replace(' ','',1)
        return g.find_where(id,person)
    if cmd[0] == '偷':
        person = cmd[1:]
        person = person.replace(' ','',1)
        return g.rob(id,person)
    
    ###王城###
    if cmd == '回家':
        return g.home(id)
    if cmd[0:2] == '王城':
        cmd = cmd[2:]
        cmd = cmd.replace(" ",'')
        return g.castle_move(id,int(cmd))
    if cmd[0:3] == '打密碼':
        cmd = cmd[3:]
        cmd = cmd.replace(" ",'')
        return g.pass_word_in_wc(id,int(cmd))
    if cmd[0:2] == '花花':
        cmd = cmd[2:]
        cmd = cmd.replace(" ",'')
        return g.flower(id,int(cmd))
    if cmd[0:2] == '士兵':
        cmd = cmd[2:]
        cmd = cmd.replace(" ",'')
        return g.soldier(id,cmd)
    if cmd[0:2] == '捐金':
        cmd = cmd[2:]
        cmd = cmd.replace(" ",'')
        return g.donate_gold(id,cmd)
    if cmd[0:2] == '捐銀':
        cmd = cmd[2:]
        cmd = cmd.replace(" ",'')
        return g.donate_silver(id,cmd)
    
    ###寵物###

    if cmd[0:2] == '走走':
        cmd = cmd[3:]
        cmd = cmd.replace(" ",'')
        return g.walk_pet(id,cmd)
    if cmd[0:2] == '轉職':
        title = cmd[3:]
        title = title.replace(" ",'')
        return g.change_title(id,title)   
    if cmd[0:2] == '傳送':
        title = cmd[3:]
        title = title.replace(" ",'')
        return g.portal(id,title)      
    if cmd[0:3] == '泰瑞爾':
        cmd = cmd[3:]
        cmd = cmd.replace(" ",'')
        return g.seller_1(id,int(cmd))
    if cmd[0:2] == '莉法':
        cmd = cmd[2:]
        cmd = cmd.replace(" ",'')
        return g.seller_2(id,int(cmd))
    if cmd[0:2] == '吉斯':
        cmd = cmd[2:]
        cmd = cmd.replace(" ",'')
        return g.seller_3(id,int(cmd))
    if cmd[0:2] == '布魯':
        cmd = cmd[2:]
        cmd = cmd.replace(" ",'')
        return g.seller_4(id,int(cmd))
    if cmd[0:3] == '芬克斯':
        cmd = cmd[3:]
        cmd = cmd.replace(" ",'')
        return g.seller_5(id,int(cmd))
    if cmd[0:6] == '蒂拉芙·林茵':
        cmd = cmd[6:]
        cmd = cmd.replace(" ",'')
        return g.teacher_1(id,int(cmd))
    if cmd[0:2] == '更名':
        return g.change_user_name(id,cmd[3:])
    if cmd == '賭':
        return g.gambling_rules(id)
    if cmd[0:3] == '存銀行':
        cmdd = cmd[4:]
        return g.put_in_bank(id,cmdd)
    if cmd == '銀行':
        return "-存銀行的幣有80%年化-\n\n要存銀行的話請輸入\n/存銀行 金幣 5\n"
    if cmd[0:2] == '提款':
        cmdd = cmd[3:]
        return g.pull_out_bank(id,cmdd)
    if cmd[0:3] == '比大小':
        amount = int(cmd[3:])
        return g.big_or_small(id,amount)
    if cmd == '指令' or cmd == '規則':
        return "指令介紹\n\n掙錢:\n/打工/敦倫/打怪/挖礦\n\n銀行:\n/銀行/提款 x/存銀行 x\n\n升等:\n/升等\n\n排名:\n/國王排名\n\n個人資訊:\n/我\n/職業\n/錢包\n/我的銀行\n/傳送\n\n看看誰偷了你的錢/是誰在偷偷摸摸\n小任務:\n村裡有 村長、祭司、商人、魔法少年 可以互動\n祝你玩得愉快\n現在還算beta版\n有問題請跟我說"
    if cmd == '職業':
        return "總共有4種職業\n\n1.劍士\n  鬥士(被動技能)\n   -打怪勝率+10%\n   -體力+2\n\n2.見習法師\n  冥想(主動技能)\n   -想想可樂果(get 1)\n   -森林裡的怪物都喜歡可樂果(區域boss掉落x10)\n\n  可樂果香(被動技能)\n  -增加小boss遇見機率\n\n3.小混混\n  偷竊(主動技能)\n   -每天可以偷別人一次\n    不一定成功就是\n\n  霸凌(被動技能)\n   -銀幣掉落增加20%\n\n4.農夫\n  -略\n\n想轉職的話請輸入\n\n/轉職 劍士\n"
    
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','加入 奶昔'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','更名 逢'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','冥想'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','職業'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','魔法少年'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','國王排名'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','偷 Feng'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','女巫'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','2023'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','村長'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','我'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','收租'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','傳送  翠綠森林'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','傳送  蘇爾德村'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','傳送  萊克爾村'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','傳送  阿拉瑪村'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','傳送  阿拉瑪村的地下城'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','傳送  永恆之森'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','祭司'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','轉職 劍士'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','女巫'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','蒂拉芙·林茵 1'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','俗頭'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','走走 2'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','萊特'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','芬克斯 3'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','打密碼 1572'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','調查'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','商人'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','捐金 2'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','花花 1'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','打怪'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','火球術'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','回家'))
# print(check_cmd('U1c1925ccd29c125ed845cc2db637f39b','提款 銀幣100'))