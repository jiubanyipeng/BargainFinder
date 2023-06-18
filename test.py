import json


# 提取分类中的关键字
def extract_keywords(data, keyword_list):
    if isinstance(data, dict):
        for value in data.values():
            if isinstance(value, str):
                keyword_list.append(value)
            elif isinstance(value, (list, dict)):
                extract_keywords(value, keyword_list)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, str):
                keyword_list.append(item)
            elif isinstance(item, (list, dict)):
                extract_keywords(item, keyword_list)


# 返回提取分类中的关键字
def keywords():
    with open('./分类.json','r',encoding='utf-8') as f:
        data = json.load(f)
        keywords = []
        extract_keywords(data, keywords)
        return keywords



print(keywords())