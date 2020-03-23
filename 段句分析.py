import time

import jieba
import csv
import pymysql


# 加载停用词
stopWordCsv = csv.reader(open('/Users/yejingxuan/downloads/python毕业论文材料/停用词.csv', encoding='utf-8-sig'))
stopWordList = []
for row in stopWordCsv:
    stopWordList.append(row[0])

# # 删除停用词
# for word in segList:
#     if word in stopWordList:
#         segList.remove(word)
# print('删除停用词之后的分词个数 = {count}'.format(count=len(segList)))

# 加载否定词, 暂时手动输入
notWordList = ['不', '没', '无', '非', '莫', '弗', '勿', '毋', '未', '否', '别', '無', '休', '难道', '不怎么', '没有', '得不到', '除非', '不是']

# 加载情感词
emotionCsv = csv.reader(open('/Users/yejingxuan/downloads/python毕业论文材料/情感词.csv', encoding='utf-8-sig'))
emotionDic = {}
for row in emotionCsv:
    emotionDic[row[0]] = row[1]

# 加载正面评价词
posCsv = csv.reader(open('/Users/yejingxuan/downloads/python毕业论文材料/正面评价词.csv', encoding='utf-8-sig'))
posList = []
for row in posCsv:
    posList.append(row[0].strip())
posList.append('好')
posList.append('满意')
posList.append('周到')
posList.append('不错')
posList.append('安全感')
posList.append('保障')
posList.append('近')

# 需要删掉五星级！！！！！！！！！！！！！！！！
# 删掉贵

# 加载负面评价词
negCsv = csv.reader(open('/Users/yejingxuan/downloads/python毕业论文材料/负面评价词.csv', encoding='utf-8-sig'))
negList = []
for row in negCsv:
    negList.append(row[0].strip())
negList.append('没有')
negList.append('坑')
negList.append('差')
negList.append('旧')
negList.append('坏的')
negList.append('异味')
negList.append('吵')
negList.append('业余')
negList.append('臭')
negList.append('不值得')
negList.append('不值')
negList.append('不好')
negList.append('很差')
negList.append('垃圾')
negList.append('不能')
negList.append('差评')
negList.append('烟味')
negList.append('污渍')
negList.append('贵')
negList.append('远')
negList.append('有味道')
negList.append('极差')
negList.append('太差')
negList.append('杂音')
# 删除地下！！！！！！
jieba.add_word('热情', tag='a')
jieba.add_word('位置', tag='n')
jieba.add_word('预定', tag='n')
jieba.add_word('卫生', tag='n')
jieba.add_word('不值', tag='v')
jieba.add_word('齐全', tag='a')
jieba.add_word('也', tag='ORG')
jieba.add_word('服务态度', tag='n')
jieba.add_word('隔音', tag='n')
jieba.add_word('房间隔音', tag='n')
jieba.add_word('安静', tag='a')
jieba.add_word('无语')
jieba.add_word('有味道')
jieba.add_word('极')
jieba.add_word('最')
jieba.add_word('太')
jieba.add_word('太多')
jieba.add_word('混乱')
jieba.add_word('房间隔音')
jieba.add_word('感觉', tag='v')
jieba.add_word('无语')
jieba.add_word('有味道')
jieba.add_word('极')
jieba.add_word('最')
jieba.add_word('太')
jieba.add_word('太多')
jieba.add_word('混乱')
jieba.add_word('房间隔音')
jieba.add_word('无语')
jieba.add_word('有味道')
jieba.add_word('极')
jieba.add_word('最')
jieba.add_word('太')
jieba.add_word('太多')
jieba.add_word('混乱')
jieba.add_word('房间隔音')
jieba.add_word('小姐姐')
jieba.add_word('小哥哥')


# 加载程度副词
degreeCsv = csv.reader(open('/Users/yejingxuan/downloads/python毕业论文材料/程度词.csv', encoding='utf-8-sig'))
degreeDic = {}
for row in degreeCsv:
    degreeDic[row[0]] = row[1]


