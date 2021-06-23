
import asyncio
from __init__ import WebMain
from config.config import SetupLogging
import sys


if __name__ == '__main__':
    mainLogger = SetupLogging(__name__)
    
    loop = asyncio.get_event_loop()

    if(len(sys.argv) == 1):
        mainLogger.warn("Need and argument of either 'web' or 'bot'")
    elif(sys.argv[1] == "bot"):
        from bot.mainbot import VotingBot
        bot = VotingBot(command_prefix="!v", description=VotingBot.__doc__)
        mainLogger.info("Bot has turned off")
    elif(sys.argv[1] =="web"):
        webSite = WebMain()
        webSite.create_app()
        webSite.run_app(True)
    else:
        mainLogger.warn("argument not recognized, Expected either 'web' or 'bot'")