# -*- coding: utf-8 -*-

"""

Brief description.

Some other description
"""

from unittest.mock import patch, create_autospec

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
    app._run_forever.assert_awaited_with()


async def _mock_sleep_interrupted(*args):
    raise InterruptedError


@pytest.mark.asyncio
@patch('asyncio.sleep', side_effect=_mock_sleep_interrupted)
async def test_run_forever(mock_sleep, app):
    """Check if run_forever is awaited."""
    with pytest.raises(InterruptedError):
        await app._run_forever()

    mock_sleep.assert_awaited_with(Application._FOREVER_SLEEP_TIMEOUT)
