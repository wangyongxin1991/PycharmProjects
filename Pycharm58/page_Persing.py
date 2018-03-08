from bs4 import BeautifulSoup
import requests
import pymongo
import time
import re
import random

client = pymongo.MongoClient('localhost',27017)
ceshi = client['ceshi']
url_list = ceshi['url_list']
item_info = ceshi['item_info']


def requests_headers():
    #head_connection = ['Keep-Alive','close']
    head_user_agent = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3']

    header = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection':'Keep-Alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Cookie':'UM_distinctid=15fca3b3abd202-09963241c6fbf6-6010137f-100200-15fca3b3abe6d4; id58=oVaaTloO6EWQLp5dU3y8hw==; als=0; commontopbar_myfeet_tooltip=end; cookieuid=9cca3f25-f3d6-4ca7-8607-74e758ea3d0e; m58comvp=t17v115.159.229.20; bj58_id58s="SnFtbS1kWHI5S3BBMTczOQ=="; br58_ershou=salev1_ershou; mcityName=%E5%B9%BF%E5%B7%9E; nearCity=%5B%7B%22cityName%22%3A%22%E5%B9%BF%E5%B7%9E%22%2C%22city%22%3A%22gz%22%7D%5D; cookieuid1=c5/nploO/tRa4BesBUitAg==; bj58_new_uv=1; myfeet_tooltip=end; gr_user_id=5825df17-fa3b-4078-88b5-c93aebe17227; wmda_uuid=32f3985882f98a906c79fe5ab296a929; wmda_new_uuid=1; wmda_visited_projects=%3B1409632296065; __utma=253535702.1904368431.1511001677.1511264982.1511264982.1; __utmz=253535702.1511264982.1.1.utmcsr=gz.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/; mcity=gz; city=gz; 58home=gz; commontopbar_ipcity=gz%7C%E5%B9%BF%E5%B7%9E%7C0; sessionid=1a23283a-ab1f-44b5-b347-f48a6810fd6b; wmda_session_id=1512404991959-8ffc7f39-4bae-6e4d; ppStore_fingerprint=D1760517FDDA3729E37298B0EE8E712909F2A7A7198E1E6B%EF%BC%BF1512404992050; GA_GTID=0d400067-05b3-2119-f567-d96859b68a26; Hm_lvt_e2d6b2d0ec536275bb1e37b421085803=1511184965,1511543519,1511788744,1512404992; Hm_lpvt_e2d6b2d0ec536275bb1e37b421085803=1512404992; _ga=GA1.2.1904368431.1511001677; _gid=GA1.2.938704022.1512404992; _gat=1; gr_session_id_98e5a48d736e5e14=7c8e7279-d7c7-4200-b6b4-308aa989550b; bai=16.; 58tj_uuid=c93a9af2-1c92-4fd3-b7f9-91e660ebde4c; new_session=0; new_uv=25; utm_source=link; spm=u-Luu6JOva1luDubj.psy_12; init_refer=; final_history=31300797475146%2C32180232299966%2C28322044779049%2C32090126619566%2C31604502842924; ipcity=gz%7C%u5E7F%u5DDE; xxzl_deviceid=qWZtrJOTdk12%2BPW2dxlp43EiT37tE66efabzJmVOafYUcggyzhcMkn5vpvjtg5g6',
        'Referer':'http://gz.58.com/pingbandiannao/31300797475146x.shtml?adtype=1&PGTID=0d305a36-0000-3d71-5939-18aa11812acd&entinfo=31300797475146_0&psid=126689244198233949998230946&iuType=_undefined&ClickID=1',
        'Host':'jst1.58.com'
    }
    return header

# http://cn-proxy.com/
proxy_list = [
    'http://192.168.1.1:80',
    'http://218.241.234.48:8080',
    'http://61.155.164.108:3128',
    'http://116.52.194.177:9999',
    'http://27.44.77.133:8080',
    'http://218.56.132.155:8080'
    ]
