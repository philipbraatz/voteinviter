import configparser
import json
import logging
from os import environ, getcwd, getenv
from os.path import isfile


class WebsiteConfig:
    def __init__(self):
        self.SECRET_KEY = None
        self.PORT = 80
        self.IP = "0.0.0.0"
        self.DEBUG = False
        self.filepath = "config\\webconfig.ini"
        self.load()

    def load(self):
        config_object = configparser.ConfigParser()
        #read config file into object
        config_object.read(self.filepath)
        #logger.debug(str(config_object.sections()))
        if(len(config_object.sections())<=0):
             logger.fatal("No content found in website config: {self.filepath}")

        for sect in config_object.sections():
            logger.debug('Section:'+ sect)
            for k,v in config_object.items(sect):
                k = k.upper()
                logger.debug('\t{} = {}'.format(k,v))

                if(v.isdigit()):
                    v = int(v)
                elif(v.isnumeric()):
                    v = float(v)

                setattr(self,k,v)
        if(self.IP == None or self.PORT == None or self.DEBUG == None):
            logger.fatal("Website config does not have any sections or not all content found in config")
        logger.info("Finished Loading Website Config")

class BotConfig():

    def __init__(self):
        self.filepath = "config\\botconfig.ini"

        # SETTINGS Config (FILE WILL OVERWRITE these DEFAULT VALUES)
        #self.vote_mode = int(Mode.Difference)# Voting has 2 modes
        self.VOTE_PING = "<@123456789>"
        self.min_vote = 3
        self.min_quick_vote = 1
        # Difference Configs
        self.min_approve = 2
        # Percentage Configs
        self.min_percentage = 0.6
        #invite
        self.invite_expire_time =24


        # BOT Config
        self.MASTER_SERVER   = 0
        self.VOTING_CHANNEL  = 0
        self.ADMIN_CHANNEL   = 0
        self.RULES_CHANNEL   = 0
        self.ROLES_CHANNEL   = 0
        self.WELCOME_CHANNEL = 0
        self.WELCOME_MESSAGE = ""
        self.CURRENT_ELECT   = ""
        self.STAFF_ROLE      = 0

        self.load()
        pass

    def load(self):

        config_object = configparser.ConfigParser()
        #read config file into object
        config_object.read(self.filepath)
        if(len(config_object.sections())<=0):
            logger.fatal(f"No content found in bot config: {self.filepath}")

        for sect in config_object.sections():
            logger.debug('Section: '+ sect)
            for k,v in config_object.items(sect):
                if(sect == "Bot"):
                    k = k.upper()
                logger.debug('\t{} = {}'.format(k,v)) #Debug
                if(v.isdigit()):
                    v = int(v)
                elif(v.isnumeric()):
                    v = float(v)
                setattr(self,k,v) # self.k = v where k is replaced with str(k)
        logger.debug("Finished Loading Bot Config")

    def save(self):
        config_object = configparser.ConfigParser()
        # Read config file into object
        config_object.read(self.filepath)
        config_object.add_section("Settings")

        #config_object.set("Settings","vote_mode",  str(self.vote_mode)) 
        config_object.set("Settings","min_approve", str(self.min_approve))
        config_object.set("Settings","min_percentage", str(self.min_percentage))
        config_object.set("Settings","min_votes",  str(self.min_vote))
        config_object.set("Settings","min_quick_votes",  str(self.min_quick_vote))
        config_object.set("Settings", "invite_expire_time", str(self.invite_expire_time))

        # Bot config Section
        config_object.add_section("Bot")
        config_object.set("Bot","MASTER_SERVER".lower(),   str(self.MASTER_SERVER))
        config_object.set("Bot","VOTING_CHANNEL".lower(),  str(self.VOTING_CHANNEL))
        config_object.set("Bot","ADMIN_CHANNEL".lower(),   str(self.ADMIN_CHANNEL))
        config_object.set("Bot","WELCOME_CHANNEL".lower(), str(self.WELCOME_CHANNEL))
        config_object.set("Bot","VOTE_PING".lower(),  str(self.VOTE_PING))
        config_object.set("Bot","RULES_CHANNEL".lower(),   str(self.RULES_CHANNEL))
        config_object.set("Bot","ROLES_CHANNEL".lower(),   str(self.ROLES_CHANNEL))
        config_object.set("Bot","STAFF_ROLE".lower(),   str(self.STAFF_ROLE))


        config_object.add_section("OAuth")
        config_object.set("OAuth","CLIENT_ID".lower(),str(self.CLIENT_ID))
                       
        with open(self.filepath, "w") as write_file:
            config_object.write(write_file)
        pass
class PrivateConfig:
    #loaded from .env
    BOT_TOKEN          = None
    OAUTH_CLIENT_TOKEN = None
    WEBSITE_SECRET_KEY = None
    API_KEY            = None
    CLIENT_ID          = None

    def __init__(self):
        self.VAPID_PRIVATE_KEY = open(
                    "config/private_key.txt", "r+").readline().strip("\n")
        self.VAPID_PUBLIC_KEY = open("config/public_key.txt", "r+").read().strip("\n")
        self.load()

    def load(self):
        if(not isfile(".env")):
            self.save()
        with open(".env","r") as fb:
            Envs = fb.readlines()
            for key,value in [i.split("=") for i in Envs ]:
                environ[key] = value.strip()
                setattr(self, key, value.strip())

def SetupLogging(name,debug=False):
    logger = logging.getLogger(name)
    if(debug):
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    #console logging
    ch = logging.StreamHandler()
    if(debug):
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.INFO)

    # create formatter
    formatter = logging.Formatter('%(name)s| %(levelname)s:\t%(message)s')#'%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

logger = SetupLogging(__name__)
