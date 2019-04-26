# coding:utf-8
import threading

from com.unif.util.HttpUtil import HttpUtil
from com.unif.util.LogUtil import LogUtil

logger = LogUtil.get_logger('PeDailyThreads')


class PeDailyThreads(threading.Thread):
    def __init__(self, thread_id, url, categoryName, obtain, save):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.url = url
        self.obtain = obtain
        self.save = save
        self.categoryName = categoryName
        logger.info("初始化:PeDailyThreads")

    def run(self):
        logger.info("开始线程:", self.thread_id)

        i = 0
        flag = True
        while True:
            i = i + 1
            act_url = self.url + str(i)
            logger.info(act_url)
            html = HttpUtil.get_html(act_url)

            if html is None:
                return

            pages = self.obtain.find_pages(html.decode("UTF-8"))
            result = self.obtain.find_page_info(pages)

            if len(result) == 0:
                break
            num = 0
            for key, value in result.items():
                flag = self.save.save_article(self.categoryName, key, value)
                if not flag:
                    break
                num = num + 1

            if not flag:
                break

    def __del__(self):
        logger.info(self.thread_id, "线程结束！)")
