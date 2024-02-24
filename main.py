from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import datetime as dt
import configparser
import keyboard

# https://chromedriver.chromium.org/downloads  # with VPN
# https://googlechromelabs.github.io/chrome-for-testing/

class Crawler:
    URL = 'https://nobat.mex.co.ir/'

    def __init__(self, executable_path, options=None):
        self.service = Service(executable_path)
        self.options = Options()
        if options:
            for option in options:
                self.options.add_argument(option)

        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.driver.get(Crawler.URL)

    def fill(self, info):
        print('the form is filled!')
        print(info)


EXECUTABLE_PATH = r"mex-assets\chromedriver.exe"
CONFIG_PATH = r'mex-assets\config.ini'
KEY = 'f1'

if __name__ == "__main__":
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH, 'utf-8')

    crawler = Crawler(EXECUTABLE_PATH, options=['start-maximized'])

    keyboard.wait(KEY, suppress=True)
    crawler.fill(dict(parser['Person']))
