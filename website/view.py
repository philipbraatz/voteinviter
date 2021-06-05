from flask import Blueprint, render_template, redirect, request, session
from flask_login import login_required, current_user
from pathlib import Path
from .discordAuth import DiscordAuth
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
    return redirect(DiscordAuth.discord_login_url)

@views.route('/discordlogin', methods = ['GET', 'POST'])
def login(): 
    code = request.args.get('code')
    access_token = DiscordAuth.get_access_token(code)
    user = DiscordAuth.get_user_json(access_token)
    if(not user):
        return redirect(DiscordAuth.discord_login_url)

    return render_template("signup.html",
        username=user.get('username'),
        avatar=DiscordAuth.getProfileImage(user.get("id"),user.get("avatar")))

@views.route('/request', methods=['POST'])
def requestvote():
    user = session.get('user',False)
    if(not user):
        return redirect(DiscordAuth.discord_login_url)

    asyncio.run(DiscordAuth.sendRequest(user,request.form))
    return render_template("signup.html",
        username=user.get('username'),
        avatar=DiscordAuth.getProfileImage(user.get("id"),user.get("avatar")))
    pass

@views.route('/profile')
@login_required
def profile():
    return "Members only club "+ current_user.is_authenticated