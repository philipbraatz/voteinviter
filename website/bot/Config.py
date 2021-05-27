import json
from enum import Enum

class Mode(Enum):
    Percentage = 0
    Difference = 1

    def __new__(cls, value):
        member = object.__new__(cls)
        member._value_ = value
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
        with open("bot\\appdata\\config.json", "r") as read_file:
            data = json.loads(read_file.read())
            print("Config: "+str(data))
            voteMode      = data["voteMode"]
            votePing      = data["votePing"]
            minVotes      = data["minVotes"]
            minApprove    = data["minApprove"]
            minPercentage = data["minPercentage"]
        pass

    def save(self):
        with open("bot\\appdata\\config.json", "w") as write_file:
            json.dump(self.__dict__,write_file)
            #write_file.write(json.dump(temp))
        pass

#Config()
