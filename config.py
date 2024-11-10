# Prompt_Toolkit 开放接口
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.buffer import Buffer
kb = KeyBindings()
indexBuffer = Buffer(name="index")
# Screen 输出IO接口
import io
textBuffer=io.StringIO()
# Logger 开放接口
import logging
level=logging.DEBUG
format="%(asctime)s[%(levelname)s]<%(name)s>:%(message)s"
datafmt="%Y-%m-%d %H:%M:%S"
flushSec=0.01
backupCount=10
# Update 开放接口
autoUpdate=False
updateUrl=""
# Drivers 开放接口
"""
AUTO 自动模式
MANUAL 手动模式
"""
driverConfig=[]


