from os import getenv
import requests

class Oauth(object):
    DISCORD_API ="https://discord.com/api/"


    client_id = "845702724032397382"
    client_secret = getenv("OAUTH_CLIENT_TOKEN","")
    scope = "identify%20guilds.join"
    redirect_uri = "http://127.0.0.1:84/discordlogin"#TODO - get from config?
    discord_login_url = DISCORD_API+"oauth2/authorize?client_id={}&redirect_uri={}&response_type=code&scope={}".format(client_id,redirect_uri,scope)
    discord_token_url = DISCORD_API+"oauth2/token"
    @staticmethod
    def get_access_token(code):
        data = {
            'client_id': Oauth.client_id,
            'client_secret': Oauth.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': Oauth.redirect_uri,
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        access_token = requests.post(url = Oauth.discord_token_url, data = data, headers = headers)
        access_token.raise_for_status()
        return access_token.json().get("access_token")

    @staticmethod
    def get_user_json(token):
        url = Oauth.DISCORD_API+"/users/@me"
        headers = {
            "Authorization": "Bearer {}".format(token)
        }
        user_json = requests.get(url = url, headers = headers).json()
        return user_json