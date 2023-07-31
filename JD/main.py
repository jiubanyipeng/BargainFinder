import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth
import pymysql.cursors
import aiomysql


def item_url():
    with open('./item_url.txt','r',encoding='utf-8') as f:
        return f.read().split('\n')


# 数据库数据为列表的操作
async def operation_mysql(sql_list):
    # 数据库链接信息
    connection = await aiomysql.connect(
        host='localhost',
        user='root',
        password='123456',
        db='a'
    )

    # 创建游标对象
    cursor = await connection.cursor()
    for sql_data in sql_list:
        try:
            if sql_data:
                if sql_data[0]:
                    if sql_data[0] == 'False':
                        await cursor.execute(sql_data[1])
                    else:
                        await cursor.execute(sql_data[1])
                        await cursor.execute(sql_data[0])
        except Exception as e:
            print(e,sql_list)

    # 提交事务
    await connection.commit()
    await cursor.close()
    connection.close()


# 数据库查询的操作或更新操作
def select_mysql(sql,p='n'):
    # 数据库链接信息
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='123456',
                         database='a')

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    if p == 'y':    #
        cursor.execute(sql)
        rests = cursor.fetchall()
        for i in rests:
            cursor.execute(f"UPDATE jd_url_item_cache SET in_yes='true' WHERE  url_id='{i[0]}'")
        return 'pass'
    cursor.execute(sql)
    # 这是查询表中所有的数据
    rest = cursor.fetchall()
    name_id = []
    for i in rest:
        name_id.append(i[0])
    # 关闭数据库连接
    db.close()
    return name_id


async def process_url(page, url_id):
    await stealth(page)
    url = 'https://item.jd.com/' + url_id + '.html'
    try:
        # headers = {"Referer": "https://www.jd.com/","Sec-Fetch-Site": "same-site"}
        # await page.setExtraHTTPHeaders(headers)
        await page.goto(url)
    except Exception as e:
        print(e,url)
        await page.close()
        return None

    # 使用XPath获取文本内容
    xpath_sort = '//*[@id="crumb-wrap"]/div/div[1]/div/a/text()'  # 商品分类
    xpath_name = '//*[@id="crumb-wrap"]/div/div[2]/div[2]/div[1]/div/a/text()'  # 商品店名
    xpath_title = '//*/div[@class="sku-name"]/text()'  # 商品标题
    xpath_product_name_color = f'//*[@id="choose-attr-1"]/div[2]/div[@data-sku="{url_id}"]/@title'  # 购买的套餐 颜色
    xpath_product_name_versions = f'//*[@id="choose-attr-2"]/div[2]/div[@data-sku="{url_id}"]/@title'  # 购买的套餐 版本
    xpath_price = f'//*/span[@class="price J-p-{url_id}"]/text()'  # 商品价格
    xpath_promotion = '//*/div[@class="prom-item"]/em[@class="hl_red"]/text()'  # 促销
    xpath_coupon = '//*/span[@class="quan-item"]/span/text()'  # 优惠券  re('满').split('减')
    xpath_in_store = '//*/div[@id="store-prompt"]/strong/text()'  # 是否有货
    xpath_evaluate = f'//*/a[@class="count J-comm-{url_id}"]/text()'  # 累计评价
    xpath_sellout = '//*/div[@class="itemover-tip"]/text()'  # 商品下架
    try:
        await page.waitForXPath(xpath_sellout, timeout=5000)   # 判断 商品下架
        await page.close()
        return ['False', f"UPDATE jd_url_item_cache SET in_yes='false' WHERE  url_id='{url_id}'"]
    except Exception as e:
        try:
            xpath_list = [xpath_sort,  xpath_title, xpath_price, xpath_in_store]
            await asyncio.gather(*[page.waitForXPath(xpath,timeout=120000) for xpath in xpath_list])  # 120秒内等待多个 XPath 元素的加载
            # await page.waitForXPath(xpath_price,timeout=120000)  # 120秒 等待元素加载
            page_sort = await page.xpath(xpath_sort)
            page_name = await page.xpath(xpath_name)
            page_title = await page.xpath(xpath_title)
            product_name_color = await page.xpath(xpath_product_name_color)
            product_name_versions = await page.xpath(xpath_product_name_versions)
            page_price = await page.xpath(xpath_price)
            page_promotion = await page.xpath(xpath_promotion)
            page_coupon = await page.xpath(xpath_coupon)
            page_in_store = await page.xpath(xpath_in_store)
            page_evaluate = await page.xpath(xpath_evaluate)
            # 提取文本内容
            sort, name, title, name_color, name_versions, price, promotion, coupon, in_store, evaluate = '', '', '', '', '', '', '', '', '',''
            for element in page_sort:
                element_text = await page.evaluate('(element) => element.textContent', element)
                sort += element_text.strip() + ' '
            for element in page_name:
                element_text = await page.evaluate('(element) => element.textContent', element)
                name += element_text.strip()
            for element in page_title:
                element_text = await page.evaluate('(element) => element.textContent', element)
                title += element_text.strip()
            for element in product_name_color:
                element_text = await page.evaluate('(element) => element.textContent', element)
                name_color += element_text.strip()
            for element in product_name_versions:
                element_text = await page.evaluate('(element) => element.textContent', element)
                name_versions += element_text.strip()
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
            # 数据库插入操作
            # 使用参数占位符，防止SQL注入攻击
            # sql_insert = f"INSERT INTO jd (name_id,sort,name,title,product_name,price,promotion,coupon,in_store,evaluate) VALUES ('{url_id}','{sort}', '{name}', '{title}', '{name_color+'#####'+name_versions}', '{price}', '{promotion}', '{coupon}', '{in_store}',' {evaluate}')"
            sql_insert = f"UPDATE jd_it set name='{name}',title='{title}',product_name='{name_color+'#####'+name_versions}',price='{price}',promotion='{promotion}',coupon='{coupon}',in_store='{in_store}',evaluate='{evaluate}' WHERE  name_id='{url_id}'"
            sql_stop = f"UPDATE jd_url_item_cache SET in_yes='true' WHERE  url_id='{url_id}'"
            await page.close()
            return [sql_insert, sql_stop]  # 直接返回数据速度会更快
        except Exception as e:
            # 访问不了的原因可能是因为商品下架了
            print('错误',url,e)
            await page.close()
            return None


