# -*- coding: utf-8 -*-

"""

Application.

Main application class
"""

import asyncio
import logging

from py_proxy.http_proxy import HttpProxy

logger = logging.getLogger(__name__)


class Application:
    """Main app class."""

    def run(self) -> None:
        """Run application."""
        asyncio.run(self._run())

    async def _run(self) -> None:
        """Coroutine which run application."""
        logging.basicConfig()
        server = await self._init()
        await server.serve_forever()

    async def _init(self) -> asyncio.AbstractServer:
        """Init app."""
        return await self._create_server(host='localhost', port=8888)

    @staticmethod
    def _protocol_factory() -> asyncio.Protocol:
        return HttpProxy()

    @classmethod
    async def _create_server(cls, host: str, port: int) -> asyncio.AbstractServer:
        loop = asyncio.get_event_loop()
        return await loop.create_server(cls._protocol_factory, host=host, port=port)
