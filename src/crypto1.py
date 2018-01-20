#!/usr/bin/python
# -*- coding: UTF-8 -*-

from CTFServer import *

SEP = '--'
COOKIE_LEN = 49

def get_ciphertext(packet):
        s = CTFServer('pwnable.kr', 9006)

        s.recv()  # Input your ID
        s.send(packet)

        s.recv()  # Input your PW
        s.send('')
        return s.recv().split('(')[1][:-1]


cookie = ''
block_offset = COOKIE_LEN/16 + 1
for i in range(0, COOKIE_LEN):
        pad_len = block_offset * 16 - len(SEP) - i - 1
        packet = '-' * pad_len
        hash1 = get_ciphertext(packet)[:block_offset * 32]

        for c in '-_abcdefghijklmnopqrstuvwxyz0123456789':
                packet = '-' * pad_len + SEP + cookie[:i] + c
                hash2 = get_ciphertext(packet)[:block_offset * 32]
                if hash1 == hash2:
                        print('Found char {0}: {1}'.format(i, c))
                        cookie += c
                        break

print('Cookie: {0}'.format(cookie))