import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

docs = np.array([
        '牛乳        を 買う',
        'パン         を 買う',
        'パン         を 食べる',
        'お菓子       を 食べる',
        '本           を 買う',
        'パン と お菓子 を 食べる',
        'お菓子        を 買う',
        'パン と パン   を 食べる'
        ])

#
# ベクトル化
#
vectorizer = TfidfVectorizer(use_idf=True, token_pattern=u'(?u)\\b\\w+\\b')
vecs = vectorizer.fit_transform(docs)

print(vecs.toarray())
#-----------------------------------------------------
# [[ 0.    0.    0.32  0.    0.    0.8   0.51  0.  ]
#  [ 0.    0.    0.41  0.65  0.    0.    0.65  0.  ]
#  [ 0.    0.    0.41  0.65  0.    0.    0.    0.65]
#  [ 0.69  0.    0.38  0.    0.    0.    0.    0.61]
#  [ 0.    0.    0.32  0.    0.8   0.    0.51  0.  ]
#  [ 0.49  0.57  0.27  0.43  0.    0.    0.    0.43]
#  [ 0.69  0.    0.38  0.    0.    0.    0.61  0.  ]
#  [ 0.    0.49  0.24  0.75  0.    0.    0.    0.37]]
#-----------------------------------------------------


#
# クラスタリング
#
clusters = KMeans(n_clusters=2, random_state=0).fit_predict(vecs)
for doc, cls in zip(docs, clusters):
    print( cls, doc)

#----------------------------
# 0 - 牛乳        を 買う
# 0 - パン         を 買う
# 1 - パン         を 食べる
# 1 - お菓子       を 食べる
# 0 - 本           を 買う
# 1 - パン と お菓子 を 食べる
# 0 - お菓子        を 買う
# 1 - パン と パン   を 食べる
#----------------------------