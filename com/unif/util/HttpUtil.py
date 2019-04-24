# coding:utf-8

import json
import urllib
import urllib.request as urllib2
from urllib import request

from lxml import etree


class HttpUtil:

    def __init__(self):
        print("初始化HttpUtil")

    @staticmethod
    def post(parameter):
        # interface_url = 'http://172.16.42.253:8080/publiccms/admin/cmsImport/reptile'
        interface_url = 'http://192.168.30.152:8095/publiccms/admin/cmsImport/reptile'

        print('入参：' + str(parameter))
        url = interface_url
        # json串数据使用
        parameter = json.dumps(parameter).encode(encoding='utf-8')
        # 普通数据使用
        # parameter = parse.urlencode(parameter).encode(encoding='utf-8')

        header_info = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                       "Content-Type": "application/json",
                       # "Content-Type": "text/plain",
                       'Cookie': "JSESSIONID=B52CD47F25204ED96235A4975E67BE87; PUBLICCMS_ADMIN=1_c6e76177-c772-4a83-bdc2-dd94474b96a1"}

        try:
            req = request.Request(url=url, data=parameter, headers=header_info)
            res = request.urlopen(req)
            res = res.read()

            # print('返回参数：' + str(res))
            print('返回参数，转码utf-8后：' + str(res.decode(encoding='utf-8')))
        except IOError as e:
            print('except:', e)

    @staticmethod
    def get_proxy():
        page = 1
        proxy = []
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}
            request = urllib2.Request("https://www.kuaidaili.com/free/inha/" + str(page), headers=headers)
            html = urllib2.urlopen(request).read()
            # print(html
            content = etree.HTML(html)
            ip = content.xpath('//td[@data-title="IP"]/text()')
            port = content.xpath('//td[@data-title="PORT"]/text()')
            # 将对应的ip和port进行拼接
            for i in range(len(ip)):
                for p in range(len(port)):
                    if i == p:
                        if ip[i] + ':' + port[p] not in proxy:
                            proxy.append(ip[i] + ':' + port[p])
        except Exception as e:
            print("获取代理出现错误")
        return proxy

    # 获取网页源代码
    @staticmethod
    def get_html(url):
        opener = urllib.request.build_opener(urllib.request.HTTPHandler)
        headers = [
            ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko')
        ]
        urllib.request.install_opener(opener)
        opener.addheaders = headers
        html = None
        try:
            res = opener.open(url, timeout=2000)
            html = res.read()  # 读取页面源代码
        except Exception as e:
            print("获取网页信息异常：" + e)

        return html
