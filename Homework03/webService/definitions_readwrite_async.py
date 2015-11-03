import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient

import motor

import pymongo
from pymongo import MongoClient

from tornado.options import define, options
from tornado import gen

define("port", default=8000, help="run on the given port", type=int)

_db = motor.MotorClient("172.19.54.79", 27017).definitions

class WordHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, word):
        db = self.settings['db']
        document = yield db.words.find_one({'word': word})
        if document:
            del document["_id"]
            self.write(document)
            self.write('\n')
        else:
            self.set_status(404)

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self, word):
        definition = self.get_argument("definition")

        db = self.settings['db']
        document = yield db.words.find_one({'word': word})
        if document:
            document['definition'] = definition
            yield db.words.update({'_id': document['_id']},
                {'definition': definition})

        else:
            document = {'word': word, 'definition': definition}
            db.words.insert({'word': word, 'definition': definition},
                callback=self.insert_callback)

        # coll = self.application.db.words
        # word_doc = coll.find_one({"word": word})
        # if word_doc:
        #     word_doc['definition'] = definition
        #     coll.save(word_doc)
        # else:
        #     word_doc = {'word': word, 'definition': definition}
        #     coll.insert(word_doc)
        del document["_id"]
        self.write(document)
        self.write('\n')

    def insert_callback(result, error):
        pass

if __name__ == "__main__":
    tornado.options.parse_command_line()
    APP = tornado.web.Application(
        [(r"/(\w+)", WordHandler)],
        db=_db,
        debug=True)
    http_server = tornado.httpserver.HTTPServer(APP)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
