
import logging
import asyncio
import threading
from __init__ import create_app

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
        from website.webmain import create_app, run_app
        app = create_app()
        run_app(app,True)
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

import os

print("My running location is: "+sys.argv[0])
print("Current Working Directory " , os.getcwd())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    if(len(sys.argv) == 1):
        runThreaded()
    elif(sys.argv[1] == "bot"):
        from bot.mainbot import VotingBot
        bot = VotingBot(command_prefix="!v", description=VotingBot.__doc__)
    elif(sys.argv[1] =="web"):
        from website.webmain import run_app
        app = create_app()
        run_app(app,False)
    else:
        print("argument not recognized")