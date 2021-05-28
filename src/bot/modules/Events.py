from discord.ext.commands import Cog
from discord.ext import commands

class Events(Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener
    async def on_member_join(self, member):
        guild = member.guild
        if(guild.id == self.bot.config.MASTER_SERVER):
            channel = guild.get_channel(self.bot.config.WELCOME_CHANNEL)
            await channel.send(self.bot.config.WELCOME_MESSAGE.replace("%username%",member.mention))

    @commands.Cog.listener
    async def on_ready(self):
        print("VoteInviter Started")
        guilds = await bot.fetch_guilds(limit=None).flatten()
        for guild in guilds:
            if str(guild.id) == str(self.bot.config.MASTER_SERVER):
                print(f"Master Server: {guild.id} : {guild.name}")
            else:
                print(f"Slave Server: {guild.id} : {guild.name}")
    

def setup(bot):
    bot.add_cog(Events(bot))