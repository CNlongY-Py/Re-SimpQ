import importlib
import logging
from libs import loader
from libs import bot as api
from libs import logger

PLUGINFO = {
    "name": "DebugCore",
    "version": "1.1.0-Official",
    "author": "CNlongY-Py",
}

code = ""
mode = "WAITING"
allows = ["DebugCore", "Input"]


def usrInput(log, dat, bot):
    global mode
    global code
    txt = dat["text"]
    if txt == "debug start":
        mode = "INPUTING"
        for i in logging.Logger.manager.loggerDict:
            if not i in allows:
                logging.getLogger(i).disabled = True
        logging.getLogger("MsgCore").disabled = True
    elif txt == "debug stop":
        mode = "WAITING"
        for i in logging.Logger.manager.loggerDict:
            if not i in allows:
                logging.getLogger(i).disabled = False
        logger.debugStatus(False)
        logging.getLogger("MsgCore").disabled = False
    elif txt == "debug run":
        func = {"importlib": importlib,
                "bot": api.API({}),
                "loader": importlib.import_module("libs.loader"),
                "log": logger.getLogger("DebugCore-DEBUG")
                }
        exec(code, func)
    elif txt == "debug clear":
        code = ""
    elif txt == "debug list":
        log.info("当前共 %s 字节\n>>\n" % len(code) + code + "<<")
    elif mode == "INPUTING":
        code += txt + "\n"


loader.regEvent("user_input", usrInput)
