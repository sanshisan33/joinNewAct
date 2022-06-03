# -*- coding: utf-8 -*-

import socketserver
import subprocess
import sqlite3
import leancloud
from datetime import datetime
import pandas as pd
import random
import json
import paho.mqtt.client as mqtt

endIdList = []
newOne = 0

leancloud.init('8MEtrBGXmxtCE52pGqndGpla-gzGzoHsz','LuBCjDXGdjPV1C7XpfpwkmUr')
OBJ = leancloud.Object.extend('postimes')
b = OBJ.query
OBJ_final = leancloud.Object.extend('generate')
OBJ_state= leancloud.Object.extend('RFID_LIST')


TemporaryList = []
finishLIst = []
ReadList = []


FFF=["念动增幅装置", "彩虹尽头探寻者", "蒸汽朋克蘑菇"]
FFZ=["时空要塞守卫","电脑棋士深蓝","木卫二意识中枢"]
FZF=["太空歌剧大师","随您便先生","软体世界滑翔伞兵"]
FZZ=["超光速旅行蜗牛","宇宙牛仔博主","科学一周的晚上"]
ZZZ=["魔幻现实主义国王","奇幻图书馆管理员","生活安全出口保安"]
ZFF=["通俗冒险故事主角","文学玉米粒播种者","持摄像机的仿生人"]
ZFZ=["基因改造发条宇航员","骑士文学侦探","乌托邦熬夜冠军"]
ZZF=["月光下的闰土","已知和未知的诗歌","种类不明的鲸"]
ch_list=[FFF,FFZ,FZF,FZZ,ZZZ,ZFF,ZFZ,ZZF]

text_list = [["《故乡》","深蓝的天空中挂着一轮金黄的圆月，下面是海边的沙地，都种着一望无际的碧绿的西瓜。其间有一个十一二岁的少年，项带银圈，手捏一柄钢叉，向一匹猹尽力的刺去。那猹却将身一扭，反从他的胯下逃走了。"],
["博尔赫斯","我希望时间会变成一个广场，照相机只是一个让我的所思暂时安生的处所，一个压扁的铁皮罐子。时间的广场可以容纳很多意外。时间之外的一切，也许只是多余的忧愁。"],
["《白银时代》","生活这个词有很古怪的用法：在公司内部，我们有组织生活、集体生活。在公司以外，我们有家庭生活、夫妻生活。除此之外，你还可以去体验生活。实际上，生活就是你不乐意发生但却发生了的事……和真实不真实没有关系。"],
["《三体》","无限长的曲线就是宇宙的抽象，一头连着无限的过去，另一头连着无限的未来，中间只有无规律无生命的随机起伏，一个个高低错落的波峰就像一粒粒大小不等的沙子，整条曲线就像是所有沙粒排成行形成的一维沙漠，荒凉寂寥，长得更令人无法忍受。你可以沿着它向前向后走无限远，但永远找不到归宿。 "],
["《狂人日记》","但是我有勇气，他们便越想吃我，沾光一点这勇气。老头子跨出门，走不多远，便低声对大哥说道，“赶紧吃罢！”大哥点点头。原来也有你！这一件大发见，虽似意外，也在意中：合伙吃我的人，便是我的哥哥！","吃人的是我哥哥！","我是吃人的人的兄弟！","我自己被人吃了，可仍然是吃人的人的兄弟！"],
["《狂人日记》","凡事总须研究，才会明白。古来时常吃人，我也还记得，可是不甚清楚。我翻开历史一查，这历史没有年代，歪歪斜斜的每叶上都写着'仁义道德'几个字。我横竖睡不着，仔细看了半夜，才从字缝里看出字来，满本都写着两个字是'吃人'！","书上写着这许多字，佃户说了这许多话，却都笑吟吟的睁着怪眼看我。我也是人，他们想要吃我了！"],
["《朝花夕拾》","人说，讽刺和冷嘲只隔一张纸，我以为有趣和肉麻也一样。","虫蛆也许是不干净的，但它们并没有自命清高；鸷禽猛兽以较弱的动物为饵，不妨说是凶残的罢，但它们从来没有竖过“公理”“正义”的旗子，使牺牲者直到被吃的时候为止，还是一味佩服赞叹它们。"],
["《门外文谈》","话已经说得不少了。总之，单是话不行，要紧的是做。要许多人做：大众和先驱；要各式的人做：教育家，文学家，言语学家……。这已经迫于必要了，即使目下还有点逆水行舟，也只好拉纤；顺水固然好得很，然而还是少不得把舵的。","这拉纤或把舵的好方法，虽然也可以口谈，但大抵得益于实验，无论怎么看风看水，目的只是一个：向前。"],
["《门外文谈》","几个读书人在书房里商量出来的方案，固然大抵行不通，但一切都听其自然，却也不是好办法。现在在码头上，公共机关中，大学校里，确已有着一种好像普通话模样的东西，大家说话，既非“国语”，又不是京话，各各带着乡音，乡调，却又不是方言，即使说的吃力，听的也吃力，然而总归说得出，听得懂。如果加以整理，帮它发达，也是大众语中的一支，说不定将来还简直是主力。我说要在方言里“加入新的去”，那“新的”的来源就在这地方。待到这一种出于自然，又加人工的话一普遍，我们的大众语文就算大致统一了。"],
["《秋夜》","在我的后园，可以看见墙外有两株树，一株是枣树，还有一株也是枣树。","这上面的夜的天空，奇怪而高，我生平没有见过这样的奇怪而高的天空。","他仿佛要离开人间而去，使人们仰面不再看见。","然而现在却非常之蓝，闪闪地眨着几十个星星的眼，冷眼。","他的口角上现出微笑，似乎自以为大有深意，而将繁霜洒在我的园里的野花草上。"]]

