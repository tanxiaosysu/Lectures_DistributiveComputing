#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# student number : 13331235
# student name   : TanXiao

import os

print "Content-type: text/html\r\n\r\n"

# 查询字符串储存在QUERY_STRING中
queryStrings = os.environ["QUERY_STRING"].split("&")
# 查询字符串可能有多组,遍历
for string in queryStrings:
    query = string.split("=")
    # 满足条件
    if len(query) == 2 and query[0] == "user":
        print "Hello %s!" % query[1]
        break
