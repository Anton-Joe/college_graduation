import pymysql
import csv
import json


connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='565648923z1',
    db='ctrip',
    charset='utf8mb4')
cur = connection.cursor()
sql = r"SELECT word, hotelid, sub_content_score FROM keyWordListScorewithid2 "
cur.execute(sql)
result = cur.fetchall()

hotel_info = {}
hotel_json = json.loads(json.dumps(hotel_info))

word_list = [
    '房间', '卫生', '环境', '位置', '交通', '性价比', '设施', '前台', '服务态度', '早餐', '价格', '隔音', '床', '地铁站', '地理位置', '地铁', '态度'
]
csv_first_row_list = [
    '房间', '卫生', '环境', '位置', '交通', '性价比', '设施', '前台', '早餐', '价格', '隔音', '床', '态度', '地铁'
]

for word, hotelid, score in result:
    if word in word_list:
        if word in ['地铁站', '地铁']: word = '地铁'
        if word in ['态度', '服务态度']: word = '态度'
        if word in ['位置', '地理位置']: word = '位置'

        if hotelid not in hotel_json.keys():
            # 当json中没有这一个酒店的时候
            json = {
                    '房间': {'count': 0, 'score': 0},
                    '卫生': {'count': 0, 'score': 0},
                    '环境': {'count': 0, 'score': 0},
                    '位置': {'count': 0, 'score': 0},
                    '交通': {'count': 0, 'score': 0},
                    '性价比': {'count': 0, 'score': 0},
                    '设施': {'count': 0, 'score': 0},
                    '前台': {'count': 0, 'score': 0},
                    '早餐': {'count': 0, 'score': 0},
                    '价格': {'count': 0, 'score': 0},
                    '隔音': {'count': 0, 'score': 0},
                    '床': {'count': 0, 'score': 0},
                    '态度': {'count': 0, 'score': 0},
                    '地铁': {'count': 0, 'score': 0}
                }
            hotel_json[hotelid] = json

        count = int(hotel_json[hotelid][word]['count'])
        count = count + 1
        score = float(hotel_json[hotelid][word]['score']) + score
        hotel_json[hotelid][word]['count'] = str(count)
        hotel_json[hotelid][word]['score'] = str(score)

    else:
        continue


for hotelID in hotel_json.keys():
    for word in hotel_json[hotelID].keys():
        if hotel_json[hotelID][word]['count'] != 0:
            hotel_json[hotelID][word]['score'] = str(float(hotel_json[hotelID][word]['score']) / float(hotel_json[hotelID][word]['count']))

# print(hotel_json)
file_path = '/Users/yejingxuan/Desktop/毕业论文/转置得分测试.csv'

with open(file_path, 'w+',encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(csv_first_row_list)
    for hotelID in hotel_json.keys():
        row = []
        row.append(hotelID)
        for word in csv_first_row_list:
            if int(hotel_json[hotelID][word]['count']) :
                row.append(hotel_json[hotelID][word]['score'])
            else:
                row.append('0')
        print(row)

        writer.writerow(row)

