# -*- coding: UTF-8 -*-
import pandas as pd

data = {
    'date': ['2024-05-26'],
    'ip': ['0.0.0.0'],
    'address': ['未知'],
    'chatroom': ['class6']
}
df = pd.DataFrame(data)
df.to_csv('test.csv', mode='a', index=False, header=False, encoding='utf-8')
