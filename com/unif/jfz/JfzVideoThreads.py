# coding:utf-8
import threading
from com.unif.util.HttpUtil import HttpUtil


class JfzVideoThreads(threading.Thread):
    def __init__(self, thread_id, url, categoryName, tag, obtain, save):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.url = url
        self.obtain = obtain
        self.save = save
        self.categoryName = categoryName
        self.tag = tag

    def run(self):
        print("开始线程:", self.thread_id)
        i = 4
        while True:
            i = i + 1
            act_url = self.url + str(i)
            print(act_url)
            html = HttpUtil.get_html(act_url)

            if html is None:
                continue

            pages, times = self.obtain.find_video_pages(html.decode("UTF-8"))
            if len(pages) == 0:
                return
            num = 0
            for url, img in pages.items():
                time = times[num]
                self.save.save_video(self.categoryName, self.tag, url, img, time)

        def __del__(self):
            print(self.thread_id, "线程结束！)")
