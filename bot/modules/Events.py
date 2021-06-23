import asyncio
import sqlite3 as sl
import time
from datetime import date

from bot.dataclasses.Vote import Vote
from config.config import SetupLogging
from discord.ext import commands
from discord.ext.commands import Cog

from ..__init__ import PRIVATECONFIG
from ..dataclasses.User import Elector, Voter
from .dataclasses.ApiHelper import ApiHelper

logger = SetupLogging(__name__,True)


def RecoverFromStartup(self,elector):
    loop = asyncio.get_event_loop()
    loop.create_task(self.continueVote())
    v= elector.get_vote_count()
    ApiHelper.postVote(v["yay"], v["nay"])
    

class Events(Cog):
    db = None#sl.connect('burbVote.db')
    
    def __init__(self,bot):
        self.bot = bot
        
        Elector.db =sl.connect('burbVote.db')
        Elector.db.row_factory =sl.Row
        
        id =Elector.get_active_vote()
        if(id is not None):
            active =Elector(id)
            RecoverFromStartup(self,active)
    
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
                ApiHelper.postVote(votes['yay'],votes['nay'])

                await self.voteMSG.edit(content =f"\n[{votes['yay']}] {Vote.YAY.value}  [{votes['nay']}] {Vote.NAY.value}")
            
            await reaction.remove(user)

            if(self.bot.elector.quickVote is True):
                await asyncio.sleep(3)#secret 3 minute wait for quick voters
                if(await self.checkVoteFinished(self.bot.elector)):
                    await ApiHelper.sendInvite(self.bot.elector.id,
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
                ApiHelper.postVote(votes['yay'],votes['nay'])

                await self.voteMSG.edit(content =f"\n[{votes['yay']}] {Vote.YAY.value}  [{votes['nay']}] {Vote.NAY.value}")
                pass
            #don't care about invalid removals
             
                    
    @commands.Cog.listener()
    async def on_message(self,message):
        if(message.author.id == int(PRIVATECONFIG.WEBHOOK_ID)):
            self.webhookMSG = message
            await self.On_webhook_message()

    async def On_webhook_message(self):
        await self.webhookMSG.add_reaction(Vote.YAY.value)
        await self.webhookMSG.add_reaction(Vote.NAY.value)
        await self.webhookMSG.add_reaction(Vote.QUE.value)
        
        #logger.debug("Message: "+str(message.content))
        #for em in message.embeds:
            #logger.debug("Title: "+str(em.title))

        def Check(reaction, user):
            #logger.debug(f"Message: {reaction.message}\nID:{user.id}\nReaction:{reaction.emoji}")
            return reaction.message == self.webhookMSG and \
                user.id != int(PRIVATECONFIG.CLIENT_ID) and \
            ( reaction.emoji == Vote.YAY.value or 
                 reaction.emoji == Vote.NAY.value or
                    reaction.emoji == Vote.QUE.value
                 ) 

        hits = 0
        try:
            reaction, user = await self.bot.wait_for("reaction_add",timeout=60.0*60.0*4,check=Check)#TODO timeout set in config
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
        if(vote == Vote.NAY.value):
            await msg.channel.send(f"User has been DENIED by {mention}\nIf you want to give a reason do `!vdeny [discord name] [optional reason denied]` ")
            await self.webhookMSG.delete()
            self.webhookMSG = None
            pass
        print(f"Vote Emoji '{str(vote)}'")
        quick = " "
        if(vote == Vote.QUE.value):
            quick =" quick "
        await msg.channel.send(f"User has been{quick}approved by {mention},{quick}vote starting...")
        self.bot.elector = self.pullDataFromMessage(msg)
        await self.startVote()
        pass

    
    async def startVote(self):
        channel =await self.bot.fetch_channel(self.bot.config.VOTING_CHANNEL)
        self.bot.elector.save()
        self.bot.elector.start_vote()
        self.voteMSG = await channel.send(
            embed=self.bot.elector.voteEmbeddedMessage(self.bot),
            content=self.bot.config.VOTE_PING+f"\n[0] {Vote.YAY.value}  [0] {Vote.NAY.value}"
            )
        
        await self.ContinueVote(self.voteMSG)
        pass
     
    async def ContinueVote(self, message):
        await message.add_reaction(Vote.YAY.value)
        await message.add_reaction(Vote.NAY.value)
        
        print("URL: "+self.bot.elector.imgUrl)
        ApiHelper.startVote(
            id=self.bot.elector.id,
            avatar=self.bot.elector.imgUrl,
            name=self.bot.elector.name)
        
        await self.endVote()
        
    
    async def EndVote(self):
        print("Going to sleep")
        await asyncio.sleep(24*60)#*60
        print("Done sleeping")
        self.bot.elector.approved =self.checkVoteFinished(self.bot.elector)
        
        emb =await self.bot.elector.voteFinishMessage(self.bot,self.voteMSG.channel)
        print(f"Approved = {self.bot.elector.approved}, "+str(emb))
       
        await self.voteMSG.channel.send(
            embed=emb,
            content=self.bot.config.VOTE_PING+f"\n[0] {Vote.YAY.value}  [0] {Vote.NAY.value}"
            )
        print("Message Sent")
    
    def PullDataFromMessage(self,message):
        title = message.embeds[0].title.replace('\n','')
        username = self.findBetween(title,"Needs Approval "," AKA (")
        nickName = self.findBetween(title," AKA (",")")

        lines = str(message.embeds[0].description.split('\n'))
        relation = lines[len("Knows: "):]
        id = int(self.findBetween(lines,"||ID: ","||"))
        url = self.findBetween(lines,"||https://cdn.discordapp.com/avatars/"+str(id)+"/",".png?size=128")

        logger.debug(lines)
        logger.debug("ID-"+str(id))
        logger.debug("TITLE-"+title)
        logger.debug("DESC-"+str(lines))
        logger.debug("URL-"+str(url))
        
        elector = Elector(int(id))
        elector.imgUrl = url
        elector.vote_date = str(date.today())
        elector.name = username
        elector.nickName = nickName
        elector.description = message.content
        elector.approved = False
        elector.messageId = message.id
        elector.relationships =relation

        logger.debug(str(elector))
        return elector
    
    def FindBetween(self,s,first,last):
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        except ValueError as e:
            raise e

    def CheckVoteFinished(self, elector):
        votes =elector.get_vote_count()
        positive, negative = [votes["yay"], votes["nay"]]
        logger.info(f"{'(Quick) ' if elector.quickVote else ''}Votes Yay: {positive}, Votes Nay: {negative}")
        if(elector.quickVote and negative == 0):
            if(positive > self.bot.config.min_quick_vote):
                return True

        print(f"Positive {positive} >= min_vote and difference {positive - negative} >= {self.bot.config.min_approve}")
        return positive >= self.bot.config.min_vote and \
           positive - negative >= self.bot.config.min_approve


def setup(bot):
    bot.add_cog(Events(bot))
    pass
