from __init__ import WEBSITECONFIG, PRIVATECONFIG
from flask_login import LoginManager
#import bot.mainbot as bot
from flask import Flask
from os import getenv

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = getenv("WEBSITE_SECRET_KEY")
    
    from .view import views

    app.register_blueprint(views, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return None

    return app

def run_app(myapp,debug = False):
    myapp.run(debug=debug,port=WEBSITECONFIG.PORT)