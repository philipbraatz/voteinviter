from bot.dataclasses.Vote import Vote
from discord.ext.commands import Cog
from discord.ext import commands
from ..__init__ import PRIVATECONFIG
import time
from datetime import date
from ..dataclasses.User import Elector, Voter
from ..dataclasses.API import Api
import asyncio

from config.config import setupLogging
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
            await guild.get_channel(self.bot.config.WELCOME_CHANNEL) \
                .send(self.bot.replaceDynamicText(
                    self.bot.config.WELCOME_MESSAGE,
                    member.name,
                    self.bot.config.RULES_CHANNEL,
                    self.bot.config.ROLES_CHANNEL)
                    )


    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.end = time.time()
        logger.info(f"VoteInviter Started in {round(self.bot.end - self.bot.startt, 2)} seconds")
        
        #display servers and Master
        guilds = await self.bot.fetch_guilds(limit=None).flatten()
        for guild in guilds:
            isMaster = str(guild.id) == str(self.bot.config.MASTER_SERVER)
            logger.info(f"{'Master' if isMaster else 'Slave'} Server: {guild.id} : {guild.name}")
    

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
                voter.nickName = user.nick
                voter.name = user.name
                voter.voteFor = self.bot.elector.id

                self.bot.elector.add_vote(reaction.emoji == Vote.YAY.value,voter)
                votes =self.bot.elector.get_vote_count()
                Api.postVote(votes['yay'],votes['nay'])

                await self.voteMSG.edit(content =f"\n[{votes['yay']}] {Vote.YAY.value}  [{votes['nay']}] {Vote.NAY.value}")
            
            await reaction.remove(user)

            if(self.bot.elector.quickVote is True):
                await asyncio.sleep(60*3)#secret 3 minute wait for quick voters
                if(self.checkVoteFinished(self.bot.elector)):
                    await Api.sendInvite(self.bot.elector.id,
                    self.bot.addMemberToGuild(self.bot.elector.id))

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
                voter.nickName = user.nick
                voter.voteFor = self.bot.elector.id

                self.bot.elector.remove_vote(reaction.emoji == Vote.YAY.value,voter)
                votes =self.bot.elector.get_vote_count()
                Api.postVote(votes['yay'],votes['nay'])

                await self.voteMSG.edit(content =f"\n[{votes['yay']}] {Vote.YAY.value}  [{votes['nay']}] {Vote.NAY.value}")
                pass
            #don't care about invalid removals
             
                    
    @commands.Cog.listener()
    async def on_message(self,message):
        if(message.author.id == int(PRIVATECONFIG.WEBHOOK_ID)):
            self.webhookMSG = message
            await self.on_webhook_message()

    async def on_webhook_message(self):
        await self.webhookMSG.add_reaction(Vote.YAY.value)
        await self.webhookMSG.add_reaction(Vote.NAY.value)
        await self.webhookMSG.add_reaction(Vote.QUE.value)
        
        #logger.debug("Message: "+str(message.content))
        #for em in message.embeds:
            #logger.debug("Title: "+str(em.title))

        def check(reaction, user):
            #logger.debug(f"Message: {reaction.message}\nID:{user.id}\nReaction:{reaction.emoji}")
            return reaction.message == self.webhookMSG and \
                user.id != int(PRIVATECONFIG.CLIENT_ID) and \
            ( reaction.emoji == Vote.YAY.value or 
                 reaction.emoji == Vote.NAY.value or
                    reaction.emoji == Vote.QUE.value
                 ) 

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
                await self.on_voteBot_reaction(reaction.emoji,reaction.message,user.mention)
        pass

    async def on_voteBot_reaction(self, vote, msg, mention):
        if(vote == Vote.NAY):
            await msg.channel.send(f"User has been DENIED by {mention}\nIf you want to give a reason do `!vdeny [discord name] [optional reason denied]` ")
            await self.webhookMSG.delete()
            self.webhookMSG = None
            pass
        logger.debug(str(vote))
        quick = " "
        if(vote == Vote.QUE):
            quick =" quick "
        await msg.channel.send(f"User has been{quick}approved by {mention},{quick}vote starting...")
        self.bot.elector = self.pullDataFromMessage(msg)
        await self.startVote()
        pass

    
    async def startVote(self):
        channel =await self.bot.fetch_channel(self.bot.config.VOTING_CHANNEL)
        self.bot.elector.start_vote()
        self.voteMSG = await channel.send(
            embed=self.bot.elector.voteEmbeddedMessage(self.bot),
            content=self.bot.config.VOTE_PING+f"\n[0] {Vote.YAY.value}  [0] {Vote.NAY.value}"
            )
        await self.voteMSG.add_reaction(Vote.YAY.value)
        await self.voteMSG.add_reaction(Vote.NAY.value)
        Api.startVote(
            id=self.bot.elector.id,
            avatar=self.bot.elector.imgUrl,
            name=self.bot.elector.name)
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
        elector.vote_date = str(date.today())
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

    def checkVoteFinished(self, elector):
        votes = elector.getVotes()
        positive, negative = [votes["Check"], votes["Cross"]]
        if(elector.quickVote and negative == 0):
            if(positive > self.bot.min_quick_vote):
                return True

        return positive > self.bot.min_vote and \
           positive - negative > self.bot.min_approve


def setup(bot):
    bot.add_cog(Events(bot))
    pass
