from libs import loader
from libs import command


def init(log, dat, bot):
    log.debug("正在加载框架组件……")
    command.init_command()


loader.regEvent("init", init)
