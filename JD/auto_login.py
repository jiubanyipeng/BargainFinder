from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 设置Chrome驱动程序的路径
driver_path = 'chromedriver.exe'  # 根据你的驱动程序路径进行修改

# 创建一个Chrome浏览器实例
driver = webdriver.Chrome(driver_path)

# 打开京东登录页面
driver.get('https://passport.jd.com/new/login.aspx')

# 等待登录页面加载完成
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'loginname')))


# 点击QQ登录
driver.find_element(By.CLASS_NAME, 'QQ-icon').click()

# 获取新页面的句柄
new_handle = driver.window_handles[-1]
driver.switch_to.window(new_handle)


# 等待页面加载完成
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

# 在 #document 中查找特定元素
iframe = driver.find_element(By.CSS_SELECTOR, "iframe#ptlogin_iframe")
driver.switch_to.frame(iframe)
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "img_out_3073935366")))

# 执行点击操作
element.click()

# 还原到默认的上下文
#driver.switch_to.default_content()

# 等待登录成功后的页面加载完成
WebDriverWait(driver, 10).until(EC.title_contains('京东'))

# 登录成功，获取Cookie
cookies = driver.get_cookies()

print(cookies)



# 关闭浏览器
driver.quit()
