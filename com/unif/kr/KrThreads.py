# coding:utf-8
import threading
from com.unif.util.HttpUtil import HttpUtil


class KrThreads(threading.Thread):
    def __init__(self, thread_id, url, sub_url, categoryName, tag, obtain, save):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.url = url
        self.obtain = obtain
        self.save = save
        self.categoryName = categoryName
        self.sub_url = sub_url
        self.tag = tag

    def run(self):
        print("开始线程:", self.thread_id)
        act_url = self.url
        print(act_url)
        html = HttpUtil.get_html(act_url)

        if html is None:
            return

        pages, b_id = self.obtain.find_pages1(html.decode("UTF-8"))

        for key, value in pages.items():
           self.save.save_article(self.categoryName, self.tag, key, value)


        while True:
            act_url = self.sub_url + '&b_id=' + str(b_id) + '&per_page=30'
            print('分页URL:'+act_url)
            html = HttpUtil.get_html(act_url)

            if html is None:
                return

            pages, b_id = self.obtain.find_pages2(html.decode("UTF-8"))
            if len(pages) == 0:
                return
            for key, value in pages.items():
                self.save.save_article(self.categoryName, self.tag, key, value)


    def __del__(self):
        print(self.thread_id, "线程结束！)")
