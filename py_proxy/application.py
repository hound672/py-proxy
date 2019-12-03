# -*- coding: utf-8 -*-

"""

Application.

Main application class
"""

import asyncio

from py_proxy.server_protocol import ServerProtocol


class Application:
    """Main app class."""

    def run(self) -> None:
        """Run application."""
        asyncio.run(self._run())

    async def _run(self) -> None:
        """Coroutine which run application."""
        server = await self._init()
        await server.serve_forever()

    async def _init(self) -> asyncio.AbstractServer:
        """Init app."""
        return await self._create_server('', '')

    @staticmethod
    def _protocol_factory():
        return ServerProtocol()

    async def _create_server(self, host, port) -> asyncio.AbstractServer:
        loop = asyncio.get_event_loop()
        return await loop.create_server(self._protocol_factory, host=host, port=port)
