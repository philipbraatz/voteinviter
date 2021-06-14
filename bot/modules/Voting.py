from discord import Embed, Colour, User
from discord.ext.commands import Cog
from discord.ext import commands

from ..__init__ import PRIVATECONFIG, BOTCONFIG
from bot.dataclasses.User import Voter, Elector
from bot.dataclasses.Vote import Vote

from logging import getLogger
from config.config import setupLogging
logger = getLogger(__name__)
setupLogging(logger)

class Voting(Cog):
    def __init__(self,bot):
        self.bot = bot
        self.voteMSG = None
        self.elector = None

    @commands.command(name="start")
    @commands.has_role(int(BOTCONFIG.STAFF_ROLE))
    async def start(self, ctx, name =None, *, description=None):
        if name is None:
            await ctx.send("voting requires a username")
            return

        emb = Embed(title="VOTE: "+name,
            description=f"{self.bot.config.vote_ping}\nDescription: {description}\n\
                \nReact with {Vote.YAY.value} if you want them\nReact with {Vote.NAY.value} if you don't",colour=Colour.blue())
        self.voteMSG = await ctx.send(embed=emb)
        await self.voteMSG.add_reaction(Vote.YAY.value)
        await self.voteMSG.add_reaction(Vote.NAY.value)
        self.elector = Elector("TEMP_NEEDS_REAL")

        def check(reaction, user):
            return reaction.message == self.voteMSG and ( reaction.emoji == Vote.YAY.value or reaction.emoji == Vote.NAY.value )


        # TODO add voting logic, loop until vote end
        try:
            reaction, user = await self.bot.wait_for("reaction_add",timeout=60.0,check=check)
        except:
            await ctx.send("You didn't respond the coin dropped into the void so we will never know the true answer.")
        else:
            await ctx.send(f"You picked: {str(reaction.emoji)}")
            await self.voteMSG.delete()
            self.voteMSG = None
        pass

    @commands.command(name="stop")
    @commands.has_role(int(BOTCONFIG.STAFF_ROLE))
    async def stop(self,ctx):
        logger.info("TODO fill out")
        pass

    @commands.command(name="remove")
    @commands.has_role(int(BOTCONFIG.STAFF_ROLE))
    async def remove(self,ctx):
        channel = self.bot.get_channel(BOTCONFIG.VOTING_CHANNEL)
        msg =await channel.fetch_message(self.voteMSG.id)
        await ctx.send(str(msg.reactions))
        await self.on_user_reaction(msg)
        pass

    async def on_user_reaction(self,msg):
        #logger.debug("All Reactions: "+str( msg.reactions))
        userReactions = [reaction for reaction in msg.reactions if not reaction.me]#filter(reaction => reaction.users.cache.has(PRIVATECONFIG.OAUTH_CLIENT_TOKEN));
        try:
            #logger.debug("User Reactions: "+str(userReactions))
            for reaction in userReactions:
                for user in await reaction.users().flatten():
                    await msg.remove_reaction(reaction.emoji, user)
        except Exception as e:
            logger.fatal(str(e))



def setup(bot):
    bot.add_cog(Voting(bot))
