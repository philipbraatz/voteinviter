from flask import Blueprint, render_template, redirect, request, session
from flask_login import login_required, current_user
from pathlib import Path
from .oauth import Oauth
from discord import Webhook, AsyncWebhookAdapter, Embed
import aiohttp
import asyncio

views = Blueprint('views',__name__)

def internalRender(file):
    reader = open("templates/"+file, "r")
    headlinks = reader.read()
    reader.close()
    return headlinks

@views.route('/')
def index():
    return render_template('landing_page/index.html',username="Scott",voteYes=4,voteNo=3)

@views.route('/signup')
def discord():
    return redirect(Oauth.discord_login_url)

@views.route('/discordlogin', methods = ['GET', 'POST'])
def login(): 
    code = request.args.get('code')
    access_token = Oauth.get_access_token(code)
    user = Oauth.get_user_json(access_token)
    if(not user):
        return redirect(Oauth.discord_login_url)

    return render_template("signup.html",
        username=user.get('username'),
        avatar=Oauth.getProfileImage(user.get("id"),user.get("avatar")))

@views.route('/request', methods=['POST'])
def requestvote():
    user = session.get('user',False)
    if(not user):
        return redirect(Oauth.discord_login_url)

    asyncio.run(sendRequest(user,request.form))
    return render_template("signup.html",
        username=user.get('username'),
        avatar=Oauth.getProfileImage(user.get("id"),user.get("avatar")))
    pass

async def sendRequest(user,data):
    emb = Embed(title="Needs Approval "+user.get("username")+" AKA ("+data.get('username')+")",
        description=f"\nKnows: {data.get('relation')}\n{data.get(user.get('username'))}",
        Author=user.get("username"), 
        Image=Oauth.getProfileImage(user.get("id"),user.get("avatar")))

    async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(Oauth.discord_webhook_url, adapter=AsyncWebhookAdapter(session))
            await webhook.send(
                content=data.get('description'),
                embed=emb)

@views.route('/profile')
@login_required
def profile():
    return "Members only club "+ current_user.is_authenticated