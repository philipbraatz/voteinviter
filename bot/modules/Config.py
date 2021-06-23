from discord.ext import commands
from discord.ext.commands import Cog

from ..__init__ import BOTCONFIG


class Config(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Config commands ----------------------------
    @commands.group(name="min",
                    invoke_without_command=True,
                    description="Set minimum number of votes")
    @commands.has_role(int(BOTCONFIG.STAFF_ROLE))
    async def Min_command(self, ctx, amount):
        self.bot.config.min_vote = amount
        pass

    @commands.command(name="quick",
                      description="Set minimum number of votes for QUICK voting")
    @commands.has_role(int(BOTCONFIG.STAFF_ROLE))
    async def SetMinQuickVote(self, ctx, amount):
        self.bot.config.min_quick_votes = amount
        pass

    @commands.command(name="votes",
                      description="Set voting requirements for percentage vote")
    @commands.has_role(int(BOTCONFIG.STAFF_ROLE))
    async def SetToPercent(self, ctx, amount):
        self.bot.config.min_percentage = amount
        pass

    @commands.group(name="set", invoke_without_command=True,
                    description="Pick between voting with difference of positive to negative OR a percentage of positive")
    @commands.has_role(int(BOTCONFIG.STAFF_ROLE))
    async def Set_mode(self, ctx):
        await ctx.send("set [difference | percentage]")
        pass

    # Switches to difference voting
    @commands.command(name="difference", aliases=["d"],
                      description="The difference in votes between YAY's and NAY's")
    @commands.has_role(int(BOTCONFIG.STAFF_ROLE))
    async def SetMinDiff(self, ctx, amount):
        pass

    # Switches to Percentage voting
    @commands.command(name="percentage", aliases=["p"],
                      description="The percentage in votes between YAY's and NAY's")
    @commands.has_role(int(BOTCONFIG.STAFF_ROLE))
    async def SetToPercent(self, ctx, percent):
        pass

    # Switches to Percentage voting
    @commands.command(name="expire", aliases=["p"],
                      description="The percentage in votes between YAY's and NAY's")
    @commands.has_role(int(BOTCONFIG.STAFF_ROLE))
    async def SetExpireDate(self, ctx, value):
        self.bot.config.invite_expire_time = value
        pass


def setup(bot):
    bot.add_cog(Config(bot))
