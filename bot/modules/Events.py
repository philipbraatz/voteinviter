from discord.ext.commands import Cog
from discord.ext import commands
from ..__init__ import BOTCONFIG, PRIVATECONFIG

class Events(Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        if(guild.id == self.bot.config.MASTER_SERVER):
            channel = guild.get_channel(self.bot.config.WELCOME_CHANNEL)
            message = self.bot.config.WELCOME_MESSAGE
            message = message.replace("(username)",member.mention)
            message = message.replace("(ruleschannel)",BOTCONFIG.RULES_CHANNEL)
            message = message.replace("(roleschannel)",BOTCONFIG.ROLES_CHANNEL)
            await channel.send()

    @commands.Cog.listener()
    async def on_ready(self):
        print("VoteInviter Started")
        guilds = await self.bot.fetch_guilds(limit=None).flatten()
        for guild in guilds:
            if str(guild.id) == str(self.bot.config.MASTER_SERVER):
                print(f"Master Server: {guild.id} : {guild.name}")
            else:
                print(f"Slave Server: {guild.id} : {guild.name}")
    
    @commands.Cog.listener()
    async def on_reaction_add(self,reaction, user):
        if(reaction.message.author.id == PRIVATECONFIG.OAUTH_CLIENT_TOKEN):
             #if a voting message and not a CHECK or CROSS
            if("VOTE: " in reaction.message):
                if(not reaction.me):
                    print(f"removed {str(reaction.emoji)} {str(user.name)}")
                    await reaction.remove(user)
                else:
                    print(f"TODO add to vote count")
                    
    @commands.Cog.listener()
    async def on_message(self,message):
        print(str(message))
        if(hasattr(message,'embed') and hasattr(message,'content') and hasattr(message,'webhook_id')):
            print(str(message.webhook_id))
        pass
        

def setup(bot):
    bot.add_cog(Events(bot))