from os import getcwd, getenv, environ
from bot.dataclasses.Mode import Mode
from os.path import isfile
import configparser
import json

class WebsiteConfig:
    def __init__(self):
        self.SECRET_KEY = None
        self.PORT = None
        self.IP = 0
        self.DEBUG = ""
        self.WEBSITE_FOLDER = ""
        self.filepath = "src\\config\\webconfig.ini"
        self.load()

    def load(self):
        config_object = configparser.ConfigParser()
        #read config file into object
        config_object.read(self.filepath)
        #print(str(config_object.sections()))
        if(len(config_object.sections())<=0):
            raise Exception("No content found in website config")

        for sect in config_object.sections():
            print('Section:', sect)
            for k,v in config_object.items(sect):
                k = k.upper()
                print(' {} = {}'.format(k,v))

                if(v.isdigit()):
                    v = int(v)
                elif(v.isnumeric()):
                    v = float(v)

                setattr(self,k,v)
        if(self.IP == None or self.PORT == None or self.DEBUG == None):
            raise Exception("Website config does not have any sections or not all content found in config")
        print("Finished Loading Website Config")

class BotConfig():

    def __init__(self):
        self.filepath = "src\\config\\botconfig.ini"

        # SETTINGS Config (Filled with default values)
        self.vote_mode = int(Mode.Difference)# Voting has 2 modes
        self.vote_ping = "<@123456789>"
        self.min_vote = 3
        # Difference Configs
        self.min_approve = 2
        # Percentage Configs
        self.min_percentage = 0.6

        # BOT Config
        self.MASTER_SERVER   = 0
        self.VOTING_CHANNEL  = 0
        self.WELCOME_CHANNEL = 0
        self.WELCOME_MESSAGE = ""
        self.CURRENT_ELECT   = ""

        self.load()
        pass

    def load(self):
        config_object = configparser.ConfigParser()
        #read config file into object
        config_object.read(self.filepath)
        # print(str(config_object.sections()))
        if(len(self.config_object.sections())<=0):
            raise Exception("No content found in bot config")

        for sect in self.config_object.sections():
            print('Section:', sect)
            for k,v in self.config_object.items(sect):
                if(sect == "Bot"):
                    k = k.upper()
                print(' {} = {}'.format(k,v)) #Debug
                if(v.isdigit()):
                    v = int(v)
                elif(v.isnumeric()):
                    v = float(v)
                setattr(self,k,v) # self.k = v where k is replaced with str(k)
        print("Finished Loading Config")

    def save(self):
        if(self.config_object is None):
            self.config_object = configparser.ConfigParser()
            # Read config file into object
            self.config_object.read(self.filepath)
            self.config_object.add_section("Settings")

            self.config_object.set("Settings","vote_mode",  str(self.vote_mode)) 
            self.config_object.set("Settings","vote_ping",  str(self.vote_ping))
            self.config_object.set("Settings","min_approve", str(self.min_approve))
            self.config_object.set("Settings","min_percentage", str(self.min_percentage))
            self.config_object.set("Settings","min_votes",  str(self.min_vote))

            # Bot config Section
            self.config_object.add_section("Bot")
            self.config_object.set("Bot","MASTER_SERVER",   str(self.MASTER_SERVER).lower())
            self.config_object.set("Bot","VOTING_CHANNEL",  str(self.VOTING_CHANNEL).lower())
            self.config_object.set("Bot","WELCOME_CHANNEL", str(self.WELCOME_CHANNEL).lower())
            self.config_object.set("Bot","WELCOME_MESSAGE", str(self.WELCOME_MESSAGE).lower())
                       
        with open(self.filepath, "w") as write_file:
            self.config_object.write(write_file)
        pass
class PrivateConfig:
    #loaded from .env
    BOT_TOKEN          = None
    OAUTH_CLIENT_TOKEN = None
    WEBSITE_SECRET_KEY = None

    def __init__(self):
        self.load()

    def load(self):
        if(not isfile(".env")):
            self.save()
        with open(".env","r") as fb:
            Envs = fb.readlines()
            for key,value in [i.split("=") for i in Envs ]:
                environ[key] = value
                setattr(self, key, value)

    def save(self):
        content = f"BOT_TOKEN={self.BOT_TOKEN}\nOAUTH_CLIENT_TOKEN={self.OAUTH_CLIENT_TOKEN}\nWEBSITE_SECRET_KEY={self.WEBSITE_SECRET_KEY}"
        with open(".env","w") as fb:
            fb.write(content)