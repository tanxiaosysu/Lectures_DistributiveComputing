#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
student number : 13331235
name           : TanXiao
"""

import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from operator import itemgetter

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

def read_dict(path):
    """
    从dict.txt中读取字典数据
    """
    theFile = open(os.path.join(path, 'dict.txt'), 'r')
    fileContent = theFile.read().splitlines()
    theFile.close()
    # 空字典
    dicts= {}
    for index in range(0, len(fileContent)):
        # 添加单词对
        if (index % 2):
            dicts[fileContent[index - 1]] = fileContent[index]
    return dicts

def write_dict(path, dicts):
    """
    向dict.txt中写入字典数据
    """
    theFile = open(os.path.join(path, 'dict.txt'), 'w')
    # 排序
    dicts = sorted(dicts.iteritems(), key=lambda d:d[0])
    for word in dicts:
        # 写入单词对
        theFile.write(word[0] + '\n' + word[1] + '\n')
    # 关闭文件
    theFile.close()

class WordHandler(tornado.web.RequestHandler):
    def get(self, word):
        # 读取字典
        dicts = read_dict(os.getcwd())
        # 查询条目
        if dicts.has_key(word):
            self.write({"word" : word ,
                        "definition" : dicts[word]})
            self.write("\n")
        else:
            self.set_status(404)
            self.write({"error": "word not found"})
            self.write("\n")

    def post(self, word):
        # 读取定义
        definition = self.get_argument("definition")
        # 读取字典
        dicts = read_dict(os.getcwd())
        # 无需查询
        dicts[word] = definition

        self.write({"word" : word ,
                    "definition" : definition})
        self.write("\n")
        dicts = write_dict(os.getcwd(), dicts)

if __name__ == "__main__":
    APP = tornado.web.Application(
        handlers = [(r"/(\w+)", WordHandler)],
        debug=True
    )
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(APP)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
