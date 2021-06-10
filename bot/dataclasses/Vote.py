from enum import Enum


class Vote(Enum):
    NONE = None
    YAY  = "\u2705"
    NAY  = "\u274C"
    QUE  = "\u2753"

    def __new__(cls, value):
        member = object.__new__(cls)
        member._value_ = value
        return member

    def __int__(self):
        return self.value
    pass

    @staticmethod
    def isVote(emoji):
        return emoji == Vote.YAY.value or \
               emoji == Vote.NAY.value or \
               emoji == Vote.QUE.value
    