# df = pd.read_csv("/wordDataTotal_quchong.csv") 
df = pd.read_csv('./wordDataTotal_quchong.csv') 

#作品维度
wenhua=[-0.2,0.2,-0.2,-0.2,0.2,0.2,0.2,0.2]
renjian=[0.2,0.2,-0.2,0.2,0.2]
siwei=[-0.2,0.2,-0.2,-0.2,0.2,0.2,-0.2]
#区域维度
AS = [0,0.78,0.4] # 文化演绎
BS = [0.65,0,-0.35] # 人间故事
CS = [-0.92,-0.55,0] # 思维核力

HOST = "zstu-interaction.art"
PORT = 1883
client = mqtt.Client()
client.connect(HOST, PORT, 60)

# 转16进制函数
def dec_to_hex(aaa):
    l = ""
    zzz = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]

    if aaa < 0:
        return "- " + dec_to_hex(abs(aaa))#负数先转为正数，再调用函数主体
    else:
        num,reminder = divmod(aaa,16)#算除法求除数和余数
        l += zzz[num]
        l += zzz[reminder]
    return l

#从读卡器客户端提取id 和地点
def tiqu2(data):
    a= [[1],[4,5,6,7,  8,9,10,11,  12,13,14,15]]
    duqu =[]
    for i in range(int(len(data)/18)):
        y=""
        z=[]
        print(type(data[a[0][0]+i*18]))
        z.append(data[a[0][0]+i*18])
        for idx in range(12):
            y += dec_to_hex(data[a[1][idx]+i*18])
        z.append(y)
        duqu.append(z)
    return duqu

def shagnchaun(data): # 上传信息到云数据库
    a = OBJ()
    
    a.set("POS",str(data[0]))
    print("上传pos")
    print(str(data[0]))
    a.set("RFID",data[1])
    print("上传ecp")
    print(data[1])
    
    a.save()

def quyuDianzan(RFID):
    q = [0,0,0]
    z = [0,0,0]
    OBJ = leancloud.Object.extend('postimes')
    b = OBJ.query
    b.equal_to('RFID','{}'.format(RFID))
    id_list = b.find()
    # print(1)
    aaa=[]
    for row in id_list:
        aa=[]
        aa.append(int(row.get('POS')))
        aa.append(datetime.timestamp(row.created_at))
        aaa.append(aa)
    
    lastTime=[]
    AT = 0
    BT = 0
    CT = 0
    for i in range(len(aaa)):
        if int(aaa[i][0]) < 10: # 区域数据
            aaa[i].append(1)
            if lastTime==[]:
                lastTime.append(aaa[i])
            else:
                if int(lastTime[0][0]) == 3:
                    AT += int(aaa[i][1])-int(lastTime[0][1])
                    lastTime = []
                    lastTime.append(aaa[i])
                elif int(lastTime[0][0]) == 4:
                    BT += int(aaa[i][1])-int(lastTime[0][1])
                    lastTime = []
                    lastTime.append(aaa[i])
                elif(int(lastTime[0][0]) == 5 or int(lastTime[0][0]) == 6):
                    CT += int(aaa[i][1])-int(lastTime[0][1])
                    lastTime = []
                    lastTime.append(aaa[i])
                else:
                    continue
        else: # 点赞数据
            # print("dianzan")
            aaa[i].append(0)
            if int(aaa[i][0])>=11 and int(aaa[i][0])<16:
                z[1] += renjian[int(aaa[i][0])-11]
            elif int(aaa[i][0])>=16 and int(aaa[i][0])<23:
                z[2] += siwei[int(aaa[i][0])-16]
            elif int(aaa[i][0])>=23 and int(aaa[i][0])<31:
                z[2] += wenhua[int(aaa[i][0])-23]

    if (AT+BT+CT)!= 0:

        #计算百分比
        AT_B = AT/(AT+BT+CT)
        BT_B = BT/(AT+BT+CT)
        CT_B = CT/(AT+BT+CT)
    else:
        AT_B = 0.33
        BT_B = 0.33
        CT_B = 0.33
    # print(4)
    for i in range(3):
        q[i] = AS[i]*AT_B + BS[i]*BT_B + CS[i]*CT_B
    
    return q,z,aaa

