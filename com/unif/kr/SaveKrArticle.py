# coding:utf-8
import base64
import json

from com.unif.kr.Obtain36KrInfo import Obtain36KrInfo
from com.unif.util.DateUtil import DateUtil
from com.unif.util.HttpUtil import HttpUtil
from com.unif.util.LogUtil import LogUtil
from com.unif.vo.paramater import paramater

logger = LogUtil.get_logger('SaveKrArticle')


# 保存文章
class SaveKrArticle:

    def __init__(self):
        self.obtainInfo = Obtain36KrInfo()
        logger.info("初始化:SaveKrArticle")

    # 保存文章
    def save_article(self, categoryName, tag, url, imgurl):
        data = HttpUtil.get_html(url)
        if data is None:
            return True
        title = self.obtainInfo.find_title(data)
        authors = self.obtainInfo.find_author_info(data)
        context = self.obtainInfo.find_context(data)
        subject = self.obtainInfo.find_subject(data)
        tags = tag
        author = ''
        public_time = ''
        if len(authors) > 0:
            for v in authors:
                if v.find(':') > 0:
                    public_time = v
                else:
                    author = v
        if public_time.find('年') > 0:
            public_time = DateUtil.time_transfer(public_time)
        flag = DateUtil.verify_time(public_time)
        if not flag:
            return False
        if not context is None:
            # 对文章内容加密
            context = context.encode('utf-8')
            bs64 = base64.b64encode(context)
            p = paramater(categoryName, title, author, author,
                          str(subject), str(bs64),
                          imgurl, tags, '36Kr网', url, public_time)
            over_dict = p.__dict__
            result = json.dumps(over_dict, ensure_ascii=False)
            js = json.loads(result)

            HttpUtil.post(js)

        return True
