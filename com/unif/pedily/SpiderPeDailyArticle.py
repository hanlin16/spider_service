# coding:utf-8
from com.unif.pedily.ObtainPeDailyInfo import ObtainPeDailyInfo
from com.unif.pedily.SavePeDailyArticle import SaveArticle
from com.unif.pedily.PeDailyThreads import PeDailyThreads


class SpiderPeDailyArticle:
    def __init__(self):
        print("初始化投资界爬虫类")

    # 执行爬虫
    def executeSpider(self):
        obtain = ObtainPeDailyInfo()
        urls = {
            'https://pe.pedaily.cn/': '投资',
            'https://news.pedaily.cn/': '投资',
            'https://people.pedaily.cn/': '资讯',
            'https://research.pedaily.cn/': '资讯'
        }
        save = SaveArticle()

        i = 0
        threads = []
        for url, name in urls.items():
            # 创建新线程
            i = i + 1
            thread1 = PeDailyThreads("Thread-" + str(i), url, name, obtain, save)

            # 开启新线程
            thread1.start()
            # 添加线程到线程列表
            threads.append(thread1)

        # 等待所有线程完成
        for t in threads:
            t.join()

        print("主进程投资界网站爬取结束！")
