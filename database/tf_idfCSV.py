import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

### TF-IDF の結果からi 番目のドキュメントの特徴的な上位 n 語を取り出す
def extract_feature_words(terms, tfidfs, i, n):
    tfidf_array = tfidfs[i]
    top_n_idx = tfidf_array.argsort()[-n:][::-1]
    words = [terms[idx] for idx in top_n_idx]
    return words
###空白を境目にしてる
def extract_feature_words_string(terms, tfidfs, i, n):
    tfidf_array = tfidfs[i]
    top_n_idx = tfidf_array.argsort()[-n:][::-1]
    words = [terms[idx] for idx in top_n_idx]
    words_string = " ".join(words)
    return words_string

filename = pd.read_csv('wakachi6.csv')

ldate = []
lwakachi = []

ldate =  filename['date']
lwakachi =  filename['wakachi']

#追加
tokuchou = []

tfidf_vectorizer = TfidfVectorizer(
    use_idf=True,
    lowercase=False,
    max_df=6,
    sublinear_tf=True
)
tfidf_matrix = tfidf_vectorizer.fit_transform(lwakachi)

# index 順の単語のリスト
terms = tfidf_vectorizer.get_feature_names()
# TF-IDF 行列 (numpy の ndarray 形式)
tfidfs = tfidf_matrix.toarray()

data_frame = pd.DataFrame(index=[], columns=['date_year', 'tokuchou'])

for i in range(0, len(ldate)):
    print("\n------------------------------------------")
    print(ldate[i])
    stokens=extract_feature_words_string(terms, tfidfs, i, 20)
    print(stokens)
    # for x in  extract_feature_words(terms, tfidfs, i, 20):
    #     print(x),

    #     tokuchou.append(x)　#追加
    #     tokuchou_str = " ".join(tokuchou)　#追加

    series = pd.Series([ldate[i], stokens], index=data_frame.columns)
    data_frame = data_frame.append(series, ignore_index = True)

#csv書き出し
data_frame.to_csv("tokuchou.csv", index=False, mode='a', header=False)#追記
# data_frame.to_csv("tokuchou.csv", index=False,header=True)#書き出し
