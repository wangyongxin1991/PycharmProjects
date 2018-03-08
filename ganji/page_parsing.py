from bs4 import BeautifulSoup
import requests
import time
import re
import pymongo

client = pymongo.MongoClient('localhost',27017)
ganjidb = client['ganjidb']
url_list = ganjidb['url_list']
page_info = ganjidb['page_info']

#获取列表页url
#http://bj.ganji.com/shouji/a2o3/
def get_list_page(channel,pages=1):
    view_url = '{}o{}/'.format(channel,pages)
    web_data = requests.get(view_url)
    soup = BeautifulSoup(web_data.text,'lxml')

    if soup.find('noinfo'):
        return
    for link in soup.select('tbody a'):
        link_url = link.get('href')
        if link_url.find('http')<0:
            link_url = 'http:'+link_url
            url_list.insert_one({'url':link_url})
            print(link_url)
    #else:
        # pass

#获取详细页
#http://bj.ganji.com/shouji/782438323x.htm
def get_page_info(url,data=None):
    time.sleep(2)
    web_data = requests.get(url)
    if web_data.status_code == 404|304:
        pass
    else:
       soup = BeautifulSoup(web_data.text,'lxml')

    try:
        title    = soup.select('h1.title-name')[0].get_text()
        type     = soup.select('ul > li:nth-of-type(1) > span > a')[1].get_text()
        price    = soup.select('i.f22.fc-orange.f-type')[0].get_text()
        pub_date = soup.select('.pr-5')[0].text.strip().split(' ')[0]
        place    = soup.select('ul > li:nth-of-type(3) > a')[2].get_text()+'-'+soup.select('ul > li:nth-of-type(3) > a')[3].get_text()
        phone    = soup.select('ul > li:nth-of-type(6) > span.phoneNum-style')[0].get_text()
        qqNum    = soup.select('ul > li:nth-of-type(7) > span')[0].get_text()
        fnname   = soup.select('div.bas-info-s > p > a')[0].get_text()
    except:
        print('查不到商品信息!!')
        return

    if data == None:
        data = {
            'fnname': formatData(fnname),
            'qqNum': formatData(qqNum),
            'phone': formatData(phone),
            'type': type,
            'pub_date':pub_date,
            'price': price,
            'place': formatData(place),
            'title':title
        }
    page_info.insert_one({'fnname':data.get('fnname'),
                          'qqNum' : data.get('qqNum'),
                          'phone' : data.get('phone'),
                          'type'  : data.get('type'),
                          'pub_date':data.get('pub_date'),
                          'price' : data.get('price'),
                          'place' : data.get('place'),
                          'title' : data.get('title'),
                          'url'   :url
                          })
    print(data)

def formatData(data):
    data = data.replace('\r','').replace('\n','').replace(' ','')
    return data

#get_list_page('http://bj.ganji.com/shouji/a2')
#get_page_info('http://bj.ganji.com/shouji/782438323x.htm')