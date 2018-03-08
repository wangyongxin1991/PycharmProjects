# coding: utf-8
'''
存数据库的配置
'''
dbconfigs = {
    "elasticsearch": {
        "HOST": ["192.168.10.219", "192.168.10.225", "192.168.12.34"],
        "USER": "elasti",
        "PASSWORD": "changeme"
    },
    "hbase": {
        "HOST": "192.168.12.34"
    },
    "mongodb": {
        "HOST": "localhost",
        "PORT": 27017,
        "DB" : "yiLongDB"
    },
    "redis": {
        "HOST": "192.168.10.219",
        "PORT": 6002,
        "DB": 3,
        "MAX_CONNECTIONS": 20,
        "PASSWORD": "Hhly2015"
    },
    "mysql": {
        "HOST": '127.0.0.1',
        "PORT": 3306,
        "DB": "yilongDB",
        "POOLSIZE": 20,
        "USER": "root",
        "PASSWORD": "root"
    }
}
