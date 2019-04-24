# coding:utf-8
from com.unif.jfz.ObtainJfzInfo import ObtainJfzInfo
from com.unif.jfz.JfzArticleThreads import JfzArticleThreads
from com.unif.jfz.JfzVideoThreads import JfzVideoThreads
from com.unif.jfz.SaveJfzArticle import SaveJfzArticle


class SpiderJfz:
    def __init__(self):
        print("初始化36Kr爬虫类")

    # 1.执行爬虫，爬取【文章】信息
    def executeSpiderArticle(self):
        obtain = ObtainJfzInfo()
        save = SaveJfzArticle()

        urls = {
            "https://v.jfz.com/item-4/": "资讯"
        }

        i = 0
        threads = []
        for url, name in urls.items():
            # 创建新线程
            i = i + 1
            categoryName = '资讯'

            thread1 = JfzArticleThreads("Thread-" + str(i), url, categoryName, name, obtain, save)

            # 开启新线程
            thread1.start()
            # 添加线程到线程列表
            threads.append(thread1)

        # 等待所有线程完成
        for t in threads:
            t.join()

        print("主进程金斧子网站爬取文章信息结束！")

    # 2.执行爬虫，爬取【视频】信息
    def executeSpiderVideo(self):
        obtain = ObtainJfzInfo()
        save = SaveJfzArticle()

        urls = {
            "https://www.jfz.com/zhibo/item-3.html?page=": "私募早餐会议",
            "https://www.jfz.com/zhibo/item-2.html?page=": "产品讲解",
            "https://www.jfz.com/zhibo/item-1.html?page=": "路演直播"
        }

        i = 1
        threads = []
        for url, name in urls.items():
            # 创建新线程
            i = i + 1
            categoryName = '资讯'

            thread2 = JfzVideoThreads("Thread-" + str(i), url, categoryName, name, obtain, save)

            # 开启新线程
            thread2.start()
            # 添加线程到线程列表
            threads.append(thread2)

        # 等待所有线程完成
        for t in threads:
            t.join()

        print("主进程金斧子网网站爬取视频结束！")
