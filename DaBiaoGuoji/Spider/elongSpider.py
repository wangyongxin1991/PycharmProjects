# -*- coding: utf-8 -*-
import os
import time
import datetime
from DaBiaoGuoji.Util import Global
import threading
from DaBiaoGuoji.Model import hotel
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


#driver = webdriver.Chrome()
#添加user-Agent和cookies信息
chromedriver = 'E:/Google/chromedriver.exe'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('lang=zh_CN.UTF-8')
chrome_options.add_argument('user-agent="Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;TencentTraveler4.0)"')
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver, chrome_options=chrome_options)

Global._init()
Global.set_value('timeFlag','False')

def jiayi_hotel_price(checkInDate=today_str, leaveTime=tomorrow_str):
    print(today_str)
    driver.get(jiayiSite)
    #获取cookies
    driver.get_cookies()
    driver.maximize_window()
    driver.implicitly_wait(10)  # 隐形等待10秒
    inputDate(checkInDate,leaveTime)
    #Global.set_value('timeFlag','True')
    time.sleep(500)
    driver.close()
    return


def inputDate(checkInDate,leaveDate):
    # 将页面滚动条下拉到合适的位置
    js = "var q=document.documentElement.scrollTop=500"
    driver.execute_script(js)
    driver.implicitly_wait(10)  # 隐形等待10秒
    driver.find_element_by_xpath('//*[@id="afterCouponContainer"]/li[2]').click()
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div[3]/div[1]/label[1]/input').clear()
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div[3]/div[1]/label[1]/input').send_keys(checkInDate)
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div[3]/div[1]/label[2]/input').clear()
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div[3]/div[1]/label[2]/input').send_keys(leaveDate)
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div[3]/div[2]').click()

    driver.implicitly_wait(10)
    #hotelTitle = '广州嘉驿国际公寓(昌岗江南大道店)'
    roomTitle = driver.find_element_by_xpath('//*[@id="lastbread"]').text
    driver.implicitly_wait(10)
    # 特价大床房
    specialRoom = driver.find_element_by_xpath('//*[@id="roomSetContainer"]/div/div/div[1]/div[2]/div[2]/p[1]/span[2]').text
    driver.implicitly_wait(10)
    # 特价双床房
    specialDoubleRoom = driver.find_element_by_xpath('//*[@id="roomSetContainer"]/div/div/div[3]/div[2]/div[2]/p[1]/span[2]').text
    driver.implicitly_wait(10)
    # #豪华大床房
    deluxeRoom = driver.find_element_by_xpath('//*[@id="roomSetContainer"]/div/div/div[2]/div[2]/div[2]/p[1]/span[2]').text
    driver.implicitly_wait(10)
    # #豪华双床房
    deluxeDoubleRoom = driver.find_element_by_xpath('//*[@id="roomSetContainer"]/div/div/div[4]/div[2]/div[2]/p[1]/span[2]').text
    driver.implicitly_wait(10)
    # #商务大床房
    businessRoom = driver.find_element_by_xpath('//*[@id="roomSetContainer"]/div/div/div[5]/div[2]/div[2]/p[1]/span[2]').text
    driver.implicitly_wait(10)
    # #商务双床房
    businessDoubleRoom = driver.find_element_by_xpath('//*[@id="roomSetContainer"]/div/div/div[6]/div[2]/div[2]/p[1]/span[2]').text
    driver.implicitly_wait(10)
    # #行政豪华大床房
    ExecutiveRoom = driver.find_element_by_xpath('//*[@id="roomSetContainer"]/div/div/div[7]/div[2]/div[2]/p[1]/span[2]').text
    driver.implicitly_wait(10)
    # #行政豪华双床房
    ExecutiveDoubleRoom = driver.find_element_by_xpath('//*[@id="roomSetContainer"]/div/div/div[8]/div[2]/div[2]/p[1]/span[2]').text

    driver.implicitly_wait(10)
    hotel.roomClass.insert_One(roomTitle,specialRoom,specialDoubleRoom,deluxeRoom,deluxeDoubleRoom,
                           businessRoom,businessDoubleRoom,ExecutiveRoom,
                           ExecutiveDoubleRoom,checkInDate)
    Global.set_value('timeFlag', 'True')
    #driver.refresh()
    return

#时间累加器
def timeCumulate(checkInTime,leaveTime):
    TcheckInTime = datetime.datetime.strptime(checkInTime, "%Y-%m-%d")
    TleaveTime = datetime.datetime.strptime(leaveTime, "%Y-%m-%d")

    while TleaveTime > TcheckInTime:
        delta = datetime.timedelta(days=1)
        print(Global.get_value('timeFlag'))
        if(Global.get_value('timeFlag')=='True'):
            TcheckInTime = TcheckInTime + delta
            inputDate(TcheckInTime.strftime("%Y-%m-%d"),(TcheckInTime + delta).strftime("%Y-%m-%d"))
        print(TcheckInTime.strftime("%Y-%m-%d"))
        time.sleep(10)

def main():
    threads = []
    t1 = threading.Thread(target=timeCumulate, args=('2018-3-15', '2018-3-25'))
    t2 = threading.Thread(target=jiayi_hotel_price,args=('2018-3-15', '2018-3-16'))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == '__main__':
   main()


# def ticket_worker_no_proxy():
#     driver = webdriver.Chrome()
#     # chromedriver = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
#     # os.environ['webdriver.chrome.driver'] = chromedriver
#     # driver = webdriver.Chrome(chromedriver)
#     driver.get(site)
#     driver.maximize_window()  # 将浏览器最大化显示
#     time.sleep(5)  # 控制间隔时间，等待浏览器反映
#
#     driver.find_element_by_id('hotel_user').send_keys(account)
#     driver.find_element_by_id('password').send_keys(password)
#     time.sleep(10)
#     driver.find_element_by_xpath('//*[@id="submit"]').click()
#     driver.find_element_by_xpath('//*[@id="roomPrice"]/span').click()
#     time.sleep(10)
#     driver.close()