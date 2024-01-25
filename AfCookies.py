# -*- encoding: utf-8 -*-

import time
from telnetlib import EC

from selenium import webdriver
from collections import OrderedDict
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_cookies(driver, url):
    driver.get(url)
    time.sleep(20)  # 等待页面加载
    # 获取 Cookie
    cookies = driver.get_cookies()
    return cookies

# 将 extract_specific_cookies 函数修改为使用 OrderedDict
def extract_specific_cookies(cookies_list):
    specific_cookies = OrderedDict()
    target_fields = ["NextChangePwd", "PdboxBbs", "PdboxTicket", "PdboxUser", "RDB", "_au", "_au3rd", "_ausa", "_ausb",
                     "isBbs"]

    for cookie in cookies_list:
        if cookie['name'] in target_fields:
            specific_cookies[cookie['name']] = cookie['value']

    return specific_cookies


# 将字典转换为适用于 requests 请求头的字符串
def dict_to_cookie_str(cookies_dict):
    cookie_str = '; '.join([f"{key}={value}" for key, value in cookies_dict.items()])
    return cookie_str


if __name__ == '__main__':
    login_url = "https://login.afreecatv.com/afreeca/login.php?szFrom=full&request_uri=https%3A%2F%2Fwww.afreecatv.com%2F"

    # 使用webdriver.ChromeOptions()来配置ChromeDriver的路径
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-save-password-bubble')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-autofill')

    # 禁用自动填充--浏览器打开了自动填充账号/密码貌似会影响运行，整个保底
    prefs = {"profile.autocomplete": "off"}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 打开登录页面
        driver.get(login_url)

        # 定位账号输入框并输入账号
        account_input = driver.find_element(By.ID, "uid")
        account_input.send_keys("登录账号")  # 替换为你的账号

        # 定位密码输入框并输入密码
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys("登录账号密码")  # 替换为你的密码

        # 定位登录按钮并点击
        login_button = driver.find_element(By.CLASS_NAME, "btn_st1")
        login_button.click()

        # 使用显式等待等待 "下次更改" 元素出现--长时间未修改密码登录后会出现这个界面
        wait = WebDriverWait(driver, 10)
        next_time_change = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[text()='下次更改']")))
        next_time_change.click()

        # 获取登录后的Cookies
        cookies_list = get_cookies(driver, login_url)
        specific_cookies = extract_specific_cookies(cookies_list)

        # 打印需要的cookie字段，每个字段占一行
        for key, value in specific_cookies.items():
            print(f"{key}:{value};")

    finally:
        # 关闭浏览器
        driver.quit()