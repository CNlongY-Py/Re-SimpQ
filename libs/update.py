import requests
import config
from libs import logger
from libs import thread


def check():
    log = logger.getLogger("AutoUpdate")
    log.debug("执行检查更新指令")
    with open("./config/core/version.txt", "r") as f:
        nowVersion = f.read()
    log.info("当前版本为:%s" % nowVersion)
    if config.autoUpdate:
        log.debug("准许自动更新")
        response = requests.get(f"{config.updateUrl}/versions.json")
        if response:
            versions = response.json()
            log.debug("写入LOGO文件")
            with open("./config/core/logo.txt", "w", encoding="utf-8") as f:
                f.write(versions["LOGO"])
        else:
            log.error(f"无法连接到更新服务器({config.updateUrl}),检查更新失败")
            return 0
        response = requests.get(f"{config.updateUrl}/versions.json")
        if response:
            versions = response.json()
            if versions["lasted"]["version"] == nowVersion:
                log.info("当前为最新版本")
            elif versions["lasted"]["version"] != nowVersion:
                log.warning("检查到最新版本 %s" % versions["lasted"]["version"])
                log.info("更新了如下内容")
                for i in versions["lasted"]["describe"]:
                    log.info(i)
                if nowVersion in versions["versions"]:
                    step = versions["versions"].index(nowVersion)
                    log.warning("您与最新版本相差了%s个版本,建议立即更新修复问题" % step)
                else:
                    log.warning("无法在版本列表中查找到您的版本信息")
        else:
            log.error(f"无法连接到更新服务器({config.updateUrl}),检查更新失败")
            return 0

    else:
        log.debug("阻止自动更新")
        log.warning("自动更新已关闭")


def run():
    thread.create(check)
