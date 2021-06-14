
import logging
import asyncio
import threading
from __init__ import WebMain

try:
    from .config.config import setupLogging
except:
    from config.config import setupLogging
import sys

threadErrors = []

async def runBotThread():
    global threadErrors
    try:
        from bot.mainbot import VotingBot
        bot = VotingBot(command_prefix="!v", description=VotingBot.__doc__)
    except Exception as e:
        threadErrors.append([e,"Bot"])
    pass

async def runWebThread():
    try:
        webApp = WebApp()
        app = webApp.create_app()
        webApp.run_app(True)
    except Exception as e:
        threadErrors.append([e,"Website"])
    pass

def runThreaded():
    #general logger
    logger = logging.getLogger(__name__)
    setupLogging(logger)

    logger.info("Initializing")
    #runBotThread()
    eventLoop = asyncio.new_event_loop()
    #asyncio.set_event_loop(eventLoop)

    #tasks to run
    #waittask =asyncio.wait([runBotThread],return_when=asyncio.FIRST_EXCEPTION)
    #webThread = threading.Thread(target=runWebThread, args=(2,),daemon=True)

    #run tasks
    try:
        logger.info("Starting Bot")
        done, _ = eventLoop.run_until_complete(runBotThread())#asyncio.run(runBotThread())
        logger.info("Starting Website")
        donew, _ = eventLoop.run_until_complete(runWebThread())#asyncio.run(runWebThread())#webThread.start()
    except asyncio.CancelledError as e:
        logger.fatal(str(e))

    logger.info("Initialization done")

    #for f in donew:
    #    if f.exception():
    #        logger.warning( str(d.exception())+' occurred in thread: Bot')
    #for d in done:
    #    if d.exception():
    #        logger.warning( str(d.exception())+' occurred in thread: Bot')


    #botThread.join()
    #webThread.join()
    if len(threadErrors) > 0: #check if there are any errors 
        for e in threadErrors:
            logger.fatal(str(e[0])+' occurred in thread: '+e[1])

if __name__ == '__main__':
    mainLogger = logging.getLogger(__name__)
    setupLogging(mainLogger)
    loop = asyncio.get_event_loop()

    if(len(sys.argv) == 1):
        runThreaded()
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