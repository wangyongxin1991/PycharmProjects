from bs4 import BeautifulSoup
import requests

start_url = 'http://bj.ganji.com/wu/'
ganjiurl = 'http://bj.ganji.com'
web_data = requests.get(start_url)
web_data.encoding = 'utf-8'
soup = BeautifulSoup(web_data.text,'lxml')

for url in soup.select('div.main dt a'):
    page_url = ganjiurl + url.get('href')+'a2'
    print(page_url)

#直接获取商家商品 , 个人商品页面有zhuanzhuan的商品
url_item = '''
    http://bj.ganji.com/shouji/a2
    http://bj.ganji.com/shoujipeijian/a2
    http://bj.ganji.com/bijibendiannao/a2
    http://bj.ganji.com/taishidiannaozhengji/a2
    http://bj.ganji.com/diannaoyingjian/a2
    http://bj.ganji.com/wangluoshebei/a2
    http://bj.ganji.com/shumaxiangji/a2
    http://bj.ganji.com/youxiji/a2
    http://bj.ganji.com/xuniwupin/a2
    http://bj.ganji.com/jiaju/a2
    http://bj.ganji.com/jiadian/a2
    http://bj.ganji.com/zixingchemaimai/a2
    http://bj.ganji.com/rirongbaihuo/a2
    http://bj.ganji.com/yingyouyunfu/a2
    http://bj.ganji.com/fushixiaobaxuemao/a2
    http://bj.ganji.com/meironghuazhuang/a2
    http://bj.ganji.com/yundongqicai/a2
    http://bj.ganji.com/yueqi/a2
    http://bj.ganji.com/tushu/a2
    http://bj.ganji.com/bangongjiaju/a2
    http://bj.ganji.com/wujingongju/a2
    http://bj.ganji.com/nongyongpin/a2
    http://bj.ganji.com/xianzhilipin/a2
    http://bj.ganji.com/shoucangpin/a2
    http://bj.ganji.com/baojianpin/a2
    http://bj.ganji.com/laonianyongpin/a2
    http://bj.ganji.com/qitaxiaochong/a2

'''
#http://bj.ganji.com/gou/a2
#http://bj.ganji.com/xiaofeika/a2
#http://bj.ganji.com menpiao/a2