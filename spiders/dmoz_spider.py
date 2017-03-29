import re

import scrapy
import subprocess
from scrapy import Request

import time


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["wdsz.net"]
    UserAgent = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) \
                       AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"}

    def start_requests(self):
        # url = "http://www.wdsz.net/login.php"
        # print "lalalalllaalallal"
        # return [Request(url, callback=self.login, meta={"cookiejar": 1})]
        url = 'http://www.wdsz.net/u.php'
        print url
        return [Request(url=url, method='get', callback=self.afterparse,
                        cookies={'PHPSESSID': '729f755184c5ec57a6708c646d3a05bf',
                                 'UM_distinctid': '15b0f33d43b41e-052677e1855919-1d336f53-13c680-15b0f33d43c5b7',
                                 '__cfduid': 'dacf265f2589460cde9041d104cf9aca11490608706',
                                 'ba1b8_cloudClientUid': '57102991',
                                 'ba1b8_jobpop': '0',
                                 'ba1b8_cknum': 'AgcKUgRTUAFRBD8%2FUVcHVAQFC1ICVQUAAloAUwEABgYDVlUHBwVVAFZVVl0',
                                 'ba1b8_winduser': 'AgMFVAVSUjFSAQUCBlUCV1QBUgcFBwtTUwFSD1cFAgYHVlABUQADUzo',
                                 'ba1b8_ck_info': '%2F%09', 'ba1b8_ol_offset': '53156',
                                 'CNZZDATA1657928': 'cnzz_eid%3D1996926882-1490608366-null%26ntime%3D1490698413',
                                 'ba1b8_lastpos': 'other', 'ba1b8_lastvisit': '14%091490701967%09%2Fu.php'},
                        headers={'Host': 'www.wdsz.net',
                                 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
                                 'Accept': '*/*',
                                 'Accept-Language': 'zh-CN,zh;q=0.8',
                                 'Accept-Encoding': 'gzip, deflate, sdch', 'DNT': '1',
                                 'Referer': 'http://www.wdsz.net/u.php',
                                 'Connection': 'keep-alive', 'Cache-Control': 'max-age=43200'})]

    def afterparse(self, response):
        filename = response.url.split("/")[-1]
        print filename
        with open('verify', 'wb') as f:
            f.write(response.body)
            from pymongo import MongoClient
            client = MongoClient('localhost', 27017)
            database = client.get_database("local")
            collection = database.get_collection("aaaa")
            collection.insert_one({"body": response.body.decode('gbk').encode('utf8')})

            # def login(self, response):
            #     current_time = str(int(time.time() * 10))
            #     verify = "http://www.wdsz.net/ck.php?nowtime=" + current_time
            #     return [Request(verify, callback=self.parse)]
            #
            #     # data = {
            #     #     "form_email": "XXXX",
            #     #     "form_password": "XXXX",
            #     #     "captcha-solution": captcha_value,
            #     # }
            #     # return [FormRequest.from_response(response,
            #     #                                   meta={"cookiejar": response.meta["cookiejar"]},
            #     #                                   headers=self.UserAgent,
            #     #                                   formdata=data,
            #     #                                   callback=self.crawlerdata,
            #     #                                   )]
            #
            # def parse(self, response):
            #     filename = response.url.split("/")[-1]
            #     print filename
            #     with open('verify', 'wb') as f:
            #         f.write(response.body)
            #         f.close()
            #         print self.image_to_string('1.png')
            #         # image_to_string('verify')
            #
            # # def image2string(self, img):
            # #     file1 = open('verify', 'r+b')
            # #     from PIL import Image
            # #     im = Image.open(file1)
            # #     text = image_to_string(im)
            # #     print "Using image_to_string(): "
            # #     print text
            #
            # def image_to_string(self, img, cleanup=True, plus=''):
            #     # subprocess.check_output('tesseract ' + img + ' ' + plus, shell=True)
            #     # text = ''
            #     # with open(img + 'txt', 'r') as f:
            #     #     text = f.read().strip()
            #     # if cleanup:
            #     #     os.remove(img + 'txt')
            #     # return text
            #     res = subprocess.check_output('tesseract ' + img + ' stdout').decode()
            #     return (re.subn('\W', '', res.strip()) if res else ('', ''))[0].lower()
