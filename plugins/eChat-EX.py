from libs import loader
from openai import OpenAI
import requests
import os
PLUGINFO={
    "name":"eChat-EX",
    "version":"BETA-1.0-EX",
    "author":"CNlongY-Py",
    "mode":"REQUEST", # 请求模式选择 OFFICIAL官方接口 / REQUEST转发接口
    "url":"", # 转发网站URL
    "key":"", # OpenAI KEY
    "BOTNAME":"Yogurt酱", # 要设定的BOT名称
    "MAX_CACHE":30, # 最大可缓存上下文数量(-1为无限)
    "model":"gpt-4o-2024-08-06", # OpenAI 大模型
}

replaces={
    "{{Name}}":PLUGINFO["BOTNAME"],
    "{{Functions}}":"",
}

groups = {}
functions = []
init_prompt=""

def init(log, dat, bot):
    log.info("高性能ですから！")
    log.info("eChat-EX 正在启动……")
    if PLUGINFO["mode"]=="OFFICIAL":
        os.environ["OPENAI_API_KEY"] = PLUGINFO["key"]
        os.environ["OPENAI_BASE_URL"] = PLUGINFO["url"]

def completions(messages,model):
    if PLUGINFO["mode"]=="OFFICIAL":
        client = OpenAI()
        chat_completion = client.chat.completions.create(
            messages=[
                messages
            ],
            model=model,
        )
        return chat_completion.choices[0].message.content
    elif PLUGINFO["mode"]=="REQUEST":
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {PLUGINFO['key']}"
        }
        data = {
            "model": model,
            "messages": messages,
            "stream": False
        }
        response = requests.post(PLUGINFO["url"], json=data, headers=headers)
        if response:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return "NET ERRoR"

def addFunction(title,text,func):
    functions.append({"title":title,"text":text,"name":func.__name__,"func":func})

def writeFunctions(log,dat,bot):
    global init_prompt
    global replaces
    log.info("eChat-EX 插件加载完毕")
    log.info("正在写入初始Prompt……")
    if not PLUGINFO["BOTNAME"]:
        replaces["name"]=bot.get_login_info()["nickname"]
    with open("./config/eChat-EX/prompt.txt","r",encoding="utf-8")as f:
        txt=f.read()
    functionTXT=""
    for i in functions:
        functionTXT+=f"""
        
        - {i["title"]}
        
        {i["text"]}
        
        """
    replaces["{{Functions}}"]=functionTXT
    for i in replaces:
        if txt.find(i)!=-1:
            txt=txt.replace(i,replaces[i])
    log.info("初始化Prompt模板……")
    init_prompt=txt
def main(log,dat,bot):
    if dat["message_type"] == "group":
        msg = dat["message"]
        gid = dat["group_id"]
        uid = dat["user_id"]
        rmsg = dat["raw_message"]
        if not gid in groups:
            groups[gid]=[]
            groups[gid].append({"role":"system","content":init_prompt})
        content=[]
        for i in msg:
            if i["type"]=="image":
                content.append({"type": "image_url", "image_url":{"url": i["data"]["url"]}})
            elif i["type"]=="text":
                content.append({"type":"text","text":i["data"]["text"]})


loader.regEvent("init", init)
loader.regEvent("init_finish",writeFunctions)
loader.regEvent("message", main)