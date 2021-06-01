from os import getenv
from requests import post, get, Response
from __init__ import PRIVATECONFIG
import json

class Oauth(object):
    DISCORD_API ="https://discord.com/api/"


    client_id = int(getenv("CLIENT_ID",""))
    client_secret = getenv("OAUTH_CLIENT_TOKEN","")
    webhook_id = int(getenv("WEBHOOK_ID",""))
    webhook_secret = getenv("WEBSITE_SECRET_KEY","")
    scope = "identify%20guilds.join"
    redirect_uri = "http://127.0.0.1:84/discordlogin"#TODO - check if development 
    discord_login_url = DISCORD_API+"oauth2/authorize?client_id={}&redirect_uri={}&response_type=code&scope={}".format(client_id,redirect_uri,scope)
    discord_token_url = DISCORD_API+"oauth2/token"
    discord_webhook_url = DISCORD_API+"webhooks/{}/{}".format(webhook_id,webhook_secret)
    @staticmethod
    def getProfileImage(profile_id,avatar_id,size =128):
        return "https://cdn.discordapp.com/avatars/{}/{}.png?size={}".format(profile_id,avatar_id,size)

    @staticmethod
    def get_access_token(code):
        data = {
            'client_id': Oauth.client_id,
            'client_secret': Oauth.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': Oauth.redirect_uri,
            'scope': "identify guilds.join"
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        access_token = post(url = Oauth.discord_token_url, data = data, headers = headers)
        access_token.raise_for_status()

        return access_token.json().get("access_token")

    @staticmethod
    def get_user_json(token):
        url = Oauth.DISCORD_API+"/users/@me"
        headers = {
            "Authorization": "Bearer {}".format(token)
        }
        user_json = get(url = url, headers = headers).json()
        return user_json

    @staticmethod
    def send_webhook_message(content):
        headers = {
            'Content-Type': 'application/json'
        }
        return post(Oauth.discord_webhook_url,headers=headers,data=json.dumps({'content': content}))