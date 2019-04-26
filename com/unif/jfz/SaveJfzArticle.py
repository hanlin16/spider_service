# coding:utf-8
import base64
import json

from com.unif.jfz.ObtainJfzInfo import ObtainJfzInfo
from com.unif.util.DateUtil import DateUtil
from com.unif.util.HttpUtil import HttpUtil
from com.unif.util.LogUtil import LogUtil
from com.unif.vo.paramater import paramater

logger = LogUtil.get_logger('SaveJfzArticle')


# 保存文章
class SaveJfzArticle:

    def __init__(self):
        self.obtainInfo = ObtainJfzInfo()
        logger.info("初始化:SaveJfzArticle")

    # 保存文章
    def save_article(self, categoryName, tag, url, desc):
        data = HttpUtil.get_html(url)
        if data is None:
            return True
        title = self.obtainInfo.find_title(data)
        authors = self.obtainInfo.find_author_info(data)
        context = self.obtainInfo.find_context(data)
        subject = desc
        tags = tag
        author = ''
        public_time = ''
        if len(authors) > 0:
            for v in authors:
                if v.find(':') > 0:
                    public_time = v
                else:
                    author = v

        flag = DateUtil.verify_time(public_time)
        if not flag:
            return False

        if not context is None:
            # 对文章内容加密
            context = context.encode('utf-8')
            bs64 = base64.b64encode(context)
            p = paramater(categoryName, title, author, author,
                          str(subject), str(bs64),
                          '', tags, '金斧子', url, public_time)
            over_dict = p.__dict__
            result = json.dumps(over_dict, ensure_ascii=False)
            js = json.loads(result)

            HttpUtil.post(js)

        return True

    # 保存视频
    def save_video(self, categoryName, tags, url, img, time):
        logger.info("视频网页地址：" + url)
        data = HttpUtil.get_html(url)
        if data is None:
            return

        context = self.obtainInfo.find_video_context(data)
        if context is None:
            return

        context = '<iframe  width="680" height="480"  src="' + context + '" frameborder=0 allowfullscreen></iframe>'
        author = self.obtainInfo.find_video_author(data)
        title = self.obtainInfo.find_video_title(data)
        subject = title
        if not context is None:
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
