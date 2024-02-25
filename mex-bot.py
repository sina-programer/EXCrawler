import configparser
import keyboard
import os

from crawler import MEXCrawler

ENCODING = 'UTF-8'
DIRECTORY = 'ex-assets'
CONFIG_PATH = os.path.join(DIRECTORY, 'config.ini')

if __name__ == "__main__":
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH, ENCODING)

    KEY = parser['Melli']['key']
    EXECUTABLE_PATH = os.path.join(DIRECTORY, parser['General']['executable'])

    crawler = MEXCrawler(EXECUTABLE_PATH, options=['start-maximized'])
    keyboard.wait(KEY, suppress=True)
    crawler.fill(dict(parser['Person']))
