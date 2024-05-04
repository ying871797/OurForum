# -*- coding: UTF-8 -*-
a = ((1, 2, 3), (2, 3, 4))
b = [list(b) for b in a]
c = tuple([tuple(c) for c in b])
d = [[1], [2, 3]]
print(b)
print(tuple(b))
print(c)
for i in d:
    i.append(4)
print(d)
