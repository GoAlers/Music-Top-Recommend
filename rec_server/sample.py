#coding=utf-8
import web
import sys
import json
import math

urls = (
    '/', 'index',
    '/test', 'test',
)

app = web.application(urls, globals())

class index:
    def GET(self):
        # step 1 : 解析请求
        params = web.input()

        ret = '123'

        return ret

class test:
    def GET(self):
        print web.input()
        return '222'

if __name__ == "__main__":
    app.run()
