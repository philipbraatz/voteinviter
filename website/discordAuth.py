from os import getenv
from requests import post, get, Response
from discord import Webhook, AsyncWebhookAdapter, Embed
from __init__ import PRIVATECONFIG
import json
import aiohttp
import asyncio


class DiscordAuth(object):
    DISCORD_API ="https://discord.com/api/"

    client_id = int(getenv("CLIENT_ID",""))
    client_secret = getenv("OAUTH_CLIENT_TOKEN","")
    webhook_id = int(getenv("WEBHOOK_ID",""))
    webhook_secret = getenv("WEBSITE_SECRET_KEY","")
    scope = "identify%20guilds.join"
    redirect_uri = "http://burbscanvote.tk/"#TODO - check if development
    discord_token_url = DISCORD_API+"oauth2/token"
    discord_webhook_url = DISCORD_API+"webhooks/{}/{}".format(webhook_id,webhook_secret)
    @staticmethod
    def getProfileImage(profile_id,avatar_id,size =128):
        return "https://cdn.discordapp.com/avatars/{}/{}.png?size={}".format(profile_id,avatar_id,size)
    
    @staticmethod
    def getRedirectURL( redirect):
        return DiscordAuth.DISCORD_API+"oauth2/authorize?client_id={}&redirect_uri={}{}&response_type=code&scope={}"\
            .format(DiscordAuth.client_id,DiscordAuth.redirect_uri,redirect,DiscordAuth.scope)

    @staticmethod
    def get_access_token(code, redirect):
        data = {
            'client_id': DiscordAuth.client_id,
            'client_secret': DiscordAuth.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': DiscordAuth.redirect_uri+redirect,
            'scope': "identify guilds.join"
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        access_token = post(url = DiscordAuth.discord_token_url, data = data, headers = headers)
        access_token.raise_for_status()

        return access_token.json().get("access_token")

    @staticmethod
    def get_user_json(token):
        url = DiscordAuth.DISCORD_API+"/users/@me"
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
        return post(DiscordAuth.discord_webhook_url,headers=headers,data=json.dumps({'content': content}))

    @staticmethod
    async def sendRequest(user,data):
        avatar_url = DiscordAuth.getProfileImage(user.get("id"),user.get("avatar"))
        username = user.get('username')+"#"+str(user.get('discriminator'))

        emb = Embed(title="Needs Approval "+username+" AKA ("+data.get('username')+")",
            description=f"\nKnows: {data.get('relation')}\n||ID: {user.get('id')}||\n||{avatar_url}||")

        async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(DiscordAuth.discord_webhook_url, adapter=AsyncWebhookAdapter(session))
                desc =data.get('description')
                await webhook.send(
                    content=desc,
                    embed=emb,
                    avatar_url=avatar_url,
                    username=username)