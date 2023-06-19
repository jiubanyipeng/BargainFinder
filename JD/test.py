import requests
from lxml import etree
from urllib.parse import quote


# 返回一百页的数据，一页60,60*100*5
def jd_list():
    a = 669
    for i in range(5):
        a += 1
        url = f'https://list.jd.com/list.html?cat={a}'







string = 'GeForce RTX 4060 Max-Q'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
xpaths = '//*[@class="gl-warp clearfix"]/li/div/div[@class="p-img"]/a/@href'
encoded_keyword = quote(string)
url = f'https://search.jd.com/Search?keyword={encoded_keyword}'
response = requests.get(url,headers=headers)
print(response.json)
s = etree.HTML(response.text)

ss = s.xpath(xpaths)

url_list = 'https://search.jd.com/s_new.php?keyword=3060&pvid=3ec880aee1c746108774e1b38abd2c64&page=3&scrolling=y&log_id=1687167533152.9633&tpl=1_M&isList=0'

print(ss)
print(len(ss))






