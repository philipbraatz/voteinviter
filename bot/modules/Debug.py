from discord.ext.commands import Cog
from discord.ext import commands
from discord import Embed
import datetime

class Debug(Cog):
    def __init__(self,bot):
        self.bot = bot

    #Debug commands ----------------------------
    @commands.command(name="manualinv")
    async def privateMessage(self, ctx):
        #await ctx.author.send("this is a test message")
        invite =await ctx.channel.create_invite(
            max_age=self.bot.config.invite_expire_time,
            max_usages=1,
            unique=False,
            reason=f"{ctx.author.name} manually created an invite"
            )
        await ctx.channel.send(f"{invite}")

    @commands.command(name="say")
    async def repeatAfterMe(self, ctx, *, words):
        await ctx.message.delete()
        emb = Embed(title=words)
        msg = await ctx.send(embed=emb)

    @commands.command(name="load",hidden=True)
    async def load(self,ctx, module : str):
        """Loads a module."""
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.channel.send('\N{PISTOL}')
            await ctx.channel.send('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say('\N{OK HAND SIGN}')

    @commands.command(name="unload",hidden=True)
    async def unload(self,ctx, module : str):
        """Unloads a module."""
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await ctx.channel.send('\N{PISTOL}')
            await ctx.channel.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.channel.send('\N{OK HAND SIGN}')

    @commands.command(name='reload', hidden=True)
    async def _reload(self, ctx, module : str):
        """Reloads a module."""
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.channel.send('\N{PISTOL}')
            await ctx.channel.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.channel.send('\N{OK HAND SIGN}')

def setup(bot):
    bot.add_cog(Debug(bot))