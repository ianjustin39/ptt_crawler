from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
from dotenv import load_dotenv
load_dotenv()


def main():

    url_list = [
        # 'https://www.ptt.cc/bbs/Gossiping',
        # 'https://www.ptt.cc/bbs/SEX'
        # 'https://www.ptt.cc/bbs/ios'
        'https://www.google.com'
    ]

    process = CrawlerProcess(get_project_settings())
    process.crawl('ptt_spider', start_urls=url_list)
    process.start()


if __name__ == '__main__':
    main()
