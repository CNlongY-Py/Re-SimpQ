# 导入prompt_toolkit用户界面
from prompt_toolkit import Application
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.layout.containers import VSplit, Window, HSplit
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.completion import NestedCompleter, ThreadedCompleter
from prompt_toolkit.layout import ScrollablePane, CompletionsMenu
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
from libs import command

# 获取日志接口
log = logger.getLogger("Core")
logger.debugStatus(False)


# 按键绑定
@kb.add('c-q')
def exit_(event):
    log.debug("接收到终止按键指令")
    # 停止刷新屏幕
    logger.flushDisable = False
    # 退出应用
    log.debug("正在退出应用……")
    event.app.exit()


# 捕获输入
def on_input(string):
    log = logger.getLogger("Input")
    if string.text:
        log.info(string.text)
        loader.callPlugins("user_input", {"text": string.text})


# 初始化界面
log.debug("初始化界面……")
with open("./config/core/logo.txt", "r", encoding="utf-8") as f:
    log.info("\n" + f.read())
log.info(" Re-SimpQ 正在为您定制个性化体验...")
# 检查更新
log.debug("下达检查更新指令")
update.run()
# 启动插件注册器
log.debug("下达启动插件注册器指令")
loader.init_load()
# 启动驱动器适配器
log.debug("下达启动默认驱动器适配器指令")
drivers.run()
# 输出窗口
log.debug("创建输出窗口")
outWindow = Window(content=BufferControl(buffer=indexBuffer), wrap_lines=True)
# 初始化建议输入
cmd_completer = NestedCompleter.from_nested_dict(command.get_completer())
# 输入窗口
log.debug("创建输入窗口")
inBuffer = Buffer(name="input", multiline=False, accept_handler=on_input, auto_suggest=AutoSuggestFromHistory(),
                  completer=ThreadedCompleter(cmd_completer))
inputWindow = Window(content=BufferControl(buffer=inBuffer))
# 格式窗口
log.debug("格式化窗口布局")
root_container = HSplit([
    VSplit([
        outWindow,
    ]),
    VSplit([
        Label(text=">", width=2),
        inputWindow,
        CompletionsMenu()
    ]),
])
container = ScrollablePane(content=root_container, show_scrollbar=False)
layout = Layout(container)
# 自动刷新窗口
log.debug("下达刷新窗口指令")
logger.autoFlushScreen()
indexBuffer.cursor_down()
# 创建应用实例
log.debug("创建应用实例")
app = Application(layout=layout, key_bindings=kb, full_screen=True)
# 聚焦至输入窗口
log.debug("聚焦输入窗口")
app.layout.focus(inBuffer)
# 启动应用
log.debug("框架初始化指令执行完毕")
log.debug("正在启动应用……")
with patch_stdout(app):
    app.run()
