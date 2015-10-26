#coding:utf-8
"""
student number:13331235
name: TanXiao
"""

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    """
    mainhandler
    """
    def get(self):
        # get argument from URL
        # http://localhost:8888/?info=Hi
        greetingInfo = self.get_argument('info', 'Hello')
        self.write(greetingInfo + ', friendly user!')

if __name__ == "__main__":
    APP = tornado.web.Application(handlers=[(r'/', MainHandler)])
    HTTP_SERVER = tornado.httpserver.HTTPServer(APP)
    # listen port
    HTTP_SERVER.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
