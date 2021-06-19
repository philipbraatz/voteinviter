from datetime import datetime
from discord import Embed, Colour
import json
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
        return "User([ID:{},Name:{},URL:{}])".format(self.id, self.name, self.imgUrl)


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
        super().__init__(id)  
        
        self.approved = False
        self.vote_date = None
        self.nickName = None
        self.yay = None
        self.voteFor = None
        
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
                quick INTEGER
            );""")
        
        self.id = id
        Vote.construct(con.execute("""Select id, isApproved, nickName, imgUrl, name FROM elector
                    WHERE id = ?""",(self.id,)).fetchone())
        

    def __repr__(self):
        return "Voter([Name:{},Aprvd:{},Date:{}])".format(self.name, self.approved, self.vote_date)

    def constructVote(vote):
        self = Voter()
        self.id = vote["voterid"]
        self.voteFor = vote["elector"]
        self.yay =vote["yay"] == 1
        return self
    
    def construct(elector):
        self = Voter()
        if(elector is not None):
            return self._exists
        self._exists = True
        
        self.id = elector["id"]
        self.approved = elector["isApproved"]
        self.vote_date = elector["vote_date"]
        self.name = elector["name"]
        self.imgUrl = elector["imgUrl"]
        self.nickName = elector["nickName"]

    pass 


#Person who is currently being voted on
class Elector(Voter):

    db =sl.connect('burbVote.db')
    db.row_factory = sl.Row

    def __init__(self, id):
        
        self.votes = [] #array of Voters
        self.electionsHeld = 0 

        #Election info
        self.description = "I am a cool user" #only needed during election
        self.relationships = "Nobody loves me" #people they know from the server
        self.quickVote = False

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
                quick INTEGER
            );""")

        self.id = id
        if(self.construct(con.execute("""SELECT * FROM elector WHERE id = ?""",(self.id,)).fetchone()) is not None):
            for vote in con.execute("""SELECT * FROM vote
                        WHERE elector = ?""",self.id):
                self.votes.append(Vote.constructVote(vote))
                pass
        pass
    pass

    def construct(self, elector):
        if(elector is not None):
            return self._exists
        self._exists = True
        
        super().construct(elector)
        self.electionsHeld =elector["electionsHeld"]
        self.name = elector["name"]
        self.description = elector["description"]
        self.relationships = elector["relationships"]
        self.quickVote =elector["quick"] == 1
        

    def __repr__(self):
        return "Elector({},[Desc:{},Votes:{},Elections:{},Relations:{}])".format(super().__repr__(),self.description, len(self.votes),self.electionsHeld, self.relationships)

    def save(self):
        con = Elector.db.cursor()
        con.execute("""INSERT INTO elector(
            id,isApproved,electionsHeld,vote_date,[name],imgUrl,nickName,[description],relationships,quick)
            VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
            (self.id,self.approved,self.electionsHeld,self.vote_date,self.name,self.imgUrl,self.nickName,self.description,self.relationships,self.quickVote))

    def voteEmbeddedMessage(self,bot):
        embedthing = Embed(title=f"VOTE: {self.name} ({self.nickName})",
            description=f"\nDescription: {self.description}\n\
                \nReact with {Vote.YAY.value} if you want them\nReact with {Vote.NAY.value} if you don't",colour=Colour.blue())
        embedthing.set_thumbnail(url=self.imgUrl)
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
                    WHERE elector = ?""",(self.id,))
        pass
    
    def add_vote(self,positiveVote, user):
        con = Elector.db.cursor()
        con.execute("""INSERT INTO vote (id, voterid, elector, yay) values(?, ?, ?);""",
                    (self.id, user.id, positiveVote))
    
    def remove_vote(self,positiveVote, user):
        con = Elector.db.cursor()
        con.execute("""DELETE FROM vote
                        WHERE voterid = ?;""",(user.id,))

    def get_vote_count(self):
        con = Elector.db.cursor()
        data = con.execute("""SELECT yay ,COUNT(*) as [count] FROM vote
                    GROUP BY yay
                    ORDER BY yay;""")

        voteCount ={}
        
        
        lend =len(data)
        if(lend > 1):
            voteCount = {"yay":data[1]["count"],"nay":data[0]["count"]}
        elif(lend==1):
            if(data[0]["yay"] == 1):
                voteCount = {"yay":data[0]["count"],"nay":0}
            else:
                voteCount = {"yay":0,"nay":data[0]["count"]}
            
        return voteCount