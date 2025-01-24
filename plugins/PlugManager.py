from prompt_toolkit.application import get_app
from libs import loader
from libs import command
import importlib
import os
import runpy
import traceback
import config
import sys
import signal

PLUGINFO = {
    "name": "PlugManager",
    "version": "1.3",
    "author": "CNlongY-Py",
}

def cmd_list(log,dat,bot):
    log.info("当前加载:")
    for i in os.listdir("./plugins"):
        if i not in loader.unloads:
            if i.find(".py") != -1:
                log.info(i[:-3])
def cmd_info(log,dat,bot):
    name=dat["result"][0]
    try:
        if config.LOADMODE == "runpy":
            if name == PLUGINFO["name"]:
                log.info("嘿！你想看我的信息？")
                for i in PLUGINFO:
                    log.info("%s --> %s" % (i, PLUGINFO[i]))
            else:
                plugin = importlib.import_module("plugins." + name)
                info = plugin.PLUGINFO
                log.info("当前插件信息如下:")
                for i in info:
                    log.info("%s --> %s" % (i, info[i]))
        elif config.LOADMODE == "importlib":
            if name == PLUGINFO["name"]:
                log.info("嘿！你想看我的信息？")
                for i in PLUGINFO:
                    log.info("%s --> %s" % (i, PLUGINFO[i]))
            else:
                info = loader.PLUGINFOS[name]
                log.info("当前插件信息如下:")
                for i in info:
                    log.info("%s --> %s" % (i, info[i]))
    except AttributeError:
        log.warning("该插件无信息描述")
    except ModuleNotFoundError:
        log.error("没有找到该插件")
def cmd_unload(log,dat,bot):
    name = dat["result"][0].replace(".py", "")
    if "%s.py" % name in os.listdir("./plugins"):
        loader.unloads.append(name)
        log.warning(f"禁用插件 {name}")
    else:
        log.error("没有找到插件")
def cmd_load(log,dat,bot):
    name = dat["result"][0].replace(".py", "")
    if "%s.py" % name in os.listdir("./plugins"):
        if name in loader.unloads:
            log.warning(f"加载插件 {name}")
            loader.unloads.remove(name)
        else:
            try:
                runpy.run_module("plugins.%s" % name.replace(".py", ""))
            except:
                log.error("\n %s" % traceback.format_exc())
    else:
        log.error("没有找到插件")
def cmd_reload(log,dat,bot):
    name = dat["result"][0].replace(".py", "")
    if name != "PluginManager":
        if "%s.py" % name in os.listdir("./plugins"):
            for j in loader.plugins:
                for k in loader.plugins[j]:
                    if k["name"] == name:
                        log.debug(f"删除事件 {j} 中 {k} 响应器")
                        loader.plugins[j].remove(k)
            try:
                runpy.run_module("plugins.%s" % name.replace(".py", ""))
            except:
                log.error("\n %s" % traceback.format_exc())
            log.warning(f"重载插件 {name}")
        elif name == "all":
            loader.plugins = {}
            loader.init_load()
            log.warning("重载全部插件完成")
        else:
            log.error("没有找到插件")
    else:
        log.error("你不能尝试卸载关键插件！")

def cmd_exit(log,dat,bot):
    log.warning("正在结束会话……")
    log.flushDisable = False
    log.debug("正在退出应用……")
    get_app().exit()
    pid = os.getpid()
    os.kill(pid, signal.SIGTERM)

command.regCommand("exit",cmd_exit)
command.regCommand("quit",cmd_exit)
command.regCommand("pm","list",cmd_list)
command.regCommand("pm","info",("<ARGS>",cmd_info))
command.regCommand("pm","unload",("<ARGS>",cmd_unload))
command.regCommand("pm","load",("<ARGS>",cmd_load))
command.regCommand("pm","reload",("<ARGS>",cmd_reload))
