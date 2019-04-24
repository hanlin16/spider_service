# coding:utf-8

from bs4 import BeautifulSoup


class ObtainJfzInfo:
    def __init__(self):
        print("初始化Obtain36KrInfo")

    # 获取标题
    def find_title(self, data):
        soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')
        v = soup.find('div', class_='title').span
        if v is None:
            return '无题'
        return v.string

    # 获取文章分页列表
    def find_pages(self, data):
        result = {}
        soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')
        content = soup.find('div', class_='article-list').find_all('div', class_='con con-description')
        if content is None:
            return result
        for v in content:
            url = 'https://v.jfz.com' + v.a.attrs['href']

            result[url] = v.get_text()

        return result

    # 获取文章分页列表
    def find_article_pages(self, data):
        result = {}
        soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')
        content = soup.find('div', class_='article-list').find_all('div', class_='con con-description')
        if content is None:
            return result
        for v in content:
            url = 'https://v.jfz.com' + v.a.attrs['href']
            result[url] = v.get_text()
        return result

    # 获取视频分页列表
    def find_video_pages(self, data):
        result = {}
        time = []
        soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')
        content = soup.find_all('div', class_='list-video-card')
        if content is None:
            return result
        for v in content:
            url = 'https://www.jfz.com' + v.div.a.attrs['href']
            img = v.div.a.img.attrs['src']
            result[url] = img

            info = v.find('div', class_='info').find('div', class_='meta').ul.find_all('li')
            if info is None:
                continue
            if len(info) > 1:
                time.append(info[1].string + ' 00:00:00')

        return result, time

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
        content = soup.find('div', class_='forum-article-content')
        if content is None:
            return ''
        return str(content)

    # 获取视频内容
    def find_video_context(self, data):
        soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')

        info = soup.find('div', class_='video').iframe
        if info is None:
            return None
        content = info.attrs['src']
        if content is None:
            return ''

        info = soup.find('div', class_='video_psw')
        if not content is None:
            content = content + '/n' + str(info)
        return str(content)

        # 获取视频内容

    def find_video_author(self, data):
        soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')
        content = soup.find('div', class_='video_author')
        if content is None:
            return ''
        author = content.get_text().split(' ')[-1]
        return str(author)

    def find_video_title(self, data):
        soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')
        content = soup.find('div', class_='video_name')
        if content is None:
            return ''
        title = content.get_text()

        return str(title)

    # 文章发布时间
    def find_author_info(self, data):
        author = []
        soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')
        content = soup.find('div', class_='thread-item forum-article-head').find('div', class_='info').span.string
        if not content is None:
            author.append(content.string)

        content = soup.find('div', class_='thread-item forum-article-head').find('div', class_='stat-list').div.string

        if not content is None:
            time = content.string
            if time.find(':') < 0:
                time = time + ': 00:00:00'
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
