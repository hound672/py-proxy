import logging
from urllib.parse import urlparse

from settings import settings
from Libs.HttpParser import HttpHeader, BaseStream, HttpCodes

logger = logging.getLogger(__name__)


class Response(BaseStream):
    """Implement Http response"""

    def __init__(self, header: HttpHeader, content: bytes) -> None:
        super().__init__(header)
        self._content = content

        self.check_redirect()

    def __iter__(self):
        yield bytes(self._header)

    @property
    def status_code(self) -> int:
        """Return response status code"""
        main = self._header['main'].split()
        return int(main[1])

    def check_redirect(self):
        """Check if there was redirect. And replace target url"""

        if self.status_code in (HttpCodes.MOVED_PERMANENTLY.value, HttpCodes.FOUND.value):
            location = self._header['Location']
            logger.debug(f'There is redirect to: {location}')

            url = urlparse(location)
            settings.set_target_url(url)

            self._header['Location'] = location.replace(settings.target_url, settings.local_url)
            logger.debug(f'Url after replace: {self._header["Location"]}')
