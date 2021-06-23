from bot.dataclasses.CrudOp import Crud
from bot.dataclasses.Vote import Vote
from config.config import SetupLogging
from discord import Colour, Embed

logger = SetupLogging(__name__)



#Person in the server
class Voter(object):

    def __init__(self, id):  
        if(id < 0): return
        super().__init__(id)
        
        self.id = id
        self.imgUrl = None
        self.name = None
        self._exists = False
        
        self.approved = False
        self.vote_date = None
        self.nickName = None
        self.yay = None
        self.voteFor = None
        
        Crud.SetData("""CREATE TABLE IF NOT EXISTS elector (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                isApproved INTEGER NOT NULL,
                electionsHeld INTEGER NOT NULL,
                vote_date DATE,
                [name] TEXT,
                imgUrl TEXT,
                nickName TEXT,
                [description] TEXT,
                relationships TEXT,
                quick INTEGER
            );""")
        
        self.id = id
        self.Construct(Crud.GetData("""Select id, isApproved, nickName, imgUrl, name FROM elector
                    WHERE id = ?""",(str(self.id),),False))
        

    def __repr__(self):
        return "Voter([Name:{},Approved:{},Date:{}])".format(self.name, self.approved, self.vote_date)

    def ConstructVote(self,vote):
        self.id = int(vote["voterid"])
        self.voteFor = vote["elector"]
        self.yay =vote["yay"] == 1
        return self
    
    def Construct(self,elector):
        if(elector == None):
            return self._exists
        self._exists = True

        self.id = int(elector["id"])
        self.approved = elector["isApproved"]
        self.name = elector["name"]
        self.imgUrl = elector["imgUrl"]
        self.nickName = elector["nickName"]
    pass 


