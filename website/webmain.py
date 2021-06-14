from .__init__ import WEBSITECONFIG, PRIVATECONFIG
from flask_login import LoginManager
from flask import Flask
from flask_pywebpush import WebPush, WebPushException
from os import getenv

import logging
from config.config import setupLogging
logger = logging.getLogger(__name__)
setupLogging(logger, True)

logger.info("Loading Website")

class WebMain:
    app = None

    def __init__(self):
        self.config = WEBSITECONFIG

    def create_app(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = getenv("WEBSITE_SECRET_KEY")
        
        from .view import views

        self.app.register_blueprint(views, url_prefix='/')

        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(self.app)
        
        @login_manager.user_loader
        def load_user(user_id):
            return None
        


        subscription = {
            'endpoint': '---some-value---',
            'keys': {...}
        }
        notification = {
            'title': 'Test',
            'body': 'notification body',
        }

        try:
            push = WebPush(private_key=PRIVATECONFIG.VAPID_PRIVATE_KEY)
            #push.send(subscription, notification)
        except WebPushException as exc:
            logger.fatal(exc)


        return self.app

    def run_app(self,debug = False):
        self.app.run(debug=debug,port=self.config.PORT,host=self.config.IP)
        logger.info("Website Offline")
