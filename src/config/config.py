from os import getcwd, getenv, environ
from bot.dataclasses.Mode import Mode
from os.path import isfile
import configparser
import json

class WebsiteConfig:
    def __init__(self):
        self.SECRET_KEY = None
        self.PORT = None
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
                print(' {} = {}'.format(k,v))
                if(k =='secret_key'):
                    self.SECRET_KEY = v
                elif(k == 'port'):
                    self.PORT = v
        if(self.SECRET_KEY == None or self.PORT == None):
            raise Exception("Website config does not have any sections")
        print("Finished Loading Website Config")

class BotConfig():

    def __init__(self):
        self.filepath = "src\\config\\botconfig.ini"
        self.config_object = None

        # SETTINGS Config
        self.voteMode = int(Mode.Difference)# Voting has 2 modes
        self.votePing = "<@845723264550830100>" # TODO - Don't use static values!!
        self.minVotes = 3
        # Difference Configs
        self.minApprove = 2
        # Percentage Configs
        self.minPercentage = 0.6

        # BOT Config
        self.MASTER_SERVER   = 0
        self.VOTING_CHANNEL  = 0
        self.WELCOME_CHANNEL = 0
        self.WELCOME_MESSAGE = ""
        self.CURRENT_ELECT   = ""

        self.load()
        pass

    # TODO convert to config.ini
    def load(self):
        if(not isfile(self.filepath)):
            self.save()
        self.config_object = configparser.ConfigParser()
        # Read config file into object
        self.config_object.read(self.filepath)
        # print(str(config_object.sections()))
        if(len(self.config_object.sections())<=0):
            raise Exception("No content found in bot config")
        for sect in self.config_object.sections():
            print('Section:', sect)
            for k,v in self.config_object.items(sect):
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
            # Capiltisation needs to be same as variable names above
            # Due to how the config is read
            self.config_object.set("Settings","voteMode", str(self.voteMode)) 
            self.config_object.set("Settings","votePing", str(self.votePing))
            self.config_object.set("Settings","minApprove", str(self.minApprove))
            self.config_object.set("Settings","minPercentage", str(self.minPercentage))
            self.config_object.set("Settings","minVotes", str(self.minVotes))
            # Bot config Section
            self.config_object.set("Bot","MASTER_SERVER",str(self.MASTER_SERVER))
            self.config_object.set("Bot","VOTING_CHANNEL",str(self.VOTING_CHANNEL))
            self.config_object.set("Bot","WELCOME_CHANNEL",str(self.WELCOME_CHANNEL))
            self.config_object.set("Bot","WELCOME_MESSAGE",str(self.WELCOME_MESSAGE))
            self.config_object.set("Bot","CURRENT_ELECT",str(self.CURRENT_ELECT))
                       
        with open(self.filepath, "w") as write_file:
            self.config_object.write(write_file)
        pass
class PrivateConfig:
    BOT_TOKEN = "Replace With Bot Token"
    OAUTH_CLIENT_TOKEN = "Replace with client secret"
    WEBSITE_SECRET_KEY = "Replace with flask website secret"
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


PRIVATECONFIG = PrivateConfig()
WEBSITECONFIG = WebsiteConfig()
BOTCONFIG = BotConfig()