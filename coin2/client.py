#!/usr/bin/python
# -*- coding: UTF-8 -*-

from CTFServer import *

s = CTFServer('pwnable.kr', 9008)

s.recv()

for _ in range(100):
    result = s.recv()
    C = int(result.split(' C=')[1])
    N = int(result.split(' C=')[0][2:])

    arr = []
    for i in range(0, C):
        # Check which integers has its bit set on the i'th starting from the back
        entry = ' '.join([str(x) for x in range(0, N) if x & (1 << i)])
        arr.append(entry)
    s.send('-'.join(arr))
    result = s.recv()
    # Check for each returned group if it contains the counterfeit coin
    bits = ''.join(['0' if int(x) % 10 == 0 else '1' for x in result.split('-')])
    # Reverse the string (because we started from the back) and convert it to an integer
    s.send(str(int(bits[::-1], 2)))
    s.recv()

s.recv()  # The flag!
