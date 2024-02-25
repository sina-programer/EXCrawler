from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from abc import ABC, abstractmethod
import os

# https://chromedriver.chromium.org/downloads  # with VPN
# https://googlechromelabs.github.io/chrome-for-testing/

class Crawler(ABC):

    @property
    @abstractmethod
    def url(self): pass

    def __init__(self, executable_path, options=None, load=True):
        if not os.path.exists(executable_path):
            raise FileExistsError(f"The executable path is not valid! <{executable_path}>")

        self.executable_path = executable_path
        self.service = Service(self.executable_path)
        self.options = Options()
        if options:
            for option in options:
                self.options.add_argument(option)

        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        if load:
            self.home()

    def go(self, url, delay=0.5):
        self.driver.get(url)
        self.driver.implicitly_wait(delay)

    def home(self, delay=0.5):
        self.go(self.url, delay)


class MEXCrawler(Crawler):
    url = 'https://nobat.mex.co.ir/'

    def fill(self, info):
        print('the form is filled!')
        print(info)



class TEXCrawler(Crawler):
    url = 'https://edexco.net/have-turn/'

    def look(self):
        print('start looking...')

