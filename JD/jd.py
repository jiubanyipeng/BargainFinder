import requests
import time
from bs4 import BeautifulSoup
import random
import smtplib
from email.mime.text import MIMEText
from apscheduler.schedulers.background import BackgroundScheduler

# 京东商品URL
product_url = "https://item.jd.com/123456789.html"  # 替换为实际商品的URL


# 邮件通知配置
sender_email = "your_sender_email"
sender_password = "your_sender_password"
receiver_email = "your_receiver_email"

# 数据持久化文件路径
data_file = "product_data.csv"

# 创建一个Session对象，并设置Headers
session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
}
session.headers.update(headers)


def send_email(subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


def get_product_info(url):
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取商品价格
    price_element = soup.find(class_='p-price')
    price = price_element.strong.string

    # 提取优惠券信息
    coupon_element = soup.find(class_='coupon')
    coupon_info = coupon_element.span.string

    # 提取库存状态
    stock_element = soup.find(class_='stock')
    stock_status = stock_element.string.strip()

    return price, coupon_info, stock_status


def monitor_product():
    # 获取商品信息
    try:
        price, coupon_info, stock_status = get_product_info(product_url)
    except requests.exceptions.RequestException as e:
        print("请求异常:", e)
        return

    # 处理价格信息
    price = float(price)
    coupon_amount = 0
    if coupon_info:
        coupon_amount = float(coupon_info)
    final_price = price - coupon_amount

    # 输出监控结果
    print("商品价格：", price)
    print("优惠券信息：", coupon_info)
    print("库存状态：", stock_status)
    print("最终付款价格：", final_price)

    # 数据持久化
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    data = f"{timestamp},{price},{coupon_info},{stock_status},{final_price}"
    with open(data_file, 'a') as f:
        f.write(data + '\n')

    # 发送通知
    if final_price == min_final_price():
        subject = "价格更新通知"
        message = f"商品最低价格已更新为 {final_price}"
        send_email(subject, message)


def min_final_price():
    # 读取数据文件，获取历史最低价格
    min_price = float('inf')
    with open(data_file, 'r') as f:
        for line in f:
            timestamp, price, coupon_info, stock_status, final_price = line.strip().split(',')
            final_price = float(final_price)
            if final_price < min_price:
                min_price = final_price
    return min_price




# 创建定时任务调度器
scheduler = BackgroundScheduler()
scheduler.add_job(monitor_product, 'interval', hours=1)  # 每小时执行一次监控任务

# 启动定时任务调度器
scheduler.start()

# 保持主线程不退出
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass

# 关闭定时任务调度器
scheduler.shutdown()
