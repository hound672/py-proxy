# -*- coding: utf-8 -*-

"""Test server protocol."""

import asyncio
from unittest.mock import patch

import pytest

from py_proxy.application import Application
from py_proxy.http_protocol import HttpProtocol


@pytest.fixture
async def get_server(get_server_address):
    """Create server object and return it with its host and port."""
    host, port = get_server_address
    server = await Application._create_server(host=host, port=port)
    yield server, host, port
    server.close()


@pytest.mark.asyncio
@patch.object(HttpProtocol, 'connection_made', autospec=True)
async def test_connection_made(mock_connection_made, get_server):
    """Check if method connection_made was called."""
    _, host, port = get_server

    _, writer = await asyncio.open_connection(host=host, port=port)
    await asyncio.sleep(0.1)  # noqa: WPS432

    mock_connection_made.assert_called()

    writer.close()


@pytest.mark.asyncio
@patch.object(HttpProtocol, 'data_received', autospec=False)
async def test_data_received(mock_data_received, get_server, faker):
    """Check if method data_received was called."""
    _, host, port = get_server
    test_send_data = faker.word().encode('utf-8')

    _, writer = await asyncio.open_connection(host=host, port=port)
    writer.write(test_send_data)
    await writer.drain()
    await asyncio.sleep(0.1)  # noqa: WPS432

    mock_data_received.assert_called_with(test_send_data)

    writer.close()
