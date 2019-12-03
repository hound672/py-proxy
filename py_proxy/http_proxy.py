# -*- coding: utf-8 -*-

"""Server protocol."""

from asyncio import Protocol, transports, Transport
from typing import cast
import logging

logger = logging.getLogger(__name__)


class HttpProxy(Protocol):
    """Class for processing TCP connections."""

    _transport: Transport

    def connection_made(self, transport: transports.BaseTransport) -> None:
        """Called when connection is established."""
        self._transport = cast(Transport, transport)

    def data_received(self, data_received: bytes) -> None:
        """Called when data is received."""
        logger.warning('Got data: {}'.format(data_received))
        # self._transport.write(data_received)
        self._transport.write(b'hello')
