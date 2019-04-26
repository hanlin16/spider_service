# coding:utf-8

import threading
import time

from com.unif.util.HttpUtil import HttpUtil
from com.unif.util.LogUtil import LogUtil

logger = LogUtil.get_logger('SimuwangThreads')


class SimuwangThreads(threading.Thread):

    def __init__(self, thread_id, url, categoryName, obtain, save):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.url = url
        self.obtain = obtain
        self.save = save
        self.categoryName = categoryName
        logger.info("初始化:SimuwangThreads")

    def run(self):
        logger.info("开始线程:", self.thread_id)

        i = 0
        flag = True
        while True:
            i = i + 1
            act_url = self.url + "?page=" + str(i)
            logger.info(act_url)  # 这里是先拿到这个界面所有的链接
            html = HttpUtil.get_html(act_url)

            if html is None:
                return

            result = self.obtain.find_page_info_by_html_str(html.decode("UTF-8"))

            if len(result) == 0:
                break
            num = 0  # 这里去循环请求
            for key, value in result.items():
                flag = self.save.save_article(self.categoryName, key, value)
                if not flag:
                    break
                num = num + 1
                time.sleep(1)

            if not flag:
                break

    def __del__(self):
        logger.info(self.thread_id, "线程结束！)")
