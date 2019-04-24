# coding:utf-8
import base64
import json
import os
import urllib
from urllib.request import urlopen

from com.unif.simuwang.ObtainSimuwangInfo import ObtainSimuwangInfo
from com.unif.util.HttpUtil import HttpUtil
from com.unif.vo.paramater import paramater


# 保存文章
class SaveArticle:
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
        'Opera/8.0 (Windows NT 5.1; U; en)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36'
    ]

    def __init__(self):
        self.obtainInfo = ObtainSimuwangInfo()
        self.default_value_source = "私募排排网"
        self.default_value_author = "私募排排网作者"
        self.default_value_editor = "私募排排网编辑"
        # self.proxy = HttpUtil.get_proxy()
        print("初始化SaveArticle")

    # 保存文章
    def save_article(self, categoryName, url, imgurl):
        # opener = urllib.request.build_opener(urllib.request.HTTPHandler)
        # headers = {
        #     "Connection": "keep-alive",
        #     "Cache-Control": "max-age=0",
        #     "Upgrade-Insecure-Requests": "1",
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        #     "Accept-Language": "zh-CN,zh;q=0.9",
        #     "Cookie": "RY=baidu"
        # }
        # urllib.request.install_opener(opener)
        # opener.addheaders = headers

        # response = None
        # try:
        #     # 从列表中随机选择UA和代理
        #     user_agent = random.choice(self.USER_AGENTS)
        #     proxy = random.choice(self.proxy)
        #     referer = url  # 随机选择访问url地址
        #     # 构建一个Handler处理器对象，参数是一个字典类型，包括代理类型和代理服务器IP+PROT
        #     httpproxy_handler = urllib2.ProxyHandler({"http": proxy})
        #     opener = urllib2.build_opener(httpproxy_handler)
        #     urllib2.install_opener(opener)
        #     request = urllib2.Request(referer, headers=headers)
        #     request.add_header("User-Agent", user_agent)
        #     response = urllib2.urlopen(request)

        opener = urllib.request.build_opener(urllib.request.HTTPHandler)
        headers = [
            ('User-Agnet', 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko')
        ]
        urllib.request.install_opener(opener)
        opener.addheaders = headers
        try:
            res = opener.open(url, timeout=1000)
        except Exception as e:
            if hasattr(e, 'reason'):
                print('reason:', e.reason)
                return
            elif hasattr(e, 'code'):
                print('error code:', e.code)
                return
            else:
                return
        # if (type(response) == None):
        #     print('未接收到数据')
        #     return
        data = res.read()
        soup_obj = self.obtainInfo.get_soup_obj(data)
        title = self.obtainInfo.get_title(soup_obj)
        time = self.obtainInfo.get_time(soup_obj)
        subject = self.obtainInfo.get_desc(soup_obj)
        context = self.obtainInfo.get_content(soup_obj)
        tags = self.obtainInfo.get_tag(soup_obj)
        author = self.obtainInfo.get_author(soup_obj)
        if not context is None:
            # self.save_context(title, time, imgurl, tags, subject, context)
            # 对文章内容加密
            context = context.encode('utf-8')
            bs64 = base64.b64encode(context)
            p = paramater(categoryName, title, author, author,
                          str(subject), str(bs64),
                          imgurl, tags, self.default_value_source, url, time)
            over_dict = p.__dict__
            result = json.dumps(over_dict, ensure_ascii=False)
            js = json.loads(result)
            # 请求数据
            HttpUtil.post(js)

    # 执行保存
    def save_context(self, title, time, img, tags, subject, context):
        if not os.path.exists('article'):
            article_path = os.path.join(os.path.abspath('.'), 'article')
            os.mkdir(article_path)
        try:
            fout = open('./article/' + title + '.txt', 'wb')
            content = title + '\n' + str(time) + '\n' + str(img) + '\n' + str(tags) + '\n' + str(subject) + '\n' + str(
                context)
            bytes = content.encode('utf-8')
            fout.write(bytes)
        except IOError as e:
            print(e)
