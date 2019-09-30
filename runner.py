import os
from os.path import join, dirname
from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser import settings
#from jobparser.spiders.hhru import HhruSpider
#from jobparser.spiders.sjru import SjruSpider
#from jobparser.spiders.instagram import InstagramSpider
#from jobparser.spiders.superjob import SuperjobSpider
from jobparser.spiders.avito import AvitoSpider
do_env = join(dirname(__file__), '.env')
load_dotenv(do_env)

INST_LOGIN = os.getenv('INST_LOGIN')
INST_PWD = os.getenv('INST_PASSWORD')

if __name__ == '__main__':
    crawler_setting = Settings()
    crawler_setting.setmodule(settings)
    process = CrawlerProcess(settings=crawler_setting)
    # process.crawl(HhruSpider)
    # process.crawl(SjruSpider)
    # process.crawl(InstagramSpider, ['geekbrains.ru'], INST_LOGIN, INST_PWD)
    # process.crawl(SuperjobSpider)
    process.crawl(AvitoSpider)
    process.start()
