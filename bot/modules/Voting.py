from discord import Embed, Colour, User
from discord.ext.commands import Cog
from discord.ext import commands

from ..__init__ import PRIVATECONFIG, BOTCONFIG
from bot.dataclasses.User import Voter, Elector

class Voting(Cog):
    def __init__(self,bot):
        self.bot = bot
        self.voteMSG = None
        self.elector = None

    @commands.command(name="start")
    async def start(self, ctx, name =None, *, description=None):
        if name is None:
            await ctx.send("voting requires a username")
            return

        #TODO - Heads up, Pings don't work in Embeds... to get around send the ping in the message using .send(content=ping) then edit the message with msg.edit(content="")
        emb = Embed(title="VOTE: "+name,
            description=f"{self.bot.config.vote_ping}\nDescription: {description}\n\
                \nReact with {self.bot.Tick} if you want them\nReact with {self.bot.Cross} if you don't",colour=Colour.blue())
        self.voteMSG = await ctx.send(embed=emb)
        await self.voteMSG.add_reaction(self.bot.Tick)
        await self.voteMSG.add_reaction(self.bot.Cross)
        self.elector = Elector()

        def check(reaction, user):
            return user == ctx.author and reaction.message == self.voteMSG and ( reaction.name == self.bot.Tick or reaction.name == self.bot.Cross )


        # TODO add voting logic, loop until vote ends
        try:
            reaction, user = await bot.wait_for("reaction_add",timeout=60.0,check=check)
        except:
            await ctx.send("You didn't respond the coin dropped into the void so we will never know the true answer.")
        else:
            value = 0 if(str(reaction.emoji) == self.bot.Tick) else 1
            await ctx.send("yay your invited!!")
            await self.voteMSG.delete()
            self.voteMSG = None
        pass

    @commands.command(name="stop")
    async def stop(self,ctx):
        print("Stop")
        pass

    @commands.command(name="remove")
    async def remove(self,ctx):
        channel = self.bot.get_channel(BOTCONFIG.VOTING_CHANNEL)
        msg =await channel.fetch_message(self.voteMSG.id)
        await ctx.send(str(msg.reactions))
        await self.on_user_reaction(msg)
        print("Removed reactions")
        pass

    async def on_user_reaction(self,msg):
        #print("All Reactions: "+str( msg.reactions))
        userReactions = [reaction for reaction in msg.reactions if not reaction.me]#filter(reaction => reaction.users.cache.has(PRIVATECONFIG.OAUTH_CLIENT_TOKEN));
        try:
            #print("User Reactions: "+str(userReactions))
            for reaction in userReactions:
                for user in await reaction.users().flatten():
                    await msg.remove_reaction(reaction.emoji, user)
        except Exception as e:
            print(str(e))



def setup(bot):
    bot.add_cog(Voting(bot))