#Person who is currently being voted on
class Elector(Voter):

    def __init__(self, id):
        super().__init__(id)
        self.votes = [] #array of Voters
        self.electionsHeld = 0 

        #Election info
        self.description = "" #only needed during election
        self.relationships = "" #people they know from the server
        self.quickVote = False
        self.messageId = 0
        self.inviteLink =None

        Crud.SetData("""CREATE TABLE IF NOT EXISTS elector (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                isApproved INTEGER NOT NULL,
                electionsHeld INTEGER NOT NULL,
                vote_date DATE,
                [name] TEXT,
                imgUrl TEXT,
                nickName TEXT,
                [description] TEXT,
                relationships TEXT,
                quick INTEGER,
                messageId INTEGER,
                inviteLink TEXT
            );""")

        self.id = id
        
        result =Crud.GetData("""SELECT * FROM elector WHERE id = ?""",(str(self.id),),False)
        if(self.Construct(result) is not None):
            Crud.SetData("""CREATE TABLE IF NOT EXISTS vote (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                voterid INTEGER NOT NULL,
                elector INTEGER NOT NULL,
                yay INTEGER
            );""")
            
            for vote in Crud.GetData("""SELECT * FROM vote
                        WHERE elector = ?""",(str(self.id),)):
                self.votes.append(self.constructVote(vote))
                pass
        pass
    pass

    def Construct(self, elector):
        if(elector is None):
            return self._exists
        self._exists = True
        
        super().Construct(elector)
        self.electionsHeld =elector["electionsHeld"]
        self.name = elector["name"]
        self.description = elector["description"]
        self.relationships = elector["relationships"]
        self.quickVote =elector["quick"] == 1
        self.messageId = elector["messageId"]
        self.inviteLink = elector["inviteLink"]
        

    def __repr__(self):
        return "Elector({},[Desc:{},Votes:{},Elections:{},Relations:{}])"\
            .format(super().__repr__(),self.description, len(self.votes),self.electionsHeld, self.relationships)

    def Save(self):
        con = Elector.db.cursor()
    
        existing =Crud.GetData("""SELECT id,isApproved,electionsHeld,vote_date,[name],imgUrl,nickName,[description],relationships,quick, messageId
                        FROM elector
                        WHERE id = ?;""",(self.id,),False)
        if(existing is None):
            Crud.SetData("""INSERT INTO elector(
                id,isApproved,electionsHeld,vote_date,[name],imgUrl,nickName,[description],relationships,quick, messageId)
                VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                (str(self.id),self.approved,self.electionsHeld,self.vote_date,self.name,self.imgUrl,self.nickName,self.description,self.relationships,self.quickVote,self.messageId))
        else:
            Crud.SetData("""UPDATE elector SET
                        isApproved=?,electionsHeld=?,vote_date=?,[name]=?,imgUrl=?,nickName=?,[description]=?,relationships=?,quick=?,messageId=?
                        WHERE id = ?
                        """,(self.approved,existing["electionsHeld"]+1,self.vote_date,self.name,self.imgUrl,self.nickName,self.description,self.relationships,self.quickVote,str(self.id),self.messageId))

    def VoteEmbeddedMessage(self):
        embedthing = Embed(title=f"VOTE: {self.name} ({self.nickName})",
            description=f"\nDescription: {self.description}\n\
                \nReact with {Vote.YAY.value} if you want them\nReact with {Vote.NAY.value} if you don't",colour=Colour.blue())
        embedthing.set_thumbnail(url="https://cdn.discordapp.com/avatars/"+str(self.id)+"/"+str(self.imgUrl)+".png?size=128")
        return embedthing
    
    async def VoteFinishMessage(self,bot,channel):
        if(self.approved):
            invite = await channel.create_invite(
                max_age= bot.config.invite_expire_time,
                max_usages=1,
                unique=False,
                reason=f"{bot.elector.name} has passed the vote"
                )
            print(str(invite))

        endVotes =self.GetVoteCount()
        message = f"Please welcome our new member! [your invite link!](<{invite}>)" if self.approved else "They did not pass the vote :("
        embedthing = Embed(title=f"Voting has ended for {self.name} ({self.nickName})",
        description=f"Result: {Vote.YAY.value}[**{endVotes['yay']}**] | {Vote.NAY.value}[**{endVotes['nay']}**]\n\
            \n{message}",colour=Colour.blue())
        embedthing.set_thumbnail(url="https://cdn.discordapp.com/avatars/"+self.id+"/"+self.imgUrl+".png?size=128")
        return embedthing

    def Start_vote(self):
        Crud.SetData("""CREATE TABLE IF NOT EXISTS vote (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                voterid INTEGER NOT NULL,
                elector INTEGER NOT NULL,
                yay INTEGER
            );""")
        
        Crud.SetData("""DELETE FROM vote
                    WHERE elector = ?""",(str(self.id),))
    
    def AddVote(self,positiveVote, user):
        self.RemoveVote(positiveVote,user)
        con = Elector.db.cursor()
        Crud.SetData("""INSERT INTO vote ( voterid, elector, yay) values(?, ?, ?);""",
                    (str(user.id),str(self.id), positiveVote))
    
    def RemoveVote(self,positiveVote, user):
        con = Elector.db.cursor()
        Crud.SetData("""DELETE FROM vote
                        WHERE voterid = ?;""",(user.id,))

    def GetVoteCount(self):
        data = Elector.getData("""SELECT yay ,COUNT(*) as [count] FROM vote
                    WHERE elector = ?
                    GROUP BY yay
                    ORDER BY yay;""",(self.id,))
        
        voteCount ={"yay":0,"nay":0}
    
        lend =len(data)
        if(lend > 1):
            voteCount = {"yay":data[1]["count"],"nay":data[0]["count"]}
        elif(lend==1):
            if(data[0]["yay"] == 1):
                voteCount = {"yay":data[0]["count"],"nay":0}
            else:
                voteCount = {"yay":0,"nay":data[0]["count"]}
            
        return voteCount
