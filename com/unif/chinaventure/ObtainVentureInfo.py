# coding:utf-8
import re  # 正则表达式
import urllib
import json
from urllib.request import urlopen

from bs4 import BeautifulSoup


class ObtainVentureInfo:
    def __init__(self):
        print("初始化ObtainInfo")

    # 获取标题
    def find_title(self, data):
        soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')
        title_info = soup.find_all('h1', class_='h1_01')

        if title_info is None:
            return '无题'
        if len(title_info) == 0:
            return '无题'

        title = title_info[0].attrs['title']

        if title is None:
            return '无题'

        # result = eval(repr(title).replace('\\', ''))
        # result = eval(repr(result).replace('/', ''))
        # result = eval(repr(result).replace('*', ''))
        # result = eval(repr(result).replace('?', ''))
        # result = eval(repr(result).replace('>', ''))
        # result = eval(repr(result).replace('<', ''))
        # result = eval(repr(result).replace('|', ''))
        # result = eval(repr(result).replace(',', ''))
        # result = eval(repr(result).replace('"', ''))
        # result = eval(repr(result).replace('.', ''))
        # result = re.sub('\s+', ' ', result).strip()
        # return result
        return title

    # 获取分页列表
    def find_pages1(self, data):
        result = {}
        import json
        hjson = json.loads(data, strict=False)
        print('-------------------')
        print(hjson)
        if hjson['data']['list'] is None:
            return result
        length = len(hjson['data']['list'])
        if length == 0:
            return result
        for i in range(0, length):
            url = 'https://www.chinaventure.com.cn/cmsmodel/news/detail/' + str(
                hjson['data']['list'][i]['news']['id']) + '.shtml'
            img = 'https://pic.chinaventure.com.cn/' + str(hjson['data']['list'][i]['news']['coverImg'])
            result[url] = img

        return result

        # 获取分页列表

    def find_pages2(self, data):
        result = {}
        import json
        hjson = json.loads(data, strict=False)
        print('-------------------')
        print(hjson)
        if hjson['data'] is None:
            return result
        length = len(hjson['data'])
        if length == 0:
            return result
        for i in range(0, length):
            url = 'https://www.chinaventure.com.cn/cmsmodel/report/detail/' + str(
                hjson['data'][i]['id']) + '.shtml'
            img = 'https://pic.chinaventure.com.cn/' + str(hjson['data'][i]['coverImg'])
            result[url] = img

        return result

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
        subject = soup.find_all('div')
        if len(subject) >= 2:
            text = str(subject[1])
        return text

    # 获取文章编辑
    def find_editor(self, data):
        editor = ''
        soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')
        subject = soup.find_all('p')
        if len(subject) >= 1:
            text = subject[-1].string
            if text.find('编辑：') > 0:
                editor = text.split('：')[1]
                if editor.endswith('）'):
                    editor = editor[0:len(editor) - 1]

        return editor

    # 获取文章内容
    def find_context(self, data):
        text = ''
        soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')
        content = soup.find_all('div', class_='content_01 m_t_30 detasbmo')
        if len(content) >= 1:
            content = str(content[0])
            text = str(content)
        return text

    # 文章发布时间
    def find_author_info(self, data):
        result = []
        soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')
        list = soup.find_all('div', class_='details_01_l')
        if list is None:
            return result
        length = len(list)  # 计算集合的个数
        if length == 0:
            return result

        data = list[0]
        sub_soup = BeautifulSoup(str(data), 'html.parser')
        tags = sub_soup.find_all('span')

        if tags is None:
            return result

        length = len(tags)
        if length == 0:
            return result

        for i in range(0, length):
            if not tags[i].string is None:
                tag = tags[i].string
                result.append(tag)
        return result

    # 获得标签
    def find_tags(self, html):
        tag = ''
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        list = soup.find_all('div', class_='lab_01 m_t_40')
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
