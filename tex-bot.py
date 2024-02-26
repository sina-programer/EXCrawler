from selenium.webdriver.common.by import By
import configparser
import winsound
import keyboard
import os

from crawler import CrawlerBase


class TEXCrawler(CrawlerBase):
    url = 'https://edexco.net/have-turn/'

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

if __name__ == "__main__":
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH, ENCODING)
    configs = parser[SECTION]
    person = parser['Person']

    EXECUTABLE_PATH = os.path.join(DIRECTORY, parser['General']['executable'])
    KEY = configs['key']
    DELAY = configs['delay']

    crawler = TEXCrawler(EXECUTABLE_PATH, options=['start-maximized'])
    icon_text = ''

    while True:
        keyboard.wait(KEY)
        level = crawler.level

        if level == 0:
            while not crawler.is_icon_visible():
                crawler.refresh()
                crawler.wait(DELAY)
            icon_text = crawler.get_icon_text()

        elif level == 1:
            pass

        elif level == 2:
            form = crawler.driver.find_element(By.CLASS_NAME, 'parent-box-input')
            form.find_element(By.ID, 'Name').send_keys(person['name'])
            form.find_element(By.ID, 'Family').send_keys(person['family'])
            form.find_element(By.ID, 'NationalCode').send_keys(person['national-code'])
            form.find_element(By.ID, 'Mobile').send_keys(person['phone'])
            form.find_element(By.ID, 'BirthDate').send_keys(person['birth-date'])
            crawler.driver.find_element(By.CLASS_NAME, 'para-6').click()

        elif level == 3:
            date_box = crawler.driver.find_element(By.ID, 'DateOfAttendance')
            time_box = crawler.driver.find_element(By.ID, 'TimeOfAppointment')
            for date in date_box.find_elements(By.TAG_NAME, 'option')[1:]:
                for time in time_box.find_elements(By.TAG_NAME, 'option')[1:]:
                    date.click()
                    time.click()
                    crawler.driver.find_element(By.CLASS_NAME, 'para-6').click()
                    crawler.wait(1)
                    if crawler.level == 4:
                        break
                if crawler.level == 4:
                    break

        elif level == 4:
            pass

        winsound.Beep(1000, 2000)
