from discord.ext.commands import Cog
from discord.ext import commands
from ..__init__ import BOTCONFIG, PRIVATECONFIG
from config.config import setupLogging
import json
import time
from datetime import date
from ..dataclasses.User import Elector, Voter

from logging import getLogger
logger = getLogger(__name__)
setupLogging(logger)

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
        self.bot.end = time.time()
        logger.info(f"VoteInviter Started in {round(self.bot.end-self.bot.startt,2)} seconds")
        guilds = await self.bot.fetch_guilds(limit=None).flatten()
        for guild in guilds:
            if str(guild.id) == str(self.bot.config.MASTER_SERVER):
                logger.info(f"Master Server: {guild.id} : {guild.name}")
            else:
                logger.info(f"Slave Server: {guild.id} : {guild.name}")
    
    @commands.Cog.listener()
    async def on_reaction_add(self,reaction, user):
        #logger.debug(reaction.message.content)
        if(reaction.message.author.id == int(PRIVATECONFIG.CLIENT_ID) and
            user.id != PRIVATECONFIG.CLIENT_ID and
            user.id != PRIVATECONFIG.WEBHOOK_ID):
             #if a voting message and not a CHECK or CROSS
             if(len(reaction.message.embeds) > 0):
                if("VOTE: " in reaction.message.embeds[0].title):
                    if(not reaction.me):
                        logger.debug(f"removed {str(reaction.emoji)} {str(user.name)}")
                        await reaction.remove(user)
                    else:
                        logger.debug(f"TODO add to vote count")
                    
    @commands.Cog.listener()
    async def on_message(self,message):
            #logger.debug("Author of message: "+str(message.author.id))
            if(message.author.id == int(PRIVATECONFIG.WEBHOOK_ID)):
                self.webhookMSG = message
                await self.webhookMSG.add_reaction(self.bot.Tick)
                await self.webhookMSG.add_reaction(self.bot.Cross)
                
                #logger.debug("Message: "+str(message.content))
                #for em in message.embeds:
                    #logger.debug("Title: "+str(em.title))

                def check(reaction, user):
                    logger.debug(f"Message: {reaction.message}\nID:{user.id}\nReaction:{reaction.emoji}")
                    return reaction.message == self.webhookMSG and \
                        user.id != int(PRIVATECONFIG.CLIENT_ID) and \
                    ( reaction.emoji == self.bot.Tick or reaction.emoji == self.bot.Cross ) 

                hits = 0
                try:
                    reaction, user = await self.bot.wait_for("reaction_add",timeout=60.0*60.0*4,check=check)#TODO timeout set in config
                except Exception as e:
                    hits+=1
                    if(hits >= 1):
                        hits = 0
                        logger.warning(str(e))
                        await message.channel.send("Vote is stale, please do `!vapprove [discord name]` or `!vdeny [discord name] [optional reason denied]`")
                else:
                    #Gets called Twice, idk why
                    hits+=1
                    if(hits >= 1):
                        hits = 0
                        if(str(reaction.emoji) == self.bot.Tick):
                            await message.channel.send(f"User has been approved by {user.mention}, vote starting...")
                            self.bot.elector= self.pullDataFromMessage(message)
                        elif(str(reaction.emoji) == self.bot.Cross):
                            await message.channel.send(f"User has been DENIED by {user.mention}\nIf you want to give a reason do `!vdeny [discord name] [optional reason denied]` ")
                        await self.webhookMSG.delete()
                        self.webhookMSG = None
                pass

    def startVote(self):

        pass
    
    def pullDataFromMessage(self,message):
        title = message.embeds[0].title
        username = self.findBetween(title,"Needs Approval "," AKA (")
        nickName = self.findBetween(title," AKA (",")")

        lines = message.embeds[0].description.split("\n")
        relation = lines[0][len("Knows: "):]
        id = self.findBetween(lines[1].strip(),"||ID: ","||")
        url = self.findBetween(lines[2].strip(),"||","||")

        logger.debug("TITLE-"+title)
        logger.debug("DESC-"+str(lines))
        
        elector = Elector(id)
        elector.imgUrl = url
        elector.vote_date = date.today()
        elector.name = username
        elector.nickName = nickName
        elector.description = message.content
        elector.approved = False

        logger.debug(str(elector))
        return elector
    
    def findBetween(self,s,first,last):
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        except ValueError:
            return ""


def setup(bot):
    bot.add_cog(Events(bot))
    pass