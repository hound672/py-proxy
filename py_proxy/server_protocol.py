# -*- coding: utf-8 -*-

"""Server protocol."""

from asyncio import Protocol, transports


class ServerProtocol(Protocol):
    """Class for processing TCP connections."""

    def connection_made(self, transport: transports.BaseTransport) -> None:
        """Called when connection is established."""
        super().connection_made(transport)

    def data_received(self, data_received: bytes) -> None:
        """Called when data is received."""
