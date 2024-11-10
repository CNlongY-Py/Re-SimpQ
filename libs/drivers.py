import config
import json
import yaml
import threading
from libs import logger
from libs import thread
from libs import loader
# 全局变量
url=""
AuthToken=""
# 检查配置文件
def checkDriverConfig():
    if config.driverConfig[0]=="AUTO":
        if config.driverConfig[1]=="Lagrange.Onebot":
            with open("./onebot/appsettings.json")as f:
                drivers=json.loads(f.read())["Implementations"]
            dat=[]
            for i in drivers:
                type=i["Type"]
                if type=="ForwardWebSocket":
                    dat.append({"error":0,"type":type,"url":"ws://"+i["Host"]+":"+str(i["Port"]),"AccessToken":i["AccessToken"]})
                elif type=="ReverseWebSocket":
                    dat.append({"error":0,"type":type,"host":i["Host"],"port":i["Port"],"suffix":i["Suffix"],"AccessToken":i["AccessToken"]})
                elif type=="HttpPost":
                    dat.append({"error":0,"type":type,"host":i["Host"],"port":i["Port"],"suffix":i["Suffix"],"AccessToken":i["AccessToken"]})
                elif type=="Http":
                    dat.append({"error":0,"type":type,"url":"http://"+i["Host"]+":"+str(i["Port"]),"AccessToken":i["AccessToken"]})
            return dat
        elif config.driverConfig[1]=="go-cqhttp":
            with open("./onebot/config.yml",encoding="utf-8") as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                drivers=data["servers"]
                dat=[]
                for i in drivers:
                    for type in i.keys():
                        if type=="http":
                            dat.append({"error": 0, "type": "Http", "url": "http://" + i["http"]["address"],"AccessToken": data["default-middlewares"]["access-token"]})
                        elif type=="ws-reverse":
                            dat.append({"error": 0, "type": "ForwardWebSocket","url":i["ws-reverse"]["universal"],"AccessToken": data["default-middlewares"]["access-token"]})
                        elif type=="ws":
                            dat.append({"error": 0, "type": "ReverseWebSocket", "host": i["ws"]["address"].split(":")[0], "port": i["ws"]["address"].split(":")[1], "AccessToken": data["default-middlewares"]["access-token"]})
                return dat
        else:
            return {"error":"Error Drivers"}
    elif config.driverConfig[0]=="MANUAL":
        dat = []
        for i in config.driverConfig[1]:
            type = i["Type"]
            if type == "ForwardWebSocket":
                dat.append({"error": 0, "type": type, "url": "ws://" + i["Host"] + ":" + str(i["Port"]) + i["Suffix"],
                        "AccessToken": i["AccessToken"]})
            elif type == "ReverseWebSocket":
                dat.append({"error": 0, "type": type, "host": i["Host"], "port": i["Port"], "suffix": i["Suffix"],
                        "AccessToken": i["AccessToken"]})
            elif type == "HttpPost":
                dat.append({"error": 0, "type": type, "host": i["Host"], "port": i["Port"], "suffix": i["Suffix"],
                        "AccessToken": i["AccessToken"]})
            elif type == "Http":
                dat.append({"error": 0, "type": type, "url": "http://" + i["Host"] + ":" + str(i["Port"]),
                        "AccessToken": i["AccessToken"]})
        return dat


# ws正向驱动器
def wsFoward(log,url,AuthToken):
    # 需安装websocket-client库
    import websocket
    def on_open(wsapp):
        log.info("ws正向连接已启动")
        loader.callPlugins("init",{"post_type":"close"})
    def on_message(wsapp,msg):
        msg=json.loads(msg)
        if msg["post_type"]!="meta_event":
            loader.callPlugins(msg["post_type"],msg)
    def on_close(wsapp):
        log.warning("ws正向连接被关闭")
        loader.callPlugins("close",{"post_type":"close"})
    if AuthToken=="":
        wsapp = websocket.WebSocketApp(url,on_open=on_open,on_message=on_message,on_close=on_close)
    else:
        wsapp = websocket.WebSocketApp(url,header={"Authorization": AuthToken},on_open=on_open,on_message=on_message,on_close=on_close)
    wsapp.run_forever()
# ws反向驱动器
"""
!!!暂不支持!!!
 计划后续修复
"""
def wsReverse(log,host,port,AuthToken):
    import asyncio
    import websockets
    log.info("ws反向连接已启动")
    async def echo(websocket, path):
        async for message in websocket:
            if message["post_type"]!="meta_event":
                log.info(message)
    asyncio.get_event_loop().run_until_complete(websockets.serve(echo, host, port))
    asyncio.get_event_loop().run_forever()
# http反向驱动器
"""
!!!未测试!!!
请遇到问题反馈
"""
def httpPost(log,host,port,AuthToken):
    # 需安装flask库
    from flask import Flask,request
    app = Flask(__name__)
    @app.route('/', methods=["POST"])
    def _():
        msg=request.get_json()
        if msg["post_type"]!="meta_event":
            loader.callPlugins(msg["post_type"],msg)
        return ""

    loader.callPlugins("init", {"post_type":"init"})
    log.info("http反向驱动器已启动")
    app.run(host,port)
# http正向API
def http():
    return {"url":url,"AuthToken":AuthToken}
# 驱动器启动接口
def run():
    log=logger.getLogger("Drivers")
    drivers=checkDriverConfig()
    for dat in drivers:
        if dat["error"]==0:
            if dat["type"]=="ReverseWebSocket":
                threading.Thread(wsReverse(logger.getLogger("WsReverse"),dat["host"],dat["port"],dat["AccessToken"]),daemon=True).start()
            elif dat["type"]=="ForwardWebSocket":
                thread.create(wsFoward,(logger.getLogger("WsForward"),dat["url"],dat["AccessToken"]))
            elif dat["type"]=="HttpPost":
                thread.create(httpPost,(logger.getLogger("HttpPost"), dat["host"], dat["port"], dat["AccessToken"]))
            elif dat["type"]=="Http":
                global url,AuthToken
                url=dat["url"]
                AuthToken=dat["AccessToken"]
        else:
            log.error(dat["error"])