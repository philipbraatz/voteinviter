import os
from os import path
import configparser

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#from bot.mainbot import *

db = SQLAlchemy()
DB_NAME = None
SECRET_KEY = None
PORT = None

def loadConfig(filepath):
    config_object= configparser.ConfigParser()
    #read config file into object
    config_object.read(filepath)
    #print(str(config_object.sections()))
    for sect in config_object.sections():
        print('Section:', sect)
        for k,v in config_object.items(sect):
            print(' {} = {}'.format(k,v))
            if(k == 'db_name'):
                global DB_NAME
                DB_NAME = v
            elif(k =='secret_key'):
                global SECRET_KEY
                SECRET_KEY = v
            elif(k == 'port'):
                global PORT
                PORT = v
    else:
        print("Config does not have any sections")
    print("Finished Loading Config")


#for subdir, dirs, files in os.walk('./'):
#    for file in files:
#      print(file)
#print("Config Path: "+os.path.join(os.path[0],"config.ini"))
loadConfig("website//config.ini")



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from view import views
    from auth import auth

    app.register_blueprint(views, url_prefix='/')
    #app.register_blueprint(auth,url_prefix='/')

    from models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('pysite/'+DB_NAME):
        db.create_all(app=app)
        print("database created!")

def getPort():
    return PORT