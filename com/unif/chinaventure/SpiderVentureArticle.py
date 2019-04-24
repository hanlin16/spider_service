# coding:utf-8
from com.unif.chinaventure.ObtainVentureInfo import ObtainVentureInfo
from com.unif.chinaventure.VentureThreads import VentureThreads
from com.unif.chinaventure.SaveVentureArticle import SaveVentureArticle


class SpiderVentureArticle:
    def __init__(self):
        print("初始化投中界爬虫类")

    # 执行爬虫
    def executeSpider(self):
        obtain = ObtainVentureInfo()
        urls = {
            'https://www.chinaventure.com.cn/cmsmodel/news/jsonListByChannel/11/': 'VC/PE',
            'https://www.chinaventure.com.cn/cmsmodel/news/jsonListByChannel/3/': '瞰三板',
            'https://www.chinaventure.com.cn/cmsmodel/news/jsonListByChannel/20/': '产业资本',
            'https://www.chinaventure.com.cn/cmsmodel/news/jsonListByChannel/14/': '锐公司',
            'https://www.chinaventure.com.cn/cmsmodel/news/jsonListByChannel/5/': '金融',
            'https://www.chinaventure.com.cn/cmsmodel/news/jsonListByChannel/4/': '潮汛Hot',
            'https://www.chinaventure.com.cn/cmsmodel/news/jsonListByChannel/23/': '人物',
            'https://www.chinaventure.com.cn/cmsmodel/report/jsonListBySearch/-1_-1_-1/': '研究院'
        }

        save = SaveVentureArticle()

        i = 0
        threads = []
        for url, name in urls.items():
            # 创建新线程
            i = i + 1
            categoryName = '投资'
            type = 1
            if name == '研究院':
                type = 2
            thread1 = VentureThreads("Thread-" + str(i), url, categoryName, obtain, save, type)

            # 开启新线程
            thread1.start()
            # 添加线程到线程列表
            threads.append(thread1)

        # 等待所有线程完成
        for t in threads:
            t.join()

        print("主进程投中网站爬取结束！")
