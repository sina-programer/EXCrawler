from selenium.webdriver.common.by import By
import configparser
import winsound
import keyboard
import os

from crawler import CrawlerBase


class TEXCrawler(CrawlerBase):
    url = 'https://edexco.net/have-turn/'

    def handle_level0(self, delay=1):
        while not self.is_icon_visible():
            self.refresh()
            self.wait(delay)
        winsound.Beep(1000, 1000)

    def handle_level1(self):
        self.driver.find_element(By.ID, 'HaveTurnCurrencyTypeId').find_elements(By.TAG_NAME, 'option')[int(person['currency'])].click()
        quantity = self.driver.find_element(By.ID, 'PriceSell')
        quantity.clear()
        quantity.send_keys(person['quantity'])
        self.driver.find_element(By.ID, 'IsRules').click()
        self.driver.find_element(By.XPATH, '//button[text()="مرحله بعد"]').click()

    def handle_level2(self):
        form = self.driver.find_element(By.CLASS_NAME, 'parent-box-input')
        form.find_element(By.ID, 'Name').send_keys(person['first-name'])
        form.find_element(By.ID, 'Family').send_keys(person['last-name'])
        form.find_element(By.ID, 'NationalCode').send_keys(person['national-code'])
        form.find_element(By.ID, 'Mobile').send_keys(person['phone'])
        form.find_element(By.ID, 'BirthDate').send_keys(person['birth-date'])
        self.driver.find_element(By.XPATH, '//button[text()="مرحله بعد"]').click()

    def handle_level3(self):
        date_box = self.driver.find_element(By.ID, 'DateOfAttendance')
        time_box = self.driver.find_element(By.ID, 'TimeOfAppointment')
        for date in date_box.find_elements(By.TAG_NAME, 'option')[1:]:
            for time in time_box.find_elements(By.TAG_NAME, 'option')[1:]:
                date.click()
                time.click()
                self.driver.find_element(By.XPATH, '//button[text()="مرحله بعد"]').click()
                self.wait(3)
                if self.level == 4:
                    break
            if self.level == 4:
                break

    def handle_level4(self):
        pass

    def is_icon_visible(self):
        return bool(len(self.driver.find_elements(By.CLASS_NAME, 'cart')))

    def get_icon_text(self):
        if self.is_icon_visible():
            return self.driver.find_element(By.CLASS_NAME, 'cart').find_element(By.TAG_NAME, 'p').text

    @property
    def level(self):
        return len(self.driver.find_element(By.CLASS_NAME, 'right-sec4').find_elements(By.TAG_NAME, 'img')) - 1


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
    DELAY = configs['delay']

    crawler = TEXCrawler(EXECUTABLE_PATH, options=['start-maximized'])

    while True:
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
