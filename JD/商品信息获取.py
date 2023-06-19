import asyncio
import aiohttp
from lxml import etree


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def process_response(response):
    # 使用lxml进行XPath解析
    root = etree.HTML(response)
    elements = root.xpath('//h1')

    for element in elements:
        print(element.text)


async def main():
    urls = [
        'https://example.com/page1',
        'https://example.com/page2',
        'https://example.com/page3',
        # 添加更多的URL...
    ]

    async with aiohttp.ClientSession() as session:
        # 设置请求头
        session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'})
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(fetch(session, url))
            tasks.append(task)

        # 并发发送请求并获取响应
        responses = await asyncio.gather(*tasks)

        # 处理响应数据
        for response in responses:
            await process_response(response)

# 运行主程序
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
