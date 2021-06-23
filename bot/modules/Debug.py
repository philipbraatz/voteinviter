import datetime

from bot import BOTCONFIG
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Cog


class Debug(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Debug commands ----------------------------
    @commands.command(name="manualinv")
    @commands.has_role(int(BOTCONFIG.STAFF_ROLE))
    async def PrivateMessage(self, ctx):
        # await ctx.author.send("this is a test message")
        invite = await ctx.channel.create_invite(
            max_age=self.bot.config.invite_expire_time,
            max_usages=1,
            unique=False,
            reason=f"{ctx.author.name} manually created an invite"
        )
        await ctx.channel.send(f"{invite}")

    @commands.command(name="load", hidden=True)
    @commands.has_role(int(BOTCONFIG.STAFF_ROLE))
    async def Load(self, ctx, module: str):
        """Loads a module."""
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.channel.send('\N{PISTOL}')
            await ctx.channel.send('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say('\N{OK HAND SIGN}')

    @commands.command(name="unload", hidden=True)
    @commands.has_role(int(BOTCONFIG.STAFF_ROLE))
    async def Unload(self, ctx, module: str):
        """Unloads a module."""
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await ctx.channel.send('\N{PISTOL}')
            await ctx.channel.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.channel.send('\N{OK HAND SIGN}')

    @commands.command(name='reload', hidden=True)
    @commands.has_role(int(BOTCONFIG.STAFF_ROLE))
    async def _Reload(self, ctx, module: str):
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
