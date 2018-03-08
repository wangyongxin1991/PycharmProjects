#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (MetaData, Table, Column, Integer, Numeric, String, Boolean,
                        DateTime, ForeignKey, ForeignKey, create_engine, insert,DATE)
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/yilongspider?charset=utf8", max_overflow=5,encoding='utf-8')

metadata = MetaData()

#Base = declarative_base()
# class hotel(Base):
#     __tablename__ = 'hotel'
#     id = Column(Integer,primary_key=True)
#     hotelName = Column(String(32))
#     hotelType = Column(Integer)
#
#     def __repr__(self):
#         return "<%s hotelName:%s hotelType:%s >" % (self.id, self.hotelName, self.hotelType)
#
# class room(Base):
#     __tablename__ = 'room'
#     id = Column(Integer,primary_key=True)
#     roomName = Column(String(64))
#     roomType = Column(Integer)
#     def __repr__(self):
#         return "<%s roomName:%s roomType:%s>" % (self.id, self.roomName, self.roomType)
#
# class price(Base):
#     __tablename__ ='price'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     hotel_id = Column(Integer,ForeignKey('hotel.id'))
#     room_id = Column(Integer,ForeignKey('room.id'))
#     price = Column(Numeric(10,2))
#     #入住日期
#     checkInDate = Column(DATE)
#     #数据是否有效 1:有效 0:无效 valid
#     isValid = Column(Integer,default=1)
#
#     def __repr__(self):
#         return "<%s hotel_id:%s room_id:%s price:%s isValid:%s>" % \
#                (self.id, self.hotel_id,self.room_id,self.price,self.checkInDate,self.isValid)
#
# def init_db():  # 创建表
#     Base.metadata.create_all(engine)
#
#
# def drop_db():  # 删除表
#     Base.metadata.drop_all(engine)

# drop_db()

#初始化数据库的方法
#init_db()

# Session_class = sessionmaker(bind=engine) #创建与数据库的会话session class,注意这里返回给session的是个类，不是实例
# Session = Session_class() #生成session实例
#
# hotel_Obj = hotel(hotelName='特价大',hotelType=1)
# Session.add(hotel_Obj)
# Session.commit()
#
# data = Session.query(hotel).filter_by(id=1).all()
# print(data)

#----------------------------------------------------------------------------
cookies = Table('cookies', metadata,
                Column('cookie_id', Integer(), primary_key=True),
                Column('cookie_name', String(50), index=True),
                Column('cookie_recipe_url', String(255)),
                Column('cookie_sku', String(55)),
                Column('quantity', Integer()),
                Column('unit_cost', Numeric(12, 2))
                )
hotels = Table('hotel',metadata,
              Column('id',Integer(),primary_key=True),
              Column('hotelName',String(32)),
              Column('hotelType',Integer())
        )
prices = Table('price',metadata,
              Column('id',Integer(),primary_key=True),
              Column('hotel_id',Integer(),ForeignKey('hotel.id')),
              Column('room_id',Integer(),ForeignKey('room.id')),
              Column('price',Numeric(10,2)),
              Column('checkInDate',DATE()),
              Column('isValid',Integer(),default=1)
        )
rooms = Table('room',metadata,
              Column('id',Integer(),primary_key=True),
              Column('roomName',String(64)),
              Column('roomType',Integer())
)

metadata.create_all(engine)

ins = cookies.insert()
roomInsert = rooms.insert()

room_list = [
    {
        'roomName':'特价大床房',
        'roomType':'1'
    },
    {
        'roomName':'特价双床房',
        'roomType':'2'
    },
    {
        'roomName':'豪华大床房',
        'roomType':'3'
    },
    {
        'roomName':'豪华双床房',
        'roomType':'4'
    },
    {
        'roomName':'商务大床房',
        'roomType':'5'
    },
    {
        'roomName':'商务双床房',
        'roomType':'6'
    },
    {
        'roomName':'行政商务大床房',
        'roomType':'7'
    },
    {
        'roomName':'行政商务双床房',
        'roomType':'8'
    }
]

#批量插入数据
inventory_list = [
    {
        'cookie_name': 'peanut butter',
        'cookie_recipe_url': 'http://some.aweso.me/cookie/peanut.html',
        'cookie_sku': 'PB01',
        'quantity': '24',
        'unit_cost': '0.25'
        },
    {
        'cookie_name': 'oatmeal raisin',
        'cookie_recipe_url': 'http://some.okay.me/cookie/raisin.html',
        'cookie_sku': 'EWW01',
        'quantity': '100',
        'unit_cost': '1.00'
        }
    ]

result = engine.connect().execute(roomInsert,room_list)
print(result)
#--------------------------------------------------------------------------------