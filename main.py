import datetime
import os
import xml.etree.ElementTree as ET

import urllib.parse
import requests
import tweepy

bearer_token = os.environ['BEARER_TOKEN']

Client = tweepy.Client(bearer_token)

# 前回の実行時刻を取得

tree = ET.parse(urllib.request.urlopen(url= 'https://denpayanara.github.io/Tweet_Get/before_datetime.xml'))

root = tree.getroot()

before_datetime = root.text

# ツイートを取得
# 時刻表記: YYYY-MM-DDTHH:mm:ssZ
tweets = Client.search_recent_tweets(
    query = '楽天モバイル 奈良 -from:ZSCCli0y6RMxYmU -from:rakuten_travel2 -retweets',
    start_time = before_datetime,
    tweet_fields = ['text', 'author_id'],
    expansions = ['author_id'],
    user_fields=["username"]
    )

def GetTweet(tweet_id):
    # メソッド実行
    GetTwt = Client.get_tweet(id=tweet_id, expansions=["author_id"], user_fields=["username"])

    # 結果加工
    twt_result = {}
    twt_result["tweet_id"] = tweet_id
    twt_result["user_id"]  = GetTwt.includes["users"][0].id
    twt_result["username"] = GetTwt.includes["users"][0].username
    twt_result["text"]     = GetTwt.data
    twt_result["url"]      = "https://twitter.com/" + GetTwt.includes["users"][0].username + "/status/" + str(tweet_id)

    # 結果出力
    return twt_result

get_tweet = []

if tweets.data != None:

    for tweet in tweets.data:

        tweet_id = tweet.id
        get_tweet.append(GetTweet(tweet_id))

send_message = '【新着ツイートあり】\n'

for i, get_teet_2 in enumerate(get_tweet):

    text = get_teet_2['text']['text']
    url = get_teet_2['url']
    send_message += f'【{i+1}件目】\n{text}\n{url}\n\n'

if not get_tweet:
    
    print('更新なし')

else:
    # 新着ツイートをLINEに送信

    Line_Token = os.environ['LINE_TOKEN']

    token_dic = {'Authorization': 'Bearer' + ' ' + Line_Token}

    send_dic = {'message': send_message} 

    r = requests.post(
        'https://notify-api.line.me/api/notify',
        headers = token_dic,
        data = send_dic
        )

# 現在のdatetimeを取得し保存(UTC)
now = datetime.datetime.utcnow()

date_time = now.strftime('%Y-%m-%dT%H:%M:00Z')

f = open('data/before_datetime.xml', 'w', encoding='UTF-8')

f.write(f'<?xml version="1.0" encoding="UTF-8" ?><date>{date_time}</date>')

f.close()
