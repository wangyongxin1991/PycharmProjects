import time

from ganji.page_parsing import url_list,page_info
import pymongo

while True:
    print(page_info.find().count())
    time.sleep(5)