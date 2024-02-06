# -*- encoding: utf-8 -*-

from collections import OrderedDict
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_specific_cookies(driver, url, target_fields):
    driver.get(url)
    
    # 等待登录按钮可点击
    wait = WebDriverWait(driver, 10)
    login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn_st1")))

    account_input = driver.find_element(By.ID, "uid")
    account_input.send_keys("name")  # 替换为你的账号

    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("password")  # 替换为你的密码

    login_button.click()

    # 处理“下次更改”界面（假设其出现）
    next_time_change = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[text()='下次更改']")))
    next_time_change.click()

    # 获取并提取特定Cookies
    specific_cookies = OrderedDict((cookie['name'], cookie['value']) for cookie in driver.get_cookies() if cookie['name'] in target_fields)

    return specific_cookies


def dict_to_cookie_str(cookies_dict):
    cookie_str = '; '.join([f"{key}={value}" for key, value in cookies_dict.items()])
    return cookie_str


if __name__ == '__main__':
    login_url = "https://login.afreecatv.com/afreeca/login.php?szFrom=full&request_uri=https%3A%2F%2Fwww.afreecatv.com%2F"
    target_fields = ["NextChangePwd", "PdboxBbs", "PdboxTicket", "PdboxUser", "RDB", "_au", "_au3rd", "_ausa", "_ausb",
                    "isBbs"]

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

    try:
        with webdriver.Chrome(options=chrome_options) as driver:
            specific_cookies = get_specific_cookies(driver, login_url, target_fields)

            # 打印需要的cookie字段，每个字段占一行
            for key, value in specific_cookies.items():
                print(f"{key}:{value};")

    except Exception as e:
        print(f"An error occurred during the operation: {e}")
