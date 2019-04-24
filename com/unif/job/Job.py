# coding:utf-8
import time
from com.unif.pedily.SpiderPeDailyArticle import SpiderPeDailyArticle
from com.unif.chinaventure.SpiderVentureArticle import SpiderVentureArticle
from com.unif.kr.Spider36KrArticle import Spider36KrArticle
from com.unif.jfz.SpiderJfz import SpiderJfz
from com.unif.simuwang.SpiderSimuwangArticle import SpiderSimuwangArticle

while True:
    # 刷新服务器时间
    current_time = time.strftime("%H:%M:%S", time.localtime())
    # 1、【投资界】设置每天定时的时间
    if current_time == "00:10:00" or current_time == "18:00:00":
        print('定时任务开始执行....')
        try:
            spider = SpiderPeDailyArticle()
            spider.executeSpider()
        except Exception as e:
            print('投资界网站文章爬取异常:', e)
        time.sleep(2)

    # 2、【投中网】设置每天定时的时间
    if current_time == "01:10:00" or current_time == "19:00:00":
        print('定时任务开始执行....')
        try:
            spider = SpiderVentureArticle()
            spider.executeSpider()
        except Exception as e:
            print('投中网网站文章爬取异常:', e)

        time.sleep(2)

    # 3、【36Kr】设置每天定时的时间
    if current_time == "02:10:00" or current_time == "20:00:00":
        print('定时任务开始执行....')
        try:
            spider = Spider36KrArticle()
            spider.executeSpider()
        except Exception as e:
            print('36Kr网站文章爬取异常:', e)

        time.sleep(2)

    # 4、【金斧子】设置每天定时的时间
    if current_time == "03:10:00" or current_time == "21:00:00":
        print('定时任务开始执行....')
        try:
            spider = SpiderJfz()
            spider.executeSpiderArticle()
            spider.executeSpiderVideo()
        except Exception as e:
            print('金斧子网站文章爬取异常:', e)

        time.sleep(2)

     # 5、【私募排排】设置每天定时的时间
    if current_time == "03:10:00" or current_time == "21:00:00":
        print('定时任务开始执行....')
        try:
            spider = SpiderSimuwangArticle()
            spider.executeSpider()
        except Exception as e:
            print('金斧子网站文章爬取异常:', e)

        time.sleep(2)

