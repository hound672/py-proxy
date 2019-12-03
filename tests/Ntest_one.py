# -*- coding: utf-8 -*-

"""

Brief description.

Some other description
"""

import asyncio
from unittest import mock


import pytest

from py_proxy.__main__ import create_server, Stream, factory

# @pytest.mark.skip
@pytest.mark.asyncio
@mock.patch.object(Stream, 'data_received', autospec=True)
async def test_one_one(mock_data_received):

    _obj = factory()

    obj = mock.MagicMock(wraps=_obj)
    # breakpoint()

    with mock.patch('py_proxy.__main__.factory', return_value=obj) as factory_mock:

        server = await create_server()

        reader, writer = await asyncio.open_connection('localhost', 8888)

        writer.write(b'12345')
        await writer.drain()

        await asyncio.sleep(0.1)

        factory_mock.assert_called()

        obj.connection_made.assert_called()
        obj.data_received.assert_called_with(b'12345')

        writer.close()
        server.close()

        # mock_data_received.assert_called_with(obj.return_value, b'12345')
        # mock_data_received.assert_called_with(b'12345')


@pytest.mark.asyncio
@mock.patch('py_proxy.__main__.factory', return_value=factory())
@mock.patch.object(Stream, 'data_received', autospec=True)
@mock.patch.object(Stream, 'connection_made', autospec=True)
async def test_one(mock_made, mock_obj, mock_factory):

    await create_server()
    reader, writer = await asyncio.open_connection('localhost', 8888)

    writer.write(b'12345')
    await writer.drain()

    await asyncio.sleep(0.1)

    mock_factory.assert_called_with()
    mock_made.assert_called()
    mock_obj.assert_called_with(mock_factory.return_value, b'12345')


def test_two(get_unused_port):
    port = get_unused_port
    print('PORT: {0}'.format(port))
    breakpoint()