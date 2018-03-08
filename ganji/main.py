from multiprocessing import Pool
from ganji.get_category_list import url_item
from ganji.page_parsing import get_list_page,get_page_info,url_list,page_info

db_urls = [item['url'] for item in url_list.find()]
index_urls = [item['url'] for item in page_info.find()]

x = set(db_urls)
y = set(index_urls)
rest_of_urls = x-y

def get_all_link(channel):
    for i in range(1,100):
        get_list_page(channel,i)

if __name__ == '__main__':
    pool = Pool()
    pool.map(get_page_info,rest_of_urls)
    pool.close()
    pool.join()