# -*- coding: utf-8 -*-

import pymongo
import datetime
import time
from DaBiaoGuoji.Util import MongoDB
_jiayi_tab = MongoDB.getConnect('jiayi_tab')

class roomClass:  # 定义房间类
    # specialDoubleRoom
    # deluxeRoom
    # deluxeDoubleRoom
    # businessRoom
    # businessDoubleRoom
    # ExecutiveRoom
    # ExecutiveDoubleRoom
    def __init__(self, specialRoom,specialDoubleRoom, deluxeRoom,deluxeDoubleRoom,
                 businessRoom,businessDoubleRoom,ExecutiveRoom,ExecutiveDoubleRoom):
        self.specialRoom = specialRoom
        self.specialDoubleRoom = specialDoubleRoom
        self.deluxeRoom = deluxeRoom
        self.deluxeDoubleRoom = deluxeDoubleRoom
        self.businessRoom = businessRoom
        self.businessDoubleRoom = businessDoubleRoom
        self.ExecutiveRoom = ExecutiveRoom
        self.ExecutiveDoubleRoom = ExecutiveDoubleRoom

    def _search_one(checkInDate):
        result=None
        try:
            result = _jiayi_tab.sheet_tab.find_one({'checkInDate':checkInDate})
        except:
            print('查找数据出现异常!!!')

        if(result != None):
            return result
        else:
            return None

    def insert_One(roomTitle,specialRoom,specialDoubleRoom,deluxeRoom,deluxeDoubleRoom, businessRoom,
                   businessDoubleRoom,ExecutiveRoom,ExecutiveDoubleRoom,checkInDate):
        result = roomClass._search_one(checkInDate)
        print(result)
        print('重复日期数据!!')
        if result is None:
            try:
                _jiayi_tab.sheet_tab.insert({
                    'roomTitle': roomTitle,
                    'specialRoom': specialRoom,
                    'specialDoubleRoom': specialDoubleRoom,
                    'deluxeRoom': deluxeRoom,
                    'deluxeDoubleRoom': deluxeDoubleRoom,
                    'businessRoom': businessRoom,
                    'businessDoubleRoom': businessDoubleRoom,
                    'ExecutiveRoom': ExecutiveRoom,
                    'ExecutiveDoubleRoom': ExecutiveDoubleRoom,
                    'checkInDate': checkInDate,
                    'operateTime': time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                })
                print('插入一条数据')
            except:
                print('插入数据异常')
        else:
            return
        return


