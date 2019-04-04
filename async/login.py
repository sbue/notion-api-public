import os
import time
from urllib.parse import urlparse

from cryptography.fernet import Fernet
from selenium.webdriver.support.ui import WebDriverWait

from utils import cookies
from utils.helpers import logger
from utils.selenium import find_element_and_click, find_element_and_send_keys

notion_url = 'https://www.notion.so'


def log_in(driver):
    logger.info('Logging In')
    # log in with Google
    driver.find_element_by_xpath(f'//text()[contains(.,"Continue with Google")]/ancestor::*[self::div][1]').click()
    notion_window, google_window = tuple(driver.window_handles)
    driver.switch_to_window(google_window)
    time.sleep(0.75)
    cookies.load_cookies(driver, 'google.plk')
    driver.refresh()
    existing_accounts = driver.find_elements_by_xpath('//div[@data-identifier="santib97@gmail.com"][@role="link"]')
    if len(existing_accounts) > 0:
        existing_accounts[0].click()
    else:
        # email input
        find_element_and_send_keys(driver, '//input[@type="email"]', os.getenv('GMAIL_EMAIL'))
        find_element_and_click(driver, '//div[@role="button"]')  # next button
        # password input (https://nitratine.net/blog/post/encryption-and-decryption-in-python/)
        pwd_path = urlparse(driver.current_url).path
        f = Fernet(os.getenv('CYPHER_SECRET_KEY').encode())
        decrypted_password = f.decrypt(os.getenv('GMAIL_PSWD_ENCRYPTED').encode()).decode()
        find_element_and_send_keys(driver, '//input[@type="password"]', decrypted_password)
        find_element_and_click(driver, '//div[@role="button"][@id="passwordNext"]')  # next button
    wait = WebDriverWait(driver, 10)
    wait.until(lambda ctx_driver: urlparse(ctx_driver.current_url).path != pwd_path)
    cookies.store_cookies(driver, 'google.plk')
    wait.until(lambda ctx_driver: len(ctx_driver.window_handles) == 1)
    driver.switch_to_window(notion_window)
    wait.until(lambda ctx_driver: ctx_driver.current_url != f'{notion_url}/login')
    logger.info('Logged in')


def enter_notion(driver):
    driver.get(notion_url)
    cookies.load_cookies(driver, 'notion.plk')
    driver.get(f'{notion_url}/login')
    at_login = len(driver.find_elements_by_xpath('//div/main/nav/div')) > 0
    if at_login:
        log_in(driver)
    """ we're in! 😎 """
    cookies.store_cookies(driver, 'notion.plk')
