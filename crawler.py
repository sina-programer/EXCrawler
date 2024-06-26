from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from abc import ABC, abstractmethod
from functools import wraps
import threading
import winsound
import operator
import time
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

        self._tab_keys = {}
        self.executable_path = executable_path
        self.service = Service(self.executable_path)
        self.options = Options()
        if options:
            for option in options:
                self.options.add_argument(option)

        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        if load:
            self.home()

    @classmethod
    def beep(cls, frequency=1000, duration=1500, thread=True):
        if thread:
            thread_beep(frequency, duration)
        else:
            beep(frequency, duration)

    def wait(self, duration=1):
        time.sleep(duration)

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

    def new_tab(self, url, key='newtab'):
        counter = 1
        base_key = key
        while key in self._tab_keys:
            counter += 1
            key = base_key + str(counter)

        self._tab_keys.add(key)
        self().execute_script(f"window.open('{url}', '{key}')")
        return key

    def switch_tab(self, key):
        self().switch_to.window(key)

    def switch_tab_by_idx(self, idx):
        self().switch_to.window(self.tabs[idx])

    def switch_tab_back(self):
        self.switch_tab_by_idx(0)

    @property
    def tabs(self): return self().window_handles

    @property
    def tab_keys(self): return list(self._tab_keys)

    def __call__(self):
        return self.driver


def thread(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        threading.Thread(target=func, args=args, kwargs=kwargs).start()
    return wrapper

def beep(freq=1000, duration=2000):
    winsound.Beep(freq, duration)

thread_beep = thread(beep)  # @thread
