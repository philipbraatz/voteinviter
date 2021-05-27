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
            description=f"{self.bot.config.votingPing}\nDescription: {description}\n\
                \nReact with {self.bot.Tick} for heads\nReact with {self.bot.Cross} for tails",colour=Colour.blue())
        msg = await ctx.send(embed=emb)
        await msg.add_reaction(self.bot.Tick)
        await msg.add_reaction(self.bot.Cross)
        num = 1
        try:
            reaction, user = await bot.wait_for("reaction_add",timeout=60.0,check=lambda reaction, user:  user == ctx.author and reaction.message == msg and ( reaction.name == self.bot.Tick or reaction.name == self.bot.Cross ))
        except:
            await ctx.send("You didn't respond the coin dropped into the void so we will never know the true answer.")
        else:
            # num = 0 == HEADS
            # num = 1 == TAILS
            value = 0 if(str(reaction.emoji) == self.bot.Tick) else 1
            message = "yay you win!!" if (num == value) else "you lose."

            if(num==0):
                await ctx.send(f"The coin lands on heads, {message}")
            else:
                await ctx.send(f"The coin lands on tails, {message}")
            await msg.delete()
        pass

    @commands.command(name="stop")
    async def stop(self,ctx):
        print("Stop")
        pass


def setup(bot):
    bot.add_cog(Voting(bot))