async def main(urls_list,num_pages):
    # 打开开发者模式  '--auto-open-devtools-for-tabs'
    browser = await launch({'headless': True, 'args': ['--no-sandbox','--window-size=1366,768']}, userDataDir=r'D:\jd',executablePath=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    jd = await browser.newPage()
    await jd.setViewport({'width': 1366, 'height': 768})  # 设置内部窗口界面大小
    await jd.goto('https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fitem.jd.com%2F10032528356427.html')  # 先登录
    await jd.click('#content > div.login-wrap > div.w > div.login-form > div.coagent > ul > li > a > span')  # 点击账户登录
    await jd.waitFor(2000)  # 延时
    frame = jd.frames  # 得到page中所有iframe对象的列表
    iframe = frame[0]
    for j in iframe.childFrames:
        con = await j.xpath('//*/div[@id="qlogin_list"]/a')
        if con:
            await con[0].click()
    await jd.waitFor(5000)  # 延时
    pages = [await browser.newPage() for _ in range(num_pages)]  # 新建十个页面
    urllist = urls_list[:num_pages]
    sql_list = await asyncio.gather(*[process_url(page, urllist.pop()) for page in pages])
    await operation_mysql(sql_list)

    run = len(urls_list) // num_pages  # 计算可运行次数
    run_remainder = len(urls_list) % num_pages  # 余数
    run_start = num_pages  # 开始位置
    run_end = num_pages+num_pages  # 结束位置
    for i in range(run):
        url_list = urls_list[run_start:run_end]
        pages = [await browser.newPage() for _ in range(num_pages)]  # 新建十个页面
        sql_list = await asyncio.gather(*[process_url(page, url_list.pop()) for page in pages])
        await operation_mysql(sql_list)
        run_start += 1
        run_end += num_pages
    # 剩余可运行次数
    url_list = urls_list[-run_remainder:]
    pages = [await browser.newPage() for _ in range(num_pages)]
    sql_list = await asyncio.gather(*[process_url(page, url_list.pop()) for page in pages])
    await operation_mysql(sql_list)


if __name__ == '__main__':
    while True:
        urls_list = select_mysql('select url_id from jd_url_item_cache where in_yes="true"')  # 一正一反
        num_pages = 20
        asyncio.get_event_loop().run_until_complete(main(urls_list,num_pages))
        select_mysql('select * from jd_it','y')  # 将全部的访问过的列表设置为真




