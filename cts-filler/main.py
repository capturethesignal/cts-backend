#! /usr/bin/env python

import os
import sys
import asyncio

MIN_PORT = os.environ.get('MIN_PORT', 10000)
MAX_PORT = os.environ.get('MAX_PORT', 10010)

MIN_PORT = int(MIN_PORT)
MAX_PORT = int(MAX_PORT)


async def handle_hello(reader, writer):
    pass

loop = asyncio.get_event_loop()
servers = []

for port in range(MIN_PORT, MAX_PORT):
    try:
        server = loop.run_until_complete(
                asyncio.start_server(handle_hello, '0.0.0.0', port, loop=loop))
        #print("Listening to {}".format(port))
    except Exception:
        print("Port {} is busy".format(port))
        server = None

    if server:
        servers.append(server)

try:
    print("Running on {} ports: press ^C to shutdown".format(len(servers)))
    loop.run_forever()
except KeyboardInterrupt:
    pass

for i, server in enumerate(servers):
    #print("Closing server {0}".format(i+1))
    server.close()
    loop.run_until_complete(server.wait_closed())

loop.close()
