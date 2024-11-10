import _thread
import traceback
from libs import logger


def create(name, data=()):  # 线程创建器
    try:
        return _thread.start_new_thread(name, data)
    except:
        log = logger.getLogger("Exception-Thread")
        log.error("\n %s" % traceback.format_exc())
        return 1

