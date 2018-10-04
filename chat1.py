# coding:utf-8
import json
import csv
import os
import MeCab
import codecs
import pandas as pd
from datetime import datetime
from bottle import route, run, template, request, response, redirect, static_file





@route("/")
def sample():
    return redirect("/chat_room")

@route("/chat_room")
def chat_room():
    """
    チャットの記載例を載せる。
    """

    return template("sample")


@route('/static/<file_path:path>')
def static(file_path):
    """
    静的ファイル専用のルーティング
    /static/* は静的ファイルが存在するものとして動く
    :param file_path:
    :return:
    """
    return static_file(file_path, root="./static")


@route("/api/talk", method="POST")
def talk_api():
    """
    発言一覧を管理するAPI
    POST : 発言を保存する
    new_dataが返答を示す
    :return:
    """
    with codecs.open("reply_word.csv",mode ="r", encoding= "Shift-JIS",errors="ignore") as file:
        reply_word = pd.read_csv(file)
    content = request.forms.getunicode("chat_word")
    print(content)

    #クエリの内容を形態素解析する。
    word_dict=parse(content)
    # print(word_dict["all"])
    print("word_dict：")
    print(word_dict)
    now = datetime.now()
    now_time = now.strftime('%Y-%m-%d %H:%M:%S')
    check = now.second
    #reply_word:1,対応しているもののみ
    greeting_list = ["おはよう","こんにちは","こんにちわ","HI","こんばんは","こんばんわ"]
    #reply_word:4
    Hayashi_list= ["早矢仕","早矢仕晃章","てるさん","HAYASHI","TERU"]
    #reply_word:4
    Ohsawa_list = ["大澤","大澤先生","大澤幸生","OHSAWA"]
    #reply_word:4
    Free_word = ["暇つぶし"]
    #reply_word:3
    Ganzaa_list = ["岩佐","岩佐太路","IWASA","GANZAA"]
    #reply_word:3
    Semple_list = ["仙田","仙田雅大","SENDA","SEMPLE"]

    for nouns_content in word_dict["nouns"]:
        print(nouns_content)
        if nouns_content in greeting_list:
            new_data = greet()
        elif nouns_content in Hayashi_list:
            four_check = check % 4
            new_data = reply_word["Hayashi"][four_check]
        elif nouns_content in Ohsawa_list:
            four_check = check % 4
            new_data = reply_word["Ohsawa"][four_check]
        elif nouns_content in Free_word:
            four_check = check % 4
            new_data = reply_word["Free"][four_check]
        elif nouns_content in Ganzaa_list:
            three_check = check % 3
            new_data = reply_word["Ganzaa"][three_check]
        elif nouns_content in Semple_list:
            three_check = check % 3
            new_data = reply_word["Semple"][three_check]
        else:
            three_check = check % 3
            new_data = reply_word["No_match"][three_check]

    save_talk(now_time, content, new_data)
    return json.dumps({
    "new_data":new_data,
    })

def greet():
    with codecs.open("reply_word.csv",mode ="r", encoding= "Shift-JIS",errors="ignore") as file:
        reply_word = pd.read_csv(file)

    # ここにcsvを読み込むコードを入力して、pandasを用いてreplyのコードを読み込む
    now = datetime.now()

    # greet_list = ["もしかして…夜明け待ちですか","おはよう","こんにちは","こんばんは","夜更かしはだめですよ~"]
    time = now.hour
    if time <= 5 and time > 3:
        return reply_word["Greeting"][0]
    elif time <=  9 and time >5:
        return reply_word["Greeting"][1]
    elif time <= 17 and time > 9:
        return reply_word["Greeting"][2]
    elif time <=20 and time > 17:
        return reply_word["Greeting"][3]
    else:
        return reply_word["Greeting"][4]

def parse(string):

    #'-Ochasen'はChaSen互換形式


    #-Ochasen-に変更
    mecab = MeCab.Tagger("-Ochasen")

    #str型じゃないと動作がおかしくなるので、str型に変換
    node = mecab.parseToNode(string)


    # 単語
    words = []
    # 名詞
    nouns = []
    # 動詞
    verbs = []
    # 形容詞
    adjs = []
    while node:
        pos = node.feature.split(",")[0]
        word = node.surface.upper()
        if pos == "名詞":
            nouns.append(word)
        elif pos == "動詞":
            verbs.append(word)
        elif pos == "形容詞":
            adjs.append(word)
        words.append(word)
        node = node.next
    parsed_words_dict ={
        "all":words[1:-1],#最初と最後には空文字列が入るので除去
        "nouns":nouns,
        "verbs":verbs,
        "adjs":adjs
    }
    return parsed_words_dict

def save_talk(talk_time, content, new_data):
    """
    チャットデータを永続化する関数
    CSVとしてチャットの内容を書き込んでいる
    :param talk_time:
    :param user:
    :param content:
    :return:
    """
    if not os.path.exists("./chat_history.csv"):
        # chat_data.csv→chat_history.csv
        open("./chat_history.csv", "w").close()

    with open('./chat_history.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow([talk_time, "user",content])
        if new_data != "null":
            writer.writerow([talk_time, "bot", new_data])


# サーバの起動
run(host='localhost', port=8080, debug=True, reloader=True)