proxy_ip = random.choice(proxy_list) # 随机获取代理ip
proxies = {'http': proxy_ip}

def get_soup(url):
    web_data = requests.get(url,headers=requests_headers(),timeout = 100)
    if web_data.status_code == 404:
        pass
    else:
        soup = BeautifulSoup(web_data.text, 'lxml')
    return soup

#spider 1 获取列表页
def get_links_from(channel,pages,who_sells=1):
    #http://gz.58.com/shouji/0/pn3/
    list_view = '{}{}/pn{}'.format(channel,str(who_sells),str(pages))
    soup = get_soup(list_view)
    time.sleep(1)

    #为了防止溢出,做一个判断 , 如果页面不包含标签则不爬取
    try:
        for link in soup.select('.left a.title.t'):
            item_link = link.get('href')#.split('?')[0]
            result = re.compile(r'.*58.*')
            if result.match(str(item_link)):
                url_list.insert_one({'url':item_link}) #插入数据库
                print(item_link)
    except:
        print('not find!!')
        return


#获取id
def get_id(url):
    pattern1 = re.compile(r"^.*entinfo.*$")
    pattern2 = re.compile(r"^.*x.shtml.*$")

    if pattern1.findall(url):
        id = url.split('entinfo=')[1].strip('_0')
        print('商品id:' + id)
    elif pattern2.findall(url):
        id = url.split('/')[4].strip('x.shtml')
        print('商品id:' + id)
    else:
        return 0
    return id

#获取人数  entinfo=32140990109895_0
def get_view_info(url):

    id = get_id(url)
    api = 'http://jst1.58.com/counter?infoid={}'.format(id)
    js = requests.get(api,headers=requests_headers(),timeout=10)
    views = js.text.split('=')[-1]
    return views

#获取详细页  http://tj.58.com/shouji/32161338069432x.shtml
def get_58_info(url,who_sells=1,data=None):
    print(url)
    web_data = requests.get(url,timeout=10)
    web_data.encoding = 'utf-8'
    if web_data.status_code == 404:
        pass
    else:
        soup = BeautifulSoup(web_data.text, 'lxml')
        print(soup.title.text)
        if soup.title.text == '您访问的页面不存在- 58.com':
            id = get_id(url)
            for item in item_info.find({'url':re.compile(id)}):
                print(item['url'])
                item_info.update({'url':re.compile(item['url'])},{'$set':{'sellTime':1}})
                print('更新sellTime'+item['url'])
                return
    # 异常字段过滤
    try:
        soup.select('.col_sub.mainTitle h1')[0].text
        soup.select('ul > li:nth-of-type(2) > div.su_con > span')[0].text.strip()
    except:
        print('No page')
        return

    if data == None:
        data = {
            'title'   : soup.select('.col_sub.mainTitle h1')[0].text,
            'price'   : formatData(soup.select('.price.c_f50')[0].text),
            'sucon'   : soup.select('ul > li:nth-of-type(2) > div.su_con > span')[0].text.strip(),
            'date'    : soup.select('li.time')[0].text,
            'counter' : get_view_info(url),
            'area'    : list(map(lambda x:x.text,soup.select('span.c_25d a'))),
            'cate'    : '个人' if who_sells == 0 else '商家',
            'url'     : url,
            'cateType':list(map(lambda x:x.text,soup.select('.breadCrumb.f12 a'))),
            'sellTime':0
        }

        print(data)
        item_info.insert_one({
              'title': data.get('title'),
              'price': data.get('price'),
              'sucon': data.get("sucon"),
              'date': data.get('date'),
              'counter': data.get('counter'),
              'area': data.get('area'),
              'cate': data.get('cate'),
              'url': data.get('url'),
              'cateType':data.get('cateType'),
              'sellTime':data.get('sellTime')
              })

#字段格式化
def formatData(data):
    data = data.replace('\r', '').replace('\n', '').replace(' ', '').replace('\t', '')
    return data

#get_58_info('http://tj.58.com/shouji/32161338069432x.shtml')