import re
from bs4 import BeautifulSoup


def get_author_info(response):
    post_info_list = response.xpath('//div[@id="main-content"]//div[@class="article-metaline"]')
    post_info_soup_list = [BeautifulSoup(post_info.get(), 'html.parser') for post_info in post_info_list]
    if post_info_soup_list:
        author = post_info_soup_list[0].find('span', class_='article-meta-value').get_text()
        title = post_info_soup_list[1].find('span', class_='article-meta-value').get_text()
        post_time = post_info_soup_list[2].find('span', class_='article-meta-value').get_text()  # TODO 轉timestamp

        regex = re.compile(r'(.+)\((.*)\)')
        match = regex.search(author.replace('\n', ''))
        author_id = match.group(1) if match else None
        author_name = match.group(2) if match else None

        return author_id, author_name, title, post_time


def get_content(response):
    content = response.xpath('//div[@id="main-content"]/text()').get()
    content = content.replace('\n', '') if content else content
    content_element = BeautifulSoup(response.text, 'html.parser').find('div', id='main-content')
    if not content:
        regex = re.compile(r'※(.*)※ 發信站')
        match = regex.search(
            content_element.get_text().replace('\n', ''))
        content = match.group(1) if match else None

    if not content:
        regex = re.compile(r'([0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]{4})(.*)※ 發信站')
        match = regex.search(
            content_element.get_text().replace('\n', ''))
        content = match.group(2)

    return content


def get_comment_info(response):
    commemnt_info_list = BeautifulSoup(response.text, 'html.parser').find_all('div', class_='push')
    result = []
    for commemnt_info in commemnt_info_list:
        comment_id = commemnt_info.find('span', class_='f3 hl push-userid').get_text().replace('\n', '')
        comment = commemnt_info.find('span', class_='f3 push-content').get_text().replace('\n', '').replace(': ','')
        comment_time = commemnt_info.find('span', class_='push-ipdatetime').get_text().replace('\n', '')

        result.append([comment_id, comment, comment_time])
    return result
