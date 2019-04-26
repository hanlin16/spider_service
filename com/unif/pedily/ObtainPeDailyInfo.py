# coding:utf-8
import re  # 正则表达式

from bs4 import BeautifulSoup

from com.unif.util.LogUtil import LogUtil

logger = LogUtil.get_logger('ObtainPeDailyInfo')


class ObtainPeDailyInfo:
    def __init__(self):
        logger.info("初始化:ObtainPeDailyInfo")

    # 获取标题
    def find_title(self, data):
        soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')
        title_info = soup.find_all('div', class_='main final-content')

        if title_info is None:
            return '无题'
        if len(title_info) == 0:
            return '无题'

        title = title_info[0].attrs['data-title']

        if title is None:
            return '无题'

        result = eval(repr(title).replace('\\', ''))
        result = eval(repr(result).replace('/', ''))
        result = eval(repr(result).replace('*', ''))
        result = eval(repr(result).replace('?', ''))
        result = eval(repr(result).replace('>', ''))
        result = eval(repr(result).replace('<', ''))
        result = eval(repr(result).replace('|', ''))
        result = eval(repr(result).replace(',', ''))
        result = eval(repr(result).replace('"', ''))
        result = eval(repr(result).replace('.', ''))
        result = re.sub('\s+', ' ', result).strip()

        return result

    # 获取分页列表
    def find_pages(self, data):
        begin = data.find(r'<li  data-special')
        end = self.find_last(data, begin, r'<div class="page-list page">')

        context = data[begin:end]
        return context

    # 查找最后一处位置
    def find_last(self, string, begin, str):
        last_position = begin
        while True:
            position = string.find(str, last_position + 1)
            if position == -1:
                return last_position
            last_position = position

    # 获取文章摘要
    def find_subject(self, data):
        text = ''
        soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')
        subject = soup.find_all('div', class_='subject')
        if len(subject) >= 1:
            text = str(subject[0].string)
        return text

    # 获取文章内容
    def find_context(self, data):
        text = ''
        soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')
        content = soup.find_all('div', class_='news-content')
        if len(content) >= 1:
            content = str(content[0])
            text = str(content)
        return text

    # 文章发布时间
    def find_time(self, data):
        public_time = ''
        soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')
        subject = soup.find_all('span', class_='date')
        if len(subject) >= 1:
            public_time = subject[0].string
        return public_time + ':00'

    # 获得文章_图片地址
    def find_page_info(self, html):
        result = {}
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        list = soup.find_all('div', class_='img')
        length = len(list)  # 计算集合的个数
        for i in range(length):
            content = list[i]
            img_soup = BeautifulSoup(str(content), 'html.parser')
            sub_img = img_soup.find_all('img')

            url_soup = BeautifulSoup(str(content), 'html.parser')
            sub_url = url_soup.find_all('a')

            if len(sub_url) == 0:
                break
            if sub_img is None:
                result[sub_url[0].attrs['href']] = ''
                continue
            if len(sub_img) == 0:
                result[sub_url[0].attrs['href']] = ''
                continue
            result[sub_url[0].attrs['href']] = sub_img[0].attrs['data-src']

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
