import datetime

# 今日の日付を取得
now = datetime.datetime.utcnow() + datetime.timedelta(hours = 9)
date_time = now.strftime('%Y-%m-%dT%H:%M:00Z')

# 現在の時刻をXMLファイルに書き込み保存
f = open('data/before_datetime.xml', 'w', encoding='UTF-8')

f.write(f'<?xml version="1.0" encoding="UTF-8" ?><date>{date_time}</date>')

f.close()
