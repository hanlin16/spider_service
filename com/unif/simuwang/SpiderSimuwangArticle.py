# coding:utf-8

from com.unif.simuwang.ObtainSimuwangInfo import ObtainSimuwangInfo
from com.unif.simuwang.SaveSimuwangArticle import SaveArticle
from com.unif.simuwang.SimuwangThreads import SimuwangThreads


class SpiderSimuwangArticle:
    def __init__(self):
        print("初始化投资界爬虫类")

    # 执行爬虫
    def executeSpider(self):
        obtain = ObtainSimuwangInfo()
        urls = {
            'https://www.simuwang.com/news/lists.html': '资讯',
        }
        save = SaveArticle()

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

        print("主进程投资界网站爬取结束！")
