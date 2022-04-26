import sys
import json
import spacy
import treetaggerwrapper

# arg:文章と時制
# 1 現在 indicative_cur
# 2 過去 indicative_pst
# 3 現在完了 aux + past_participle
# 4 過去完了 aux + past_participle
# 5 未来 werden + original
# 6 未来完了 werden + past_participle + aux
# 7 接続法1式 subjunctive_1
    # 7a 間接話法(誰かから聞いた話。〜が言ってたよ)
    # 7b 要求話法(願望や要求を表す。)
# 8 接続法2式 subjunctive_2
    # 8a 仮定話法(仮定や願望)
    # 8b 婉曲話法(丁寧なお願い)
def main(arg_text, arg_s_form):
    # 文体
    s_form = ""
    # 時制
    s_tens = ""
    # 人称
    s_person = ""
    # 文章動詞以前
    s_fore = ""
    # 動詞
    s_verb = ""
    # 文章動詞以後
    s_back = ""
    # 変化した動詞
    s_v_form = ""
    # 助動詞
    s_aux = ""
    # 変化後助動詞
    s_a_form = ""

    #jsonファイル取得
    json_open = open('data/words.json', 'r')
    json_load = json.load(json_open)

    #文情報取得
    # "v_form": "",
    #  "aux": "",
    #  "tens": "",
    #  "wrdn_aux": ""
    s_inf = de_sentence_form(arg_s_form)

    #入力文解析
    #  "r_s_person": s_person,
    #  "r_s_fore": s_fore,
    #  "r_s_verb": s_verb,
    #  "r_s_back": s_back
    input_inf = get_input_inf(arg_text)

    #助動詞が必要な場合
    if s_inf["aux"] == "auxiliary_verb":
        # 助動詞取得
        s_aux = json_load[input_inf["r_s_verb"]][s_inf["aux"]]
        s_a_form = ' ' + json_load[s_aux][s_inf["tens"]][input_inf["r_s_person"]]
        # 動詞
        s_v_form = ' ' + json_load[input_inf["r_s_verb"]]["past_participle"]
        print(s_v_form)

        #完成文
        input_inf["r_s_back"] = input_inf["r_s_back"].strip(".")
        sentence = input_inf["r_s_fore"] + s_a_form + input_inf["r_s_back"] + s_v_form + "."
        sentence = sentence.lstrip()

    elif s_inf["aux"] == "werden":
        # 助動詞
        s_aux = s_inf["aux"]
        s_a_form = ' ' + json_load[s_aux][s_inf["tens"]][input_inf["r_s_person"]]
        # 動詞
        s_v_form = ' ' + json_load[input_inf["r_s_verb"]]["past_participle"]
        if s_inf["wrdn_aux"] == "true":
            w_aux = ' ' + json_load[input_inf["r_s_verb"]]["auxiliary_verb"]
            s_v_form += w_aux

        #完成文
        input_inf["r_s_back"] = input_inf["r_s_back"].strip(".")
        sentence = input_inf["r_s_fore"] + s_a_form + input_inf["r_s_back"] + s_v_form + "."
        sentence = sentence.lstrip()

    else:
        s_inf["v_form"]
        s_v_form = ' ' + json_load[input_inf["r_s_verb"]][s_inf["v_form"]][input_inf["r_s_person"]]

        #完成文
        sentence = input_inf["r_s_fore"] + s_v_form + input_inf["r_s_back"]
        sentence = sentence.lstrip()

    print(sentence)
    return sentence
        

