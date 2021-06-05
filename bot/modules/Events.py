from discord.ext.commands import Cog
from discord.ext import commands
from ..__init__ import BOTCONFIG, PRIVATECONFIG
from config.config import setupLogging
import json
import time
from datetime import date
from ..dataclasses.User import Elector, Voter
import asyncio

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
        
        #display servers and Master
        guilds = await self.bot.fetch_guilds(limit=None).flatten()
        for guild in guilds:
            if str(guild.id) == str(self.bot.config.MASTER_SERVER):
                logger.info(f"Master Server: {guild.id} : {guild.name}")
            else:
                logger.info(f"Slave Server: {guild.id} : {guild.name}")
    
    @commands.Cog.listener()
    async def on_reaction_add(self,reaction, user):
        #logger.debug(reaction.message.content)
        if(self.bot.check_user_reaction(reaction,user)):
            if(reaction.me):
                #valid votes
                logger.debug(f"ADDING VOTE: {user.name} - {reaction.emoji}")

                #TODO load data
                voter = Voter(user.id)
                voter.approved = True
                voter.name = user.name

                print("BIRD: "+str(PRIVATECONFIG.CLIENT_ID)+" == "+str(user.id))
                self.bot.elector.add_vote(await self.bot.cleanVoteToBool(reaction),voter)
                votes =self.bot.elector.getVotes()
                print(str(votes))
                await self.voteMSG.edit(content =f"\n[{votes['Check']}] {self.bot.Tick}  [{votes['Cross']}] {self.bot.Cross}")
            await reaction.remove(user)

    @commands.Cog.listener()
    async def on_reaction_remove(self,reaction, user):
        #logger.debug(reaction.message.content)
        if(self.bot.check_user_reaction(reaction,user)):
            if(reaction.me):
                logger.debug(f"REMOVING VOTE: {user.name} - {reaction.emoji}")

                #TODO load data
                voter = Voter(user.id)
                voter.approved = True
                voter.name = user.name

                self.bot.elector.remove_vote(await self.bot.cleanVoteToBool(reaction),voter)
                votes =self.bot.elector.getVotes()
                await self.voteMSG.edit(content =f"\n[{votes['Check']}] {self.bot.Tick}  [{votes['Cross']}] {self.bot.Cross}")
                pass
            #don't care about invalid removals
             
                    
    @commands.Cog.listener()
    async def on_message(self,message):
        if(message.author.id == int(PRIVATECONFIG.WEBHOOK_ID)):
            self.webhookMSG = message
            await self.on_webhook_message()

    async def on_webhook_message(self):
        await self.webhookMSG.add_reaction(self.bot.Tick)
        await self.webhookMSG.add_reaction(self.bot.Cross)
        
        #logger.debug("Message: "+str(message.content))
        #for em in message.embeds:
            #logger.debug("Title: "+str(em.title))

        def check(reaction, user):
            #logger.debug(f"Message: {reaction.message}\nID:{user.id}\nReaction:{reaction.emoji}")
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
                await self.webhookMSG.channel.send("Vote is stale, please do `!vapprove [discord name]` or `!vdeny [discord name] [optional reason denied]`")
        else:
            #Gets called Twice, idk why
            hits+=1
            if(hits >= 1):
                hits = 0
                await self.on_voteBot_reaction(await self.bot.cleanVoteToBool(reaction),reaction.message,user.mention)
        pass

    async def on_voteBot_reaction(self, isTick, msg, mention):
        if(isTick != None):
            if(isTick):
                await msg.channel.send(f"User has been approved by {mention}, vote starting...")
                self.bot.elector= self.pullDataFromMessage(msg)
                await self.startVote()
            else:
                await msg.channel.send(f"User has been DENIED by {mention}\nIf you want to give a reason do `!vdeny [discord name] [optional reason denied]` ")
                pass#TODO SAVE as denied
        await self.webhookMSG.delete()
        self.webhookMSG = None
        pass

    
    async def startVote(self):
        channel =await self.bot.fetch_channel(BOTCONFIG.VOTING_CHANNEL)
        self.voteMSG = await channel.send(
            embed=self.bot.elector.voteEmbeddedMessage(self.bot),
            content=BOTCONFIG.VOTE_PING+f"\n[0] {self.bot.Tick}  [0] {self.bot.Cross}"
            )
        await self.voteMSG.add_reaction(self.bot.Tick)
        await self.voteMSG.add_reaction(self.bot.Cross)
        pass
    
    def pullDataFromMessage(self,message):
        title = message.embeds[0].title
        username = self.findBetween(title,"Needs Approval "," AKA (")
        nickName = self.findBetween(title," AKA (",")")

        lines = message.embeds[0].description.split("\n")
        relation = lines[0][len("Knows: "):]
        id = self.findBetween(lines[1].strip(),"||ID: ","||")
        url = self.findBetween(lines[2].strip(),"||","]||")

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