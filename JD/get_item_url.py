import requests
from lxml import etree
from urllib.parse import quote
import time


# 返回一百页的数据，一页60,60*100*5
def get_list_item():
    run_page = 100
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cookie': '__jdu=322959; shshshfpa=eaa5fefb-e748-b2af-be36-940c110d1275-1684398876; shshshfpx=eaa5fefb-e748-b2af-be36-940c110d1275-1684398876; qrsc=3; unpl=JF8EAKdnNSttD0gEBUlRHBASQ1tVWwoAQkcDOjIMXA1RSVYMGAJOFEV7XlVdXxRKEB9vZhRUXFNKVg4ZCisSEXteXVdZDEsWC2tXVgQFDQ8VXURJQlZAFDNVCV9dSRZRZjJWBFtdT1xWSAYYRRMfDlAKDlhCR1FpMjVkXlh7VAQrABgRGE9VZF9tD3snM29gBFBbaEpkBCtAT04QQ1pWX1pFSRQAZ2MNZFxoSA; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_f2a1cb6339704f98a1dd89a833821d7d|1686362620546; rkv=1.0; pin=%E7%8E%96%E4%BC%B4%E4%B8%80%E9%B9%8F; _tp=4zRrM9YpPXMr0gZUn5PYUyddTrEEJ76c2XK0oQJBVKOjsKqUYF%2FfXN03gxbbuDat; _pst=%E7%8E%96%E4%BC%B4%E4%B8%80%E9%B9%8F; TrackID=1XUVkkKa4SCtnxv0218Zn2eJUu90Q_fGPQnPZ8msV_WBm39NrnStsF34nN8OR26zNwXFZVda9iEQrMBbkqNuZRWA6qxDNumuhD-6xcb45myY|||e02rlt3J6lZVoNrvGZWKRA; unick=%E7%8E%96%E4%BC%B4%E4%B8%80%E9%B9%8FcNc; pinId=e02rlt3J6lZVoNrvGZWKRA; PCSYCityID=CN_440000_440300_0; areaId=19; ipLoc-djd=19-1607-4773-62121; shshshfpb=g0fazoakDjkhE7neTj4l1qA; 3AB9D23F7A4B3CSS=jdd03VSSLOGJDPQZGHSFYJN4TRQUZYLMRXZI7ZH34UJYTRQDYECUXRQ73BOII7TISGS3B7HHM2GIXIXXGRAD7JFHNPIVKPUAAAAMI45JNKQYAAAAAC23GUJYQUAXAH4X; _gia_d=1; shshshsID=b9798980451d87db241d8da4e57f94f0_1_1687508145759; jsavif=1; jsavif=1; xapieid=jdd03VSSLOGJDPQZGHSFYJN4TRQUZYLMRXZI7ZH34UJYTRQDYECUXRQ73BOII7TISGS3B7HHM2GIXIXXGRAD7JFHNPIVKPUAAAAMI45JNKQYAAAAAC23GUJYQUAXAH4X; __jda=122270672.322959.1684398874.1687506073.1687508145.24; __jdb=122270672.2.322959|24.1687508145; __jdc=122270672; 3AB9D23F7A4B3C9B=VSSLOGJDPQZGHSFYJN4TRQUZYLMRXZI7ZH34UJYTRQDYECUXRQ73BOII7TISGS3B7HHM2GIXIXXGRAD7JFHNPIVKPU'
    }

    referer = ['https://list.jd.com/listNew.php?cat=670&page=1&s=1&click=0']
    jj = 669
    for j in range(1, 33):
        i = 1
        count = 1
        while i - 1 < run_page:
            print(i)
            base_url = f'https://list.jd.com/listNew.php?cat={jj + j}&page={i}&s={count}&scrolling=y&log_id=1687599800208.7063&tpl=1_M&isList=1'
            xpaths = '//*/li/*/div[@class="p-img"]/a/@href'
            try:
                headers['Referer'] = referer[-1]
                r = etree.HTML(requests.get(base_url, headers=headers).text)
                url_list = r.xpath(xpaths)
                # print(url_list)
                # 页面是否存在数据
                if len(url_list) < 1:
                    break
                elif len(url_list) < 30:
                    referer.append(base_url)
                    for ii in url_list:
                        with open('item_url1.txt', 'a', encoding='utf-8') as f:
                            f.write('https:' + ii + '\n')
                    break
                else:
                    referer.append(base_url)
                    for ii in url_list:
                        with open('item_url1.txt', 'a', encoding='utf-8') as f:
                            f.write('https:' + ii + '\n')
                i += 1
                count += 30
                time.sleep(3)

            except Exception as e:
                print('出错', e)
                time.sleep(600)


