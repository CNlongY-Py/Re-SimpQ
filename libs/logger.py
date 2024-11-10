import logging
import config
import time
import threading
from logging.handlers import TimedRotatingFileHandler
flushDisable=True
def flushScreen(type="",flushSec=config.flushSec):
    if type=="auto":
        while True:
            if flushDisable:
                config.indexBuffer.text = config.textBuffer.getvalue()
                time.sleep(flushSec)
            else:
                break
    else:
        config.indexBuffer.text = config.textBuffer.getvalue()
th=threading.Thread(target=flushScreen,kwargs={"type":"auto"})
def autoFlushScreen():
    th.start()
def debugStatus(type=True):
    logging.getLogger("asyncio").disabled = not type
    logging.getLogger("urllib3.connectionpool").disabled = not type
def getLogger(name):
    logging.basicConfig(stream=config.textBuffer,level=config.level,format=config.format, datefmt=config.datafmt)
    log = logging.getLogger(name)
    if not log.handlers:
        log_handel=TimedRotatingFileHandler(encoding="utf-8",when="MIDNIGHT",filename="./logs/lasted.log",backupCount=config.backupCount,delay=True)
        log_handel.setFormatter(fmt=logging.Formatter(config.format,datefmt=config.datafmt))
        log.addHandler(log_handel)
    return log
