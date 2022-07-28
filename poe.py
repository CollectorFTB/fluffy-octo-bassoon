import pdb
import time
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

from driver import *
from filters import filter_names

DOMAIN = 'pathofexile.com'
POE_SESSION_ID = 'c45cfbd6bf600b7775a8f02504e9885c'

TRADE_URL = 'https://www.pathofexile.com/trade/search/Sentinel'

class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class TradeSite:
    SEARCH_BUTTON = '//*[@id="trade"]/div[4]/div/div[3]/div[2]/button'
    SEARCH_INPUT = '//*[@id="trade"]/div[4]/div/div[1]/div[1]/div/div[2]/input'
    
    CURRENCY_PRICE = 'div > div.price > span > span:nth-child(5) > span'
    CURRENCY_AMOUNT = 'div > div.price > span > span:nth-child(3)'
    WHISPER_BUTTON = 'div > div.btns > span:nth-child(1) > button'
    FILTER = '//*[@id="trade"]/div[4]/div/div[2]/div/div[1]/div[{}]/div[1]/div/span[1]/button'
    FILTERS = {'type': 1, 'weapon': 2, 'armour' : 3, 'socket': 4, 'requirement': 5, 'map': 6, 'heist': 7, 'sentinel': 8, 'misc': 9}
    
    @classproperty
    def search_button(cls) -> WebElement:
        return wait_for_element(TradeSite.SEARCH_BUTTON)

    @classproperty
    def search_input(cls) -> WebElement:
        return wait_for_element(TradeSite.SEARCH_INPUT)

    @staticmethod
    @needs_driver
    def search(driver: Chrome, item: str):
        TradeSite.search_input.send_keys(item)
        option = driver.find_elements(By.CLASS_NAME, 'multiselect__content-wrapper')[0] # click first result in search bar
        wait_for_element("multiselect__option--highlight", By.CLASS_NAME)
        click_elem(option)
        TradeSite.search_button.click()
        wait_for_element('price', By.CLASS_NAME)

        scroll_to_bottom()
        
        # print(list(TradeSite.get_listings()))
        
    @staticmethod
    @needs_driver
    def get_listings(driver: Chrome):
        for row in driver.find_elements(By.CLASS_NAME, 'right'):
            amount, price = row.find_element(By.CSS_SELECTOR, TradeSite.CURRENCY_AMOUNT).text, row.find_element(By.CSS_SELECTOR, TradeSite.CURRENCY_PRICE).text
            row.find_element(By.CSS_SELECTOR, TradeSite.WHISPER_BUTTON).click()
            whisper = get_clipboard()
            yield amount, price, whisper

    @staticmethod
    @needs_driver
    def search_filters(driver: Chrome, item: str = None, **filters):
        new_filters = set()
        
        for i, filter_list in enumerate(filter_names):
            for k, _ in filters.items():
                if k in filter_list:
                    new_filters.add(list(TradeSite.FILTERS.values())[i])


        if item:
            TradeSite.search_input.send_keys(item)
            option = next(elem for elem in driver.find_elements(By.CLASS_NAME, 'multiselect__element') if elem.text == item) # click first result in search bar
            wait_for_element("multiselect__option--highlight", By.CLASS_NAME)
            click_elem(option)

        for category_index in new_filters:
            if category_index != 1:
                wait_for_element(TradeSite.FILTER.format(category_index)).click()

        for filter_group in driver.find_elements(By.CLASS_NAME, 'filter-group-body') :
            for prop in filter_group.find_elements(By.CLASS_NAME, 'filter'):
                text = prop.text
                if text in filters.keys():
                    inputs = prop.find_elements(By.TAG_NAME, 'input')
                    if len(inputs) == 1:
                        inputs[0].send_keys(filters[text])
                        click(Keys.ENTER)
                    else:
                        for i, value in zip(inputs, filters[text]):
                            i.send_keys(value)
        
        TradeSite.search_button.click()
        wait_for_element('price', By.CLASS_NAME)
        for a,b,c in TradeSite.get_listings():
            print(a,b,c)

    @staticmethod
    def wait():
        wait_for_element(TradeSite.SEARCH_INPUT)

    @staticmethod
    @needs_driver
    def load(browser: Chrome):
        set_cookie('POESESSID', POE_SESSION_ID, DOMAIN)
        browser.get(TRADE_URL)
        TradeSite.wait()
        

def search_item(item: str = None, **kwargs):
    TradeSite.load()
    TradeSite.search_filters(item, **kwargs)
