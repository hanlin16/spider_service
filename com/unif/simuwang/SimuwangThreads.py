# coding:utf-8

import threading
import time


class SimuwangThreads(threading.Thread):

    def __init__(self, thread_id, url, categoryName, obtain, save):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.url = url
        self.obtain = obtain
        self.save = save
        self.categoryName = categoryName

    def run(self):
        print("开始线程:", self.thread_id)

        i = 0
        while True:
            i = i + 1
            act_url = self.url + "?page=" + str(i)
            print(act_url)  # 这里是先拿到这个界面所有的链接
            html = self.obtain.get_html(act_url)

            if html is None:
                return

            result = self.obtain.find_page_info_by_html_str(html.decode("UTF-8"))

            if len(result) == 0:
                break
            num = 0  # 这里去循环请求
            for key, value in result.items():
                self.save.save_article(self.categoryName, key, value)
                num = num + 1
                time.sleep(1)

    def __del__(self):
        print(self.thread_id, "线程结束！)")
