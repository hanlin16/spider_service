# coding:utf-8

import datetime
import json
import re

from bs4 import BeautifulSoup


class Obtain36KrInfo:
    def __init__(self):
        print("初始化Obtain36KrInfo")

    # 获取标题
    def find_title(self, data):
        soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')

        if soup.h1 is None:
            return '无题'
        return soup.h1.string

    # 获取分页列表
    def find_pages1(self, data):
        result = {}
        soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')
        content = soup.find_all('script')
        if content is None:
            return result
        for v in content:
            data = v.string
            if data is None:
                continue
            if data.startswith('window.initialState='):
                data = data.split('=')[1]
                break
        if data is None:
            return result

        hjson = json.loads(data, strict=False)

        if hjson['information']['informationList'] is None:
            return result
        length = len(hjson['information']['informationList'])
        if length == 0:
            return result
        for i in range(0, length):
            url = 'https://36kr.com/p/' + str(hjson['information']['informationList'][i]['entity_id'])
            img = str(hjson['information']['informationList'][i]['images'][0])
            result[url] = img
            b_id = hjson['information']['informationList'][i]['id']
        return result, b_id

    # 获取分页列表
    def find_pages2(self, data):
        result = {}
        hjson = json.loads(data, strict=False)
        print(hjson)
        i_data = hjson['data']
        if i_data is None:
            return result
        i_data = hjson['data']['items']
        if i_data is None:
            return result

        length = len(i_data)
        if length == 0:
            return result

        for i in range(0, length):
            url = 'https://36kr.com/p/' + str(hjson['data']['items'][i]['entity_id'])
            img = str(hjson['data']['items'][i]['images'][0])
            result[url] = img
            b_id = hjson['data']['items'][i]['id']
        return result, b_id

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
        soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')
        subject = soup.find_all('div', class_='summary')

        if subject is None:
            return ''
        if len(subject) == 0:
            return ''

        subject = subject[0].string

        if subject is None:
            return ''

        return subject

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
        content = soup.find_all('div', class_='common-width content articleDetailContent kr-rich-text-wrapper')
        if len(content) >= 1:
            content = str(content[0])
            text = str(content)
        return text

    # 文章发布时间
    def find_author_info(self, data):
        author = []
        soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')
        list = soup.find_all('div', class_='article-title-icon common-width margin-bottom-40')
        if list is None:
            return author
        length = len(list)  # 计算集合的个数
        if length == 0:
            return author
        data = list[0]

        soup = BeautifulSoup(str(data), 'html.parser', from_encoding='utf-8')
        if not soup.a is None:
            author.append(soup.a.string)
        if not soup.span is None:
            time = str(soup.span)
            if time.find('小时'):
                time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            elif time.find('昨'):
                time = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d %H:%M:%S")
            else:
                mat = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", test_date)
                time = mat.groups()[0]

        if time is None:
            return author
        if time.find(':') < 0:
            time = time + ' 00:00:00'
        author.append(time)

        return author

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
