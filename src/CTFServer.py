#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket, sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def log(message):
    print bcolors.OKGREEN + message + bcolors.ENDC
    sys.stdout.flush()


def log_client(message):
    print bcolors.HEADER + message + bcolors.ENDC
    sys.stdout.flush()


def log_server(message):
    print bcolors.OKBLUE + message + bcolors.ENDC
    sys.stdout.flush()


class CTFServer:
    def __init__(self, server_address, server_port):
        # Create a TCP/IP socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        log('Connecting to %s port %s' % (server_address, server_port))
        self.server.connect((server_address, server_port))

    def send(self, message):
        self.server.send(message + '\n')
        log_client(message)

    def recv(self):
        response = self.server.recv(4096).strip()
        log_server(response)
        return response
