from .__init__ import BOTCONFIG
from discord import Color, Embed, __version__ as discordVersion
from discord.errors import LoginFailure
from discord.ext.commands import Bot

from os import listdir, getenv
from enum import Enum
import json

import time

import discord
print(discord.__file__)

class VotingBot(Bot):
    """Just another discord bot"""
    config = BOTCONFIG
    Tick = "\u2705"
    Cross = "\u274C"
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        print ("Discord Version:",discordVersion)
        print ("Loading Bot")

        start = time.time()
        try:
            TOKEN = getenv("BOT_TOKEN",None)
            if(TOKEN is None): 
                raise LoginFailure("No Token in Config")
            self.load_cogs()

            end = time.time()
            print(f"Took {round(end - start,2)} seconds")

            self.run(TOKEN)
        except LoginFailure as e:
            print(str(e))
        pass

    def load_cogs(self):
        # Gets all the modules for the discord bot
        cogs = [cog for cog in sorted(listdir("bot/modules")) if cog.endswith(".py")] 
        #print("Modules: "+ str(len(cogs)))
        for cog in cogs:
            try:
                name = cog.replace('.py','')
                cog = f"bot.modules.{name}"
                self.load_extension(cog)
                print(f"bot.loaded {name}")
            except Exception as e:
                #print(f"{cog} can not be loaded")
                print(f"Skipping module '{name}': {str(e)}")
        #print(f"{len(cog.get_commands())} Commands loaded")

bot = VotingBot(command_prefix="!v", description=VotingBot.__doc__)
