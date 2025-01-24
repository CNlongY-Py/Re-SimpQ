from mistune import create_markdown
from markdown2image import async_api as md2img
from libs import loader
import requests
import datetime
import base64
import asyncio

PLUGINFO = {
    "name": "BangumiGO",
    "version": "1.0",
    "author": "CNlongY-Py"
}

# 特别鸣谢
# Bangumi API    https://github.com/bangumi/dev-docs
# markdown2image https://github.com/Slontia/markdown2image

path = "./config/BangumiGO/cache.png"

model_txt = """
## 今日放送({{TODAY}})
| 图 | 番 | 译 | 评 |  
|----|----|----|----|  
"""
html_txt = """
<body>
    {{CONTENT}}
</body>
<style>
  td{
    text-align:center;
  }
  h2{
    text-align:center;
  }
  table{
      width: 100%;
      border-collapse: collapse;
  }

  table caption{
      font-size: 2em;
      font-weight: bold;
      margin: 1em 0;
  }

  th,td{
      border: 1px solid #999;
      text-align: center;
      padding: 20px 0;
  }

  table thead tr{
      background-color: #008c8c;
      color: #fff;
  }

  table tbody tr:nth-child(odd){
      background-color: #eee;
  }

  table tbody tr:hover{
      background-color: #ccc;
  }

  table tbody tr td:first-child{
      color: #f40;
  }

  table tfoot tr td{
      text-align: right;
      padding-right: 20px;
  }
</style>
"""


def init(log, dat, bot):
    log.info("BangumiGO 準備が整いました")


async def save_html(html, path):
    await md2img.html2image(html, path)


def message(log, dat, bot):
    global md_txt
    if dat["message_type"] == "group":
        msg = dat["message"]
        gid = dat["group_id"]
        uid = dat["user_id"]
        rmsg = dat["raw_message"]
        if rmsg == "/今日放送":
            response = requests.get("https://api.bgm.tv/calendar")
            if response:
                data = response.json()
                now = datetime.datetime.now().weekday()
                for i in data:
                    if i["weekday"]["id"] == now:
                        md_txt = model_txt.replace("{{TODAY}}", i["weekday"]["ja"])
                        for j in range(0, 10):
                            img = i["items"][j]["images"]["small"]
                            name = i["items"][j]["name"]
                            name_cn = i["items"][j]["name_cn"]
                            if not name_cn:
                                name_cn = "暂无译名"
                            if "rating" in i["items"][j].keys():
                                score = i["items"][j]["rating"]["score"]
                            else:
                                score = "__"
                            txt = f"|![Image]({img})|__{name}__|_{name_cn}_|({score}/10.0)|  \n"
                            md_txt = md_txt + txt
                        markdown = create_markdown(plugins=["table"])
                        html = markdown(md_txt)
                        html = html_txt.replace("{{CONTENT}}", html)
                        asyncio.run(save_html(html, path))
                        with open(path, "rb") as f:
                            b_img = base64.b64encode(f.read())
                        bot.reply("[CQ:image,file=base64://%s]" % b_img.decode("utf-8"))

            else:
                bot.reply("Bangumi遇到了一点错误,请稍后再试")


def heartbeat(log, dat, bot):
    pass


loader.regEvent("init", init)
loader.regEvent("message", message)
loader.regEvent("meta_event", heartbeat)
