from libs import loader
from libs import esetup
from libs import command
import os

PLUGINFO = {
    "name": "eSetup",
    "version": "1.0",
    "author": "CNlongY-Py"
}


def meta_event(log, dat, bot):
    dirs = os.listdir("./plugins")
    for i in dirs:
        name, suffix = os.path.splitext(i)
        if suffix == ".epkg":
            log.warning(f"正在安装软件包 {name}{suffix}")
            esetup.setup(f"./plugins/{name}{suffix}")


loader.regEvent("meta_event", meta_event)
