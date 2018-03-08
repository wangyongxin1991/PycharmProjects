import pymongo

client = pymongo.MongoClient('localhost',27017)
#给数据库命名
walden = client['walden']
#创建表单
sheet_tab = walden['sheet_tab']

# path = 'F://testFile/walden.txt'
# with open(path,'r') as f:
#     lines = f.readlines()
#     for index,line in enumerate(lines):
#         data = {
#             'index': index,
#             'line': line,
#             'words':len(line.split())
#         }
#         sheet_tab.insert(data)

#$lt / $lte / $gt / $gte  / $ne 等价于 < <= > >= !=
for item in sheet_tab.find({'words':0}):
    print(item)