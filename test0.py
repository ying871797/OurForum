# -*- coding:utf-8 -*-

"""
@author: 87-MyFriends
@version: 1.0.0
@date: 2024/3/30
@function:
"""
import json
from datetime import datetime

# import pymysql
#
# from op import Mysql
#
# db_ = Mysql()
# db = pymysql.connect(host='43.143.201.36',
#                      user='root',
#                      password='xiang090526',
#                      database='ourforum')
# cursor = db.cursor()
# # cursor.execute('select * from data')
# # data = cursor.fetchall()
# data = db_.get_all('ipblacklist')
# print(data)
# db.commit()
# db.close()
import re

with open('./logs/20241003.log', 'r', encoding='utf-8') as f:
    txt = f.read()
    res = re.sub('\s+', ',', txt)
    print(res)
    with open('./logs/20241003.csv', 'w', encoding='utf-8') as f:
        f.write(res)
