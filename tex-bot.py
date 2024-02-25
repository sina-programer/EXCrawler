import configparser
import os

from crawler import TEXCrawler

ENCODING = 'UTF-8'
DIRECTORY = 'ex-assets'
CONFIG_PATH = os.path.join(DIRECTORY, 'config.ini')

if __name__ == "__main__":
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH, ENCODING)

    EXECUTABLE_PATH = os.path.join(DIRECTORY, parser['General']['executable'])

    crawler = TEXCrawler(EXECUTABLE_PATH, options=['start-maximized'])
    crawler.look()
