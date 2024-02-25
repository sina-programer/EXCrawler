from selenium.webdriver.common.by import By
import configparser
import keyboard
import os

from crawler import CrawlerBase


class MEXCrawler(CrawlerBase):
    url = 'https://nobat.mex.co.ir/'

    def fill(self, info):
        print('the form is filled!')
        print(info)

    def _fill(self, info):
        self.driver.find_element(By.ID, "btnGetSchedule").click()
        self.driver.find_element(By.ID, 'txtNationalCode').send_keys(info['code'])
        self.driver.find_element(By.ID, 'txtBirthDate').send_keys(info['birthday'])
        self.driver.save_screenshot(f'{info["code"]}.png')


SECTION = 'Melli'
ENCODING = 'UTF-8'
DIRECTORY = 'ex-assets'
CONFIG_PATH = os.path.join(DIRECTORY, 'config.ini')

if __name__ == "__main__":
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH, ENCODING)
    configs = parser[SECTION]

    KEY = configs['key']
    EXECUTABLE_PATH = os.path.join(DIRECTORY, parser['General']['executable'])

    crawler = MEXCrawler(EXECUTABLE_PATH, options=['start-maximized'])
    keyboard.wait(KEY, suppress=True)
    crawler.fill(dict(parser['Person']))
