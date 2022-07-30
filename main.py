from http.server import executable
import os
from platform import platform
import sys
import time

from selenium import webdriver

from driver import driver
from poe import search_item, TradeSite

def main():
    item = {'Name': 'Grace', 'Corrupted': 'No', 'Mirrored': 'No', 'Quality': (1,10)}

    with TradeSite.load():
        TradeSite.search(**item)
        print(list(TradeSite.get_listings()))


if __name__ == '__main__':
    if sys.platform == 'NT':
        browser = webdriver.Chrome
        executable_path = 'data/chromedriver.exe' 
    else:
        browser = webdriver.Firefox  
        executable_path = 'data/geckodriver'
    
    with driver(browser, executable_path):
        main()
