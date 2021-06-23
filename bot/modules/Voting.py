from bot.dataclasses.Elector import Elector, Voter
from bot.dataclasses.Vote import Vote
from config.config import SetupLogging
from discord import Colour, Embed, User
from discord.ext import commands
from discord.ext.commands import Cog

from ..__init__ import BOTCONFIG, PRIVATECONFIG

logger = SetupLogging(__name__)


class Voting(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voteMSG = None
        self.elector = None

    @commands.command(name="stop")
    @commands.has_role(int(BOTCONFIG.STAFF_ROLE))
    async def Stop(self, ctx):
        logger.info("TODO fill out")
        pass

    @commands.command(name="quick")
    @commands.has_role(int(BOTCONFIG.STAFF_ROLE))
    async def Quick(self, ctx):
        logger.info("TODO fill out")
        pass


def setup(bot):
    bot.add_cog(Voting(bot))
