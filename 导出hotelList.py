import pymysql
import csv
connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='565648923z1',
    db='ctrip',
    charset='utf8mb4')
cur = connection.cursor()
sql = "select * from hotelFinalList"
cur.execute(sql)
result = cur.fetchall()

with open('/Users/yejingxuan/Desktop/毕业论文/hotelFinalList.csv', 'w+', encoding='utf-8-sig') as f:
    for row in result:
        writer = csv.writer(f)
        writer.writerow(row)