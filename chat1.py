# coding:utf-8
import json
import csv
import os
from datetime import datetime
from bottle import route, run, template, request, response, redirect, static_file


start_check = "START"

@route("/")
def sample():
    return redirect("/chat_room")

@route("/chat_room")
def chat_room():
    """
    チャットを行う画面
    :return:
    チャットの記載例を載せる。
    """
    global start_check
    start_check = "TRUE"
    # print("HELLO WORLD!")

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



def talk(request_content ="null"):
    """
    発言を登録し、チャットルームへリダイレクトします
    :return:
    """
    global start_check
    #時間を取得
    tdatetime = datetime.now()
    now_time = tdatetime.strftime('%Y-%m-%d %H:%M:%S')

    if start_check == "TRUE":
        content="null"
        new_data = "何か文字を入力してね"
        start_check = "FALSE"
        # print("talk()の中身は…")
        # print(now_time,content,new_data)


    else:
        # マルチバイトデータのためgetではなくgetunicodeにする
        content = request_content
        new_data = "null"
        print(now_time,content,new_data)

    return now_time,content,new_data


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


@route("/api/talk", method=["GET", "POST"])
def talk_api():
    """
    発言一覧を管理するAPI
     GET -> 発言一覧を戻す
    POST -> 発言を保存する
     json eg.
     [
        {
            talk_time:2016-09-17 15:00:49.937402
            username:sayamada
            content:おはよう
        }
    :
        },
        {
            talk_time:2016-09-17 15:58:03.200027
            username:sayamada
            content:こんにちは
        },
        {
            talk_time:2016-09-17 15:58:12.289631
            username:sayamada
            content:元気ですか？
        }
     ]
     :return:
    """
    if request.forms.getunicode("chat_word") == None:
        talk_list = talk()
        return json.dumps({
        "talk_time":talk_list[0],
        "content":talk_list[1],
        "new_data":talk_list[2],
        })

    else:
        talk_list = []
        content = request.forms.getunicode("chat_word")
        tdatetime = datetime.now()
        now_time = tdatetime.strftime('%Y-%m-%d %H:%M:%S') + "%08d" % (tdatetime.microsecond // 1000)
        print(tdatetime)

        greeting_list = ["おはよう","こんにちは","こんにちわ","Hi","hi","こんばんは","こんばんわ"]

        if content in greeting_list:
            new_data = greet()
        elif content == "削除":
            new_data = "やめてくりー"
        else:
            new_data = "その言葉はまだわかんないんだ！ ごめんねm(__)m"

        save_talk(now_time, content, new_data)
        return json.dumps({
        "talk_time": now_time,
        #"content": content,
        "new_data":new_data,
        })

"""
    if request.method == "GET":
        content = request.query.getunicode("chat_word")
        talk_list = talk(content)
        return json.dumps({
        "talk_time":talk_list[0],
        "content":talk_list[1],
        "new_data":talk_list[2],
        })

    elif request.method == "POST":
        talk_list = []
        content = request.forms.getunicode("chat_word")
        tdatetime = datetime.now()
        now_time = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
        greeting_list = ["おはよう","こんにちは","こんにちわ","Hi","hi","こんばんは","こんばんわ"]

        if content in greeting_list:
            new_data = greet()
        elif content == "削除":
            new_data = "やめてくりー"
        else:
            new_data = "その言葉はまだわかんないんだ！ ごめんねm(__)m"

        save_talk(now_time, content, new_data)
        return json.dumps({
        "talk_time": now_time,
        #"content": content,
        "new_data":new_data,
        })
"""

def save_talk(talk_time, content, new_data):
    """
    チャットデータを永続化する関数
    CSVとしてチャットの内容を書き込んでいる

    :param talk_time:
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
