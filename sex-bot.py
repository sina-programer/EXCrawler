from selenium.webdriver.common.by import By
import configparser
import time
import os

from crawler import CrawlerBase


class SEXCrawler(CrawlerBase):
    url = 'https://se24.ir/queueing/'

    def fill(self, **person):
        self().find_element(By.XPATH,'//*[@id="new_firstname"]').send_keys(person['first_name'])
        self().find_element(By.XPATH,'//*[@id="new_lastname"]').send_keys(person['last_name'])
        self().find_element(By.XPATH,'//*[@id="new_nationalcode"]').send_keys(person['national_code'])
        self().find_element(By.XPATH,'//*[@id="new_mobilephone"]').send_keys(person['phone'])
        self().find_element(By.XPATH,'//*[@id="new_birthdate"]').send_keys(person['birth'])
        self().find_element(By.XPATH,'//*[@id="InsertButton"]').click()


def print_figlet(delay=.2):
    for line in FIGLET.splitlines():
        print(line)
        time.sleep(delay)


ENCODING = 'UTF-8'
DIRECTORY = 'ex-assets'
CONFIG_PATH = os.path.join(DIRECTORY, 'config.ini')
EXECUTABLE_PATH = os.path.join('ex-assets', 'chromedriver.exe')
FIGLET = '''
   _____ _               ____
  / ____(_)             |  __|
 | (___  _ _ __   __ _  | |__ 
  \___ \| | '_ \ / _` | |  __|
  ____) | | | | | (_| |_| |  
 |_____/|_|_| |_|\__,_(_)_| 
\n\n'''


if __name__ == "__main__":
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH, ENCODING)
    person = parser['Person']

    print_figlet()
    print('Welcome to the Bot!')

    crawler = SEXCrawler(EXECUTABLE_PATH, options=['start-maximized'])

    while True:
        try:
            crawler.refresh()
            crawler.wait(.5)
            if crawler().find_elements(By.CLASS_NAME, "btn-primary"):
                crawler.fill(**person)
                crawler.wait(1)
                break
        except Exception as error:
            print(error)

    input('press <enter> to exit...')
