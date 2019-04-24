# coding:utf-8
from com.unif.kr.Obtain36KrInfo import Obtain36KrInfo
from com.unif.kr.KrThreads import KrThreads
from com.unif.kr.SaveKrArticle import SaveKrArticle


class Spider36KrArticle:
    def __init__(self):
        print("初始化36Kr爬虫类")

    # 执行爬虫
    def executeSpider(self):
        obtain = Obtain36KrInfo()
        save = SaveKrArticle()

        urls = {
            "https://36kr.com/information/contact": "创投",
             "https://36kr.com/information/technology": "科技",
             "https://36kr.com/information/happy_life": "生活",
             "https://36kr.com/information/web_zhichang": "职场",
             "https://36kr.com/information/travel": "出行",
             "https://36kr.com/information/innovate": "创新",
             "https://36kr.com/information/real_estate": "房产",
             "https://36kr.com/information/other": "其他"
        }
        sub_url = [
            'https://36kr.com/pp/api/feed-stream?type=web&feed_id=305',
            'https://36kr.com/pp/api/feed-stream?type=web&feed_id=306',
            'https://36kr.com/pp/api/feed-stream?type=web&feed_id=307',
            'https://36kr.com/pp/api/feed-stream?type=web&feed_id=309',
            'https://36kr.com/pp/api/feed-stream?type=web&feed_id=310',
            'https://36kr.com/pp/api/feed-stream?type=web&feed_id=325',
            'https://36kr.com/pp/api/feed-stream?type=web&feed_id=311',
            'https://36kr.com/pp/api/feed-stream?type=web&feed_id=312'
        ]

        i = 0
        threads = []
        for url, name in urls.items():
            # 创建新线程
            i = i + 1
            categoryName = '资讯'

            thread1 = KrThreads("Thread-" + str(i), url, sub_url[i - 1], categoryName, name, obtain, save)

            # 开启新线程
            thread1.start()
            # 添加线程到线程列表
            threads.append(thread1)

        # 等待所有线程完成
        for t in threads:
            t.join()

        print("主进程投中网站爬取结束！")
