from selenium.webdriver.common.by import By
import configparser
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

EXECUTABLE_PATH = None
DELAY = None

if __name__ == "__main__":
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH, ENCODING)
    configs = parser[SECTION]
    person = parser['Person']

    EXECUTABLE_PATH = os.path.join(DIRECTORY, parser['General']['executable'])
    DELAY = float(configs['delay'])

    url = input('Enter the link to be filled: ')

    crawler = MEXCrawler(EXECUTABLE_PATH, options=['start-maximized'], load=False)
    crawler.go(url, delay=DELAY)
    crawler.fill(dict(parser['Person']))
