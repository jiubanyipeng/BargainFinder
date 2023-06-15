# 用户登录信息处理


import requests
import time
from bs4 import BeautifulSoup
import random
import smtplib
from email.mime.text import MIMEText
from apscheduler.schedulers.background import BackgroundScheduler


# 京东登录信息（用于处理验证码）
username = "your_username"
password = "your_password"



# 创建一个Session对象，并设置Headers
session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",

}
session.headers.update(headers)


def login_with_captcha(username, password):
    login_url = "https://passport.jd.com/new/login.aspx"

    # 获取登录页的内容
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取验证码图片URL和表单参数
    captcha_img_url = "https:" + soup.select("#JD_Verification1")[0]["src2"]
    login_form = {
        "uuid": soup.select("#uuid")[0]["value"],
        "_t": soup.select("#__t")[0]["value"],
        "loginType": soup.select("#loginType")[0]["value"],
        "pubKey": soup.select("#pubKey")[0]["value"],
        "sa_token": soup.select("#sa_token")[0]["value"],
        "seqSid": soup.select("#seqSid")[0]["value"],
        "useSlideAuthCode": soup.select("#useSlideAuthCode")[0]["value"],
        "isShadowLogin": "false",
        "loginname": username,
        "nloginpwd": password,
    }

    # 下载验证码图片
    response = session.get(captcha_img_url)
    with open("captcha.jpg", "wb") as f:
        f.write(response.content)

    # 处理验证码
    # 这里需要你自己编写验证码处理的代码，可以手动输入验证码或使用第三方验证码识别服务

    # 提交登录表单
    response = session.post(login_url, data=login_form)
    if "验证码不正确" in response.text:
        print("验证码不正确，请重新尝试登录")
        return False

    return True


# 登录京东账号
if not login_with_captcha(username, password):
    print("登录失败，请检查登录信息和验证码处理")
    exit()