from discord.ext.commands import Cog
from discord.ext import commands

class Config(Cog):
    def __init__(self,bot):
        self.bot = bot

    #Config commands ----------------------------
    @commands.group(name="min", invoke_without_command=True)
    async def min_command(self,ctx):
        pass

    @min_command.command(name="approve")
    async def setMinApproval(self, amount):
        pass
        
    @min_command.command(name="votes")
    async def setToPercent(self, ctx, amount):
        pass

    @commands.group(name="set", invoke_without_command=True)
    async def set_mode(self, ctx):
        await ctx.send("set [difference | percentage]")
        pass
   
    #Switches to difference voting
    @set_mode.command(name="difference",aliases=["d"])
    async def setMinDiff(self, ctx, amount):
        pass

    #Switches to Percentage voting
    @set_mode.command(name="percentage",aliases=["p"])
    async def setToPercent(self, ctx, percent):
        pass


def setup(bot):
    bot.add_cog(Config(bot))