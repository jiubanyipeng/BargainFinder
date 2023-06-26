import requests
from lxml import etree
import asyncio
import aiomysql

from pyppeteer import launch


# 设置请求头、Cookie和代理
headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cookie': '__jdu=322959; shshshfpa=eaa5fefb-e748-b2af-be36-940c110d1275-1684398876; shshshfpx=eaa5fefb-e748-b2af-be36-940c110d1275-1684398876; qrsc=3; unpl=JF8EAKdnNSttD0gEBUlRHBASQ1tVWwoAQkcDOjIMXA1RSVYMGAJOFEV7XlVdXxRKEB9vZhRUXFNKVg4ZCisSEXteXVdZDEsWC2tXVgQFDQ8VXURJQlZAFDNVCV9dSRZRZjJWBFtdT1xWSAYYRRMfDlAKDlhCR1FpMjVkXlh7VAQrABgRGE9VZF9tD3snM29gBFBbaEpkBCtAT04QQ1pWX1pFSRQAZ2MNZFxoSA; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_f2a1cb6339704f98a1dd89a833821d7d|1686362620546; rkv=1.0; pin=%E7%8E%96%E4%BC%B4%E4%B8%80%E9%B9%8F; _tp=4zRrM9YpPXMr0gZUn5PYUyddTrEEJ76c2XK0oQJBVKOjsKqUYF%2FfXN03gxbbuDat; _pst=%E7%8E%96%E4%BC%B4%E4%B8%80%E9%B9%8F; TrackID=1XUVkkKa4SCtnxv0218Zn2eJUu90Q_fGPQnPZ8msV_WBm39NrnStsF34nN8OR26zNwXFZVda9iEQrMBbkqNuZRWA6qxDNumuhD-6xcb45myY|||e02rlt3J6lZVoNrvGZWKRA; unick=%E7%8E%96%E4%BC%B4%E4%B8%80%E9%B9%8FcNc; pinId=e02rlt3J6lZVoNrvGZWKRA; PCSYCityID=CN_440000_440300_0; areaId=19; ipLoc-djd=19-1607-4773-62121; shshshfpb=g0fazoakDjkhE7neTj4l1qA; 3AB9D23F7A4B3CSS=jdd03VSSLOGJDPQZGHSFYJN4TRQUZYLMRXZI7ZH34UJYTRQDYECUXRQ73BOII7TISGS3B7HHM2GIXIXXGRAD7JFHNPIVKPUAAAAMI45JNKQYAAAAAC23GUJYQUAXAH4X; _gia_d=1; shshshsID=b9798980451d87db241d8da4e57f94f0_1_1687508145759; jsavif=1; jsavif=1; xapieid=jdd03VSSLOGJDPQZGHSFYJN4TRQUZYLMRXZI7ZH34UJYTRQDYECUXRQ73BOII7TISGS3B7HHM2GIXIXXGRAD7JFHNPIVKPUAAAAMI45JNKQYAAAAAC23GUJYQUAXAH4X; __jda=122270672.322959.1684398874.1687506073.1687508145.24; __jdb=122270672.2.322959|24.1687508145; __jdc=122270672; 3AB9D23F7A4B3C9B=VSSLOGJDPQZGHSFYJN4TRQUZYLMRXZI7ZH34UJYTRQDYECUXRQ73BOII7TISGS3B7HHM2GIXIXXGRAD7JFHNPIVKPU'
    }

cookie = {
    'name': 'session_id',
    'value': 'your_session_id',
    'domain': 'example.com',
    'path': '/',
}
proxy_server = 'your_proxy_server_address:your_proxy_port'


