from discord import Color, Embed, __version__ as discordVersion
from discord.errors import LoginFailure
from discord.ext.commands import Bot

from config.config import BOTCONFIG

from os import listdir, getenv
from enum import Enum
import json


class VotingBot(Bot):
    """Just another discord bot"""
    config = BOTCONFIG
    Tick = "\u2705"
    Cross = "\u274C"
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        print ("Discord Version:",discordVersion)
        print ("Loading Bot, Please Wait")

    def load_cogs(self):
        # Gets all the modules for the discord bot
        cogs = [cog for cog in sorted(listdir("./modules")) if cog.endswith(".py")] 
        for cog in cogs:
            try:
                cog = f"modules.{cog.replace('.py','')}"
                bot.load_extension(cog)
                print(f"loaded {cog}")
            except Exception as e:
                print(f"{cog} can not be loaded")
                print(f"{str(type(e))} : "+str(e))

bot = VotingBot(command_prefix="!v", description=VotingBot.__doc__)


try:
    
    TOKEN = getenv("BOT_TOKEN",None)
    if(TOKEN is None): 
        raise LoginFailure("No Token in Config")
    bot.run(TOKEN)
except LoginFailure as e:
    print(str(e))
