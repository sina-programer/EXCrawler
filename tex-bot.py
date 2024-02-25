from selenium.webdriver.common.by import By
import configparser
import keyboard
import os

from crawler import CrawlerBase


class TEXCrawler(CrawlerBase):
    url = 'https://edexco.net/have-turn/'

    def look(self):
        print('start looking...')


ENCODING = 'UTF-8'
DIRECTORY = 'ex-assets'
CONFIG_PATH = os.path.join(DIRECTORY, 'config.ini')

if __name__ == "__main__":
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH, ENCODING)

    EXECUTABLE_PATH = os.path.join(DIRECTORY, parser['General']['executable'])
    KEY = parser['Tosee']['key']

    crawler = TEXCrawler(EXECUTABLE_PATH, options=['start-maximized'])
    keyboard.wait(KEY)
    if not crawler.is_home():
        crawler.home()
    crawler.look()
