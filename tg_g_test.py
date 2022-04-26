# import treetaggerwrapper as ttw

# def main():
#     tagger = ttw.TreeTagger(TAGLANG='en')
#     tags = tagger.TagText('I have a pen.')
#     print(tags)

# if __name__ == '__main__':
#     main()

import json
import treetaggerwrapper
# tagger = treetaggerwrapper.TreeTagger(TAGLANG='en',TAGDIR='/Applications/XAMPP/xamppfiles/htdocs/NLP_test/')
tagger = treetaggerwrapper.TreeTagger(TAGLANG='de',TAGDIR='/Applications/XAMPP/xamppfiles/htdocs/NLP_test/')
tags = tagger.TagText("In Japan haben die Leute ein Klavier.")

# jsonファイル読み込み
json_open = open('data/words.json', 'r')
json_load = json.load(json_open)

ori_words = []

s_person = ""
sentence = ""
s_fore = ""
s_verb = ""
s_back = ""

for tag in tags:

    print(tag)
    l_word = tag.split("\t")[0]
    p_word = tag.split("\t")[1]
    o_word = tag.split("\t")[2]

    # 人称を決める
    if p_word == "PPER":
        s_person = json_load['person'][o_word]
        if s_person == "":
            s_person = "s_3"
            

    # 動詞変化
    if(p_word == "VVFIN"):
        s_verb = o_word

    else:
        if s_verb != "":
            if l_word != ".":
                s_back = " " + s_back + l_word
            else:
                s_back += l_word
        elif s_verb == "":
            if l_word != ".":
                s_fore = " " + s_fore + l_word
            else:
                s_fore += l_word


s_v_form = " " + json_load[s_verb]['indicative_pst'][s_person]

sentence = s_fore + s_v_form + s_back

print(s_person)
print(s_fore)
print(s_verb)
print(s_back)
print(sentence.lstrip())

#1.Ichなどの単語を探す。
#2.主格の定冠詞を探す。
    #2-2.(女性名詞と中性)1格と2格が同じ形。

#3.定冠詞がなく、主格がわからない場合。
#4.形容詞などが名詞化している場合。
#5.節が主語になっている場合