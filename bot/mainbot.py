#this is global to
#get the time it took to load the config WITH VotingBot
import logging
from config.config import setupLogging
import time

logger = logging.getLogger(__name__)
setupLogging(logger)

logger.info("Loading Bot")
start = time.time()

from .__init__ import BOTCONFIG
from discord import Color, Embed, __version__ as discordVersion
from discord.errors import LoginFailure
from discord.ext.commands import Bot

from os import listdir, getenv

class VotingBot(Bot):
    """Just another discord bot"""
    config = BOTCONFIG
    Tick = "\u2705"
    Cross = "\u274C"
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        logger.debug("Discord Version: "+discordVersion)

        try:
            TOKEN = getenv("BOT_TOKEN",None)
            if(TOKEN is None): 
                raise LoginFailure("No Token in Config")
            self.load_cogs()

            end = time.time()
            logger.info(f"Loaded Bot in {round(end - start,2)} seconds")

            self.run(TOKEN)
        except LoginFailure as e:
            logger.warning(str(e))
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
                logger.info(f"loaded module {name}")
            except Exception as e:
                #print(f"{cog} can not be loaded")
                logger.warning(f"Skipping module '{name}': {str(e)}")
        #print(f"{len(cog.get_commands())} Commands loaded")
