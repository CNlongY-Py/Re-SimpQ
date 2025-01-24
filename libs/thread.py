import _thread
import traceback
from libs import logger


def create(name, data=()):  # 线程创建器
    log = logger.getLogger("Thread")
    log.debug("接收到创建新线程指令")
    log.debug(f"{name} 传入 {data}")
    try:
        log.debug("尝试线程创建……")
        return _thread.start_new_thread(name, data)
    except:
        log.debug("创建线程失败，正在记录错误日志……")
        log = logger.getLogger("Exception-Thread")
        log.error("\n %s" % traceback.format_exc())
        return 1