async def fetch_and_save(url, pool, semaphore):
    async with semaphore:
        browser = await launch(headless=False,dumpio=True, autoClose=False,args=['--no-sandbox', '--window-size=1000,800', '--disable-infobars']) # f'--proxy-server={proxy_server}',
        page = await browser.newPage()

        await page.setExtraHTTPHeaders(headers)
        # await page.setCookie(cookie)

        await page.goto(url)

        # 使用XPath获取文本内容
        product_name = url.split('https://item.jd.com/')[1].split('.')[0]  # 获取商品的item的id
        xpath_sort = '//*[@id="crumb-wrap"]/div/div[1]/div/a/text()'  # 商品分类
        xpath_name = '//*[@id="crumb-wrap"]/div/div[2]/div[2]/div[1]/div/a/text()'  # 商品店名
        xpath_title = '/html/body/div[6]/div/div[2]/div[1]/text()'  # 商品标题
        xpath_product_name = f'//*[@id="choose-attr-1"]/div[2]/div[@data-sku="{product_name}"]/a/i/text()'  # 购买的商品名称，比如套餐
        xpath_price = f'//*/span[@class="price J-p-{product_name}"]/text()'  # 商品价格
        xpath_promotion = '//*/div[@class="prom-item"]/em[@class="hl_red"]/text()'  # 促销 先判断是否存在多个，促销 ('元')[0]('满')  [1]('减') ，最后得到数字
        xpath_coupon = '//*/span[@class="quan-item"]/span/text()'  # 优惠券  re('满').split('减')
        xpath_in_store = '//*/div[@id="store-prompt"]/strong/text()'  # 是否有货
        xpath_evaluate = f'//*/a[@class="count J-comm-10071503513070"]/text()'  # 累计评价

        page_sort = await page.xpath(xpath_sort)
        page_name = await page.xpath(xpath_name)
        page_title = await page.xpath(xpath_title)
        page_product_name = await page.xpath(xpath_product_name)
        page_price = await page.xpath(xpath_price)
        page_promotion = await page.xpath(xpath_promotion)
        page_coupon = await page.xpath(xpath_coupon)
        page_in_store = await page.xpath(xpath_in_store)
        page_evaluate = await page.xpath(xpath_evaluate)

        # 提取文本内容
        text = ''
        for element in page_sort:
            element_text = await page.evaluate('(element) => element.textContent', element)
            text += element_text.strip() + ' '
        print(text)
        # 保存到MySQL数据库
        # async with pool.acquire() as conn:
        #     async with conn.cursor() as cur:
        #         await cur.execute("INSERT INTO your_table_name (url, content) VALUES (%s, %s)", (url, text))
        #         await conn.commit()
        # 每次访问完成后等待3秒
        await asyncio.sleep(30)
        await browser.close()

        # 每次访问完成后等待3秒
        await asyncio.sleep(3)


async def main():
    # 创建MySQL连接池
    pool = await aiomysql.create_pool(host='127.0.0.1', port=3306,
                                      user='root', password='123456',
                                      db='a', loop=loop)

    # 要访问的网页列表
    urls = ['https://item.jd.com/70615112236.html', 'https://item.jd.com/10071886235956.html', ]

    # 设置并发数量为50
    concurrency = 50
    semaphore = asyncio.Semaphore(concurrency)

    tasks = []
    for url in urls:
        tasks.append(fetch_and_save(url, pool, semaphore))

    await asyncio.gather(*tasks)

    pool.close()
    await pool.wait_closed()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())


# referer = 'https://jd.com/'
# headers['Referer'] = referer
# url = 'https://item.jd.com/60518348474.html'
#
# xpath_sort = '//*[@id="crumb-wrap"]/div/div[1]/div/a/text()'
# xpath_name = '//*[@id="crumb-wrap"]/div/div[2]/div[2]/div[1]/div/a/text()'
# xpath_title = '/html/body/div[6]/div/div[2]/div[1]/text()'
# product_name = url.split('https://item.jd.com/')[1].split('.')[0]
# xpath_product_name = f'//*[@id="choose-attr-1"]/div[2]/div[@data-sku="{product_name}"]/a/i/text()'
# r = etree.HTML(requests.get(url,headers=headers).text)
# sort = r.xpath(xpath_sort)
# name = r.xpath(xpath_name)
# title = [r.xpath(xpath_title)[0].strip()]  # 去除两边除字符串中的空格和换行符
# product_name = r.xpath(xpath_product_name)
# print(sort,name,title,product_name)








