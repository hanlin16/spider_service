# coding:utf-8

from com.unif.simuwang.ObtainSimuwangInfo import ObtainSimuwangInfo
from com.unif.simuwang.SaveSimuwangArticle import SaveSimuwangArticle
from com.unif.simuwang.SimuwangThreads import SimuwangThreads
from com.unif.util.LogUtil import LogUtil

logger = LogUtil.get_logger('SpiderSimuwangArticle')


class SpiderSimuwangArticle:
    def __init__(self):
        logger.info("初始化:SpiderSimuwangArticle")

    # 执行爬虫
    def executeSpider(self):
        obtain = ObtainSimuwangInfo()
        urls = {
            'https://www.simuwang.com/news/lists.html': '资讯',
        }
        save = SaveSimuwangArticle()

        i = 0
        threads = []
        for url, name in urls.items():
            # 创建新线程
            i = i + 1
            thread1 = SimuwangThreads("Thread-" + str(i), url, name, obtain, save)

            # 开启新线程
            thread1.start()
            # 添加线程到线程列表
            threads.append(thread1)

        # 等待所有线程完成
        for t in threads:
            t.join()

        logger.info("主进程投资界网站爬取结束！")
