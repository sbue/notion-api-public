import os
import time

from selenium import webdriver
from selenium.common.exceptions import InvalidElementStateException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from utils.helpers import current_env


def get_driver():
    chrome_options = Options()
    if current_env == 'linux':
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--single-process')
        chrome_options.binary_location = f'{os.getcwd()}/bin/headless-chromium'
    return webdriver.Chrome(f'{os.getcwd()}/bin/chromedriver-{current_env}', chrome_options=chrome_options)


def find_element(driver, xpath, timeout=15):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.XPATH, xpath)),
    )


def find_element_and_click(driver, xpath, timeout=15):
    WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.XPATH, xpath)),
        EC.element_to_be_clickable((By.XPATH, xpath))
    ).click()


def find_element_and_send_keys(driver, xpath, value_to_write, escape=False):
    input_value = find_element(driver, xpath).get_attribute('value')
    while input_value not in [None, '']:
        try:
            input_element = find_element(driver, xpath)
            input_element.clear()
            input_value = find_element(driver, xpath).get_attribute('value')
        except (InvalidElementStateException, StaleElementReferenceException):
            pass
    input_element = find_element(driver, xpath)
    input_element.send_keys(value_to_write)
    time.sleep(0.1)
    if escape:
        time.sleep(0.25)
        input_element.send_keys(Keys.ESCAPE)
