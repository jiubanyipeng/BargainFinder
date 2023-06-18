import requests
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
}

s = 2016
url = f'https://www.techpowerup.com/gpu-specs/?released={s}&sort=name'
xpaths = '//*[@class="vendor-ATI"]/a/text()'

response = requests.get(url, headers=headers)
html = etree.HTML(response.text)
gpu_names = html.xpath(xpaths)
print(gpu_names)
