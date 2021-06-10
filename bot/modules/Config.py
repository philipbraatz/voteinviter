from discord.ext.commands import Cog
from discord.ext import commands

class Config(Cog):
    def __init__(self,bot):
        self.bot = bot

    #Config commands ----------------------------
    @commands.group(name="min",
        invoke_without_command=True,
        description="Set minimum number of votes")
    async def min_command(self,ctx,amount):
        self.bot.config.min_vote = amount
        pass

    @min_command.command(name="approve",
    description="Set minimum number of votes")
    async def setMinApproval(self,ctx, amount):
        self.bot.config.min_approve = amount
        pass
        
    @min_command.command(name="votes",
    description="Set voting requirements for percentage vote")
    async def setToPercent(self, ctx, amount):
        self.bot.config.min_percentage = amount
        pass

    @commands.group(name="set", invoke_without_command=True,
        description="Pick between voting with difference of positive to negative OR a percentage of positive")
    async def set_mode(self, ctx):
        await ctx.send("set [difference | percentage]")
        pass
   
    #Switches to difference voting
    @set_mode.command(name="difference",aliases=["d"],
    description="The difference in votes between YAY's and NAY's")
    async def setMinDiff(self, ctx, amount):
        pass

    #Switches to Percentage voting
    @set_mode.command(name="percentage",aliases=["p"],
        description="The percentage in votes between YAY's and NAY's")
    async def setToPercent(self, ctx, percent):
        pass


def setup(bot):
    bot.add_cog(Config(bot))