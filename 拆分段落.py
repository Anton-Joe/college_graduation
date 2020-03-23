
import jieba
import jieba.posseg as pseg
import pymysql
import re
import time


def getContentList():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='565648923z1',
                                 db='ctrip',
                                 charset='utf8mb4')
    cur = connection.cursor()
    sql = """
        select content, userGiveScore, hotelid from hotelContent where hotelID in (
        select distinct hotelid from hotelFinalList where hotelScore > 3.5 
        and hotelSumComment >= 50 
        and hotelenvironment >= 3.5
        and hotelequipment >= 3.3
        and hotelservice >= 3.6
        and hotelhealth >= 3.5
        and hotelRecommend2 >= 72
        )
        """
    cur.execute(sql)
    result = cur.fetchall()
    # return [content for (content,) in result]
    return result

def get_sub_content(content):
    # 分段，将每一条评论分成很多段，以， 。 ? ! 、 进行分割。
    # 分段目的：找出句子中的名词短句
    break_word = [',', '。', '!', '?', '、', '，', '和']
    sub_contents = []
    start_index = 0
    end_index = 0
    for index, word in enumerate(content):
        if word in break_word:
            end_index = index
            sub_contents.append(content[start_index:end_index])
            start_index = index + 1
            continue
        elif index == len(content) - 1:
            sub_contents.append(content[start_index:end_index + 2])
        else:
            end_index = end_index + 1
    return sub_contents


def build_new_sub_content(sub_content):
    cut_content_word_list = pseg.cut(sub_content, use_paddle=True)
    new_content_list = []
    for word, flag in cut_content_word_list:
        new_content_list.append(word)
        new_content_list.append(flag)
    return ''.join(new_content_list)



# ORG用于删除

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

all_contents = getContentList()

for content, score, hotelid in all_contents:
    print("当前评论：{content}".format(content=content))
    print("用户评分：{score}".format(score=score))
    print("酒店ID：{id}".format(id=hotelid))
    sub_contents = get_sub_content(content)
    print(sub_contents)
    for sub_content in sub_contents:
        # time.sleep(2)
        pattern = '[\u4e00-\u9fa5]+[n]'
        new_Str = build_new_sub_content(sub_content)
        m = re.findall(pattern, new_Str)
        if len(m) != 0:
            for title in m:
                title = re.sub('[a-zA-Z]', '', title)
                new_Str = re.sub('[a-zA-Z]', '', new_Str)
                print("捕捉到名词：{word}".format(word=title))
                print('即将插入名词对应断句与评分：{strd}'.format(strd=new_Str))
                connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='565648923z1',
                                             db='ctrip',
                                             charset='utf8mb4')
                cur = connection.cursor()
                sql = "INSERT INTO keywordlistwithID2 VALUES ('{word}','{content}','{score}','{id}')".format(word=title, content=new_Str, score=score, id=hotelid)
                print(sql)
                try:
                    cur.execute(sql)
                except:
                    continue
                connection.commit()
                connection.close()
        else:
            print("没有捕捉到名词类主题")
    print('')