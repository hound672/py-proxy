# -*- coding: utf-8 -*-

"""Main entry point."""

import asyncio
from asyncio import protocols, transports

from py_proxy.application import Application


class Stream(protocols.Protocol):

    def connection_made(self, transport: transports.BaseTransport) -> None:
        print('Connection made is called')

    def data_received(self, data: bytes) -> None:
        print('got data: {}'.format(data))


def factory():
    print('!!!!!!')
    return Stream()


async def create_server():
    loop = asyncio.get_event_loop()
    server = await loop.create_server(factory, host='localhost', port=8888)
    # server = await loop.create_server(None, host='localhost', port=8888)
    return server

    # return factory()


async def main():
    print('Start...')

    await create_server()

    while True:
        await asyncio.sleep(1024)

if __name__ == '__main__':  # pragma: no cover
    app = Application()
    app.run()
