from datetime import datetime
from discord import Embed, Colour
from bot.dataclasses.Vote import Vote
import sqlite3 as sl

from config.config import setupLogging
from logging import getLogger
logger = getLogger(__name__)
setupLogging(logger)

class User(object):
    def __init__(self, id):
        self.id = id
        self.imgUrl = None
        self.name = None
        self._exists = False
    pass

    def __repr__(self):
        return "User([ID:{},Name:{},URL:{}])".format(str(self.id), self.name, self.imgUrl)


#Person in the server
class Voter(User):
    """AI is creating summary for Voter

    Args:
        User ([type]): [description]

    Returns:
        [type]: [description]
    """
    
    db =sl.connect('burbVote.db')
    db.row_factory = sl.Row

    def __init__(self, id):  
        if(id < 0): return
        super().__init__(id)
        
        self.approved = False
        self.vote_date = None
        self.nickName = None
        self.yay = None
        self.voteFor = None
        
        con = Voter.db.cursor()
        con.execute("""CREATE TABLE IF NOT EXISTS elector (
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
        self.construct(con.execute("""Select id, isApproved, nickName, imgUrl, name FROM elector
                    WHERE id = ?""",(str(self.id),)).fetchone())
        

    def __repr__(self):
        return "Voter([Name:{},Aprvd:{},Date:{}])".format(self.name, self.approved, self.vote_date)

    def constructVote(self,vote):
        self.id = int(vote["voterid"])
        self.voteFor = vote["elector"]
        self.yay =vote["yay"] == 1
        return self
    
    def construct(self,elector):
        if(elector == None):
            return self._exists
        self._exists = True
        
        #print(str(elector))
        self.id = int(elector["id"])
        self.approved = elector["isApproved"]
        self.name = elector["name"]
        self.imgUrl = elector["imgUrl"]
        self.nickName = elector["nickName"]

    pass 


#Person who is currently being voted on
class Elector(Voter):

    db = None#sl.connect('burbVote.db')

    def __init__(self, id):
        super().__init__(id)
        self.votes = [] #array of Voters
        self.electionsHeld = 0 

        #Election info
        self.description = "I am a cool user" #only needed during election
        self.relationships = "Nobody loves me" #people they know from the server
        self.quickVote = False
        self.messageid = 0
        self.inviteLink =None

        con = Elector.db.cursor()
        con.execute("""CREATE TABLE IF NOT EXISTS elector (
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
        
        result =con.execute("""SELECT * FROM elector WHERE id = ?""",(str(self.id),)).fetchone()
        if(self.construct(result) is not None):
            con = Elector.db.cursor()
            con.execute("""CREATE TABLE IF NOT EXISTS vote (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                voterid INTEGER NOT NULL,
                elector INTEGER NOT NULL,
                yay INTEGER
            );""")
            
            for vote in con.execute("""SELECT * FROM vote
                        WHERE elector = ?""",(str(self.id),)):
                self.votes.append(self.constructVote(vote))
                pass
        pass
    pass

    def construct(self, elector):
        if(elector is None):
            return self._exists
        self._exists = True
        
        super().construct(elector)
        self.electionsHeld =elector["electionsHeld"]
        self.name = elector["name"]
        self.description = elector["description"]
        self.relationships = elector["relationships"]
        self.quickVote =elector["quick"] == 1
        self.messageId = elector["messageId"]
        self.inviteLink = elector["inviteLink"]
        

    def __repr__(self):
        return "Elector({},[Desc:{},Votes:{},Elections:{},Relations:{}])".format(super().__repr__(),self.description, len(self.votes),self.electionsHeld, self.relationships)

    def save(self):
        con = Elector.db.cursor()
    
        existing =con.execute("""SELECT id,isApproved,electionsHeld,vote_date,[name],imgUrl,nickName,[description],relationships,quick, messageId
                        FROM elector
                        WHERE id = ?;""",(self.id,)).fetchone()
        if(existing is None):
            con.execute("""INSERT INTO elector(
                id,isApproved,electionsHeld,vote_date,[name],imgUrl,nickName,[description],relationships,quick, messageId)
                VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                (str(self.id),self.approved,self.electionsHeld,self.vote_date,self.name,self.imgUrl,self.nickName,self.description,self.relationships,self.quickVote,self.messageid))
        else:
            con.execute("""UPDATE elector SET
                        isApproved=?,electionsHeld=?,vote_date=?,[name]=?,imgUrl=?,nickName=?,[description]=?,relationships=?,quick=?,messageId=?
                        WHERE id = ?
                        """,(self.approved,existing["electionsHeld"]+1,self.vote_date,self.name,self.imgUrl,self.nickName,self.description,self.relationships,self.quickVote,str(self.id),self.messageid))
        Elector.db.commit()

    def voteEmbeddedMessage(self,bot):
        embedthing = Embed(title=f"VOTE: {self.name} ({self.nickName})",
            description=f"\nDescription: {self.description}\n\
                \nReact with {Vote.YAY.value} if you want them\nReact with {Vote.NAY.value} if you don't",colour=Colour.blue())
        embedthing.set_thumbnail(url="https://cdn.discordapp.com/avatars/"+str(self.id)+"/"+str(self.imgUrl)+".png?size=128")
        return embedthing
    
    async def voteFinishMessage(self,bot,channel):
        if(self.approved):
            invite = await channel.create_invite(
                max_age= bot.config.invite_expire_time,
                max_usages=1,
                unique=False,
                reason=f"{bot.elector.name} has passed the vote"
                )
            print(str(invite))

        endVotes =self.get_vote_count()
        message = f"Please welcome our new member! [your invite link!](<{invite}>)" if self.approved else "They did not pass the vote :("
        embedthing = Embed(title=f"Voting has ended for {self.name} ({self.nickName})",
        description=f"Result: {Vote.YAY.value}[**{endVotes['yay']}**] | {Vote.NAY.value}[**{endVotes['nay']}**]\n\
            \n{message}",colour=Colour.blue())
        embedthing.set_thumbnail(url="https://cdn.discordapp.com/avatars/"+self.id+"/"+self.imgUrl+".png?size=128")
        return embedthing

    def start_vote(self):
        con = Elector.db.cursor()
        con.execute("""CREATE TABLE IF NOT EXISTS vote (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                voterid INTEGER NOT NULL,
                elector INTEGER NOT NULL,
                yay INTEGER
            );""")
        
        con.execute("""DELETE FROM vote
                    WHERE elector = ?""",(str(self.id),))
        Elector.db.commit()
        pass
    
    def add_vote(self,positiveVote, user):
        self.remove_vote(positiveVote,user)
        con = Elector.db.cursor()
        con.execute("""INSERT INTO vote ( voterid, elector, yay) values(?, ?, ?);""",
                    (str(user.id),str(self.id), positiveVote))
        Elector.db.commit()
    
    def remove_vote(self,positiveVote, user):
        con = Elector.db.cursor()
        con.execute("""DELETE FROM vote
                        WHERE voterid = ?;""",(user.id,))
        Elector.db.commit()

    def get_vote_count(self):
        con = Elector.db.cursor()
        data = con.execute("""SELECT yay ,COUNT(*) as [count] FROM vote
                    WHERE elector = ?
                    GROUP BY yay
                    ORDER BY yay;""",(self.id,)).fetchall()
        Elector.db.commit()

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
    
    @staticmethod
    def get_active_vote():
        con = Elector.db.cursor()
        existing =con.execute("""SELECT id FROM elector
            WHERE vote_date >datetime('now','-1 day');""").fetchone()
        return existing