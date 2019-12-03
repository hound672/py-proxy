# -*- coding: utf-8 -*-

"""Test application."""

from unittest.mock import AsyncMock, patch, create_autospec

import pytest

from py_proxy.application import Application


@pytest.fixture
def app():
    """Return app object."""
    return Application()


@patch.object(Application, '_run', autospec=True)
def test_run(mock_run, app):
    """Check if run method is awaited."""
    app.run()

    mock_run.assert_awaited_with(app)


@pytest.mark.asyncio
async def test__run():  # noqa: WPS116  # ignore underscores name
    """Check if init method is awaited."""
    app = create_autospec(Application)
    app._run = lambda: Application._run(app)

    await app._run()  # type: ignore

    app._init.assert_awaited_with()
    app._init.return_value.serve_forever.assert_awaited_with()


@pytest.mark.skip  # skip until there is no settings
@pytest.mark.asyncio
async def test_init():
    """Check if init method raises all methods for init."""
    app = create_autospec(Application)
    app._init = lambda: Application._init(app)

    server = await app._init()  # type: ignore

    app._create_server.assert_awaited_with('', '')
    assert server == app._create_server.return_value


@patch('py_proxy.application.HttpProxy')
def test_protocol_factory(mock_http_protocol, app):
    """Check protocol factory method."""
    protocol = app._protocol_factory()
    mock_http_protocol.assert_called_with()
    assert mock_http_protocol.return_value == protocol


@pytest.mark.asyncio
@patch('asyncio.get_event_loop')
async def test_create_server(mock_get_event_loop, get_server_address):
    """Check if server starts with correct params."""
    mock_loop = AsyncMock()
    mock_get_event_loop.return_value = mock_loop

    host, port = get_server_address

    server = await Application._create_server(host=host, port=port)

    mock_get_event_loop.assert_called_with()
    mock_loop.create_server.assert_awaited_with(
        Application._protocol_factory,
        host=host,
        port=port,
    )
    assert server == mock_loop.create_server.return_value
