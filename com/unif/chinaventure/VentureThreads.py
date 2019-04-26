# coding:utf-8
import threading

from com.unif.util.HttpUtil import HttpUtil
from com.unif.util.LogUtil import LogUtil

logger = LogUtil.get_logger('VentureThreads')


class VentureThreads(threading.Thread):
    def __init__(self, thread_id, url, categoryName, obtain, save, type):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.url = url
        self.obtain = obtain
        self.save = save
        self.categoryName = categoryName
        self.type = type
        logger.info("初始化:VentureThreads")

    def run(self):
        logger.info("开始线程:", self.thread_id)

        i = 0
        flag = True
        while True:
            i = i + 1
            act_url = self.url + str(i) + '-10.shtml'
            logger.info(act_url)
            html = HttpUtil.get_html(act_url)
            if html is None:
                continue
            if self.type == 1:
                pages = self.obtain.find_pages1(html.decode("UTF-8"))
            elif self.type == 2:
                pages = self.obtain.find_pages2(html.decode("UTF-8"))

            if len(pages) == 0:
                break
            num = 0

            for key, value in pages.items():
                flag = self.save.save_article(self.categoryName, key, value)
                if not flag:
                    break
                num = num + 1

            if not flag:
                break

    def __del__(self):
        logger.info(self.thread_id, "线程结束！)")
