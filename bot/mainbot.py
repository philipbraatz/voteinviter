import time
import logging
from config.config import setupLogging
from .__init__ import PRIVATECONFIG

#this is global to
#get the time it took to load the config WITH VotingBot
startOfEverything = time.time()
logger = logging.getLogger(__name__)
setupLogging(logger)

logger.info("Loading Bot")


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
    Question = "\u2753"

    startt = None
    end = 0

    elector = None

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        logger.debug("Discord Version: "+discordVersion)

        self.startt = startOfEverything
        #logger.debug(f"start time {str(self.startt)}")FF

        try:
            TOKEN = getenv("BOT_TOKEN",None)
            if(TOKEN is None): 
                raise LoginFailure("No Token in Config")

            self.load_cogs()

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

    def check_user_reaction(self, reaction, user):
        #is bot message, 
        #is not the bot,
        #is not the website,
        #is a VOTE message
        return reaction.message.author.id == int(PRIVATECONFIG.CLIENT_ID) and\
            int(user.id) != int(PRIVATECONFIG.CLIENT_ID) and\
            int(user.id) != int(PRIVATECONFIG.WEBHOOK_ID) and\
            len(reaction.message.embeds) > 0 and\
            "VOTE: " in reaction.message.embeds[0].title

    def check_webhook_reaction(self,webhookMSG,reaction,user):
        #is webhook
        #is not the bot
        #is valid vote
        return  reaction.message == webhookMSG and \
                user.id != int(PRIVATECONFIG.CLIENT_ID) and \
                self.cleanVoteToBool(reaction,user) != None

    async def cleanVoteToBool(self,r,user=None):
        if(r.emoji == self.Tick):
            return True
        elif(r.emoji == self.Cross):
            return False
        elif(r.emoji == self.Question):
            return 2
        elif(user != None and not r.me):
            await r.remove(user)
        return None

    async def addMemberToGuild(self, userId):
        self.bot.get_channel(BOTCONFIG.WELCOME_CHANNEL).create_invite(
            max_age=60*60*24, max_uses=1,reason=f"{self.elector.name} \
            has been voted in ({str(self.elector.getVotes())})")
