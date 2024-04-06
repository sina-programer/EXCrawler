from selenium.webdriver.common.by import By
import configparser
import threading
import winsound
import keyboard
import time
import os

from crawler import CrawlerBase


class TEXCrawler(CrawlerBase):
    url = 'https://edexco.net/have-turn/'

    def handle_levels(self, person):
        while (level := crawler.level) < 3:
            if level == 1:
                self.handle_level1(person)
            elif level == 2:
                self.handle_level2(person)
            self.wait(2)

    def handle_level0(self, delay=1):
        while not self.is_icon_visible():
            self.refresh()
            self.wait(delay)
        self.beep()

    def handle_level1(self, person):
        self().find_element(By.ID, 'HaveTurnCurrencyTypeId').find_elements(By.TAG_NAME, 'option')[int(person['currency'])].click()
        quantity = self().find_element(By.ID, 'PriceSell')
        quantity.clear()
        quantity.send_keys(person['quantity'])
        self().find_element(By.ID, 'IsRules').click()
        self().find_element(By.XPATH, '//button[text()="مرحله بعد"]').click()

    def handle_level2(self, person):
        form = self().find_element(By.CLASS_NAME, 'parent-box-input')
        form.find_element(By.ID, 'Name').send_keys(person['first-name'])
        form.find_element(By.ID, 'Family').send_keys(person['last-name'])
        form.find_element(By.ID, 'NationalCode').send_keys(person['national-code'])
        form.find_element(By.ID, 'Mobile').send_keys(person['phone'])
        form.find_element(By.ID, 'BirthDate').send_keys(person['birth-date'])
        self().find_element(By.XPATH, '//button[text()="مرحله بعد"]').click()

    def handle_level3(self):
        i = 1
        j = 0
        while True:
            j += 1
            dates = self().find_element(By.ID, 'DateOfAttendance').find_elements(By.TAG_NAME, 'option')
            times = self().find_element(By.ID, 'TimeOfAppointment').find_elements(By.TAG_NAME, 'option')
            dates[i].click()
            times[j].click()
            self().find_element(By.XPATH, '//button[text()="مرحله بعد"]').click()
            self.wait(.5)

            if self.level == 4:
                break

            if len(times) == j+1:
                j = 1
                i += 1

            if len(dates) == i+1:
                break

    def handle_level4(self):
        self().find_element(By.XPATH, "//button[contains(@text, 'تایید نهایی')]").click()

    def new_tab(self, url, key='newtab'):
        self().execute_script(f"window.open('{url}', '{key}')")

    def switch_tab(self, key):
        self().switch_to.window(key)

    def switch_tab_idx(self, idx):
        self().switch_to.window(self.tabs[idx])

    def switch_tab_back(self):
        self.switch_tab_idx(0)

    def is_icon_visible(self):
        return bool(len(self().find_elements(By.CLASS_NAME, 'cart')))

    def get_icon_text(self):
        if self.is_icon_visible():
            return self().find_element(By.CLASS_NAME, 'cart').find_element(By.TAG_NAME, 'p').text
        return ''

    def get_level(self):
        return self.level

    @property
    def tabs(self):
        return self().window_handles

    @property
    def level(self):
        return len(self().find_element(By.CLASS_NAME, 'right-sec4').find_elements(By.TAG_NAME, 'img')) - 1


def beep(freq=1000, duration=2000):
    winsound.Beep(freq, duration)

def thread_beep(**kwargs):
    threading.Thread(target=beep, kwargs=kwargs).start()


def print_figlet(delay=.2):
    for line in FIGLET.splitlines():
        print(line)
        time.sleep(delay)


EXECUTABLE_PATH = os.path.join('ex-assets', 'chromedriver.exe')
KEY = 'F2'
DELAY = 1
FIGLET = '''
   _____ _               ____
  / ____(_)             |  __|
 | (___  _ _ __   __ _  | |__ 
  \___ \| | '_ \ / _` | |  __|
  ____) | | | | | (_| |_| |  
 |_____/|_|_| |_|\__,_(_)_| 
\n\n'''


if __name__ == "__main__":
    print_figlet()
    print('Welcome to the Bot!')

    icon_text = ''
    tabs = {
        'checker': '',
        'central': 'شعبه مرکزی',
        'ferdousi': 'شعبه فردوسی'
    }
    tabs_inv = {value: key for key, value in tabs.items()}

    crawler = TEXCrawler(EXECUTABLE_PATH, options=['start-maximized'])

    for tab_id, tab_identifier in tabs.items():
        if tab_id == 'checker':
            continue
        print(f"Press <{KEY}> to continue for a new tab as <{tab_id}> (forms must be filled before appearing icon)")
        keyboard.wait(KEY)
        crawler.new_tab(crawler.url, tab_id)
        crawler.switch_tab(tab_id)

    print(f'Press <{KEY}> to back checkker and refresh constantly!')
    keyboard.wait(KEY)
    crawler.switch_tab_back()
    print('Notice: when the icon appears, the bot will click on <next-step> and then <final-submit> buttons and take a screenshot from the window of turn.')

    while True:
        try:
            crawler.refresh()
            crawler.wait(DELAY)
            new_icon_text = crawler.get_icon_text()
            if new_icon_text != icon_text:
                icon_text = new_icon_text
                tab_id = tabs_inv[icon_text]
                print(f'The icon <{tab_id}> was shown at', time.ctime())
                if tab_id != 'checker':
                    thread_beep()
                    crawler.switch_tab(tab_id)
                    keyboard.wait(KEY)
                crawler.switch_tab_back()

        except Exception as error:
            print('Error:', error, 'at', time.ctime())
            crawler.switch_tab_back()

    input('press <enter> to exit...')
