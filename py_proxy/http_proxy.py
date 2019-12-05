# -*- coding: utf-8 -*-

"""Server protocol."""

from asyncio import Protocol, transports, Transport
from typing import cast, Optional
import logging

from py_proxy.http_parser import HttpParser

logger = logging.getLogger(__name__)


class HttpProxy(Protocol):
    """Class for processing TCP connections."""

    _transport: Transport
    _request_parser: HttpParser

    def connection_made(self, transport: transports.BaseTransport) -> None:
        """Called when connection is established."""
        self._transport = cast(Transport, transport)
        self._request_parser = HttpParser()

    def data_received(self, received_data: bytes) -> None:
        """Called when data is received."""
        assert self._request_parser is not None

        logger.warning('Got data: {}'.format(received_data))
        self._request_parser.feed_data(received_data)
        # self._transport.write(data_received)
        # self._transport.write(b'hello')
