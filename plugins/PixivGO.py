from libs import loader
import requests
import random

PLUGINFO = {
    "name": "PixivGO",
    "version": "1.0",
    "author": "CNlongY-Py"
}


# 特别鸣谢
# 🖼️ Pixiv 每日排行榜小挂件 https://github.com/mokeyjay/Pixiv-daily-ranking-widget

def init(log, dat, bot):
    log.info("PixivGO 正在为您定制个性化服务……")


def message(log, dat, bot):
    if dat["message_type"] == "group":
        msg = dat["message"]
        gid = dat["group_id"]
        uid = dat["user_id"]
        rmsg = dat["raw_message"]
        if rmsg == "/今日随机":
            response = requests.get("https://pixiv.mokeyjay.com/?r=api/pixiv-json")
            if response:
                data = response.json()["data"]
                img = random.choice(data)["url"]
                bot.reply("[CQ:image,file=%s]" % img)
            else:
                bot.reply(f"PixivGO 伺服器错误，请稍后再试({response.reason})")


loader.regEvent("init", init)
loader.regEvent("message", message)
