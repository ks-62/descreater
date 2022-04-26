from natto import MeCab

mc = MeCab()
text = "私は昨日ラーメンを食べました。"

print(mc.parse(text))

print ('Input text:\n'+text)

print('====================================================')

# -F / --node-format オプションでノードの出力フォーマットを指定する
#
# %m    ... 形態素の表層文
# %f[0] ... 品詞
# %h    ... 品詞 ID (IPADIC)
# %f[8] ... 発音
#
words = []
with MeCab('-F%m,%f[0],%h') as nm:
    for n in nm.parse(text, as_nodes=True):
        node = n.feature.split(',');
        if len(node) != 3:
            continue
        if node[1] == '名詞':
            # if True:
            words.append(node[0])
print(words)