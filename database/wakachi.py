#!/usr/bin/env python
# -*- coding:utf-8 -*-
import mysql.connector
import configparser
import MeCab
import numpy as np
from multiprocessing import Pool
import multiprocessing as multi
import pandas as pd


config = configparser.ConfigParser()
# 設定ファイルを読み込み
config.read('config.ini')

#databese
conn = mysql.connector.connect(
    host = config['detabase_server']['host'],
    port = config['detabase_server']['port'],
    user = config['detabase_server']['user'],
    password = config['detabase_server']['password'],
    database = config['detabase_server']['database'],
)

conn.ping(reconnect=True)
cursor = conn.cursor()


### MySQL上のデータ取得用関数
def fetch_target_day_n_random(target_day, n = 2000):
    sql = 'select dialogue from origin partition (p%s) where date_format(date, "%Y") = "%s";'
    cursor.execute(sql, [target_day,target_day])
    result = cursor.fetchall()
    l = [x[0] for x in result]
    return l
 
### MeCab による単語への分割関数 (名詞のみ残す)
tagger = MeCab.Tagger()
def split_text_only_noun(text):
 
    words = []
    for chunk in tagger.parse(text).splitlines()[:-1]:
        (surface, feature) = chunk.split('\t')
        if feature.startswith('名詞'):
            # print(surface)
            words.append(surface)
    return " ".join(words)


 
### メイン処理
docs_count = 20 # 取得数
target_days = [
    2000,
    2001,
    2002,
    2003,
    2004,
    2005,
    2006,
    2007,
    2008,
    2009,
    2010,
    2011,
    2012,
    2013
]

data_frame = pd.DataFrame(index=[], columns=['date', 'wakachi'])
# target_day_nouns = []
for target_day in target_days:
    print(target_day)
    # MySQL からのデータ取得
    txts = fetch_target_day_n_random(target_day, docs_count)
    print('並列処理するよ')
    p = Pool(multi.cpu_count())
    each_nouns=p.map(split_text_only_noun, txts)
    p.close()

    all_nouns = " ".join(each_nouns)
    print(all_nouns)
    series = pd.Series([target_day, all_nouns], index=data_frame.columns)
    data_frame = data_frame.append(series, ignore_index = True)

data_frame.to_csv("wakachi6.csv", index=False,header=True)#書き出し