def jiance(data): # 打卡数据判断
    global newOne
    global endIdList

    for item in data:
        print("抓取单条数据")
        # print(item[0])
        if (item[0] < 10):
            shagnchaun(item)# 发送到服务器
            if int(item[0]) == 7 or int(item[0]) == 6: # 加音乐内容
                if item[1] not in finishLIst:
                    chuangeState(item[1])
                    finishLIst.append(item[1])
                else:
                    pass

        else:
            shagnchaun(item)# 发送到服务器
            if (item[0] == 16):
                client.publish("/cxx/energy",str(random.randint(500,5000)),2) 
    # conn.close()

def quci(RFID):
    #取词 数据
    WordOBJ = leancloud.Object.extend('word_record')
    c = WordOBJ.query
    c.equal_to('RFID','{}'.format(RFID))
    word_list = c.find()
    w = [0,0,0]
    recordWord=[]
    word1_list = []
    word2_list = []
    for row in word_list:
        word1_list.append(row.get('word1'))
        recordWord.append(row.get('word1'))
        word2_list.append(row.get('word2'))
        recordWord.append(row.get('word2'))

    random.shuffle(word1_list)
    if len(word1_list)!=0:
        word1 = word1_list[0]
    else:
        word1 = "故事"
    random.shuffle(word2_list)
    if len(word2_list)!=0:
        word2 = word2_list[0]
    else:
        word2 = "生活"


    for wordOne in recordWord:
        w[0] += float(df[df["word"]=="{}".format(wordOne)]["v1"])
        w[1] += float(df[df["word"]=="{}".format(wordOne)]["v2"])
        w[2] += float(df[df["word"]=="{}".format(wordOne)]["v3"])

    if len(recordWord)!=0:
        w[0] = w[0]/len(recordWord)
        w[1] = w[1]/len(recordWord)
        w[2] = w[2]/len(recordWord)
    else:
        pass

    return w,word1,word2

def zongweidu(q,z,w):
    weidu = [0,0,0]
    # 总维度
    for i in range(3):
        # weidu[i] = float(format((q[i]*0.4 + z[i]*0.5 + w[i]*0.7), '.2f')) 
        weidu[i] = float(format((q[i] + z[i] + w[i]), '.2f')) 

    # 人格 + 称号
    if weidu[0] >= 0 and weidu[1] >= 0 and weidu[2] >= 0:
        renge = 0
        chenghao = ZZZ[random.randint(0,2)]
    elif weidu[0] >= 0 and weidu[1] >= 0 and weidu[2] < 0:
        renge = 1
        chenghao = ZZF[random.randint(0,2)]
    elif weidu[0] >= 0 and weidu[1] < 0 and weidu[2] < 0:
        renge = 2
        chenghao = ZFF[random.randint(0,2)]
    elif weidu[0] < 0 and weidu[1] < 0 and weidu[2] < 0:
        renge = 3
        chenghao = FFF[random.randint(0,2)]
    elif weidu[0] < 0 and weidu[1] < 0 and weidu[2] >= 0:
        renge = 4
        chenghao = FFZ[random.randint(0,2)]
    elif weidu[0] < 0 and weidu[1] >= 0 and weidu[2] >= 0:
        renge = 5
        chenghao = FZZ[random.randint(0,2)]
    elif weidu[0] >= 0 and weidu[1] < 0 and weidu[2] >= 0:
        renge = 6
        chenghao = ZFZ[random.randint(0,2)]
    elif weidu[0] < 0 and weidu[1] >= 0 and weidu[2] < 0:
        renge = 7
        chenghao = FZF[random.randint(0,2)]

    return weidu,renge,chenghao

def shengcheng(RFID):
    q,z,postime = quyuDianzan(RFID)
    w,word1,word2 = quci(RFID)
    weidu,renge,chenghao = zongweidu(q,z,w)
    userText = text_list[random.randint(0,9)]
    musicId = random.randint(0,15)
    return weidu,renge,chenghao,word1,word2,userText,musicId,postime

def shagnchaun_zuizhong(rfid): # 上传信息到云数据库
    weidu,renge,chenghao,word1,word2,userText,musicId,postime = shengcheng(rfid)
    print(postime)
    c = OBJ_final()

    c.set("nickName",chenghao)
    c.set("RFID",rfid)
    postime_str = json.dumps(postime)
    print(postime_str)
    c.set("posData",postime_str)
    userText_str = json.dumps(userText)
    c.set("userText",userText_str)
    c.set("userType",renge)
    c.set("v1",weidu[0])
    c.set("v2",weidu[1])
    c.set("v3",weidu[2])
    c.set("word1",word1)
    c.set("word2",word2)
    c.set("musicId",musicId)
    c.save()

def chuangeState(RFID):
    shagnchaun_zuizhong(RFID)
    state = OBJ_state.query
    state.equal_to('RFID', '{}'.format(RFID))
    statelist = state.find()
    for row in statelist:
        objectId = row.id

    stateChange = OBJ_state.create_without_data(objectId)
    stateChange.set('isFinished', True)
    stateChange.save()

class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            conn = self.request
            data = conn.recv(1024)
            ReadList =  tiqu2(data)
            jiance(ReadList)
if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('192.168.1.100',8080), MyServer)
    ip, port = server.server_address
    print (ip, port)
    server.serve_forever()