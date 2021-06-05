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
    return render_template('landing_page/index.html',
    username=session.get("name"),
    avatar=DiscordAuth.getProfileImage(session.get("id"), session.get("avatar")),
    voteYes=session.get("positive"),
    voteNo=session.get("negative"))

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
    secret = request.args.get('secret')
    if (secret == "myBallsAreMassive"):
        session['positive'] = int(request.args.get('positive'))
        session['negative'] = int(request.args.get('negative'))

@views.route('api/startvote', methods=['POST'])
def startvote():
    secret = request.args.get('secret')
    if (secret == "myBallsAreSmaller"):
        session['positive'] = 0
        session['negative'] = 0
        session['name'] = request.args.get('name')
        session['id'] = request.args.get('id')
        session['avatar'] = request.args.get('avatar')

@views.route('/profile')
@login_required
def profile():
    return "Members only club "+ current_user.is_authenticated