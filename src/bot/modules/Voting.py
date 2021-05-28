from discord import Embed, Colour, User
from discord.ext.commands import Cog
from discord.ext import commands

class Voting(Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="start")
    async def start(self, ctx, name, *, description=None):
        if not name:
            await ctx.send("voting requires a username")

        #TODO - Heads up, Pings don't work in Embeds... to get around send the ping in the message using .send(content=ping) then edit the message with msg.edit(content="")
        emb = Embed(title="VOTE: "+name,
            description=f"{self.bot.config.voting_ping}\nDescription: {description}\n\
                \nReact with {self.bot.Tick} if you want them\nReact with {self.bot.Cross} if you don't",colour=Colour.blue())
        msg = await ctx.send(embed=emb)
        await msg.add_reaction(self.bot.Tick)
        await msg.add_reaction(self.bot.Cross)

        # TODO test if allows other reactions
        def check(reaction, user):
            return user == ctx.author and reaction.message == msg and ( reaction.name == self.bot.Tick or reaction.name == self.bot.Cross )


        # TODO add voting logic, loop until vote ends
        try:
            reaction, user = await bot.wait_for("reaction_add",timeout=60.0,check=check)
        except:
            await ctx.send("You didn't respond the coin dropped into the void so we will never know the true answer.")
        else:
            value = 0 if(str(reaction.emoji) == self.bot.Tick) else 1
            await ctx.send("yay your invited!!")
            await msg.delete()
        pass

    @commands.command(name="stop")
    async def stop(self,ctx):
        print("Stop")
        pass


def setup(bot):
    bot.add_cog(Voting(bot))