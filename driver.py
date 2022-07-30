import time
import clipboard
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from contextlib import contextmanager

DRIVER: webdriver.Chrome = None


def needs_driver(func):
    def wrapper(*args, **kwargs):
        return func(DRIVER, *args, **kwargs)
    return wrapper

@contextmanager
def driver(browser, executable_path) -> webdriver.Chrome:
    global DRIVER
    try:
        DRIVER  = browser(executable_path=executable_path)
        yield DRIVER
    finally:
        if DRIVER:
            DRIVER.close()


def set_cookie(name: str, value: str, domain: str):
    DRIVER.get('http://' + domain)
    DRIVER.add_cookie({'name': name, 'value': value, 'domain': domain})
    DRIVER.refresh()

def wait_for_element(path, by=By.XPATH) -> WebElement:
    try:
        return DRIVER.find_element(by, path)
    except NoSuchElementException:
        return WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((by, path)))
    
def get_element(path, by=By.XPATH) -> WebElement:
    return DRIVER.find_element(by, path)

def click(button):
    ac = ActionChains(DRIVER)
    ac.send_keys(button).perform()

def click_elem(elem):
    ac = ActionChains(DRIVER)
    ac.move_to_element_with_offset(DRIVER.find_element(By.TAG_NAME, 'body'), 0,0)
    ac.move_to_element(elem).click().perform()

def scroll_to_bottom(amount=2):
    time.sleep(0.5)
    for _ in range(amount):
        # Scroll down to bottom
        time.sleep(0.4)
        DRIVER.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        DRIVER.execute_script("window.scrollTo(0, 0);")

def get_clipboard():
    return clipboard.paste()

    