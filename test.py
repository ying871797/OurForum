# -*- coding: UTF-8 -*-
import os

import json
from datetime import datetime

# 假设有一个包含 datetime 对象的元组
data = (1, datetime.now(), 'example')

# 将 datetime 对象转换为字符串
data_with_str = tuple(str(item) if isinstance(item, datetime) else item for item in data)

# 将转换后的元组进行 JSON 序列化
json_string = json.dumps(data_with_str)

print(json_string)

