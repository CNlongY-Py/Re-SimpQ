from libs import loader
from libs import esetup
import datetime

PLUGINFO={
    "name":"eBuild",
    "version":"1.0",
    "author":"CNlongY-Py"
}

plugins_allow=[
    "DebugCore.py",
    "InitCore.py",
    "MsgCore.py",
    "PlugManager.py",
]

def init(log,dat,bot):
    now=datetime.datetime.today()
    Y=now.strftime("%y")[1]
    M=now.strftime("%#m")
    D=now.strftime("%#d")
    version=f"Snapshot-{Y}y{M}m{D}d-Nightly"
    log.warning(f"正在自动构建 {version}")
    app=esetup.epkg(
        "Re-SimpQ",
        "CNlongY-Py",
        version,
        "项目自动构建包",
        "lystudio@cnlongy.cn",
        "http://github.com/CNlongY-Py/Re-SimpQ"
    )
    app.addFolder("./config")
    app.addFolder("./logs",True)
    app.addFolder("./onebot",True)
    app.addFolder("./libs")
    app.addFile("./index.py")
    app.addFile("./requirements.txt")
    for i in plugins_allow:
        app.addFile("./plugins/"+i)
    app.pack("./Build-Nightly")

loader.regEvent("init",init)