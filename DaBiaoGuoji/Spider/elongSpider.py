import os
import time
import datetime
from DaBiaoGuoji.configs import config
import pymysql
from DaBiaoGuoji.Util import Global
import codecs
import multiprocessing as mp
from os import makedirs
from os.path import exists
from selenium import webdriver


site = 'https://ebooking.elong.com'
site2 = 'http://hotel.elong.com/search/list_cn_2001.html'
# ?keywords=%E8%BE%BE%E9%95%96%E5%9B%BD%E9%99%85%E4%B8%AD%E5%BF%83
jiayiSite = 'http://hotel.elong.com/90568833/'
locaction = '广州市'
today = datetime.date.today()
today_str = today.strftime('%Y-%m-%d')
tomorrow_str = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

localKeyWords = '达镖国际中心'
account = 'jiayi2014'
password = 'jiayi001.'

def ticket_worker_no_proxy():
    driver = webdriver.Chrome()
    # chromedriver = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
    # os.environ['webdriver.chrome.driver'] = chromedriver
    # driver = webdriver.Chrome(chromedriver)
    driver.get(site)
    driver.maximize_window()  # 将浏览器最大化显示
    time.sleep(5)  # 控制间隔时间，等待浏览器反映

    driver.find_element_by_id('hotel_user').send_keys(account)
    driver.find_element_by_id('password').send_keys(password)
    time.sleep(10)
    driver.find_element_by_xpath('//*[@id="submit"]').click()
    driver.find_element_by_xpath('//*[@id="roomPrice"]/span').click()
    time.sleep(10)
    driver.close()

    # 嘉驿公寓价格获取


def jiayi_hotel_price(checkInDate=today, leaveTime=tomorrow_str):
    driver = webdriver.Chrome()
    driver.get(jiayiSite)
    driver.maximize_window()
    driver.implicitly_wait(10)  # 隐形等待10秒

    # 将页面滚动条下拉到合适的位置
    js = "var q=document.documentElement.scrollTop=500"
    driver.execute_script(js)
    driver.implicitly_wait(10)  # 隐形等待10秒
    driver.find_element_by_xpath('//*[@id="afterCouponContainer"]/li[2]').click()
    driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div[3]/div[1]/label[1]/input').clear()
    driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div[3]/div[1]/label[1]/input').send_keys(checkInDate)
    driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div[3]/div[1]/label[2]/input').clear()
    driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div[3]/div[1]/label[2]/input').send_keys(leaveTime)
    driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div[3]/div[2]').click()
    # 特价大床房
    driver.implicitly_wait(10)
    hotelTitle = '广州嘉驿国际公寓(昌岗江南大道店)'
    roomTitle = driver.find_element_by_xpath('//*[@id="roomSetContainer"]/div/div/div[1]/div[2]/div[3]/p[1]/span').text
    print(roomTitle)
    specialRoomPrice = driver.find_element_by_xpath(
        '//*[@id="roomSetContainer"]/div/div/div[1]/div[2]/div[2]/p[1]/span[2]').text
    print(specialRoomPrice)
    time.sleep(1)

    # 特价大床房
    # specialRoom
    # 特价双床房
    #hotel.specialDoubleRoom = driver.find_element_by_xpath('//*[@id="roomSetContainer"]/div/div/div[3]/div[2]/div[2]/p[1]/span[2]').text
    # #豪华大床房
    # hotel.deluxeRoom = driver.find_element_by_xpath('//*[@id="roomSetContainer"]/div/div/div[2]/div[2]/div[2]/p[1]/span[2]').text
    # #豪华双床房
    # hotel.deluxeDoubleRoom = driver.find_element_by_xpath('//*[@id="roomSetContainer"]/div/div/div[4]/div[2]/div[2]/p[1]/span[2]').text
    # #商务大床房
    # hotel.businessRoom = driver.find_element_by_xpath('//*[@id="roomSetContainer"]/div/div/div[5]/div[2]/div[2]/p[1]/span[2]').text
    # #商务双床房
    # hotel.businessDoubleRoom = driver.find_element_by_xpath('//*[@id="roomSetContainer"]/div/div/div[6]/div[2]/div[2]/p[1]/span[2]').text
    # #行政豪华大床房
    # hotel.ExecutiveRoom = driver.find_element_by_xpath('//*[@id="roomSetContainer"]/div/div/div[7]/div[2]/div[2]/p[1]/span[2]').text
    # #行政豪华双床房
    # hotel.ExecutiveDoubleRoom = driver.find_element_by_xpath('//*[@id="roomSetContainer"]/div/div/div[8]/div[2]/div[2]/p[1]/span[2]').text

    # ------------连接mysql数据库的方法-----------
    # try:
    #     mysqlUtil =  Mysql()
    #     # 获取数据库连接
    #     mysqlUtil.__init__()
    #     print('数据库连接成功!!')
    #     sql = '''insert into price(hotel_id,room_id,price,checkInDate) values(%s,%s,%s,%s)'''
    #     param = [['1','1',specialRoomPrice,checkInDate]]
    #     mysqlUtil.insert(sql,param)
    # except Exception as e:
    #   print("异常" + e)



    time.sleep(20)
    driver.close()


jiayi_hotel_price()
