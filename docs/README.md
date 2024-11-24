# 📄 简介 📄
> **SimpQ-Bot系列**最新力作，重置了SimpQ-Ref的大部分代码    

![Re-SimpQ](https://socialify.git.ci/CNlongY-Py/Re-SimpQ/image?forks=1&issues=1&language=1&logo=https%3A%2F%2Fraw.githubusercontent.com%2FCNlongY-Py%2FRe-SimpQ%2Frefs%2Fheads%2Fmain%2Fdocs%2FICON.png&name=1&owner=1&pulls=1&stargazers=1&theme=Light)

![LICENSE](https://img.shields.io/badge/license-icon?style=for-the-badge&label=GPL-3.0&color=green) 
![PYTHON](https://img.shields.io/badge/3.8%2B-icon?style=for-the-badge&label=Python&color=lightblue)
[![QQ](https://img.shields.io/badge/%E5%AE%98%E6%96%B9-%E7%A4%BE%E5%8C%BA?style=for-the-badge&label=QQ%E7%BE%A4&color=blue)](https://qm.qq.com/cgi-bin/qm/qr?k=LteZqCk_lsIO7OWgx3HtQqWzGGDVYjTq&jump_from=webapi&authKey=Gcg2D/di5o7qI31M4mTVpdjfqJNOuLdnUqZCafC9Chtocq8kPVBoAAqMB8hukDxO)
![ONEBOT](https://img.shields.io/badge/11-icon?style=for-the-badge&label=Onebot&labelColor=black&color=gray)

Re-SimpQ具有高可扩展性，轻量化的主体，易用的命令系统，灵活的事件系统  
***
**基本插件示例**
```python3
from libs import loader
# 监听事件
def init(log,dat,bot):
    log.info("即刻出发!")
loader.listen_event("init",init)
```
