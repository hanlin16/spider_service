# coding:utf-8
import time

from com.unif.chinaventure.SpiderVentureArticle import SpiderVentureArticle
from com.unif.jfz.SpiderJfz import SpiderJfz
from com.unif.kr.Spider36KrArticle import Spider36KrArticle
from com.unif.pedily.SpiderPeDailyArticle import SpiderPeDailyArticle
from com.unif.simuwang.SpiderSimuwangArticle import SpiderSimuwangArticle
from com.unif.util.LogUtil import LogUtil
from com.unif.util.SendEmailUtil import SendEmailUtil

logger = LogUtil.get_logger('Job')


class Job:
    def __init__(self):
        logger.info("初始化Job")

    def execute(self):
        logger.info('Job启动中....')
        logger.info('Job启动成功！')
        while True:
            # 刷新服务器时间
            current_time = time.strftime("%H:%M:%S", time.localtime())

            # --------------------------------------------------------------------------------------
            # 1、【投资界】设置每天定时的时间
            if current_time == "12:10:00" or current_time == "18:00:00":
                logger.info('【投资界】爬虫任务开始执行....')
                SendEmailUtil.send_email('【投资界】爬虫任务开始执行', '【投资界】爬虫任务开始执行....')
                try:
                    spider = SpiderPeDailyArticle()
                    spider.executeSpider()
                except Exception as e:
                    logger.error('【投资界】网站文章爬取异常:', e)
                    SendEmailUtil.send_email('【投资界】网站文章爬取异常', e)
                time.sleep(2)

            # --------------------------------------------------------------------------------------
            # 2、【投中网】设置每天定时的时间
            if current_time == "13:10:00" or current_time == "19:00:00":
                logger.info('【投中网】爬虫任务开始执行....')
                SendEmailUtil.send_email('【投中网】爬虫任务开始执行', '【投中网】爬虫任务开始执行....')
                try:
                    spider = SpiderVentureArticle()
                    spider.executeSpider()
                except Exception as e:
                    logger.error('【投中网】网站文章爬取异常:', e)
                    SendEmailUtil.send_email('【投中网】网站文章爬取异常', e)

                time.sleep(2)

            # --------------------------------------------------------------------------------------
            # 3、【36Kr】设置每天定时的时间
            if current_time == "14:10:00" or current_time == "20:00:00":
                logger.info('【36Kr】爬虫任务开始执行....')
                SendEmailUtil.send_email('【36Kr】爬虫任务开始执行', '【36Kr】爬虫任务开始执行....')
                try:
                    spider = Spider36KrArticle()
                    spider.executeSpider()
                except Exception as e:
                    logger.error('【36Kr】网站文章爬取异常:', e)
                    SendEmailUtil.send_email('【36Kr】网站文章爬取异常', e)

                time.sleep(2)

            # --------------------------------------------------------------------------------------
            # 4、【金斧子】设置每天定时的时间
            if current_time == "15:10:00" or current_time == "21:00:00":
                logger.info('【金斧子】爬虫任务开始执行....')
                SendEmailUtil.send_email('【金斧子】爬虫任务开始执行', '【金斧子】爬虫任务开始执行....')
                try:
                    spider = SpiderJfz()
                    spider.executeSpiderArticle()
                except Exception as e:
                    logger.error('【金斧子】网站文章爬取异常:', e)
                    SendEmailUtil.send_email('【金斧子】网站文章爬取异常', e)
                try:
                    spider = SpiderJfz()
                    spider.executeSpiderVideo()
                except Exception as e:
                    logger.error('【金斧子】网站视频爬取异常:', e)
                    SendEmailUtil.send_email('【金斧子】网站视频爬取异常', e)

                time.sleep(2)

            # --------------------------------------------------------------------------------------
            # 5、【私募排排】设置每天定时的时间
            if current_time == "16:10:00" or current_time == "22:00:00":
                logger.info('【私募排排】爬虫任务开始执行....')
                SendEmailUtil.send_email('【私募排排】爬虫任务开始执行', '【私募排排】爬虫任务开始执行....')
                try:
                    spider = SpiderSimuwangArticle()
                    spider.executeSpider()
                except Exception as e:
                    logger.error('【私募排排】网站文章爬取异常:', e)
                    SendEmailUtil.send_email('【私募排排】网站文章爬取异常', e)

                time.sleep(2)
            # --------------------------------------------------------------------------------------


job = Job()
job.execute()
