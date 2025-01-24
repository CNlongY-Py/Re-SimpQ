import os
import json


class Config:
    def __init__(self, folder):
        """
        Re-SimpQ提供的统一配置文件接口
        :param folder: 文件夹名称
        """
        self.folder = "./config/" + folder
        self.file = ""
        self.cache = {}
        if folder not in os.listdir("./config"):
            os.mkdir("./config/" + folder)

    def load(self, file):
        """
        加载配置文件，不存在则自动创建
        :param file: 文件名称
        :return: None
        """
        if "%s.json" % file in os.listdir(self.folder):
            self.file = file
            self.cache = self.read()
        else:
            with open(f"{self.folder}/{file}.json", "w+", encoding="utf-8") as f:
                f.write("{}")
            self.file = file
            self.cache = self.read()

    def getFile(self, file):
        """
        判断配置文件是否存在
        :param file: 文件名称
        :return: 存在返回True，不存在返回False
        """
        if "%s.json" % file in os.listdir(self.folder):
            return True
        else:
            return False

    def set(self, key, value):
        """
        设置数据
        :param key: 键名
        :param value: 键值
        :return: None
        """
        self.cache[key] = value
        self.save()

    def get(self, key):
        """
        读取数据
        :param key: 键名
        :return: 存在则返回数据，不存在则返回 None
        """
        if key in self.cache:
            return self.cache[key]
        else:
            return None

    def save(self):
        """
        保存数据
        :return: None
        """
        with open(f"{self.folder}/{self.file}.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(self.cache))

    def read(self):
        """
        读取数据
        :return: 配置数据
        """
        with open(f"{self.folder}/{self.file}.json", "r", encoding="utf-8") as f:
            cache = json.loads(f.read())
            return cache
