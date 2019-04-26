# coding:utf-8
import base64
import json

from com.unif.chinaventure.ObtainVentureInfo import ObtainVentureInfo
from com.unif.util.DateUtil import DateUtil
from com.unif.util.HttpUtil import HttpUtil
from com.unif.util.LogUtil import LogUtil
from com.unif.vo.paramater import paramater

logger = LogUtil.get_logger('SaveVentureArticle')


# 保存文章
class SaveVentureArticle:

    def __init__(self):
        self.obtainInfo = ObtainVentureInfo()
        logger.info("初始化:SaveVentureArticle")

    # 保存文章
    def save_article(self, categoryName, url, imgurl):
        data = HttpUtil.get_html(url)
        if data is None:
            return True
        title = self.obtainInfo.find_title(data)
        authors = self.obtainInfo.find_author_info(data)
        context = self.obtainInfo.find_context(data)
        subject = self.obtainInfo.find_subject(data)
        tags = self.obtainInfo.find_tags(data)
        editor = self.obtainInfo.find_editor(context)
        author = ''
        public_time = ''
        if len(authors) > 0:
            for v in authors:
                if v.find('作者：') > 0:
                    author = v.split('：')[1]
                elif v.find('年') > 0:
                    public_time = v
        if public_time.find('年') > 0:
            public_time = DateUtil.time_transfer(public_time)

        flag = DateUtil.verify_time(public_time)
        if not flag:
            return False

        if not context is None:
            # 对文章内容加密
            context = context.encode('utf-8')
            bs64 = base64.b64encode(context)
            p = paramater(categoryName, title, author, editor,
                          str(subject), str(bs64),
                          imgurl, tags, '投中网', url, public_time)
            over_dict = p.__dict__
            result = json.dumps(over_dict, ensure_ascii=False)
            js = json.loads(result)

            HttpUtil.post(js)

        return True
