![Header](/docs/Re-SimpQ.png)
***
![LICENSE](https://img.shields.io/badge/license-icon?style=for-the-badge&label=GPL-3.0&color=green) 
![PYTHON](https://img.shields.io/badge/3.8%2B-icon?style=for-the-badge&label=Python&color=lightblue)
[![QQ](https://img.shields.io/badge/%E5%AE%98%E6%96%B9-%E7%A4%BE%E5%8C%BA?style=for-the-badge&label=QQ%E7%BE%A4&color=blue)](https://qm.qq.com/cgi-bin/qm/qr?k=LteZqCk_lsIO7OWgx3HtQqWzGGDVYjTq&jump_from=webapi&authKey=Gcg2D/di5o7qI31M4mTVpdjfqJNOuLdnUqZCafC9Chtocq8kPVBoAAqMB8hukDxO)
![ONEBOT](https://img.shields.io/badge/11-icon?style=for-the-badge&label=Onebot&labelColor=black&color=gray)


# 📄 简介 📄
**SimpQ-Bot系列**最新力作，重置了SimpQ-Ref的大部分代码  
Re-SimpQ具有高可扩展性，轻量化的主体，易用的命令系统，灵活的事件系统  
```python3
from libs import loader
# 监听事件
def init(log,dat,bot):
    log.info("即刻出发!")
loader.listen_event("init",init)
```
# ⚡即刻开始⚡
## 📩下载框架📩
- *Release* 获取最新稳定版本
- *Download Zip* 获取最新快照版本
## 🪛安装环境🪛
支持 ___Python3.8+___ 环境
```bash
pip install -r requirements.txt
```
## 📡配置协议📡
 |                               协议名称                               | 状态 |
 |:----------------------------------------------------------------:| :--:|
 |    go-cqhttp（[仓库](https://github.com/Mrs4s/go-cqhttp)）    |  ✅  |
 | Lagrange.Onebot（[仓库](https://github.com/LagrangeDev/Lagrange.Core)） |  ✅  |
 |     NapCat（[仓库](https://github.com/NapNeko/NapCatQQ)）      |  ✅  |  
**[点我食用文档](/onebot/食用说明.md)**
## 🧩插件开发🧩
**[点我食用文档](https://cnlongy-py.github.io/Re-SimpQ/#/%E6%8F%92%E4%BB%B6%E5%BC%80%E5%8F%91)**
## 🔍快速功能🔎
#### 高效Debug(DebugCore插件)
命令系统中输入 **debug start** 开始记录,在命令行逐行输入你的代码   
输入 **debug stop** 停止记录  
输入 **debug list** 展示记录  
输入 **debug run** 运行代码  
输入 **debug clear** 清除记录  
#### 高效退出(Exit)
按下**Ctrl-Q**安全退出框架,**~~Ctrl-C不是很安全就是了~~**
### ️️️️✏️写在最后✏️
**Re-SimpQ** 现在仍然处于没有达到预期的状态，有一些功能可能会带来一些麻烦，期待后续更新越来越好!
