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
    try:
        await asyncio.sleep(2)
        async with semaphore:
            browser = await launch({'headless': True, 'userDataDir': r'D:\jd','args': ['--disable-infobars', '--window-size=1920,1080'], 'dumpio': True})
            page = await browser.newPage()  # await browser.createIncognitoBrowserContext() # 隐身模式
            await page.setExtraHTTPHeaders(headers)
            # await page.setCookie(cookie)

            await page.goto(url,{'waitUntil': 'networkidle2'})  # 访问页面 当500毫秒内无网络连接进行下一步
            # 使用XPath获取文本内容
            product_name_id = url.split('https://item.jd.com/')[1].split('.')[0]  # 获取商品的item的id
            xpath_sort = '//*[@id="crumb-wrap"]/div/div[1]/div/a/text()'  # 商品分类
            xpath_name = '//*[@id="crumb-wrap"]/div/div[2]/div[2]/div[1]/div/a/text()'  # 商品店名
            xpath_title = '/html/body/div[6]/div/div[2]/div[1]/text()'  # 商品标题
            xpath_product_name = f'//*[@id="choose-attr-1"]/div[2]/div[@data-sku="{product_name_id}"]/a/i/text()'  # 购买的商品名称，比如套餐
            xpath_price = f'//*/span[@class="price J-p-{product_name_id}"]/text()'  # 商品价格
            xpath_promotion = '//*/div[@class="prom-item"]/em[@class="hl_red"]/text()'  # 促销 先判断是否存在多个，促销 ('元')[0]('满')  [1]('减') ，最后得到数字
            xpath_coupon = '//*/span[@class="quan-item"]/span/text()'  # 优惠券  re('满').split('减')
            xpath_in_store = '//*/div[@id="store-prompt"]/strong/text()'  # 是否有货
            xpath_evaluate = f'//*/a[@class="count J-comm-{product_name_id}"]/text()'  # 累计评价

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
            sort,name,title,product_name,price,promotion,coupon,in_store,evaluate = '','','','','','','','',''
            for element in page_sort:
                element_text = await page.evaluate('(element) => element.textContent', element)
                sort += element_text.strip() + ' '
            for element in page_name:
                element_text = await page.evaluate('(element) => element.textContent', element)
                name += element_text.strip()
            for element in page_title:
                element_text = await page.evaluate('(element) => element.textContent', element)
                title += element_text.strip()
            for element in page_product_name:
                element_text = await page.evaluate('(element) => element.textContent', element)
                product_name += element_text.strip()
            for element in page_price:
                element_text = await page.evaluate('(element) => element.textContent', element)
                price += element_text.strip()
            for element in page_promotion:
                element_text = await page.evaluate('(element) => element.textContent', element)
                promotion += element_text.strip()
            for element in page_coupon:
                element_text = await page.evaluate('(element) => element.textContent', element)
                coupon += element_text.strip()
            for element in page_in_store:
                element_text = await page.evaluate('(element) => element.textContent', element)
                in_store += element_text.strip()
            for element in page_evaluate:
                element_text = await page.evaluate('(element) => element.textContent', element)
                evaluate += element_text.strip()
            # print('name_id:'+product_name_id,'sort :'+sort,'name :'+name,'title :'+title,'product_name :'+product_name,'price :'+price,'promotion :'+promotion,'coupon :'+coupon,'in_store :'+in_store,'evaluate :'+evaluate)

            if len(sort) < 1:
                return ''
            # 数据库插入操作
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    # 使用参数占位符，防止SQL注入攻击
                    sql = f"INSERT INTO jd (name_id,sort,name,title,product_name,price,promotion,coupon,in_store,evaluate) VALUES ('{product_name_id}','{sort}', '{name}', '{title}', '{product_name}', '{price}', '{promotion}', '{coupon}', '{in_store}',' {evaluate}')"
                    await cur.execute(sql)
                    await conn.commit()
            # print('pass:',product_name_id)
            # 每次访问完成后等待3秒

            await browser.close()
    except Exception as e:
        print(e)
        print(url)


def item_url():
    with open('item_url.txt','r',encoding='utf-8') as f:
        return f.read().split('\n')


async def main():
    # 创建MySQL连接池
    pool = await aiomysql.create_pool(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='123456',
        db='a',
        charset='utf8mb4',
        autocommit=True,
        minsize=1,
        maxsize=10
    )

    urls = item_url()
    # 设置并发数量为50
    # 创建信号量，限制同时进行的协程数量
    semaphore = asyncio.Semaphore(5)

    tasks = [fetch_and_save(url, pool, semaphore) for url in urls]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())









