#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# student number : 13331235
# student name   : TanXiao

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])

    # 查询字符串储存在QUERY_STRING中,环境变量储存在env中
    queryStrings = env["QUERY_STRING"].split("&")
    # 查询字符串可能有多组,遍历
    result = ""
    for string in queryStrings:
        query = string.split("=")
        # 满足条件
        if len(query) == 2 and query[0] == "user":
            result = "Hello " + query[1] + "!"
            break
    return result
