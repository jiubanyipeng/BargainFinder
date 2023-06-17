import json

with open('./分类.json','r',encoding='utf-8') as f:
    s = json.load(f)
    for i in s:
        print(i)






