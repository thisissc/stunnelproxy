#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import signal
import urlparse
import gevent
import time
from gevent.server import StreamServer
from gevent.socket import create_connection, gethostbyname


class ProxyServer(StreamServer):
    def __init__(self, listener, **kwargs):
        super(ProxyServer, self).__init__(listener, **kwargs)

    def handle(self, client, address):
        try:
            line = ''
            while 1:
                _data = client.recv(1)
                line += _data
                if not _data or _data == '\n':
                    break

            if line:
                log(line)
                target_address = parse_address(line.split()[1])
                target = create_connection(target_address)
                target.sendall(line)
                gevent.spawn(forward, client, target)
                gevent.spawn(forward, target, client, 500000)
            
            else:
                client.close()
                return  

        except IOError, ex:
            log('failed : {}', ex)
            import traceback
            traceback.print_exc()
            return


def forward(source, dest, limit=0):
    t1 = time.time()
    count = 0
    while 1:
        data = source.recv(1024)
        if data:
            count += len(data)
            dest.sendall(data)

            # speed limit
            if limit > 0 and count >= limit:
                t2 = time.time()
                t_wait = 1 - (t2 - t1)
                if t_wait > 0:
                    gevent.sleep(t_wait)

                count = 0
                t1 = t2
        else:
            break


def parse_address(address):

    try:
        urls = urlparse.urlparse(address)
        address = urls.netloc or urls.path
        _addr = address.split(':')
        hostname, port = len(_addr) == 2 and  _addr or (_addr[0], 80)
        port = int(port)
    except ValueError:
        sys.exit('Expected HOST:PORT: %r' % address)
    return gethostbyname(hostname), port


def log(message, *args):
    if args:
        message = message.format(*args)
    sys.stderr.write('{}\n'.format(message))


def main():
    server = ProxyServer(('0.0.0.0', 8080))
    log('Starting proxy server {}:{}', *(server.address[:2]))
    gevent.signal(signal.SIGTERM, server.stop)
    gevent.signal(signal.SIGINT, server.stop)
    server.serve_forever();


if __name__ == '__main__':
    main()

