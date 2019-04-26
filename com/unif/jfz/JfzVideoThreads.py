# coding:utf-8
import threading
import time

from com.unif.util.DateUtil import DateUtil
from com.unif.util.HttpUtil import HttpUtil
from com.unif.util.LogUtil import LogUtil

logger = LogUtil.get_logger('JfzVideoThreads')


class JfzVideoThreads(threading.Thread):
    def __init__(self, thread_id, url, categoryName, tag, obtain, save):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.url = url
        self.obtain = obtain
        self.save = save
        self.categoryName = categoryName
        self.tag = tag
        logger.info("初始化:JfzVideoThreads")

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
                continue

            pages, times = self.obtain.find_video_pages(html.decode("UTF-8"))
            if len(pages) == 0:
                return
            num = 0
            for url, img in pages.items():
                public_time = times[num]
                if public_time is None or public_time.find('前'):
                    public_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                flag = DateUtil.verify_time(public_time)
                if not flag:
                    break
                self.save.save_video(self.categoryName, self.tag, url, img, public_time)

            if not flag:
                break

        def __del__(self):
            logger.info(self.thread_id, "线程结束！)")
