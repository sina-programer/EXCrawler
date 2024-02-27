from selenium.webdriver.common.by import By
import configparser
import keyboard
import os

from crawler import CrawlerBase


class TEXCrawler(CrawlerBase):
    url = 'https://edexco.net/have-turn/'

    def handle_level0(self, delay=1):
        while not self.is_icon_visible():
            self.refresh()
            self.wait(delay)
        self.beep()

    def handle_level1(self):
        self().find_element(By.ID, 'HaveTurnCurrencyTypeId').find_elements(By.TAG_NAME, 'option')[int(person['currency'])].click()
        quantity = self().find_element(By.ID, 'PriceSell')
        quantity.clear()
        quantity.send_keys(person['quantity'])
        self().find_element(By.ID, 'IsRules').click()
        self().find_element(By.XPATH, '//button[text()="مرحله بعد"]').click()

    def handle_level2(self):
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
        ''' look for branches '''

    def handle_level5(self):
        ''' submit final success (maybe screenshot) '''

    def is_icon_visible(self):
        return bool(len(self().find_elements(By.CLASS_NAME, 'cart')))

    def get_icon_text(self):
        if self.is_icon_visible():
            return self().find_element(By.CLASS_NAME, 'cart').find_element(By.TAG_NAME, 'p').text

    def level3_step(self):
        pass

    @property
    def level(self):
        return len(self().find_element(By.CLASS_NAME, 'right-sec4').find_elements(By.TAG_NAME, 'img')) - 1


SECTION = 'Tosee'
ENCODING = 'UTF-8'
DIRECTORY = 'ex-assets'
CONFIG_PATH = os.path.join(DIRECTORY, 'config.ini')

EXECUTABLE_PATH = None
KEY = None
DELAY = None

if __name__ == "__main__":
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH, ENCODING)
    configs = parser[SECTION]
    person = parser['Person']

    EXECUTABLE_PATH = os.path.join(DIRECTORY, parser['General']['executable'])
    KEY = configs['key']
    DELAY = float(configs['delay'])

    crawler = TEXCrawler(EXECUTABLE_PATH, options=['start-maximized'])

    while True:
        try:
            keyboard.wait(KEY)
            level = crawler.level
            if level == 0:
                crawler.handle_level0(delay=DELAY)
            elif level == 1:
                crawler.handle_level1()
            elif level == 2:
                crawler.handle_level2()
            elif level == 3:
                crawler.handle_level3()
            elif level == 4:
                crawler.handle_level4()
            elif level == 5:
                crawler.handle_level5()

        except Exception as error:
            print(error)
