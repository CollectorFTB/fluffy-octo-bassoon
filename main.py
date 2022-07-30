import sys
import time

from selenium import webdriver

from driver import driver
from poe import TradeSite

def main():
    item = {'Name': 'Grace', 'Corrupted': 'No', 'Mirrored': 'No', 'Quality': (1,10)}

    with TradeSite.load():
        TradeSite.search(**item)
        print(list(TradeSite.get_listings()))


if __name__ == '__main__':
    if sys.platform == 'NT':
        browser = webdriver.Chrome
        executable_path = './driver/chromedriver.exe' 
    else:
        browser = webdriver.Firefox  
        executable_path = './driver/geckodriver'
    
    with driver(browser, executable_path):
        main()
