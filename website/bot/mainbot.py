from discord.ext.commands import Bot
from discord import Color, Embed
#config
import json
from enum import Enum

class Mode(Enum):
    Percentage = 0
    Difference = 1

    def __new__(cls, value):
        member = object.__new__(cls)
        member._value_ = val
        return member

    def __int__(self):
        return self.value
    pass

class Config():

    def __init__(self):
        self.voteMode = int(Mode.Difference)#Voting has 2 modes
        self.votePing = "<@845723264550830100>"
        self.minVotes   = 3

        #Difference Configs
        self.minApprove = 2

        #Percentage Configs
        self.minPercentage = 0.6


        self.load()
        pass

    def load(self):
        with open("website\\bot\\appdata\\config.json", "r") as read_file:
            data = json.loads(read_file.read())
            print("Config: "+str(data))
            voteMode      = data["voteMode"]
            votePing      = data["votePing"]
            minVotes      = data["minVotes"]
            minApprove    = data["minApprove"]
            minPercentage = data["minPercentage"]
        pass

    def save(self):
        with open("website\\bot\\appdata\\config.json", "w") as write_file:
            json.dump(self.__dict__,write_file)
            #write_file.write(json.dump(temp))
        pass

#Config()



class Voter(object):
    id =""
    approved = False

    def __init__(self,id, approved):
        self.id = id
        self.approved = approved
    pass 

class Elector(Voter):
    votes = []
    electionsHeld = 0
    pass

bot = Bot(command_prefix="!v")

class VoteBot(object):
    def __init__(self):

        #test
        import os
        directory_path = os.getcwd()
        print("My current directory is : " + directory_path)
        folder_name = os.path.basename(directory_path)
        print("My directory name is : " + folder_name)

        self.config = Config()

        self.elect = ""#current elector being ran
        with open("website\\bot\\appdata\\token.txt","r", encoding='utf-8') as f:
            self.TOKEN           = f.readline().strip()
            self.MASTER_SERVER   = f.readline().strip()
            self.VOTING_CHANNEL  = f.readline().strip()
            self.WELCOME_CHANNEL = f.readline().strip()
            self.WELCOME_MESSAGE = f.readline().strip()

        with open("website\\bot\\appdata\\votes.json","r", encoding='utf-8') as f:
            #TOKEN = f.readline()
            #MASTER_SERVER = f.readline()
            pass
        pass

voteBot = VoteBot()

#Main commands -----------------------------
@bot.command(name="start")
async def start(ctx, name, *description):
    if not name:
        await ctx.send("voting requires a username")

    emb = Embed(title="VOTE: "+name,description= voteBot.config.votePing +"\nDescription: "+' '
                .join(description)+"\n\nReact with \u2705 for heads\nReact with \u274C for tails")
    msg = await ctx.send(embed=emb)
    await msg.add_reaction("\u2705")
    await msg.add_reaction("\u274c")
    def check(reaction, user):
            return user == ctx.author and reaction.message ==msg
    num = 1
    try:
        reaction, user = await bot.wait_for("reaction_add",timeout=60.0,check=check)
    except:
        await ctx.send("You didn't respond the coin dropped into the void so we will never know the true answer.")
    else:
        #print(str(reaction.emoji))
        if(str(reaction.emoji) == "\u2705"):
            if(num==0):
                await ctx.send("The coin lands on heads !! yay you win!!")
            else:
                await ctx.send("The coin lands on tails , you lose")
            await msg.delete()
        elif(str(reaction.emoji) == "\u274c"):
            if(num==0):
                await ctx.send("The coin lands on heads , you lose")
            else:
                await ctx.send("The coin lands on tails !! yay you win!!")
            await msg.delete()
    pass

@bot.command(name="stop")
async def stop(ctx):
    pass



#Config commands ----------------------------
@bot.command(name="min approve")
async def setMinApproval( amount):
    pass
    
@bot.command(name="min votes")
async def setToPercent(ctx, amount):
    pass

#Switches to difference voting
@bot.command(name="set difference")
async def setMinDiff(ctx, amount):
    pass

#Switches to Percentage voting
@bot.command(name="set percentage")
async def setToPercent(ctx, percent):
    pass


#Debug commands ----------------------------
@bot.command(name="msg")
async def privateMessage(ctx,id , * words):
    #await ctx.author.send("this is a test message")
    global voteBot
    user1 = await voteBot.bot.fetch_user(id)
    await user1.send("id test msg");

@bot.command(name="say")
async def repeatAfterMe( ctx, * , words):
    await ctx.message.delete()
    emb = Embed(title=words)
    msg = await ctx.send(embed=emb)

@bot.event
async def on_member_join(member):
    guild = member.guild
    global voteBot
    if(guild.id == voteBot.MASTER_SERVER):
        channel = guild.get_channel(voteBot.WELCOME_CHANNEL)
        await channel.send(voteBot.WELCOME_MESSAGE.replace("%username%",member.mention))#member.mention

@bot.event
async def on_ready():
    print("VoteInviter Starting")
    guilds = await bot.fetch_guilds(limit=None).flatten()
    #print(MASTER_SERVER +" == " +str(guilds[0].id))
    global voteBot
    for guild in guilds:
        if str(guild.id) != voteBot.MASTER_SERVER:
            print(f"Slave Server: {guild.id} : {guild.name}")
        else:
            print(f"Master Server: {guild.id} : {guild.name}")


bot.run(voteBot.TOKEN)