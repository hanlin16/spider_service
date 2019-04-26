# coding:utf-8
import threading

from com.unif.util.HttpUtil import HttpUtil
from com.unif.util.LogUtil import LogUtil

logger = LogUtil.get_logger('JfzArticleThreads')


class JfzArticleThreads(threading.Thread):
    def __init__(self, thread_id, url, categoryName, tag, obtain, save):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.url = url
        self.obtain = obtain
        self.save = save
        self.categoryName = categoryName
        self.tag = tag
        logger.info("初始化:JfzArticleThreads")

    def run(self):
        logger.info("开始线程:", self.thread_id)
        i = 0
        flag = True
        while True:
            i = i + 1
            act_url = self.url + 'p' + str(i) + '.html'
            logger.info(act_url)
            html = HttpUtil.get_html(act_url)

            if html is None:
                continue

            pages = self.obtain.find_article_pages(html.decode("UTF-8"))
            if len(pages) == 0:
                return
            for key, desc in pages.items():
                flag = self.save.save_article(self.categoryName, self.tag, key, desc)
                if not flag:
                    break

            if not flag:
                break

        def __del__(self):
            logger.info(self.thread_id, "线程结束！)")
