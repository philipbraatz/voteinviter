from flask import Blueprint, render_template, redirect, request, session
from flask_login import login_required, current_user
from pathlib import Path
from .discordAuth import DiscordAuth
import aiohttp
import asyncio
from __init__ import PRIVATECONFIG

views = Blueprint('views',__name__)

myValues = {"name":"","positive": 0,"negative":0,"id":0,"avatar":0}

def internalRender(file):
    reader = open("templates/"+file, "r")
    headlinks = reader.read()
    reader.close()
    return headlinks

@views.route('/')
def index():
    global myValues
    return render_template('landing_page/index.html',
    username=myValues["name"],
    avatar=DiscordAuth.getProfileImage(myValues["id"], myValues["avatar"]),
    voteYes=myValues["positive"],
    voteNo=myValues["negative"])

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
        avatar=DiscordAuth.getProfileImage(user.get("id"),user.get("avatar"))
        )

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

@views.route('api/sendvote', methods=['POST'])
def sendvote():
    global myValues
    secret = request.args.get('secret')
    if (secret == PRIVATECONFIG.API_KEY):
        myValues["positive"] = int(request.args.get('positive'))
        myValues["negative"] = int(request.args.get('negative'))
    return "I am text"

@views.route('api/startvote', methods=['POST'])
def startvote():
    global myValues
    secret = request.args.get('secret')
    if (secret == PRIVATECONFIG.API_KEY):
        myValues["positive"] = 0
        myValues["negative"] = 0
        myValues["name"] = request.args.get('name')
        myValues["id"] = request.args.get('id')
        myValues["avatar"] = request.args.get('avatar')
    return "I am text"

@views.route('/profile')
@login_required
def profile():
    return "Members only club "+ current_user.is_authenticated