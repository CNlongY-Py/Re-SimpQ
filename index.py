# 导入prompt_toolkit用户界面
from prompt_toolkit import Application
from prompt_toolkit.layout.containers import VSplit, Window , HSplit
from prompt_toolkit.layout.controls import  BufferControl
from prompt_toolkit.layout import ScrollablePane
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.widgets import Label
# 导入配置文件
from config import kb
from config import indexBuffer
# 导入libs
from libs import logger
from libs import update
from libs import drivers
from libs import loader
# 按键绑定
@kb.add('c-q')
def exit_(event):
    # 停止刷新屏幕
    logger.flushDisable = False
    # 退出应用
    event.app.exit()

# 捕获输入
def on_input(string):
    log=logger.getLogger("Input")
    if string.text:
        log.info(string.text)
        loader.callPlugins("user_input",{"text":string.text})
# 输出窗口
outWindow=Window(content=BufferControl(buffer=indexBuffer))
# 输入窗口
inBuffer=Buffer(name="input",multiline=False,accept_handler=on_input,auto_suggest=False)
inputWindow=Window(content=BufferControl(buffer=inBuffer))
# 格式窗口
root_container = HSplit([
    VSplit([
        outWindow,
    ]),
    VSplit([
        Label(text=">",width=2),
        inputWindow
    ]),
])
container=ScrollablePane(content=root_container,show_scrollbar=False)
layout = Layout(container)
# 创建应用实例
app = Application(layout=layout,key_bindings=kb,full_screen=True)
# 聚焦至输入窗口
app.layout.focus(inBuffer)
# 自动刷新窗口
logger.autoFlushScreen()
indexBuffer.cursor_down()
# 获取日志接口
log=logger.getLogger("Core")
logger.debugStatus(False)
# 初始化界面
with open("./config/core/logo.txt","r")as f:
    log.info("\n"+f.read())
log.info(" Re-SimpQ 正在为您定制个性化体验...")
# 检查更新
update.check()
# 启动插件注册器
loader.init_load()
# 启动驱动器适配器
drivers.run()
# 启动应用
with patch_stdout(app):
    app.run()