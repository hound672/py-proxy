# -*- coding: utf-8 -*-

"""

Application.

Main application class
"""

import asyncio


class Application:
    """Main app class."""

    _FOREVER_SLEEP_TIMEOUT: int = 3600

    def run(self) -> None:
        """Run application."""
        asyncio.run(self._run())

    async def _run(self) -> None:
        """Coroutine which run application."""
        await self._init()
        await self._run_forever()

    async def _init(self) -> None:
        """Init app."""

    async def _run_forever(self) -> None:
        while True:
            await asyncio.sleep(self._FOREVER_SLEEP_TIMEOUT)