#文情報取得
def de_sentence_form(n):
    dct_s_inf = {}
    if n == "1":
        # 現在
        dct_s_inf = {
            "v_form": "indicative_cur",
            "aux": "false",
            "tens": "indicative_cur",
            "wrdn_aux": "false"
        }
        
        return dct_s_inf
    elif n == "2":
        # 過去
        dct_s_inf = {
            "v_form": "indicative_pst",
            "aux": "false",
            "tens": "indicative_pst",
            "wrdn_aux": "false"
        }
        return dct_s_inf
    elif n == "3":
        # 現在完了
        dct_s_inf = {
            "v_form": "past_participle",
            "aux": "auxiliary_verb",
            "tens": "indicative_cur",
            "wrdn_aux": "false"
        }
        return dct_s_inf
    elif n == "4":
        # 過去完了
        dct_s_inf = {
            "v_form": "past_participle",
            "aux": "auxiliary_verb",
            "tens": "indicative_pst",
            "wrdn_aux": "false"
        }
        return dct_s_inf
    elif n == "5":
        # 未来
        dct_s_inf = {
            "v_form": "original",
            "aux": "werden",
            "tens": "indicative_cur",
            "wrdn_aux": "false"
        }
        return dct_s_inf
    elif n == "6":
        # 未来完了
        dct_s_inf = {
            "v_form": "past_participle",
            "aux": "werden",
            "tens": "indicative_cur",
            "wrdn_aux": "true"
        }
        return dct_s_inf
    elif n == "7":
        # 接続法1式
        dct_s_inf = {
            "v_form": "subjunctive_1",
            "aux": "false",
            "tens": "false",
            "wrdn_aux": "false"
        }
        return dct_s_inf
    elif n == "8":
        # 接続法2式
        dct_s_inf = {
            "v_form": "subjunctive_2",
            "aux": "false",
            "tens": "false",
            "wrdn_aux": "false"
        }
        return dct_s_inf
    else:
        return "nothing"

#入力文解析
def get_input_inf(ipt_text):
    # 元の文章
    s_orig = []
    # 主語
    s_sb = ""
    #人称
    s_person = ""
    # 動詞より前の文章
    s_fore = ""
    # 動詞
    s_verb = ""
    # 動詞より後の文章
    s_back = ""
    # 補助動詞
    s_oc_aux = ""
    s_oc_verb = ""

    #jsonファイル取得
    json_open = open('data/words.json', 'r')
    json_load = json.load(json_open)

    nlp = spacy.load('de_core_news_sm')
    doc = nlp(ipt_text)

    for i, d in enumerate(doc):
        # sb = 主語
        print((d.text, d.pos_, d.dep_))
        
        s_orig.append(d.text)

        if d.dep_ != "ROOT" \
        and d.dep_ != "oc": 
            if s_verb == "" \
            and (s_oc_aux == "" or s_oc_verb == ""):
                # まだ動詞が出てきていない場合
                s_fore = s_fore + ' ' + d.text
            elif s_verb != "" \
            and (s_oc_aux == "" or s_oc_verb == ""):
                # すでに動詞が出てきている場合
                if d.text == ".":
                    s_back = s_back + d.text
                else:
                    s_back = s_back + ' ' + d.text

            
            if d.dep_ == 'sb':
                #主語特定 ichとか以外ならother
                if d.text.lower() != 'ich' \
                and d.text.lower() != 'du' \
                and d.text.lower() != 'er' \
                and d.text.lower() != 'es' \
                and d.text.lower() != 'wir' \
                and d.text.lower() != 'ihr' \
                and d.text.lower() != 'sie':
                    s_sb = s_orig[i - 1] + ' ' + s_orig[i]
                else:
                    s_sb = d.text

                #人称特定 ichとか以外ならother
                if d.text.lower() != 'ich' \
                and d.text.lower() != 'du' \
                and d.text.lower() != 'er' \
                and d.text.lower() != 'es' \
                and d.text.lower() != 'wir' \
                and d.text.lower() != 'ihr' \
                and d.text.lower() != 'sie':
                    s_person = json_load['person']['other']
                else:
                    s_person = json_load['person'][d.text.lower()]
        
        #動詞特定
        elif d.dep_ == "ROOT":
            # 第二位動詞の場合
            s_verb = get_verb_lemma(d.text)
            print(d.text)
        
        elif d.dep_ == "oc":
            # 第二位動詞ではない場合
            if d.pos_ == "AUX":
                s_oc_aux = d.text

            elif d.pos_ == "VERB":
                s_oc_verb = d.text
                s_verb = get_verb_lemma(d.text)

    #返す
    print(s_oc_aux)
    print(s_oc_verb)
    dct_re = {
        "r_s_person": s_person,
        "r_s_fore": s_fore,
        "r_s_verb": s_verb,
        "r_s_back": s_back
    }

    print(dct_re)
    return dct_re

#動詞の原型取得
def get_verb_lemma(v):
    #動詞の原型
    v_origin = ""
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='de',TAGDIR='/Applications/XAMPP/xamppfiles/htdocs/NLP_test/')
    tag = tagger.TagText(v)
    l_word = tag[0].split("\t")[0]
    p_word = tag[0].split("\t")[1]
    o_word = tag[0].split("\t")[2]
    v_origin = o_word
    return v_origin


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

    
