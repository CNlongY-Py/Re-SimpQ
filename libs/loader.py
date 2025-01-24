import importlib
import runpy
import threading
import os
import traceback
import config
from libs import logger
from libs import bot

plugins = {}
PLUGINFOS = {}
unloads = ["__pycache__"]
log = logger.getLogger("Loader")


def init_load():
    log = logger.getLogger("Loader")
    log.debug("插件系统初始化加载中……")
    for i in os.listdir("./plugins"):
        if i not in unloads:
            name, suffix = os.path.splitext(i)
            if config.LOADMODE == "runpy":
                if suffix == ".py":
                    try:
                        log.debug(f"正在加载 {i}")
                        runpy.run_module("plugins.%s" % name)
                    except:
                        log.debug(f"加载{i}时错误，正在输出错误日志……")
                        log = logger.getLogger("Init_load")
                        log.error("\n %s" % traceback.format_exc())
            elif config.LOADMODE == "importlib":
                if suffix == ".py":
                    try:
                        log.debug(f"正在加载 {i}")
                        plugin = importlib.import_module("plugins.%s" % name)
                        info = plugin.PLUGINFO
                        PLUGINFOS[info["name"]] = info
                    except AttributeError:
                        pass
                    except:
                        log.debug(f"加载{i}时错误，正在输出错误日志……")
                        log = logger.getLogger("Init_load")
                        log.error("\n %s" % traceback.format_exc())
                elif suffix == "" and os.path.exists(f"./plugins/{name}/__init__.py"):
                    try:
                        log.debug(f"正在加载 {i} 软件包")
                        plugin = importlib.import_module("plugins.%s" % name)
                        info = plugin.PLUGINFO
                        PLUGINFOS[info["name"]] = info
                    except AttributeError:
                        pass
                    except:
                        log.debug(f"加载{i}时错误，正在输出错误日志……")
                        log = logger.getLogger("Init_load")
                        log.error("\n %s" % traceback.format_exc())
    callPlugins("init_finish", {})


def regEvent(event, func):
    log.debug(f"{func} 注册事件 {event}")
    if event not in plugins.keys():
        log.debug(f"创建新事件 {event}")
        plugins[event] = []
    plugins[event].append({"name": func.__module__.split(".", 1)[1], "func": func})


def callPluginThread(name, dat, api, func):
    log = logger.getLogger("Loader")
    log.debug(f"创建插件 {name} 响应器线程")
    try:
        log.debug(f"尝试回调插件 {name}")
        func(logger.getLogger(name), dat, api)
    except:
        log.debug(f"调用插件 {name} 时发生错误，正在输出错误日志……")
        log = logger.getLogger("Exception-%s" % func.__module__.split(".", 1)[1])
        log.error("\n %s" % traceback.format_exc())


def callPlugins(event, dat, extAPI=None):
    log.debug("接收到调用事件指令")
    if "listen_events" in plugins.keys():
        log.debug("正在回调 listen_events 事件")
        for i in plugins["listen_events"]:
            name = i["name"]
            if name not in unloads:
                dat["event_type"] = event
                if extAPI:
                    api = extAPI
                else:
                    api = bot.API(dat)
                func = i["func"]
                th = threading.Thread(callPluginThread(name, dat, api, func))
                th.start()
    if event in plugins.keys():
        log.debug(f"正在回调 {event} 事件")
        for i in plugins[event]:
            name = i["name"]
            if name not in unloads:
                dat["event_type"] = event
                if extAPI:
                    api = extAPI
                else:
                    api = bot.API(dat)
                func = i["func"]
                th = threading.Thread(callPluginThread(name, dat, api, func))
                th.start()
