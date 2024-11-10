import requests
import config
from libs import logger
def check():
    log = logger.getLogger("AutoUpdate")
    with open("./config/core/version.txt","r")as f:
        nowVersion=f.read()
    log.info("当前版本为:%s"%nowVersion)
    if config.autoUpdate:
        pass
    else:
        log.warning("自动更新已关闭")