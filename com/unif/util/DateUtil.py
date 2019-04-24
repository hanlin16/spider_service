# coding:utf-8

import time


class DateUtil:
    def __init__(self):
        print('初始化日期工具类')


    # 入参： '2019年01月09日  14:02:00'
    @staticmethod
    def time_transfer(publish_time):
        array = time.strptime(publish_time, u"%Y年%m月%d日 %H:%M:%S")
        try:
            date_time = time.strftime("%Y-%m-%d %H:%M:%S", array)
        except Exception as e:
            print(e)
        return date_time


dt = DateUtil.time_transfer('2019年01月09日  14:02:00')
print(dt)
