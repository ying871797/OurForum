# -*- coding:utf-8 -*-

"""
@author: 87-MyFriends
@version: 1.0.0
@date: 2024/3/5
@function:
"""
import requests


def get_address(ip):
    req = requests.get(f'https://opendata.baidu.com/api.php?query={ip}&co=&resource_id=6006&oe=utf8')
    address = req.json()['data'][0]['location']
    return address
