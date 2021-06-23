import requests
from config.config import SetupLogging

from ..__init__ import PRIVATECONFIG

logger = SetupLogging(__name__)


class ApiHelper(object):
    URL = "http://burbscanvote.tk/api/"  # "http://127.0.0.1:84/api/"
    secret = f"secret={PRIVATECONFIG.API_KEY}"

    @staticmethod
    def PostVote(positive, negative):
        builder = f"{ApiHelper.URL}sendvote?{ApiHelper.secret}&positive={positive}&negative={negative}"
        logger.info(builder)
        return requests.post(builder)

    @staticmethod
    def StartVote(id, avatar, name):
        builder = f"{ApiHelper.URL}startvote?{ApiHelper.secret}&id={id}&avatar={avatar}&name={name}"
        logger.info(builder)
        return requests.post(builder)

    @staticmethod
    def EndVote(id, avatar, name):
        builder = f"{ApiHelper.URL}endVote?{ApiHelper.secret}&id={id}&avatar={avatar}&name={name}"
        logger.info(builder)
        return requests.post(builder)

    @staticmethod
    def SendInvite(id, inviteLink):
        builder = f"{ApiHelper.URL}sendInvite?{ApiHelper.secret}&id={id}&invite={inviteLink}"
        logger.info(builder)
        # TODO https://suryasankar.medium.com/how-to-setup-basic-web-push-notification-functionality-using-a-flask-backend-1251a5413bbe
