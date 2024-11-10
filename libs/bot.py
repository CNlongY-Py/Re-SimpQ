import requests
from libs import drivers


def http(action, args={}):
    dat = drivers.http()
    if dat["AuthToken"]:
        response = requests.get(dat["url"] + action, params=args, headers={"Authorization": dat["AuthToken"]})
    else:
        response = requests.get(dat["url"] + action, params=args)
    if response:
        return response.json()["data"]
    else:
        raise ConnectionError


class API:
    def __init__(self, user_id, group_id, message_id):
        self.user_id = user_id
        self.group_id = group_id
        self.message_id = message_id

    """
     Onebot 标准接口(含有go-cqhttp拓展接口)
    """

    # Bot账号
    def get_login_info(self):
        """
        获取登录号信息
        :return:
        """
        return http("/get_login_info")

    def set_qq_profile(self, nickname, company, email, collage, personal_note):
        """
        设置登录号资料
        :param nickname: 名称
        :param company: 公司
        :param email: 邮箱
        :param collage: 大学
        :param personal_note: 个人说明
        :return:
        """
        return http("/set_qq_profile", {"nickname": nickname, "company": company, "email": email, "collage": collage,
                                        "personal_note": personal_note})

    def qidian_get_account_info(self):
        """
        获取企点账号信息
        :return:
        """
        return http("/qidian_get_account_info")

    def _get_model_show(self, model):
        """
        获取在线机型
        :param model: 机型名称
        :return:
        """
        return http("/_get_model_show", {"model": model})

    def _set_model_show(self, model, model_show):
        """
        设置在线机型
        :param model: 机型名称
        :param model_show: N/A
        :return:
        """
        return http("/_set_model_show", {"model": model, "model_show": model_show})

    def get_online_clients(self, no_cache):
        """
        获取当前账号的在线客户端列表
        :param no_cache: 是否无视缓存
        :return:
        """
        return http("/get_online_clients", {"no_cache": no_cache})

    # 好友信息
    def get_stranger_info(self, user_id, no_cache=False):
        """
        获取陌生人信息
        :param user_id: QQ号
        :param no_cache: 是否不使用缓存（使用缓存可能更新不及时, 但响应更快）
        :return:
        """
        return http("/get_stranger_info", {"user_id": user_id, "no_cache": no_cache})

    def get_friend_list(self):
        """
        获取好友列表
        :return:
        """
        return http("/get_friend_list")

    def get_unidirectional_friend_list(self):
        """
        获取单向好友列表
        :return:
        """
        return http("/get_unidirectional_friend_list")

    # 好友操作
    def delete_friend(self, user_id):
        """
        删除好友
        :param user_id: 好友QQ号
        :return:
        """
        return http("/delete_friend", {"user_id": user_id})

    def delete_unidirectional_friend(self, user_id):
        """
        删除单向好友
        :param user_id:
        :return:
        """
        return http("/delete_unidirectional_friend", {"user_id": user_id})

    # 消息
    def send_private_msg(self, user_id, group_id, message, auto_escape=False):
        """
        发送私聊消息
        :param user_id: 对方 QQ 号
        :param group_id: 主动发起临时会话时的来源群号(可选, 机器人本身必须是管理员/群主)
        :param message: 要发送的内容
        :param auto_escape: 消息内容是否作为纯文本发送 ( 即不解析 CQ 码 ) , 只在 message 字段是字符串时有效
        :return:
        """
        return http("/send_private_msg",
                    {"user_id": user_id, "group_id": group_id, "message": message, "auto_escape": auto_escape})

    def send_group_msg(self, group_id, message, auto_escape=False):
        """
        发送群聊消息
        :param group_id: 群号
        :param message: 要发送的内容
        :param auto_escape: 消息内容是否作为纯文本发送 ( 即不解析 CQ 码 ) , 只在 message 字段是字符串时有效
        :return:
        """
        return http("/send_group_msg", {"group_id": group_id, "message": message, "auto_escape": auto_escape})

    def send_msg(self, message_type, user_id, group_id, message, auto_escape=False):
        """
        发送消息
        :param message_type: 消息类型, 支持 private、group , 分别对应私聊、群组, 如不传入, 则根据传入的 *_id 参数判断
        :param user_id: 对方 QQ 号 ( 消息类型为 private 时需要 )
        :param group_id: 群号 ( 消息类型为 group 时需要 )
        :param message: 要发送的内容
        :param auto_escape: 消息内容是否作为纯文本发送 ( 即不解析 CQ 码 ) , 只在 message 字段是字符串时有效
        :return:
        """
        return http("/send_msg",
                    {"message_type": message_type, "user_id": user_id, "group_id": group_id, "message": message,
                     "auto_escape": auto_escape})

    def get_msg(self, message_id):
        """
        获取消息
        :param message_id: 消息id
        :return:
        """
        return http("/get_msg", {"message_id": message_id})

    def delete_msg(self, message_id):
        """
        撤回消息
        :param message_id: 消息id
        :return:
        """
        return http("/delete_msg", {"message_id": message_id})

    def mark_msg_as_read(self, message_id):
        """
        标记消息已读
        :param message_id: 消息id
        :return:
        """
        return http("/mark_msg_as_read", {"message_id": message_id})

    def get_forward_msg(self, message_id):
        """
        获取合并转发内容
        :param message_id: 消息id
        :return:
        """
        return http("/get_forward_msg", {"message_id": message_id})

    def send_group_forward_msg(self, group_id, messages):
        """
        发送合并转发(群聊)
        :param group_id: 群号
        :param messages: 自定义转发消息, 具体看 https://docs.go-cqhttp.org/cqcode/#%E5%90%88%E5%B9%B6%E8%BD%AC%E5%8F%91%E6%B6%88%E6%81%AF%E8%8A%82%E7%82%B9
        :return:
        """
        return http("/send_group_forward_msg", {"group_id": group_id, "messages": messages})

    def send_private_forward_msg(self, user_id, messages):
        """
        发送合并转发(好友)
        :param user_id: 好友QQ号
        :param messages: 自定义转发消息，具体看 https://docs.go-cqhttp.org/cqcode/#%E5%90%88%E5%B9%B6%E8%BD%AC%E5%8F%91%E6%B6%88%E6%81%AF%E8%8A%82%E7%82%B9
        :return:
        """
        return http("/send_private_forward_msg", {"user_id": user_id, "messages": messages})

    def get_group_msg_history(self, message_seq, group_id):
        """
        获取群消息历史记录
        :param message_seq: 起始消息序号, 可通过 get_msg 获得
        :param group_id: 群号
        :return:
        """
        return http("/get_group_msg_history", {"message_seq": message_seq, "group_id": group_id})

    # 图片
    def get_image(self, file):
        """
        获取图片
        :param file: 图片缓存文件名
        :return:
        """
        return http("/get_image", {"file": file})

    def can_send_image(self):
        """
        检查是否可以发送图片
        :return:
        """
        return http("/can_send_image")

    def ocr_image(self, image):
        """
        图片OCR
        :param image: 图片id
        :return:
        """
        return http("/ocr_image", {"image": image})

    # 语音
    def get_record(self, file, out_format):
        """
        获取语音(ffmpeg)
        :param file: 收到的语音文件名（消息段的 file 参数）, 如 0B38145AA44505000B38145AA4450500.silk
        :param out_format: 要转换到的格式, 目前支持 mp3、amr、wma、m4a、spx、ogg、wav、flac
        :return:
        """
        return http("/get_record", {"file": file, "out_format": out_format})

    def can_send_record(self):
        """
        检查是否可以发送语音
        :return:
        """
        return http("/can_send_record")

    # 处理
    def set_friend_add_request(self, flag, approve=True, remark=None):
        """
        处理加好友请求
        :param flag: 加好友请求的 flag（需从上报的数据中获得）
        :param approve: 是否同意请求
        :param remark: 	添加后的好友备注（仅在同意时有效）
        :return:
        """
        return http("/set_friend_add_request", {"flag": flag, "approve": approve, "remark": remark})

    def set_group_add_request(self, flag, sub_type, approve=True, reason=None):
        """
        处理加群请求／邀请
        :param flag: 加群请求的 flag（需从上报的数据中获得）
        :param sub_type: add 或 invite, 请求类型（需要和上报消息中的 sub_type 字段相符）
        :param approve: 是否同意请求／邀请
        :param reason: 拒绝理由
        :return:
        """
        return http("/set_group_add_request",
                    {"flag": flag, "sub_type": sub_type, "approve": approve, "reason": reason})

    # 群消息
    def get_group_info(self, group_id, no_cache=False):
        """
        获取群信息
        :param group_id: 群号
        :param no_cache: 是否不使用缓存（使用缓存可能更新不及时, 但响应更快）
        :return:
        """
        return http("/get_group_info", {"group_id": group_id, "no_cache": no_cache})

    def get_group_list(self, no_cache=False):
        """
        获取群列表
        :param no_cache: 是否不使用缓存（使用缓存可能更新不及时, 但响应更快）
        :return:
        """
        return http("/get_group_list", {"no_cache": no_cache})

    def get_group_member_info(self, group_id, user_id, no_cache=False):
        """
        获取群成员信息
        :param group_id: 群号
        :param user_id: QQ号
        :param no_cache: 是否不使用缓存（使用缓存可能更新不及时, 但响应更快）
        :return:
        """
        return http("/get_group_member_info", {"group_id": group_id, "user_id": user_id, "no_cache": no_cache})

    def get_group_member_list(self, group_id, no_cache=False):
        """
        获取群成员列表
        :param group_id: 群号
        :param no_cache: 是否不使用缓存（使用缓存可能更新不及时, 但响应更快）
        :return:
        """
        return http("/get_group_member_list", {"group_id": group_id, "no_cache": no_cache})

    def get_group_honor_info(self, group_id, type):
        """
        获取群荣誉信息
        :param group_id: 群号
        :param type: 要获取的群荣誉类型, 可传入 talkative performer legend strong_newbie emotion 以分别获取单个类型的群荣誉数据, 或传入 all 获取所有数据
        :return:
        """
        return http("/get_group_honor_info", {"group_id": group_id, "type": type})

    def get_group_system_msg(self, invited_requests, join_requests):
        """
        获取群系统消息
        :param invited_requests: 邀请消息列表
        :param join_requests: 	进群消息列表
        :return:
        """
        return http("/get_group_system_msg", {"invited_requests": invited_requests, "join_requests": join_requests})

    def get_essence_msg_list(self, group_id):
        """
        获取群精华消息列表
        :param group_id: 群号
        :return:
        """
        return http("/get_essence_msg_list", {"group_id": group_id})

    def get_group_at_all_remain(self, group_id):
        """
        获取群 @全体成员 剩余次数
        :param group_id: 群号
        :return:
        """
        return http("/get_group_at_all_remain", {"group_id": group_id})

    # 群设置
    def set_group_name(self, group_id, group_name):
        """
        设置群名
        :param group_id: 群号
        :param group_name: 新群名
        :return:
        """
        return http("/set_group_name", {"group_id": group_id, "group_name": group_name})

    def set_group_portrait(self, group_id, file, cache):
        """
        设置群头像
        :param group_id: 群号
        :param file: 图片文件名
        :param cache: 表示是否使用已缓存的文件
        :return:
        """
        return http("/set_group_portrait", {"group_id": group_id, "file": file, "cache": cache})

    def set_group_admin(self, group_id, user_id, enable=True):
        """
        设置群管理员
        :param group_id: 群号
        :param user_id:要设置为管理员的QQ号
        :param enable: true为设置，false为取消
        :return:
        """
        return http("/set_group_admin", {"group_id": group_id, "user_id": user_id, "enable": enable})

    def set_group_card(self, group_id, user_id, card=None):
        """
        设置群名片 ( 群备注 )
        :param group_id: 群号
        :param user_id: 要设置的QQ号
        :param card: 群名片内容, 不填或空字符串表示删除群名片
        :return:
        """
        return http("/set_group_card", {"group_id": group_id, "user_id": user_id, "card": card})

    def set_group_special_title(self, group_id, user_id, special_title=None, duration=-1):
        """
        设置群组专属头衔
        :param group_id: 群号
        :param user_id: 要设置的QQ号
        :param special_title: 专属头衔, 不填或空字符串表示删除专属头衔
        :param duration: 专属头衔有效期, 单位秒, -1 表示永久, 不过此项似乎没有效果, 可能是只有某些特殊的时间长度有效, 有待测试
        :return:
        """
        return http("/set_group_special_title",
                    {"group_id": group_id, "user_id": user_id, "special_title": special_title, "duration": duration})

    # 群操作
    def set_group_ban(self, group_id, user_id, duration=30 * 60):
        """
        群单人禁言
        :param group_id: 群号
        :param user_id: 要禁言的QQ号
        :param duration: 禁言时长, 单位秒, 0 表示取消禁言
        :return:
        """
        return http("/set_group_ban", {"group_id": group_id, "user_id": user_id, "duration": duration})

    def set_group_whole_ban(self, group_id, enable=True):
        """
        群全员禁言
        :param group_id: 群号
        :param enable: 是否禁言
        :return:
        """
        return http("/set_group_whole_ban", {"group_id": group_id, "enable": enable})

    def set_group_anonymous_ban(self, group_id, anonymous, anonymous_flag, duration=30 * 60):
        """
        群匿名用户禁言
        :param group_id: 群号
        :param anonymous:  可选,要禁言的匿名用户对象（群消息上报的 anonymous 字段）
        :param anonymous_flag: 可选,要禁言的匿名用户的 flag（需从群消息上报的数据中获得）
        :param duration: 禁言时长, 单位秒, 无法取消匿名用户禁言
        :return:
        """
        return http("/set_group_anonymous_ban")

    def set_essence_msg(self, message_id):
        """
        设置精华消息
        :param message_id: 消息id
        :return:
        """
        return http("/set_essence_msg", {"message_id": message_id})

    def delete_essence_msg(self, message_id):
        """
        移出精华消息
        :param message_id: 消息id
        :return:
        """
        return http("/set_essence_msg", {"message_id": message_id})

    def send_group_sign(self, group_id):
        """
        群打卡
        :param group_id: 群号
        :return:
        """
        return http("/send_group_sign", {"group_id": group_id})

    def set_group_anonymous(self, group_id, enable=True):
        """
        群设置匿名
        :param group_id: 群号
        :param enable: 是否允许匿名聊天
        :return:
        """
        return http("/set_group_anonymous", {"group_id": group_id, "enable": enable})

    def _send_group_notice(self, group_id, content, image):
        """
        发送群公告
        :param group_id 群号:
        :param content: 公告内容
        :param image: 图片内容(可选)
        :return:
        """
        return http("/_send_group_notice", {"group_id": group_id, "content": content, "image": image})

    def _get_group_notice(self, group_id):
        """
        获取群公告
        :param group_id: 群号
        :return:
        """
        return http("/_get_group_notice", {"group_id": group_id})

    def set_group_kick(self, group_id, user_id, reject_add_request=False):
        """
        群组踢人
        :param group_id: 群号
        :param user_id: 要踢的QQ号
        :param reject_add_request: 拒绝此人的加群请求
        :return:
        """
        return http("/set_group_kick",
                    {"group_id": group_id, "user_id": user_id, "reject_add_request": reject_add_request})

    def set_group_leave(self, group_id, is_dismiss=False):
        """
        退出群组
        :param group_id: 群号
        :param is_dismiss: 是否解散, 如果登录号是群主, 则仅在此项为 true 时能够解散
        :return:
        """
        return http("/set_group_leave", {"group_id": group_id, "is_dismiss": is_dismiss})

    # 文件
    def upload_group_file(self, group_id, file, name, folder):
        """
        上传群文件
        :param group_id: 群号
        :param file: 本地文件路径
        :param name: 储存名称
        :param folder: 父目录id
        :return:
        """
        return http("/upload_group_file", {"group_id": group_id, "file": file, "name": name, "folder": folder})

    def delete_group_file(self, group_id, file_id, busid):
        """
        删除群文件
        :param group_id: 群号
        :param file_id: 文件id，参考File对象
        :param busid: 文件类型，参考File对象
        :return:
        """
        return http("/delete_group_file", {"group_id": group_id, "file_id": file_id, "busid": busid})

    def create_group_file_folder(self, group_id, name, parent_id):
        """
        创建群文件文件夹
        :param group_id: 群号
        :param name: 文件夹名称
        :param parent_id: 仅能为 /
        :return:
        """
        return http("/create_group_file_folder", {"group_id": group_id, "name": name, "parent_id": parent_id})

    def delete_group_folder(self, group_id, folder_id):
        """
        删除群文件夹
        :param group_id: 群号
        :param folder_id: 文件夹ID 参考 Folder 对象
        :return:
        """
        return http("/delete_group_folder", {"group_id": group_id, "folder_id": folder_id})

    def get_group_file_system_info(self, group_id):
        """
        获取群文件系统信息
        :param group_id: 群号
        :return:
        """
        return http("/get_group_file_system_info", {"group_id": group_id})

    def get_group_root_files(self, group_id):
        """
        获取群根目录文件列表
        :param group_id: 群号
        :return:
        """
        return http("/get_group_root_files", {"group_id": group_id})

    def get_group_files_by_folder(self, group_id, folder_id):
        """
        获取群子目录文件列表
        :param group_id: 群号
        :param folder_id: 文件夹id，参考 Folder 对象
        :return:
        """
        return http("/get_group_files_by_folder", {"group_id": group_id, "folder_id": folder_id})

    def get_group_file_url(self, group_id, file_id, busid):
        """
        获取群文件资源链接
        :param group_id: 群号
        :param file_id: 文件id，参考 File 对象
        :param busid: 文件类型，参考 File 对象
        :return:
        """
        return http("/get_group_file_url", {"group_id": group_id, "file_id": file_id, "busid": busid})

    def upload_private_file(self, user_id, file, name):
        """
        上传私聊文件
        :param user_id: 对方QQ号
        :param file: 本地文件路径
        :param name: 文件名称
        :return:
        """
        return http("/upload_private_file", {"user_id": user_id, "file": file, "name": name})

    # go-cqhttp相关
    def get_cookies(self, domain):
        """
        获取 Cookies
        :param domain: 需要获取 cookies 的域名
        :return:
        """
        return http("/get_cookies", {"domain": domain})

    def get_csrf_token(self):
        """
        获取 CSRF Token
        :return:
        """
        return http("/get_csrf_token")

    def get_credentials(self, domain):
        """
        获取 QQ 相关接口凭证
        :param domain: 需要获取 cookies 的域名
        :return:
        """
        return http("/get_credentials", {"domain": domain})

    def get_version_info(self):
        """
        获取版本信息
        :return:
        """
        return http("/get_version_info")

    def get_status(self):
        """
        获取状态
        :return:
        """
        return http("/get_status")

    def clean_cache(self):
        """
        清理缓存
        :return:
        """
        return http("/clean_cache")

    def reload_event_filter(self, file):
        """
        重载事件过滤器
        :param file: 事件过滤器文件
        :return:
        """
        return http("/reload_event_filter", {"file": file})

    def download_file(self, url, thread_count, headers):
        """
        下载文件到缓存目录
        :param url: 链接地址
        :param thread_count: 下载线程数
        :param headers: 自定义请求头
        :return:
        """
        return http("/download_file", {"url": url, "thread_count": thread_count, "headers": headers})

    def check_url_safely(self, url):
        """
        获取连接安全性
        :param url: 需要检查的链接
        :return:
        """
        return http("/check_url_safely", {"url": url})

    # Lagrange 拓展接口
    def fetch_custom_face(self):
        """
        获取收藏表情
        :return:
        """
        return http("/fetch_custom_face")

    def get_friend_msg_history(self, user_id, message_id, count):
        """
        获取好友历史消息记录
        :param user_id: 好友ID
        :param message_id: 要获取的消息的最后一条的 ID
        :param count: 获取的消息数量
        :return:
        """
        return http("/get_friend_msg_history", {"user_id": user_id, "message_id": message_id, "count": count})

    def _get_group_msg_history(self, group_id, message_id, count):
        """
        !!!重复，Lagrange协议前面需加_前缀!!!
        获取群组历史消息记录
        :param group_id: 群组ID
        :param message_id: 要获取的消息的最后一条的 ID
        :param count: 获取的消息数量
        :return:
        """
        return http("/get_group_msg_history", {"group_id": group_id, "message_id": message_id, "count": count})

    def send_forward_msg(self, messages):
        """
        构造合并转发消息
        :param messages: 参考https://lagrangedev.github.io/Lagrange.Doc/Lagrange.OneBot/API/Extend/#%E6%9E%84%E9%80%A0%E5%90%88%E5%B9%B6%E8%BD%AC%E5%8F%91%E6%B6%88%E6%81%AF
        :return:
        """
        return http("/send_forward_msg", {"messages": messages})

    def _send_group_forward_msg(self, group_id, messages):
        """
        !!!重复，Lagrange协议签需加_前缀!!!
        发送合并转发 (群聊)
        :param group_id: 群号
        :param messages: 自定义转发消息, 要求参看前文
        :return:
        """
        return http("/send_group_forward_msg", {"group_id": group_id, "messages": messages})

    def _send_private_forward_msg(self, user_id, messages):
        """
        !!!重复，Lagrange协议签需加_前缀!!!
        发送合并转发 (好友)
        :param user_id: 好友 QQ 号
        :param messages: 自定义转发消息, 要求参看前文
        :return:
        """
        return http("/send_private_forward_msg", {"user_id": user_id, "messages": messages})

    def _upload_group_file(self, group_id, file, name, folder):
        """
        !!!重复，Lagrange协议签需加_前缀!!!
        上传群文件
        :param group_id: 群号
        :param file: 本地文件路径
        :param name: 储存名称
        :param folder: 父ID目录
        :return:
        """
        return http("/upload_group_file", {"group_id": group_id, "file": file, "name": name, "folder": folder})

    def _upload_private_file(self, user_id, file, name):
        """
        !!!重复，Lagrange协议签需加_前缀!!!
        私聊发送文件
        :param user_id: 对方QQ号
        :param file: 本地文件路径
        :param name: 文件名称
        :return:
        """
        return http("/upload_private_file", {"user_id": user_id, "file": file, "name": name})

    def _get_group_root_files(self, group_id):
        """
        !!!重复，Lagrange协议签需加_前缀!!!
        获取群根目录文件列表
        :param group_id: 群号
        :return:
        """
        return http("/get_group_root_files", {"group_id": group_id})

    def _get_group_files_by_folder(self, group_id, folder_id):
        """
        !!!重复，Lagrange协议签需加_前缀!!!
        获取群子目录文件列表
        :param group_id: 群号
        :param folder_id: 文件夹 ID 参考 Folder 对象
        :return:
        """
        return http("/get_group_files_by_folder", {"group_id": group_id, "folder_id": folder_id})

    def _get_group_file_url(self, group_id, file_id, busid):
        """
        !!!重复，Lagrange协议签需加_前缀!!!
        获取群文件资源链接
        :param group_id: 群号
        :param file_id: 文件ID
        :param busid: 文件类型
        :return:
        """
        return http("/get_group_file_url", {"group_id": group_id, "file_id": file_id, "busid": busid})

    def friend_poke(self, user_id):
        """
        好友戳一戳
        :param user_id: 对方QQ号
        :return:
        """
        return http("/friend_poke", {"user_id": user_id})

    def group_poke(self, group_id, user_id):
        """
        群组戳一戳
        :param group_id: 群号
        :param user_id: 对方QQ号
        :return:
        """
        return http("/group_poke", {"group_id": group_id, "user_id": user_id})

    def _set_group_special_title(self, group_id, user_id, special_title):
        """
        !!!重复，Lagrange协议签需加_前缀!!!
        设置群组专属头衔
        :param group_id: 群号
        :param user_id: 要设置的 QQ 号
        :param special_title: 专属头衔, 空字符串表示删除专属头衔
        :return:
        """
        return http("/set_group_special_title",
                    {"group_id": group_id, "user_id": user_id, "special_title": special_title})