def get_page_item(keyword, run_page):
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cookie': '__jdu=322959; shshshfpa=eaa5fefb-e748-b2af-be36-940c110d1275-1684398876; shshshfpx=eaa5fefb-e748-b2af-be36-940c110d1275-1684398876; qrsc=3; unpl=JF8EAKdnNSttD0gEBUlRHBASQ1tVWwoAQkcDOjIMXA1RSVYMGAJOFEV7XlVdXxRKEB9vZhRUXFNKVg4ZCisSEXteXVdZDEsWC2tXVgQFDQ8VXURJQlZAFDNVCV9dSRZRZjJWBFtdT1xWSAYYRRMfDlAKDlhCR1FpMjVkXlh7VAQrABgRGE9VZF9tD3snM29gBFBbaEpkBCtAT04QQ1pWX1pFSRQAZ2MNZFxoSA; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_f2a1cb6339704f98a1dd89a833821d7d|1686362620546; rkv=1.0; pin=%E7%8E%96%E4%BC%B4%E4%B8%80%E9%B9%8F; _tp=4zRrM9YpPXMr0gZUn5PYUyddTrEEJ76c2XK0oQJBVKOjsKqUYF%2FfXN03gxbbuDat; _pst=%E7%8E%96%E4%BC%B4%E4%B8%80%E9%B9%8F; TrackID=1XUVkkKa4SCtnxv0218Zn2eJUu90Q_fGPQnPZ8msV_WBm39NrnStsF34nN8OR26zNwXFZVda9iEQrMBbkqNuZRWA6qxDNumuhD-6xcb45myY|||e02rlt3J6lZVoNrvGZWKRA; unick=%E7%8E%96%E4%BC%B4%E4%B8%80%E9%B9%8FcNc; pinId=e02rlt3J6lZVoNrvGZWKRA; PCSYCityID=CN_440000_440300_0; areaId=19; ipLoc-djd=19-1607-4773-62121; shshshfpb=g0fazoakDjkhE7neTj4l1qA; 3AB9D23F7A4B3CSS=jdd03VSSLOGJDPQZGHSFYJN4TRQUZYLMRXZI7ZH34UJYTRQDYECUXRQ73BOII7TISGS3B7HHM2GIXIXXGRAD7JFHNPIVKPUAAAAMI45JNKQYAAAAAC23GUJYQUAXAH4X; _gia_d=1; shshshsID=b9798980451d87db241d8da4e57f94f0_1_1687508145759; jsavif=1; jsavif=1; xapieid=jdd03VSSLOGJDPQZGHSFYJN4TRQUZYLMRXZI7ZH34UJYTRQDYECUXRQ73BOII7TISGS3B7HHM2GIXIXXGRAD7JFHNPIVKPUAAAAMI45JNKQYAAAAAC23GUJYQUAXAH4X; __jda=122270672.322959.1684398874.1687506073.1687508145.24; __jdb=122270672.2.322959|24.1687508145; __jdc=122270672; 3AB9D23F7A4B3C9B=VSSLOGJDPQZGHSFYJN4TRQUZYLMRXZI7ZH34UJYTRQDYECUXRQ73BOII7TISGS3B7HHM2GIXIXXGRAD7JFHNPIVKPU'
    }
    encoded_keyword = quote(keyword)
    referer = f'https://search.jd.com/Search?keyword={encoded_keyword}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&psort=3&click=0'
    headers['Referer'] = referer
    data = []
    i = 1
    count = 26
    while i - 1 < run_page:
        print(i)
        base_url = f'https://search.jd.com/s_new.php?keyword={encoded_keyword}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&psort=3&page={i}&s={count}&click=0'
        xpaths = '//*[@class="gl-warp clearfix"]/li/div/div[@class="p-img"]/a/@href'
        try:
            r = etree.HTML(requests.get(base_url, headers=headers).text)
            url_list = r.xpath(xpaths)
            # print(url_list)
            # 页面是否存在数据
            if len(url_list) < 1:
                break
            elif len(url_list) < 30:
                data.append(url_list)
                break
            else:
                data.append(url_list)
            time.sleep(3)

            # 第二页
            i = i + 1
            count += 30
            base_url = f'https://search.jd.com/s_new.php?keyword={encoded_keyword}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&psort=3&page={i}&s={count}&click=0'
            r = etree.HTML(requests.get(base_url, headers=headers).text).xpath(xpaths)
            data.append(r)

            # 之后的页数
            i = i + 1
            count += 30
            time.sleep(5)
        except Exception as e:
            print('出错', e)
            time.sleep(600)
    return data


def get_itmeurl():
    with open('../处理器型号.txt', 'r', encoding='utf-8') as f:
        string_list = f.read().split('\n')

    for string in string_list:
        for i in get_page_item(string, 100):
            for ii in i:
                with open('item_url.txt', 'a', encoding='utf-8') as f:
                    f.write('https:'+ii + '\n')



