from bs4 import BeautifulSoup
import requests

start_url = 'http://gz.58.com/sale.shtml'
url_host =  'http://gz.58.com'
def get_channel_urls(url):
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text,'lxml')

    links = soup.select('ul.ym-submnu li b a')

    for link in links:
        page_url = url_host + link.get('href')
        print('page_url'+page_url)


#get_channel_urls(start_url)

#要提取的频道的连接
channel_list = '''
    http://gz.58.com/shouji/
    http://gz.58.com/tongxunyw/
    http://gz.58.com/danche/
    http://gz.58.com/diandongche/
    http://gz.58.com/fzixingche/
    http://gz.58.com/sanlunche/
    http://gz.58.com/peijianzhuangbei/
    http://gz.58.com/diannao/
    http://gz.58.com/bijiben/
    http://gz.58.com/pbdn/
    http://gz.58.com/diannaopeijian/
    http://gz.58.com/zhoubianshebei/
    http://gz.58.com/shuma/
    http://gz.58.com/shumaxiangji/
    http://gz.58.com/mpsanmpsi/
    http://gz.58.com/youxiji/
    http://gz.58.com/ershoukongtiao/
    http://gz.58.com/dianshiji/
    http://gz.58.com/xiyiji/
    http://gz.58.com/bingxiang/
    http://gz.58.com/jiadian/
    http://gz.58.com/binggui/
    http://gz.58.com/chuang/
    http://gz.58.com/ershoujiaju/
    http://gz.58.com/yingyou/
    http://gz.58.com/yingeryongpin/
    http://gz.58.com/muyingweiyang/
    http://gz.58.com/muyingtongchuang/
    http://gz.58.com/yunfuyongpin/
    http://gz.58.com/fushi/
    http://gz.58.com/nanzhuang/
    http://gz.58.com/fsxiemao/
    http://gz.58.com/xiangbao/
    http://gz.58.com/meirong/
    http://gz.58.com/yishu/
    http://gz.58.com/shufahuihua/
    http://gz.58.com/zhubaoshipin/
    http://gz.58.com/yuqi/
    http://gz.58.com/tushu/
    http://gz.58.com/tushubook/
    http://gz.58.com/wenti/
    http://gz.58.com/yundongfushi/
    http://gz.58.com/jianshenqixie/
    http://gz.58.com/huju/
    http://gz.58.com/qiulei/
    http://gz.58.com/yueqi/
    http://gz.58.com/bangongshebei/
    http://gz.58.com/diannaohaocai/
    http://gz.58.com/bangongjiaju/
    http://gz.58.com/ershoushebei/
    http://gz.58.com/chengren/
    http://gz.58.com/nvyongpin/
    http://gz.58.com/qinglvqingqu/
    http://gz.58.com/qingquneiyi/
    http://gz.58.com/chengren/
    http://gz.58.com/xiaoyuan/
    http://gz.58.com/ershouqiugou/
    http://gz.58.com/tiaozao/
'''