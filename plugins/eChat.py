from libs import loader
import requests
import base64

PLUGINFO = {
    "name": "eChat",
    "version": "1.0.0",
    "author": "CNlongY-Py",
}

url = 'http://15.204.101.64:4000/v1/chat/completions'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer sk-YI0TdPyiPfFWSxeV000bA77eFb5d4875A2544643D3A66f6b'
}
groups = {}


def init(log, dat, bot):
    log.info("高性能萝卜子！")
    for i in bot.get_group_list():
        groups[i["group_id"]] = []


def main(log, dat, bot):
    if dat["message_type"] == "group":
        msg = dat["message"]
        gid = dat["group_id"]
        uid = dat["user_id"]
        rmsg = dat["raw_message"]
        userName = bot.get_group_member_info(gid, uid)["nickname"]
        groups[gid].append({"role": "user", "content": "[%s]:" % userName + rmsg})
        if msg[0]["type"] == "image":
            groups[gid].append({"role": "user", "content": [
                {"type": "image_url", "image_url":
                    {"url": msg[0]["data"]["url"]}
                 }
            ]})
        for i in msg:
            if i["type"] == "at" and i["data"]["qq"] == str(bot.get_login_info()["user_id"]):
                messages = groups[gid]
                data = {
                    "model": "gpt-4o-2024-08-06",
                    "messages": messages,
                    "stream": False
                }
                response = requests.post(url, json=data, headers=headers)
                if response:
                    smsg = response.json()["choices"][0]["message"]["content"]
                    myname = bot.get_login_info()["nickname"]
                    groups[gid].append({"role": "assistant", "content": smsg})
                    bot.send_group_msg(gid, smsg)
                    break
                else:
                    groups[gid] = []
                    bot.send_group_msg(gid, "请求失败!")


loader.regEvent("init", init)
loader.regEvent("message", main)
