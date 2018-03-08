import pymongo
from DaBiaoGuoji.configs import config
import sys
from logbook import Logger, StreamHandler

StreamHandler(sys.stdout).push_application()
log = Logger('FileOperation')
# 获取mongodb的配置信息
conf = config.dbconfigs.get('mongodb')


class MongoDB(object):
    StreamHandler(sys.stdout).push_application()
    logger = Logger('MongoDB')

    #初始化
    def __init__(self):
        self._conn = self.getConnAndDB()

    def getConnAndDB(self):
        # 创建mongoDB连接
        self._conn = pymongo.MongoClient(conf.get('HOST'),conf.get('PORT'))
        # 给数据库命名
        self._DB = self._conn[conf.get('DB')]
        return self._DB

MongoDB()