# coding:utf-8
import base64
import json

from com.unif.pedily.ObtainPeDailyInfo import ObtainPeDailyInfo
from com.unif.util.DateUtil import DateUtil
from com.unif.util.HttpUtil import HttpUtil
from com.unif.util.LogUtil import LogUtil
from com.unif.vo.paramater import paramater

logger = LogUtil.get_logger('SaveArticle')


# 保存文章
class SaveArticle:

    def __init__(self):
        self.obtainInfo = ObtainPeDailyInfo()
        logger.info("初始化:SaveArticle")

    # 保存文章
    def save_article(self, categoryName, url, imgurl):
        logger.info("视频网页地址：" + url)
        data = HttpUtil.get_html(url)
        if data is None:
            return True

        title = self.obtainInfo.find_title(data)
        public_time = self.obtainInfo.find_time(data)

        flag = DateUtil.verify_time(public_time)
        if not flag:
            return False

        subject = self.obtainInfo.find_subject(data)
        context = self.obtainInfo.find_context(data)
        tags = self.obtainInfo.find_tags(data)
        if not context is None:
            # 对文章内容加密
            context = context.encode('utf-8')
            bs64 = base64.b64encode(context)
            p = paramater(categoryName, title, '', '',
                          str(subject), str(bs64),
                          imgurl, tags, '投资界', url, public_time)
            over_dict = p.__dict__
            result = json.dumps(over_dict, ensure_ascii=False)
            js = json.loads(result)

            HttpUtil.post(js)

        return True
