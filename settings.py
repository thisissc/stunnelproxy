#!/usr/bin/env python3
# -*- coding: utf-8 -*-

local = {
    'port': 8080,
    'cafile': 'cert/CA.crt',
}

remote = {
    'host': '127.0.0.1',
    'port': 8081,
    'hostname': 'localhost',
    'certfile': 'cert/server.crt',
}

try:
    from settings_custom import *
except:
    pass

