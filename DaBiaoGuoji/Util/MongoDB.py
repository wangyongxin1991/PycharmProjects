# -*- coding: utf-8 -*-
import pymongo
from DaBiaoGuoji.configs import config
import sys
from logbook import Logger, StreamHandler

StreamHandler(sys.stdout).push_application()
_log = Logger('FileOperation')
# 获取mongodb的配置信息
_conf = config.dbconfigs.get('mongodb')


class getConnect(object):
    StreamHandler(sys.stdout).push_application()
    logger = Logger('MongoDB')

    # 初始化
    def __init__(self,_sheet_tab):
        self._conn = self._getConnAndDB(_sheet_tab)
    #
    def _getConnAndDB(self,_sheet_tab):
        # 创建mongoDB连接
        self._conn = pymongo.MongoClient(_conf.get('HOST'),_conf.get('PORT'))
        print('HOST='+ _conf.get('HOST')+',PORT='+ str(_conf.get('PORT')))
        # 给数据库命名
        self._DB = self._conn[_conf.get('DB')]
        print('DB='+_conf.get('DB'))
        #连接的表
        self.sheet_tab = self._DB[_sheet_tab]
        print('sheet_tab='+_sheet_tab)
        return self.sheet_tab


