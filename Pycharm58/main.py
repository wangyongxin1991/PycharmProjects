from multiprocessing import Pool
from Pycharm58.channel_extract import channel_list
from Pycharm58.page_Persing  import get_links_from,url_list,item_info,get_58_info

db_urls = [item['url'] for item in url_list.find()]
index_urls = [item['url'] for item in item_info.find()]
x = set(db_urls)
y = set(index_urls)
rest_of_urls = y


def get_all_links_from(channel):
    for i in range(1,100):
        if channel in db_urls:
            continue
            print('have')
        get_links_from(channel,i)

if __name__ == '__main__':
    #pool = Pool()
    pool = Pool(processes=10)
    #pool.map(get_all_links_from,channel_list.split())
    pool.map(get_58_info, rest_of_urls)
    pool.join()
    pool.close()