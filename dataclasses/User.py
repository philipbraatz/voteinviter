from datetime import datetime

class User(object):
    id = None

    def __init__(self, id):
        self.id = id
    pass

#Person in the server
class Voter(User):
    approved = False
    vote_date = None


    def __init__(self, id):
        super().__init__(id)
    pass 

#Person who is currently being voted on
class Elector(Voter):
    votes = [] #array of Voters
    electionsHeld = 0 

    #Election info
    description = "I am a cool user" #only needed during election
    staff_notes = "This man knows about water" #staff comments about that everyone can see, optional
    relationships = [] #people they know from the server

    def __init__(self, id):
        super().__init__(id)
        self.approved = vote_date = datetime.now()
    pass