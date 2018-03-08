from bs4 import BeautifulSoup
import requests
import time
'''
url = 'http://cn.toursforfun.com'
wb_data = requests.get(url)
soup = BeautifulSoup(wb_data.text,'lxml')
print(soup)
'''
url_saves = 'http://cn.toursforfun.com/new-york-city-tours/'
urls = ['http://cn.toursforfun.com/new-york-city-tours/p-{}'.format(str(i)) for i in range(1,6,1)]
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Cookies':'_TFFID=c8mla7ti0skfeb2ljdon0lrhl1; referer_url=https%3A%2F%2Fwww.baidu.com%2Fbaidu.php%3Fsc.af0000akyWrKhev-XGDV43VR0ACOmkFnUspf2wwpnXSUzdcE5jB-YCbJjaskn_JTyzdkGaAI0kr2VkeDFxXtDe9symLJliHcakksbUncvEQXXFXwuMCitEnprMWlgpcWU_in8zSOyhwei6xwtsK_wLN3_BxYoi853QqlUENu8fV2FI2Vh6.Db_ifkXNKvap5ylUg6BwKDM61lZHI8X7qjwMCrsHwsIt7jHzk8sHfGmEukmcxCl32AM-YG8x6Y_f33X8a9G4pauVQZqHSGO6OvxlEOHOKO45SgSLOHOSxSQOkOl5t5qUOKOmOmyFWkvyyyurzE-LTVHQ8gZJyAp7BEke2e70.U1Yk0ZDqkpUREnofs_5H1olsVXn0mywkXHL7GVitzVjasq5rEoad3sK9uZ7Y5Hc0TA-W5HD0IjL7GVits_5fY0KGUHYznWR0u1ddugK1n0KdpHdBmy-bIykV0ZKGujYY0APGujY3P0KVIjYknjDLg1DsnH-xnW0vn-t1PW0k0AVG5H00TMfqPWmL0ANGujY0mhbqnW0Yg1DdPfKVm1YvrjRknjnvP1uxPW6dnH01PWT4g1cvPH0zPW61n1uxn0KkTA-b5H00TyPGujYs0ZFMIA7M5H00mycqn7ts0ANzu1Ys0ZKs5H00UMus5H08nj0snj0snj00Ugws5H00uAwETjYs0ZFJ5H00uANv5gKW0AuY5H00TA6qn0KET1Ys0AFL5HDs0A4Y5H00TLCq0ZwdT1Ykn1nLPW6sP1bvn1mLPHnznHTdn0Kzug7Y5HDdnH03PjDkn1fkPjD0Tv-b5ynsnjF-uAf3nj0snj--nhn0mLPV5RPKrjbvPWIAPWmzfWbvPbm0mynqnfKsUWYs0Z7VIjYs0Z7VT1Ys0ZGY5H00UyPxuMFEUHYsg1Kxn7ts0Aw9UMNBuNqsUA78pyw15HKxn7tsg100TA7Ygvu_myTqn0Kbmv-b5Hcvrjf1PHfdP6K-IA-b5iYk0A71TAPW5H00IgKGUhPW5H00Tydh5HDv0AuWIgfqn0KhXh6qn0Khmgfqn0KlTAkdT1Ys0A7buhk9u1Yk0Akhm1Ys0APzm1Yzrj0YPf%26ck%3D6643.1.110.385.141.418.150.905%26shh%3Dwww.baidu.com%26sht%3D78000241_5_hao_pg%26us%3D1.0.1.0.1.301.0%26ie%3Dutf-8%26f%3D8%26tn%3D78000241_5_hao_pg%26wd%3D%25E7%25BA%25BD%25E7%25BA%25A6%25E5%25B8%2582%25E6%2597%2585%25E6%25B8%25B8%25E6%2599%25AF%25E7%2582%25B9%26oq%3D%2525E7%2525BA%2525BD%2525E7%2525BA%2525A6%2525E6%252597%252585%2525E6%2525B8%2525B8%2525E6%252594%2525BB%2525E7%252595%2525A5%26rqlang%3Dcn%26inputT%3D6086%26bs%3D%25E7%25BA%25BD%25E7%25BA%25A6%25E6%2597%2585%25E6%25B8%25B8%25E6%2594%25BB%25E7%2595%25A5%26bc%3D110101; no_ref=1; pageSize=20; PHPSESSID=q1kohe7uai3kv6c4i6s541p3n4; BI_TAToken=TA1510841141103208; __ssid=fa8cbbcb-3151-4790-a220-10a61dd2fb76; MEIQIA_EXTRA_TRACK_ID=0wRb1IUXSrZ5HRARiHocqXcmxE6; MEIQIA_REJECT_INVITATION=yes; BI___TAReferer=; cps_tag=%7B%22channel%22%3A%22DuoMai%22%2C%22cps_params%22%3A%7B%22euid%22%3A%2218012444%22%2C%22mid%22%3A%22218037%22%7D%7D; cps_track=%7B%22cps%22%3A%22duomai%22%2C%22sid%22%3A%22218037%22%2C%22cid%22%3A%2218012444%22%2C%22ref%22%3A%22%22%2C%22channel%22%3A%22PC%22%7D; utm_medium=refapi; customers_advertiser=duomai; customers_ad_click_id=316806892; BI___TAFirstSource=%7B%22utm_source%22%3A%22duomai%22%2C%22utm_medium%22%3A%22refapi%22%7D; BI___TALastSource=%7B%22utm_source%22%3A%22duomai%22%2C%22utm_medium%22%3A%22refapi%22%7D; ta_tn=5a0d9c41_284b; ta_sn=5a0d9c41_a532; ta_0=refapi|duomai|; ta_1=refapi|duomai|; language=sc; _ga=GA1.2.1728232450.1510841141; _gid=GA1.2.987381346.1510841141; Hm_lvt_ed2f1880a0adca8fff9b63d94cd62442=1510841141,1510841362,1510841409; Hm_lpvt_ed2f1880a0adca8fff9b63d94cd62442=1510841813; BI_TAIndex=6; ta_2=|'
}

def get_favs(url,data=None):
    time.sleep(4)
    web_data  = requests.get(url,headers=headers)
    soup      = BeautifulSoup(web_data.text,'lxml')
    images    = soup.select('a.img-wrap > img')
    titles    = soup.select('div.item-info > h2 > a')
    dess      = soup.select('div.item-info > p.des')
    tags      = soup.select('div.item-info > p.tags')
    prices    = soup.select('div.item-info > p.price')
    delPris   = soup.select('div.item-info > p.price > del')

    if(data==None):
        for image,title,des,price,delPri,tag in zip(images,titles,dess,prices,delPris,tags):
            data = {
                'image':image.get('src'),
                'title':title.get_text(),
                'des':des.get_text(),
                'price':price.get_text(),
                'delPri':delPri.get_text(),
                'tag':list(tag.stripped_strings)
            }
            print(data)

for single_url in urls:
    get_favs(single_url)