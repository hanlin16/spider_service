# coding:utf-8

import time

from com.unif.util.LogUtil import LogUtil
from com.unif.util.SendEmailUtil import SendEmailUtil

logger = LogUtil.get_logger('DateUtil')


class DateUtil:
    def __init__(self):
        logger.info('初始化日期工具类')

    # 入参： '2019年01月09日  14:02:00'
    @staticmethod
    def time_transfer(publish_time):
        array = time.strptime(publish_time, u"%Y年%m月%d日 %H:%M:%S")
        try:
            date_time = time.strftime("%Y-%m-%d %H:%M:%S", array)
        except Exception as e:
            logger.error(e)
            SendEmailUtil.send_email('带年月日时间转换异常', e)
        return date_time

    # 为避免时间格式等问题，只针对确切时间比
    @staticmethod
    def verify_time(time_str):
        if time_str is None:
            return True
        try:
            if time_str.find(':') > 0:
                date_time = time.mktime(time.strptime(time_str, '%Y-%m-%d %H:%M:%S'))
            else:
                date_time = time.mktime(time.strptime(time_str, '%Y-%m-%d'))
        except Exception as e:
            logger.error(e)
            SendEmailUtil.send_email('时间校验异常', e)
            return True

        last_time = time.mktime(time.strptime('2019-01-01', '%Y-%m-%d'))
        return date_time > last_time

# dt = DateUtil.time_transfer('2019年01月09日  14:02:00')
# logger.info(dt)
#
# flag = DateUtil.verify_time('2019-03-19')
# logger.info(flag)