def handleContent(keyword, content, sccore, id):

    # 分词
    seg_list = jieba.lcut(content, cut_all=False)

    # 删除停用词，停用词有点问题，暂时注销
    # for word in segList:
    #     if word in stopWordList:
    #         segList.remove(word)
    # print('删除停用词之后的分词个数 = {count}'.format(count=len(segList)))


    # 处理当前评论
    # 遍历每一个word，判断word类型（属于否定词 or 正面词 or 负面词），并记录这个word在分词list中的位置
    # 创建三个字典，用于记录位置
    contentNotWordDic = {}
    contentPosDic = {}
    contentNegDic = {}
    keyword_index = 0
    for index, word in enumerate(seg_list):
        if word in notWordList and word not in posList and word not in negList:
            contentNotWordDic[word] = index
        elif word in posList:
            contentPosDic[word] = index
        elif word not in notWordList and word not in posList and word in negList:
            contentNegDic[word] = index
        elif word == keyword:
            keyword_index = index

    score = 0
    diver_flag = 1
    degree_flag = 1

    print("当前段落名词:{a}".format(a=keyword))
    print("当前段落原句:{b}".format(b=content))

    print("正观词典：{d}".format(d=contentPosDic))
    print("负面词典：{d}".format(d=contentNegDic))

    # 遍历正面词
    for word in contentPosDic:
        # 排除类似于 卫生 为关键词 且 卫生为正面词的情况
        if word == keyword:
            break
        if keyword_index != contentPosDic[word]:
            a = 0
            b = 0
            if keyword_index < contentPosDic[word]:
                a = keyword_index
                b = contentPosDic[word]
            else:
                a = contentPosDic[word]
                b = keyword_index
            # 遍历主题与正面次中间的分词，查看是否有程度词
            for i in range(a+1, b):
                word = seg_list[i]
                if word in notWordList:
                    diver_flag = diver_flag * -1
                elif word in degreeDic.keys():
                    degree_flag = degree_flag * float(degreeDic[word])
        score = float(1 * degree_flag) + float(score)
        score = diver_flag * score
        diver_flag = 1



    # for word in contentNegDic:
    #     jude_not_word_index = contentNegDic[word] - 1
    #     word_score = -1
    #     if jude_not_word_index in contentNotWordDic.values():
    #         word_score = word_score * -1
    #     score = word_score + score

    count = 0
    for word in contentNegDic:
        if word == keyword:
            score = 0
            break
        if count == 0 and score > 0:
            score = 0
            count = count + 1
        if keyword_index != contentNegDic[word]:
            a = 0
            b = 0
            if keyword_index < contentNegDic[word]:
                a = keyword_index
                b = contentNegDic[word]
            else:
                a = contentNegDic[word]
                b = keyword_index
            # 遍历主题与正面次中间的分词，查看是否有程度词
            for i in range(a + 1, b):
                word = seg_list[i]
                if word in notWordList:
                    diver_flag = diver_flag * -1
                elif word in degreeDic.keys():
                    degree_flag = degree_flag * float(degreeDic[word])
        score = float(-1 * degree_flag) + float(score)
        score = diver_flag * score
        diver_flag = 1
    print("分词效果：{list}".format(list=seg_list))
    print("翻转标志：{d}".format(d=diver_flag))
    print("程度得分：{d}".format(d=degree_flag))




    print("当前段落句得分:{score}".format(score=score))
    content = str(content).replace("'",'')

    sql = "INSERT INTO keyWordListScorewithid2 VALUES ('{word}','{sub_content}','{content_score}','{sub_content_score}', '{id}')".format(word = keyword, sub_content=content, content_score=sccore, sub_content_score=score, id=id)
    print(sql)
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='565648923z1',
                                 db='ctrip',
                                 charset='utf8mb4')
    cur = connection.cursor()
    cur.execute(sql)
    connection.commit()
    connection.close()



connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='565648923z1',
                                 db='ctrip',
                                 charset='utf8mb4')
cur = connection.cursor()
sql = "select word , wordwar ,score, hotelid from keywordlistwithID2 where LENGTH(wordwar) < 30 "
# sql = "SELECT word , wordwar ,score, hotelid FROM keywordlistwithID2 WHERE wordwar='价格不是很贵' LIMIT 10"
cur.execute(sql)
hotelContent = cur.fetchall()
connection.close()
print(hotelContent)
for (keyword, sub_content, score, id) in hotelContent:
    handleContent(keyword, sub_content, score, id)
    print('')
#
# handleContent('差劲','实在太差劲了','5')
#
# handleContent('差评','差评 前台换了临时位置也不告知 不打电话都不知道在哪办理入住 第二天早晨不到6点就有人敲门  竟然安排了别人来入住我的房间 一大早就被吵醒 睡意全无 最可笑的是起来洗澡竟然没有热水 什么玩意','5')
#
