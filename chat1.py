# coding:utf-8
import json
import csv
import os
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
    new_dataが返答を示す。
    :return:
    """
    content = request.forms.getunicode("chat_word")
    now = datetime.now()
    now_time = now.strftime('%Y-%m-%d %H:%M:%S')
    greeting_list = ["おはよう","こんにちは","こんにちわ","Hi","hi","こんばんは","こんばんわ"]
    if content in greeting_list:
        new_data = greet()
    elif content == "削除":
        new_data = "やめてくりー"
    else:
        new_data = "その言葉はまだわかんないんだ！ ごめんねm(__)m"

    save_talk(now_time, content, new_data)
    return json.dumps({
    "new_data":new_data,
    })

def greet():
    now = datetime.now()
    greet_list = ["もしかして…夜明け待ちですか","おはよう","こんにちは","こんばんは","夜更かしはだめですよ~"]
    time = now.hour
    if time <= 5 and time > 3:
        return greet_list[0]
    elif time <=  9 and time >5:
        return greet_list[1]
    elif time <= 17 and time > 9:
        return greet_list[2]
    elif time <=20 and time > 17:
        return greet_list[3]
    else:
        return greet_list[4]

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
