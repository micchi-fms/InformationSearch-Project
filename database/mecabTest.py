import MeCab
#辞書を指定する
t = MeCab.Tagger()
print(t.parse("特急はくたか"))