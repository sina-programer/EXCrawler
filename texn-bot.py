from selenium.webdriver.common.by import By
import time
import os

from crawler import CrawlerBase


class TEXCrawler(CrawlerBase):
    url = 'https://edexco.net/have-turn/'

    def is_icon_visible(self):
        return bool(len(self().find_elements(By.CLASS_NAME, 'cart')))

    def get_icon_text(self):
        if self.is_icon_visible():
            return self().find_element(By.CLASS_NAME, 'cart').find_element(By.TAG_NAME, 'p').text
        return ''

    def get_level(self):
        return len(self().find_element(By.CLASS_NAME, 'right-sec4').find_elements(By.TAG_NAME, 'img')) - 1


EXECUTABLE_PATH = os.path.join('ex-assets', 'chromedriver.exe')
DELAY = 1

if __name__ == "__main__":
    icon_text = ''
    crawler = TEXCrawler(EXECUTABLE_PATH, options=['headless', 'disable_gpu', 'disable-dev-shm-usage', '--no-sandbox'])

    while True:
        try:
            crawler.refresh()
            crawler.wait(DELAY)
            new_icon_text = crawler.get_icon_text()
            print('Text: <', new_icon_text, '> at', time.ctime())
            if new_icon_text != icon_text:
                icon_text = new_icon_text
                crawler.beep()

        except Exception as error:
            print('Error:', error, 'at', time.ctime())
