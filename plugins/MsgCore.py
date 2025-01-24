from libs import loader

PLUGINFO = {
    "name": "MsgCore",
    "version": "1.0.0",
    "author": "CNlongY-Py",
}


def msglog(log, dat, bot):
    sub_type = dat["message_type"]
    if sub_type == "group":
        group_id = dat["group_id"]
        user_id = dat["user_id"]
        message = dat["raw_message"]
        groupName = bot.get_group_info(group_id)["group_name"]
        userName = bot.get_group_member_info(group_id, user_id)["nickname"]
        log.info(f"[群聊消息]<{groupName}>{userName}:{message}")
    elif sub_type == "private":
        user_id = dat["user_id"]
        message = dat["raw_message"]
        userName = bot.get_stranger_info(user_id)["nickname"]
        log.info(f"[私聊消息]<{userName}>:{message}")


loader.regEvent("message", msglog)
