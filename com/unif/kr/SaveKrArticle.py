# coding:utf-8
import base64
import os
import urllib
import json
from urllib.request import urlopen
from com.unif.kr.Obtain36KrInfo import Obtain36KrInfo
from com.unif.vo.paramater import paramater
from com.unif.util.HttpUtil import HttpUtil
from com.unif.util.DateUtil import DateUtil


# 保存文章
class SaveKrArticle:

    def __init__(self):
        self.obtainInfo = Obtain36KrInfo()
        print("初始化SaveKrArticle")

    # 保存文章
    def save_article(self, categoryName, tag, url, imgurl):
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
        subject = self.obtainInfo.find_subject(data)
        tags = tag
        author = ''
        time = ''
        if len(authors) > 0:
            for v in authors:
                if v.find(':') > 0:
                    time = v
                else:
                    author = v
        if (time.find('年') > 0):
            time = DateUtil.time_transfer(time)
        if not context is None:
            # self.save_context(title, time, imgurl, tags, subject, context)
            # 对文章内容加密
            context = context.encode('utf-8')
            bs64 = base64.b64encode(context)
            p = paramater(categoryName, title, author, author,
                          str(subject), str(bs64),
                          imgurl, tags, '36Kr网', url, time)
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
