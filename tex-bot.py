from selenium.webdriver.common.by import By
import configparser
import winsound
import keyboard
import os

from crawler import CrawlerBase


class TEXCrawler(CrawlerBase):
    url = 'https://edexco.net/have-turn/'

    def is_icon_visible(self):
        return bool(len(self.driver.find_elements(By.CLASS_NAME, 'cart')))

    def get_icon_text(self):
        if self.is_icon_visible():
            return self.driver.find_element(By.CLASS_NAME, 'cart').find_element(By.TAG_NAME, 'p').text


SECTION = 'Tosee'
ENCODING = 'UTF-8'
DIRECTORY = 'ex-assets'
CONFIG_PATH = os.path.join(DIRECTORY, 'config.ini')

if __name__ == "__main__":
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH, ENCODING)
    configs = parser[SECTION]

    EXECUTABLE_PATH = os.path.join(DIRECTORY, parser['General']['executable'])
    KEY = configs['key']
    DELAY = configs['delay']

    crawler = TEXCrawler(EXECUTABLE_PATH, options=['start-maximized'])

    keyboard.wait(KEY)
    while not crawler.is_icon_visible():
        crawler.refresh()
        crawler.wait(DELAY)
    icon_text = crawler.get_icon_text()
    winsound.Beep(1000, 2000)
