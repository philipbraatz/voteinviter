import requests
from ..__init__ import PRIVATECONFIG

class Api(object):
    URL = "http://127.0.0.1:84/api/"

    @staticmethod
    def postVote(positive, negative):
        builder = f"{Api.URL}sendvote?secret={PRIVATECONFIG.API_KEY}&positive={positive}&negative={negative}"
        return requests.post(builder)

    @staticmethod
    def startVote( id, avatar, name):
        print(PRIVATECONFIG.API_KEY)
        builder = f"{Api.URL}startvote?secret={PRIVATECONFIG.API_KEY}&id={id}&avatar={avatar}&name={name}"
        return requests.post(builder)
