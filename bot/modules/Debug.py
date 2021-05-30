from discord.ext.commands import Cog
from discord.ext import commands
from discord import Embed

class Debug(Cog):
    def __init__(self,bot):
        self.bot = bot

    #Debug commands ----------------------------
    @commands.command(name="msg")
    async def privateMessage(self, ctx, user, *, words="There was no context :eyes:"):
        #await ctx.author.send("this is a test message")
        await user.send(f"{words}")

    @commands.command(name="say")
    async def repeatAfterMe(self, ctx, *, words):
        await ctx.message.delete()
        emb = Embed(title=words)
        msg = await ctx.send(embed=emb)
    

def setup(bot):
    bot.add_cog(Debug(bot))