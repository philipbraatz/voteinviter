class User(object):
    id = None

    def __init__(self, id):
        self.id = id
    pass

class Voter(User):
    id = ""
    approved = False

    def __init__(self, id, approved):
        super().__init__(id)
        self.approved = approved
    pass 

class Elector(User):
    votes = []
    electionsHeld = 0
    pass