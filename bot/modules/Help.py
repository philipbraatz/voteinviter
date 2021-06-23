from discord.ext import commands
from discord.ext.commands import Cog

from ..__init__ import BOTCONFIG


class Help(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Config commands ----------------------------
    @commands.command(name="invite", invoke_without_command=True,
                      description="How to invite someone",
                      help="This bot allows outsiders to request to join the server.\n\
            This is done by going to http://burbscanvote.tk/signup and filling out all the information.\n\
            If staff approve it, the vote will begin.")
    async def Invite(self, ctx):
        await ctx.channel.send("http://burbscanvote.tk/signup")
        pass

    @commands.command(name="link", invoke_without_command=True,
                      description="Link to website",
                      help="The active vote are visible on http://burbscanvote.tk/\n\
        This allows people being voted on to see their votes. (And for staff to show off)")
    async def Link(self, ctx):
        await ctx.channel.send("http://burbscanvote.tk/")
        pass


def setup(bot):
    bot.add_cog(Help(bot))
