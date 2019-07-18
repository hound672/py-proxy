import logging
from io import BufferedReader
from collections import UserDict


logger = logging.getLogger(__name__)

class HttpHeader(UserDict):
    """Implements workflow with Http header"""

    def __init__(self, headers_list: list, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if headers_list:
            # headers_list is not empty so it contains full header
            self['main'] = headers_list.pop(0)
        for header in headers_list:
            key, value = header.split(':', maxsplit=1)
            self[key] = value

    @classmethod
    def read_from_buffer(cls, buffer: BufferedReader):
        """
        Read Http header from BufferedRead.
        And create HttpHeader instance
        """
        headers_list = []
        while True:
            data = buffer.readline()
            if not data or data == b'\r\n':
                break
            headers_list.append(data.decode('utf8').strip())

        return cls(headers_list)


