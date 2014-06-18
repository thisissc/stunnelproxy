#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import ssl
import settings


@asyncio.coroutine
def forward(src, desc):
    while 1:
        data = yield from src.read(1)
        
        if data:
            desc.write(data)
        else:
            break


@asyncio.coroutine
def handle_stream(client_r, client_w):
    ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    ssl_ctx.verify_mode = ssl.CERT_REQUIRED
    ssl_ctx.load_verify_locations(settings.local['cafile'])
    ssl_ctx.check_hostname = False

    target_r, target_w = yield from asyncio.open_connection(settings.remote['host'], settings.remote['port'], ssl=ssl_ctx)
    tasks = [
        forward(client_r, target_w),
        forward(target_r, client_w),
    ]
    yield from asyncio.wait(tasks, timeout=10)

    client_w.close()
    target_w.close()


def main():
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_stream, port=8080)
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("exit")
    finally:
        server.close()
        loop.close()


if __name__ == '__main__':
    main()

