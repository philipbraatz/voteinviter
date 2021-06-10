from datetime import datetime
from discord import Embed, Colour
import json

class User(object):
    id = None
    imgUrl = None
    name = None

    def __init__(self, id):
        self.id = id
    pass

    def __repr__(self):
        return "User([ID:{},Name:{},URL:{}])".format(self.id, self.name, self.imgUrl)


#Person in the server
class Voter(User):
    approved = False
    vote_date = None
    nickName = None


    def __init__(self, id):
        super().__init__(id)
    def __repr__(self):
        return "Voter([Name:{},Aprvd:{},Date:{}])".format(self.name, self.approved, self.vote_date)

    pass 

#Person who is currently being voted on
class Elector(Voter):
    votes = [] #array of Voters
    electionsHeld = 0 

    #Election info
    description = "I am a cool user" #only needed during election
    relationships = "Nobody loves me" #people they know from the server
    quickVote = False

    def __init__(self, id):
        super().__init__(id)
        self.approved = vote_date = datetime.now()
    pass

    def __repr__(self):
        return "Elector({},[Desc:{},Votes:{},Elections:{},Relations:{}])".format(super().__repr__(),self.description, len(self.votes),self.electionsHeld, self.relationships)

    def voteEmbeddedMessage(self,bot):
        embedthing = Embed(title=f"VOTE: {self.name} ({self.nickName})",
            description=f"\nDescription: {self.description}\n\
                \nReact with {bot.YAY} if you want them\nReact with {bot.NAY} if you don't",colour=Colour.blue())
        embedthing.set_thumbnail(url=self.imgUrl)
        return embedthing

    def start_vote(self):
        json.dump(open("config/votes","a"))
        pass
    
    def add_vote(self,positiveVote, user):
        self.removeExistingVotes(user.id)
        self.votes.append({"voter":user,"stance":positiveVote})

        fileData = []
        with open("config/votes", "r") as reader:
            fileData.append(json.load(reader.readline()))
        fileData[-1] = json.dumps(self)
        with open("config/votes", "w") as rewrite:
            rewrite.writelines(fileData)
        pass
    
    def remove_vote(self,positiveVote, user):
        self.removeExistingVotes(user.id)
        fileData = []
        with open("config/votes", "r") as reader:
            fileData.append(json.load(reader.readline()))
        fileData[-1] = json.dumps(self)
        with open("config/votes", "w") as rewrite:
            rewrite.writelines(fileData)
        pass

    def getVotes(self):
        #logger.debug(str(self.votes))
        checks = len([v for v in self.votes if v["stance"]])
        return {"Check":checks, "Cross":len(self.votes)-checks}

    def removeExistingVotes(self,id):
        existing =[v for v in self.votes if v["voter"].id == id]
        if(len(existing) >0):
            for vote in existing:
                self.votes.remove(vote)
