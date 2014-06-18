#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import signal
import urllib.parse
import socket

from tornado import ioloop
from tornado import iostream
from tornado import tcpserver
from tornado import gen


class ProxyServer(tcpserver.TCPServer):
    def handle_stream(self, client, address):
        self._client = client
        client.read_until(b'\n', self._connect_target)

    def _connect_target(self, line):
        self.line = line
        target_address = parse_address(line.split()[1])
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self._target = iostream.IOStream(s)
        self._target.connect(target_address, self._do_forward)

    def _do_forward(self):
        def _do_do():
            self.forward(self._client, self._target)
            self.forward(self._target, self._client)

        self._target.write(self.line, _do_do)


    def forward(self, source, dest):
        def _write(data):
            if data:
                dest.write(data)

        source.read_until_close(do_nothing, _write)

def do_nothing(*args, **kwargs):
    pass


def parse_address(address):
    try:
        urls = urllib.parse.urlparse(address)
        address = urls.netloc or urls.path
        _addr = address.split(b':')
        hostname, port = len(_addr) == 2 and  _addr or (_addr[0], 80)
        port = int(port)
    except ValueError:
        sys.exit('Expected HOST:PORT: %r' % address)

    return socket.gethostbyname(hostname), port


def log(message, *args):
    message = message % args
    sys.stderr.write(message + '\n')


def main():

    server = ProxyServer()
    server.listen(8080)

    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()

