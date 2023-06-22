import requests
from lxml import etree
from urllib.parse import quote


# 返回一百页的数据，一页60,60*100*5
def jd_list():
    url_list = []
    a = 669
    for i in range(5):
        a += 1
        url = f'https://list.jd.com/list.html?cat={a}'
        url_list.append(url)
    return url_list


def run(keyword,run_page):
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    encoded_keyword = quote(keyword)
    referer = f'https://search.jd.com/Search?keyword={encoded_keyword}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&psort=3&click=0'
    headers['Referer'] = referer

    # 每页前30个商品
    base_url = '''https://search.jd.com/s_new.php?keyword=''' + encoded_keyword + '''
        &enc=utf-8&qrst=1&rt=1&stop=1&vt=2&psort=3&page={p}&s={count}&click=0'''
    # 每页后30个商品
    ajax_url = '''https://search.jd.com/s_new.php?keyword=''' + encoded_keyword + '''
        &enc=utf-8&qrst=1&rt=1&stop=1&vt=2&psort=3&page={p}&s=31&scrolling=y
        &log_id=1507459781.34746&tpl=1_M'''

    i = 1
    while i < run_page * 2 + 1:
        print(i)
        url = base_url.format(p=i, count=(i - 1) * 60 + 1)
        r = requests.get(url, headers=headers).text
        i = i + 1

        url = ajax_url.format(p=i)
        r = requests.get(url, headers=headers).text
        i = i + 1


string = 'RTX 4060'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
xpaths = '//*[@class="gl-warp clearfix"]/li/div/div[@class="p-img"]/a/@href'
xp = '//*[@class="p-skip"]/em/b/text()'
encoded_keyword = quote(string)
url = f'https://search.jd.com/Search?keyword={encoded_keyword}'
response = requests.get(url,headers=headers)
s = etree.HTML(response.text)
print(response.text)
ss = s.xpath(xp)

url_list = 'https://search.jd.com/s_new.php?keyword=3060&pvid=3ec880aee1c746108774e1b38abd2c64&page=3&scrolling=y&log_id=1687167533152.9633&tpl=1_M&isList=0'

print(ss)
print(len(ss))






