# coding:utf-8
import base64
import json
import os
import urllib
from urllib.request import urlopen

from com.unif.jfz.ObtainJfzInfo import ObtainJfzInfo
from com.unif.util.HttpUtil import HttpUtil
from com.unif.vo.paramater import paramater


# 保存文章
class SaveJfzArticle:

    def __init__(self):
        self.obtainInfo = ObtainJfzInfo()
        print("初始化SaveKrArticle")

    # 保存文章
    def save_article(self, categoryName, tag, url, desc):
        opener = urllib.request.build_opener(urllib.request.HTTPHandler)
        headers = [
            ('User-Agnet', 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko')
        ]
        urllib.request.install_opener(opener)
        opener.addheaders = headers
        try:
            res = opener.open(url, timeout=1000)
        except Exception as e:
            if hasattr(e, 'reason'):
                print('reason:', e.reason)
                return
            elif hasattr(e, 'code'):
                print('error code:', e.code)
                return
            else:
                return
        data = res.read()
        title = self.obtainInfo.find_title(data)
        authors = self.obtainInfo.find_author_info(data)
        context = self.obtainInfo.find_context(data)
        subject = desc
        tags = tag
        author = ''
        time = ''
        if len(authors) > 0:
            for v in authors:
                if v.find(':') > 0:
                    time = v
                else:
                    author = v

        if not context is None:
            # self.save_context(title, time, imgurl, tags, subject, context)
            # 对文章内容加密
            context = context.encode('utf-8')
            bs64 = base64.b64encode(context)
            p = paramater(categoryName, title, author, author,
                          str(subject), str(bs64),
                          '', tags, '金斧子', url, time)
            over_dict = p.__dict__
            result = json.dumps(over_dict, ensure_ascii=False)
            js = json.loads(result)

            HttpUtil.post(js)

    # 保存视频
    def save_video(self, categoryName, tags,url, img, time):
        print("视频网页地址："+url)
        data = HttpUtil.get_html(url)

        if data is None:
            return

        context = self.obtainInfo.find_video_context(data)
        if context is None:
            return

        context = '<iframe  width="680" height="480"  src="'+context+'" frameborder=0 allowfullscreen></iframe>'
        author = self.obtainInfo.find_video_author(data)
        title = self.obtainInfo.find_video_title(data)
        subject = title
        if not context is None:
            # self.save_context(title, time, imgurl, tags, subject, context)
            # 对文章内容加密
            context = context.encode('utf-8')
            bs64 = base64.b64encode(context)
            p = paramater(categoryName, title, author, author,
                          str(subject), str(bs64),
                          img, tags, '金斧子', url, time)
            over_dict = p.__dict__
            result = json.dumps(over_dict, ensure_ascii=False)
            js = json.loads(result)

            HttpUtil.post(js)

    # 执行保存
    def save_context(self, title, time, img, tags, subject, context):
        if not os.path.exists('article'):
            article_path = os.path.join(os.path.abspath('.'), 'article')
            os.mkdir(article_path)
        try:
            fout = open('./article/' + title + '.txt', 'wb')
            content = title + '\n' + str(time) + '\n' + str(img) + '\n' + str(tags) + '\n' + str(subject) + '\n' + str(
                context)
            bytes = content.encode('utf-8')
            fout.write(bytes)
        except IOError as e:
            print(e)
