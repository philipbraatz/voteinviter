from datetime import datetime

class User(object):
    id = None
    imgUrl = None
    name = None

    def __init__(self, id):
        self.id = id
    pass

    def __repr__(self):
        return "User(\n[ID:{},Name:{},URL:{}])".format(self.id, self.name, self.imgUrl)


#Person in the server
class Voter(User):
    approved = False
    vote_date = None
    nickName = None


    def __init__(self, id):
        super().__init__(id)
    def __repr__(self):
        return "Voter(\n{},\n[Nick:{},Aprvd:{},Date:{}])".format(super().__repr__(),self.nickName, self.approved, self.vote_date)

    pass 

#Person who is currently being voted on
class Elector(Voter):
    votes = [] #array of Voters
    electionsHeld = 0 

    #Election info
    description = "I am a cool user" #only needed during election
    relationships = "" #people they know from the server

    def __init__(self, id):
        super().__init__(id)
        self.approved = vote_date = datetime.now()
    pass

    def __repr__(self):
        return "Elector(\n{},\n[Desc:{},Votes:{},Elections:{},Relations:{}])".format(super().__repr__(),self.description, len(self.votes),self.electionsHeld, self.relationships)
