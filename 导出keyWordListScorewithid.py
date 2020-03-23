import pymysql
import csv
connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='565648923z1',
    db='ctrip',
    charset='utf8mb4')
cur = connection.cursor()
sql = "select * from keyWordListScorewithid2"
cur.execute(sql)
result = cur.fetchall()

with open('/Users/yejingxuan/Desktop/毕业论文/keyWordListScorewithid2.csv', 'w+', encoding='utf-8-sig') as f:
    for row in result:
        print(row)
        writer = csv.writer(f)
        writer.writerow(row)