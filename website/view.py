from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, current_user
from pathlib import Path
from .oauth import Oauth

views = Blueprint('views',__name__)

def internalRender(file):
    reader = open("templates/"+file, "r")
    headlinks = reader.read()
    reader.close()
    return headlinks

@views.route('/')
def index():
    return render_template('landing_page/index.html',username="Scott",voteYes=4,voteNo=3)

@views.route('/discord')
def discord():
    return redirect(Oauth.discord_login_url)

@views.route('discordlogin', methods = ["get"])
def login(): 
    code = request.args.get('code')
    access_token = Oauth.get_access_token(code)
    user_json = Oauth.get_user_json(access_token)
    #username = user_json.get("username")
    return user_json#code+"\n"+access_token+"\n"+str(user_json)
    
@views.route('/profile')
@login_required
def profile():
    return "Members only club "+ current_user.is_authenticated