from datetime import datetime
from discord import Embed, Colour
import json
from bot.dataclasses.Vote import Vote

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
    vote_date = False

    def __init__(self, id):
        super().__init__(id)
        self.approved = True
    pass

    def __repr__(self):
        return "Elector({},[Desc:{},Votes:{},Elections:{},Relations:{}])".format(super().__repr__(),self.description, len(self.votes),self.electionsHeld, self.relationships)

    def voteEmbeddedMessage(self,bot):
        embedthing = Embed(title=f"VOTE: {self.name} ({self.nickName})",
            description=f"\nDescription: {self.description}\n\
                \nReact with {Vote.YAY.value} if you want them\nReact with {Vote.NAY.value} if you don't",colour=Colour.blue())
        embedthing.set_thumbnail(url=self.imgUrl)
        return embedthing

    def start_vote(self):
        with open("config/votes", "a") as write:
            write.write("\n")
            json.dump(self.__dict__,write)
        pass
    
    def add_vote(self,positiveVote, user):
        self.removeExistingVotes(user.id)
        self.votes.append({"voter":user,"stance":positiveVote})
        self.printVoteData()

        fileData = []
        with open("config/votes", "r") as reader:
            fileData.append(json.loads(reader.readline()))
        print(json.dumps(self.__dict__))
        fileData[-1] = json.dumps(self.__dict__)
        with open("config/votes", "w") as rewrite:
            rewrite.writelines(fileData)
        pass
    
    def remove_vote(self,positiveVote, user):
        self.removeExistingVotes(user.id)
        fileData = []
        with open("config/votes", "r") as reader:
            fileData.append(json.load(reader.readline()))
        fileData[-1] = json.dumps(self.__dict__)
        with open("config/votes", "w") as rewrite:
            rewrite.writelines(fileData)
        pass

    def getVotes(self):
        #logger.debug(str(self.votes))
        yays = len([v for v in self.votes if v["stance"]])
        return {"YAY":yays, "NAY":len(self.votes)-yays}

    def removeExistingVotes(self,id):
        existing =[v for v in self.votes if v["voter"].id == id]
        if(len(existing) >0):
            for vote in existing:
                self.votes.remove(vote)


    def printVoteData(self):
        print("Votes: ",dict(enumerate(self.votes)))
        return {"id":self.id,"vote": self.votes}


    def getIndexInFile(self,id):
        with open("config/votes", "r") as reader:
            fileData = [ 
                i
                for i,line in enumerate(reader.readlines())
                    if str(id) == json.load(line)["id"]
                ]
            return fileData[0] if len(fileData) >0 else None

    def checkif(self,id, line):
        return bool(line) and str(id) != json.loads(line)["id"]

    def removeIfExists(self, id):
        existing = [v for v in self.votes if v["voter"].id == id]
        if(len(existing) >0):
            for vote in existing:
                self.votes.remove(vote)

        with open("config/votes", "r") as reader:
            fileData = [
                json.load(line)
                for line in reader.readlines()
                   if self.checkif(id,line)
            ]
        with open("config/votes", "w") as rewrite:
            rewrite.writelines(fileData)
        pass

    def add_vote(self, positiveVote, user):
        self.removeIfExists(user.id)

        fileData = []
        with open("config/votes", "r") as reader:
            print(reader.readline())
            fileData.append(json.loads(reader.readline()))
        fileData[-1] = json.dumps(self.__dict__)
        with open("config/votes", "w") as rewrite:
            rewrite.writelines(fileData)
        pass
