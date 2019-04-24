# coding:utf-8
import datetime
import urllib
from urllib.request import urlopen

from bs4 import BeautifulSoup


class ObtainSimuwangInfo:
    def __init__(self):
        print("初始化ObtainInfo")

    def get_soup_obj(self, html_str):
        return BeautifulSoup(html_str, 'html.parser', from_encoding='utf-8')

    def get_title(self, data):
        article_title_obj = data.find('div', class_='article-header')  # 标题
        return article_title_obj.h1.string

    def get_time(self, data):
        article_time_obj = data.find('span', class_='time')  # 时间
        if len(article_time_obj.string) == 4:
            return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
        else:
            return article_time_obj.string

    def get_desc(self, data):
        article_desc_obj = data.find('meta', attrs={'name': 'Description'})  # 描述/简介
        return article_desc_obj['content']

    def get_author(self, data):
        article_author_obj = data.find('span', class_='author')  # 作者
        return article_author_obj.contents[0].strip()

    def get_content(self, data):
        article_content_obj = data.find('div', class_='article-content')  # 内容
        return str(article_content_obj)

    def get_tag(self, data):
        return "资讯"

    def find_time(self, data):
        time = ''
        soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')
        subject = soup.find_all('span', class_='date')
        if len(subject) >= 1:
            time = subject[0].string
        return time + ':00'

    # 获取网页源代码
    def get_html(self, url):
        opener = urllib.request.build_opener(urllib.request.HTTPHandler)
        headers = [
            ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko')
        ]
        urllib.request.install_opener(opener)
        opener.addheaders = headers
        res = opener.open(url, timeout=2000)
        html = res.read()  # 读取页面源代码
        return html

    # 根据页面html获取键值对
    def find_page_info_by_html_str(self, htmlStr):
        result = {}
        soup = BeautifulSoup(htmlStr, 'html.parser', from_encoding='utf-8')
        imgZooms = soup.find_all('div', class_='article-pic img-zoom')
        for item in imgZooms:
            result[item.a['href']] = item.a.img['src']
        return result

    # 获得标签
    def find_tags(self, html):
        tag = ''
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        list = soup.find_all('div', class_='news-tag')
        if list is None:
            return ''
        length = len(list)  # 计算集合的个数
        if length == 0:
            return ''

        data = list[0]
        sub_soup = BeautifulSoup(str(data), 'html.parser')
        tags = sub_soup.find_all('a')

        if tags is None:
            return ''

        length = len(tags)
        if length == 0:
            return ''

        for i in range(0, length):
            if i == 0:
                if not tags[i].string is None:
                    tag = tags[i].string
            else:
                if not tags[i].string is None:
                    tag = tag + ',' + tags[i].string

        return tag
