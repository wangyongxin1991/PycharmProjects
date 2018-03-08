from bs4 import BeautifulSoup
import requests
import  time
import pymongo
import re
urls = ['http://gz.xiaozhu.com/search-duanzufang-p{}-0/'.format(str(i)) for i in range(1,4,1)]

client = pymongo.MongoClient('localhost',27017)
walden = client['walden']
xiaozhu_tab = walden['xiaozhu_tab']

def get_data(url,data=None):
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text,'lxml')

    imgs = soup.select('img.lodgeunitpic')
    prices = soup.select('span.result_price')
    htitles = soup.select('span.result_title.hiddenTxt')
    hiddenTxts  = soup.select('em.hiddenTxt')

    if(data==None):
        for img,price,htitle,hiddenTxt in zip(imgs,prices,htitles,hiddenTxts):
            p = re.compile(r"(\d+)")
            for m in  p.finditer(price.text):
                data = {
                    'img':img.get('src'),
                    'price':int(m.group()),
                    'htitle':htitle.get_text(),
                    'hiddenTxt':hiddenTxt.get_text().replace('\n',"").replace(" ","")
                }
            xiaozhu_tab.insert(data)

    time.sleep(2)

#for sing_url in urls:
  #  get_data(sing_url)

for item in xiaozhu_tab.find({'price':{'$gte':500}}):
    print(item)

