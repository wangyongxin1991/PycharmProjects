from bs4 import BeautifulSoup
import requests
import time
import random
import re


url = 'http://gz.58.com/jiadian/32112939422791x.shtml?spm=u-Luu6JOva1luDubj.psy_12&utm_source=link&psid=199275793198040150693510361&entinfo=32112939422791_0&iuType=z_2&PGTID=0d300027-0000-3aec-54fe-78c820725aa1&ClickID=1&adtype=3'
def requests_headers():
    head_connection = ['Keep-Alive','close']
    head_accept = ['text/html,application/xhtml+xml,*/*']
    head_accept_language = ['zh-CN,fr-FR;q=0.5','en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']
    head_user_agent = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                       'Opera/9.27 (Windows NT 5.2; U; zh-cn)']

    header = {
        'Connection':'Keep-Alive',
        'User-Agent': head_user_agent[random.randrange(0, len(head_user_agent))],
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Cookie':'userid360_xml=62A349A731A55A9DE47A9D821272762B; time_create=1513774451476; f=n; userid360_xml=62A349A731A55A9DE47A9D821272762B; time_create=1513774813604; ipcity=gz%7C%u5E7F%u5DDE; f=n; UM_distinctid=15fca3b3abd202-09963241c6fbf6-6010137f-100200-15fca3b3abe6d4; id58=oVaaTloO6EWQLp5dU3y8hw==; als=0; commontopbar_myfeet_tooltip=end; bdshare_firstime=1510929879034; cookieuid=9cca3f25-f3d6-4ca7-8607-74e758ea3d0e; m58comvp=t17v115.159.229.20; bj58_id58s="SnFtbS1kWHI5S3BBMTczOQ=="; br58_ershou=salev1_ershou; mcityName=%E5%B9%BF%E5%B7%9E; nearCity=%5B%7B%22cityName%22%3A%22%E5%B9%BF%E5%B7%9E%22%2C%22city%22%3A%22gz%22%7D%5D; cookieuid1=c5/nploO/tRa4BesBUitAg==; bj58_new_uv=1; myfeet_tooltip=end; gr_user_id=5825df17-fa3b-4078-88b5-c93aebe17227; wmda_uuid=32f3985882f98a906c79fe5ab296a929; wmda_new_uuid=1; wmda_visited_projects=%3B1409632296065; __utma=253535702.1904368431.1511001677.1511264982.1511264982.1; __utmz=253535702.1511264982.1.1.utmcsr=gz.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ppStore_fingerprint=D1760517FDDA3729E37298B0EE8E712909F2A7A7198E1E6B%EF%BC%BF1511789314055; Hm_lvt_e2d6b2d0ec536275bb1e37b421085803=1511184965,1511543519,1511788744; _ga=GA1.2.1904368431.1511001677; final_history=28322044779049%2C32090126619566%2C31604502842924%2C32180990658120%2C32036288861888; CNZZDATA1267526846=247142500-1510925836-%7C1512400439; mcity=gz; city=gz; 58home=gz; commontopbar_ipcity=gz%7C%E5%B9%BF%E5%B7%9E%7C0; f=n; sessionid=1a23283a-ab1f-44b5-b347-f48a6810fd6b; 58tj_uuid=c93a9af2-1c92-4fd3-b7f9-91e660ebde4c; new_session=0; new_uv=25; utm_source=link; spm=u-Luu6JOva1luDubj.psy_12; init_refer=; xxzl_deviceid=qWZtrJOTdk12%2BPW2dxlp43EiT37tE66efabzJmVOafYUcggyzhcMkn5vpvjtg5g6',
        'Referer': 'http://gz.58.com/',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate',
        'Host' :'gz.58.com'
    }
    return header

#格式化数据
def dealText(str):
    str = str.replace("\n","").replace("\r","").replace("\t","").replace(" ","")
    return str

#获取列表页信息,默认是个人
def get_list_info(who_sells=0):
    urls = []
    view_list = 'http://gz.58.com/ershoukongtiao/{}/?PGTID=0d3001f6-0000-3216-c336-c230fa90a4d1&ClickID=1'.format(str(who_sells))
    web_data = requests.get(view_list)
    soup = BeautifulSoup(web_data.text,'lxml')
    time.sleep(2)

    for link in soup.select('td.img a'):
        urls.append(link.get('href'))
        #print(urls)
    return urls

#获取人数
def get_view_info(url):
    id = url.split('?')[0].split('/')[-1].strip('x.shtml')
    api = 'http://jst1.58.com/counter?infoid={}'.format(id)
    js = requests.get(api)
    views = js.text.split('=')[-1]
    return views

#获取详细页信息
def get_item_info(who_sells=0):

    urls = get_list_info(who_sells)

    for url in urls:
        print(url)
        web_data = requests.get(url)
        soup = BeautifulSoup(web_data.text,'lxml')
        price = soup.select('div.su_con span.price.c_f50')
        time  = soup.select('#content li.time')
        chengse = soup.select('div.col_sub.sumary > ul > li:nth-of-type(2) > div.su_con') #if soup.find_all('span','su_con') else None

        data = {

            'totalcount':get_view_info(url)
        }
        print(data)

get_item_info(0)