import asyncio
from datetime import datetime
from pathlib import Path

import aiohttp
from config.config import SetupLogging
from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)
from flask_login import current_user, login_required
from pywebpush import WebPushException, webpush

from __init__ import PRIVATECONFIG

from .Database import GetLastDayResult, GetLastVoteResult
from .discordAuth import DiscordAuth

logger = SetupLogging(__name__)


views = Blueprint('views',__name__)

myValues = {"name":"","positive": 0,"negative":0,"id":0,"avatar":0,"vote_date":0}
        
def internalRender(file):
    reader = open("templates/"+file, "r")
    headlinks = reader.read()
    reader.close()
    return headlinks


@views.route('/index.html')
@views.route('/index')
@views.route('/index/')
@views.route('/')
def Index():
    
    global myValues
    
    vote = GetLastDayResult()
    if(vote is not None):
        myValues = vote
        vote = True
        print("Got Day")
    else:
        temp = GetLastVoteResult()
        print("Last vote value: "+str(temp))
        if(temp != None):
            myValues = temp
            print("Got Last Vote")
        Vote = False

    avatar =""
    if(session.get('user',False) != False):
        avatar = DiscordAuth.getProfileImage(session['user']["id"],session['user']["avatar"])
        print("User: "+str(dict(session['user'])))
    else: 
        session['user'] = False
    
    p =myValues["positive"] if myValues["positive"] is not None else 0
    n =myValues["negative"] if myValues["negative"] is not None else 0

    print(f"Vote {str(vote)} "+ str(myValues["negative"])+"\n"+
          str(myValues["positive"])+"\n"+
          str(myValues["name"])+"\n"+
          str(myValues["avatar"])+"\n"+
          str(myValues["vote_date"]))
    print("IP: "+request.remote_addr)
    #session["test"] = "I Eat taco"
    print("Session: "+str(session.keys()))
    print("Session: "+str(session.values()))

    return render_template('v2/index.html',
    username=myValues["name"],
    avatar=DiscordAuth.getProfileImage(myValues["id"], myValues["avatar"]),
    yay=p,
    nay=n,
    votePercent=round(p/(p+n+0.000001)*100),
    vote=vote,
    vote_date= myValues["vote_date"] if not vote else datetime.now().date(),
    userAvatar=avatar,
    user=session['user'])


@views.route('/login/')
@views.route('/login')
def Login():
    return redirect(DiscordAuth.getRedirectURL("login/discord"))

@views.route('/signup/')
@views.route('/signup')
def Signup():
    if(GetLastDayResult() is None):
        return redirect(DiscordAuth.getRedirectURL("signup/discord"))
    else:
        return ("Vote is active, you must wait the vote to be over",403)

@views.route('/login/discord', methods = ['GET', 'POST'])
def LoginDiscord(): 
    
    code = request.args.get('code')
    #try:
    access_token = DiscordAuth.get_access_token(code,"login/discord")

    user = DiscordAuth.get_user_json(access_token)
    if(not user):
        return redirect(DiscordAuth.getRedirectURL("login/discord"))

    session['user'] = user
    
    logger.info(f"User: {str(session['user']['username'])} has logged in")
 
    return redirect(url_for(".index"))
    #except Exception as e:
    #    return redirect(url_for(".login"))#try again

@views.route('/signup/discord', methods = ['GET', 'POST'])
def SignupDiscord(): 
    if(GetLastDayResult() is not None):
        return ("Vote is active, you must wait the vote to be over",403)
    
    code = request.args.get('code')
    try:
        access_token = DiscordAuth.get_access_token(code,"signup/discord")

        user = DiscordAuth.get_user_json(access_token)
        if(not user):
            return redirect(DiscordAuth.getRedirectURL("signup/discord"))
            
        session['user'] = user

        return render_template("signup.html",
            username=user.get('username'),
            avatar=DiscordAuth.getProfileImage(user.get("id"),user.get("avatar"))
            )
    except Exception as e:
        return e#redirect(DiscordAuth.getRedirectURL())

@views.route('/request', methods=['POST'])
def Requestvote():
    if(GetLastDayResult() is not None):
        return("Vote is active, you must wait the vote to be over",403)
    
    user = session.get('user',False)
    if(not user):
        return redirect(DiscordAuth.getRedirectURL("signup/discord"))

    asyncio.run(DiscordAuth.sendRequest(user,request.form))
    return redirect("/index?vote")

@views.route('api/sendvote', methods=['POST'])
def Sendvote():
    global myValues
    secret = request.args.get('secret')
    if (secret == PRIVATECONFIG.API_KEY):
        myValues["positive"] = int(request.args.get('positive'))
        myValues["negative"] = int(request.args.get('negative'))
    return "I am text"

@views.route('api/startvote', methods=['POST'])
def Startvote():
    global myValues
    secret = request.args.get('secret')
    if (secret == PRIVATECONFIG.API_KEY):
        myValues["positive"] = 0
        myValues["negative"] = 0
        myValues["name"] = request.args.get('name')
        myValues["id"] = request.args.get('id')
        myValues["avatar"] = request.args.get('avatar')
        myValues["vote_date"] = datetime.now()
        logger.debug("AVATAR: "+myValues["avatar"] )
    return "I am text"

@views.route('/profile')
@login_required
def Profile():
    return "Members only club "+ current_user.is_authenticated

@views.route('/subscription',methods=['GET', 'POST'])
def Subscription():
    pass

@views.route('/push', methods=['POST'])
def push():
    pass


def Send_web_push(subscription_information, message_body):
    return webpush(
        subscription_info=subscription_information,
        data=message_body,
        vapid_private_key=PRIVATECONFIG.VAPID_PRIVATE_KEY,
        vapid_claims=PRIVATECONFIG.VAPID_CLAIMS
    )
