import logging
import time
import traceback
from os import listdir

from config.config import SetupLogging
from discord import Color, Embed
from discord import __version__ as discordVersion
from discord.errors import LoginFailure
from discord.ext.commands import Bot

from .__init__ import BOTCONFIG, PRIVATECONFIG
from .dataclasses.Vote import Vote

# this is global to
# get the time it took to load the config WITH VotingBot
startOfEverything = time.time()
logger = SetupLogging(__name__, True)


logger.info("Loading Bot")


class VotingBot(Bot):
    WEBHOOK_ID = PRIVATECONFIG.WEBHOOK_ID
    CLIENT_ID = PRIVATECONFIG.CLIENT_ID

    config = BOTCONFIG

    startt = None
    end = 0

    elector = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug("Discord Version: "+discordVersion)

        self.startt = startOfEverything
        # logger.debug(f"start time {str(self.startt)}")FF

        try:
            TOKEN = PRIVATECONFIG.BOT_TOKEN  # getenv("BOT_TOKEN",None)
            if(TOKEN is None):
                raise LoginFailure("No Token in Config")

            # self.remove_command("help")
            self.load_cogs()

            self.run(TOKEN)
        except LoginFailure as e:
            logger.warning(str(e))
        pass

    def load_cogs(self):
        # Gets all the modules for the discord bot
        cogs = [cog for cog in sorted(
            listdir("bot/modules")) if cog.endswith(".py")]
        #logger.debug("Modules: "+ str(len(cogs)))
        for cog in cogs:
            try:
                name = cog.replace('.py', '')
                cog = f"bot.modules.{name}"
                self.load_extension(cog)
                logger.info(f"loaded module {name}")
            except Exception as e:
                #logger.debug(f"{cog} can not be loaded")
                logger.warning(f"Skipping module '{name}': {str(e)}")
                traceback.print_exc()
        #logger.debug(f"{len(cog.get_commands())} Commands loaded")

    def check_user_reaction(self, reaction, user):
        # is bot message,
        # is not the bot,
        # is not the website,
        # is a VOTE message
        return reaction.message.author.id == int(self.CLIENT_ID) and\
            int(user.id) != int(self.CLIENT_ID) and\
            int(user.id) != int(self.WEBHOOK_ID) and\
            len(reaction.message.embeds) > 0 and\
            "VOTE: " in reaction.message.embeds[0].title

    def check_webhook_reaction(self, webhookMSG, reaction, user):
        # is webhook
        # is not the bot
        # is valid vote
        return reaction.message == webhookMSG and \
            user.id != int(self.CLIENT_ID) and \
            Vote.isVote(reaction.emoji)

    async def addMemberToGuild(self, userId):
        self.elector.inviteLink = await self.bot.get_channel(
            await self.config.WELCOME_CHANNEL)\
            .create_invite(
                max_age=self.config.invite_expire_time,
                max_uses=1,
                reason=f"{self.elector.name} has been voted in ({str(self.elector.getVotes())})")
        return self.elector.inviteLink

    def replaceDynamicText(self, message, name, rule, role):
        message = message.replace("(username)", name)
        message = message.replace("(ruleschannel)", rule)
        message = message.replace("(roleschannel)", role)
        return message
