#!/usr/bin/python
# -*- coding: UTF-8 -*-

from CTFServer import *

s = CTFServer('pwnable.kr', 9007)

s.recv()

for _ in range(100):
    result = s.recv()
    C = int(result.split(' C=')[1])
    N = int(result.split(' C=')[0][2:])

    min = 0
    max = N - 1

    for x in range(0, C):
        mid = (max - min)/2 + min
        msg = ' '.join([str(x) for x in range(min, mid)])
        s.send(msg)
        result = s.recv()
        if int(result) % 10 == 0:
            min = mid
        else:
            max = mid
    s.send(str(min))
    s.recv()

s.recv()  # The flag!
