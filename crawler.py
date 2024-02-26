from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from abc import ABC, abstractmethod
import operator
import os

# https://chromedriver.chromium.org/downloads  # with VPN
# https://googlechromelabs.github.io/chrome-for-testing/

class CrawlerBase(ABC):

    click = operator.methodcaller('click')
    send = operator.methodcaller('send_keys')
    get_text = operator.methodcaller('getText')

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

    def wait(self, duration=1):
        self.driver.implicitly_wait(duration)

    def go(self, url, delay=0.5):
        self.driver.get(url)
        self.wait(delay)

    def home(self, delay=0.5):
        self.go(self.url, delay)

    @property
    def current_url(self):
        return self.driver.current_url

    def is_home(self):
        return self.current_url == self.url

    def refresh(self):
        self.driver.refresh()

    def __call__(self):
        return self.driver

