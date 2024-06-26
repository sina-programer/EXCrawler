from selenium.webdriver.common.by import By
import configparser
import os

from crawler import CrawlerBase


class MEXCrawler(CrawlerBase):
    url = 'https://nobat.mex.co.ir/'

    def fill(self, info, translate_dict):
        form = self().find_element(By.TAG_NAME, 'form')
        div = form.find_element(By.TAG_NAME, 'div')

        for title_fa, title in translate_dict.items():
            xpath = rf'//span[text()="{title_fa}"]//parent::div//following-sibling::div'
            field = div.find_element(By.XPATH, xpath)

            if title == 'gender':
                field.click()
                idx = int(info['currency'])
                idx = 0 if idx==2 else idx
                field.find_elements(By.TAG_NAME, 'li')[idx].click()

            elif title == 'currency':
                field.click()
                idx = int(info['gender']) - 1
                field.find_elements(By.TAG_NAME, 'li')[idx].click()

            elif title == 'address':
                field.find_element(By.TAG_NAME, 'textarea').send_keys(info[title])

            else:
                field.find_element(By.TAG_NAME, 'input').send_keys(info[title])


ENCODING = 'UTF-8'
DIRECTORY = 'ex-assets'
CONFIG_PATH = os.path.join(DIRECTORY, 'mex-config.ini')
EXECUTABLE_PATH = os.path.join(DIRECTORY, 'chromedriver.exe')

dictionary = {
    'نام': 'first-name',
    'نام خانوادگی': 'last-name',
    'کد ملی': 'national-code',
    'تاریخ تولد': 'birth-date',
    'ملیت': 'nation',
    'محل تولد': 'birth-place',
    'جنسیت': 'gender',
    'کد پستی': 'post-code',
    'تلفن ثابت': 'phone',
    'تعداد ارز ': 'quantity',
    'نوع ارز': 'currency',
    'آدرس': 'address',
}

if __name__ == "__main__":
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH, ENCODING)
    person = dict(parser['Person'])

    url = input('Enter the link to be filled: ')

    crawler = MEXCrawler(EXECUTABLE_PATH, options=['start-maximized'], load=False)
    crawler.go(url, delay=1)

    try:
        crawler.fill(person, dictionary)
    except Exception as error:
        print(error)

    input('press <enter> to exit...')
