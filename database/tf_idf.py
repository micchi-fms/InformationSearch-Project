#!/usr/bin/env python
# -*- coding:utf-8 -*-
import mysql.connector
import configparser
import MeCab
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.externals.joblib import Parallel, delayed
# from joblib import Parallel, delayed
from multiprocessing import Pool
import multiprocessing as multi


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
    # sql = 'select dialogue from origin where date_format(date, "%Y") = %s;'
    cursor.execute(sql, [target_day,target_day])
    result = cursor.fetchall()
    l = [x[0] for x in result]
    print(l)
    return l
 
### MeCab による単語への分割関数 (名詞のみ残す)
tagger = MeCab.Tagger()
def split_text_only_noun(text):
#    tagger.parse("")
    #text_str = text.encode('utf-8') # str 型じゃないと動作がおかしくなるので変換
#    node = tagger.parseToNode(text)
 
    words = []
    # while node:
    #     pos = node.feature.split(",")[0]
    #     if pos == "名詞":
    #         # unicode 型に戻す
    #         #word = node.surface.decode("utf-8")
    #         print(node.surface)
    #         words.append(node.surface)
    #     node = node.next
    for chunk in tagger.parse(text).splitlines()[:-1]:
        (surface, feature) = chunk.split('\t')
        if feature.startswith('名詞'):
            # print(surface)
            words.append(surface)
    return " ".join(words)
 
### TF-IDF の結果からi 番目のドキュメントの特徴的な上位 n 語を取り出す
def extract_feature_words(terms, tfidfs, i, n):
    tfidf_array = tfidfs[i]
    top_n_idx = tfidf_array.argsort()[-n:][::-1]
    words = [terms[idx] for idx in top_n_idx]
    return words
 
### メイン処理
docs_count = 20 # 取得数
target_days = [
    1947,
    1948,
    1949,
    1950
]

target_day_nouns = []
for target_day in target_days:
    print(target_day)
    # MySQL からのデータ取得
    txts = fetch_target_day_n_random(target_day, docs_count)
    # 名詞のみ抽出
    # each_nouns = [split_text_only_noun(txt) for txt in txts]
    # each_nouns = Parallel(n_jobs=-1, pre_dispatch='all')(delayed(split_text_only_noun)(txt) for txt in txts)
    print('並列処理するよ')
    p = Pool(multi.cpu_count())
    each_nouns=p.map(split_text_only_noun, txts)
    p.close()

    # each_nouns = Parallel(n_jobs=2)(delayed(split_text_only_noun)(txt) for txt in txts)
    all_nouns = " ".join(each_nouns)
    print(all_nouns)
    target_day_nouns.append(all_nouns)
 
# TF-IDF 計算
# (合計6日以上出現した単語は除外)
tfidf_vectorizer = TfidfVectorizer(
    use_idf=True,
    lowercase=False,
    max_df=6
)
tfidf_matrix = tfidf_vectorizer.fit_transform(target_day_nouns)
 
# index 順の単語のリスト
terms = tfidf_vectorizer.get_feature_names()
# TF-IDF 行列 (numpy の ndarray 形式)
tfidfs = tfidf_matrix.toarray()
 
# 結果の出力
for i in range(0, len(target_days)):
    print("\n------------------------------------------")
    print(target_days[i])
    for x in  extract_feature_words(terms, tfidfs, i, 10):
        print(x),
 