# -*- coding: utf-8 -*-
import scrapy
from PTTCrawler.items import PttCrawlerItem
from bs4 import BeautifulSoup
import main.util.ptt_info_parser as info_parser
import main.util.tool as tool
import re
from main.redis_tool.redis_conn import RedisConn
import datetime
import os
from dotenv import load_dotenv
load_dotenv()


class PttCrawlerSpider(scrapy.Spider):
    name = 'ptt_spider'
    allowed_domains = ['www.ptt.cc']
    start_urls = ['https://www.ptt.cc/bbs/Gossiping/M.1582019742.A.DA2.html']

    redis_conn = RedisConn(os.getenv("REDIS_HOST"), os.getenv("REDIS_PORT"), os.getenv("REDIS_DUPLICATE_DB"))

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, cookies={'over18': '1'})

    def parse(self, response):
        # 取得今天日期
        now = datetime.datetime.now()
        month = str(int(now.strftime('%m')))
        day = str(int(now.strftime('%d')) - 3) # 往前爬三天以免漏文
        today = f'{month}/{day}'
        # 預設要翻頁
        need_crawl_next_page = True

        # 取得所有文章ＵＲＬ元素
        post_list = response.xpath('//div[@class="r-list-container action-bar-margin bbs-screen"]//div[@class="r-ent"]')
        # 爬取文章ＵＲＬ
        for post in post_list:
            post_soup = BeautifulSoup(post.get(), 'html.parser')

            post_date = post_soup.find('div', class_='date')
            # 若所有文章都是今天則需要翻頁
            if post_date and post_date.text.strip() == today:
                url_tag = post_soup.find('div', class_='title').find('a')
                url = url_tag.get('href') if url_tag else ''

                # 去重複
                key = tool.get_redis_key(url)
                if not self.redis_conn.get(key):
                    # self.redis_conn.set(key)
                    yield scrapy.Request(url=f'https://www.ptt.cc{url}', callback=self.post_parser,
                                         cookies={'over18': '1'})

            else:
                need_crawl_next_page = False

        # 第一頁判斷
        regex = re.compile(r'(.+index.html)')
        match = regex.search(response.url)
        is_first_page = True if match else False

        post_soup = BeautifulSoup(response.text, 'html.parser')
        next_page_url = 'https://www.ptt.cc' + \
                        post_soup.find('div', class_='btn-group btn-group-paging').find_all('a', class_='btn wide')[
                            1].get('href')

        # 若需要翻頁／第一頁
        if need_crawl_next_page or is_first_page:
            print('crawler next page')
            yield scrapy.Request(url=next_page_url, callback=self.parse, cookies={'over18': '1'})

    def post_parser(self, response):

        item = PttCrawlerItem()

        author_id, author_name, title, post_time = info_parser.get_author_info(response)

        item['authorId'] = author_id
        item['authorName'] = author_name
        item['title'] = title
        item['publishedTime'] = post_time

        item['content'] = info_parser.get_content(response)
        url = response.url
        item['canonicalUrl'] = url

        comment_info_list = info_parser.get_comment_info(response)
        for comment_info in comment_info_list:
            comment_id = comment_info[0]
            item['commentId'] = comment_id
            item['commentContent'] = comment_info[1]
            item['commentTime'] = comment_info[2]

            item['_id'] = tool.get_mongo_id(url, comment_id)

            yield item
