import requests
from ..__init__ import PRIVATECONFIG

class Api(object):
    URL = "http://65.31.250.51/api/"#"http://127.0.0.1:84/api/"
    secret = "secret={PRIVATECONFIG.API_KEY}"

    @staticmethod
    def postVote(positive, negative):
        builder = f"{Api.URL}sendvote?{Api.secret}&positive={positive}&negative={negative}"
        return requests.post(builder)

    @staticmethod
    def startVote( id, avatar, name):
        builder = f"{Api.URL}startvote?{Api.secret}&id={id}&avatar={avatar}&name={name}"
        return requests.post(builder)
    
    @staticmethod
    def sendInvite(id, inviteLink):
        builder = f"{Api.URL}{Api.secret}&id={id}&invite={inviteLink}"
        #TODO https://suryasankar.medium.com/how-to-setup-basic-web-push-notification-functionality-using-a-flask-backend-1251a5413bbe
