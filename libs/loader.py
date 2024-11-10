import runpy
import os
import traceback
from libs import logger
from libs import bot
plugins={}
unloads=["__pycache__"]
log=logger.getLogger("Loader")
def init_load():
    for i in os.listdir("./plugins"):
        if i not in unloads:
            if i.find(".py")!=-1:
                try:
                    runpy.run_module("plugins.%s"%i.replace(".py",""))
                except:
                    log = logger.getLogger("Init_load")
                    log.error("\n %s" % traceback.format_exc())
def regEvent(event,func):
    if event not in plugins.keys():
        plugins[event]=[]
    plugins[event].append({"name":func.__module__[8:],"func":func})
def callPlugins(event,dat):
    if "listen_events" in plugins.keys():
        for i in plugins["listen_events"]:
            name = i["name"]
            if name not in unloads:
                api = bot.API(0, 0, 0)
                func = i["func"]
                try:
                    func(logger.getLogger(name), dat, api)
                except:
                    log = logger.getLogger("Exception-%s" % func.__module__[8:])
                    log.error("\n %s" % traceback.format_exc())
    if event in plugins.keys():
        for i in plugins[event]:
            name=i["name"]
            if name not in unloads:
                api=bot.API(0,0,0)
                func=i["func"]
                try:
                    func(logger.getLogger(name), dat, api)
                except:
                    log = logger.getLogger("Exception-%s" % func.__module__[8:])
                    log.error("\n %s" % traceback.format_exc())
