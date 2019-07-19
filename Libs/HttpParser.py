import logging
from enum import Enum
from io import BufferedReader
from typing import BinaryIO
from collections import UserDict
from copy import copy

logger = logging.getLogger(__name__)


class HttpCodes(Enum):
    SUCCESS = 200
    MOVED_PERMANENTLY = 301
    FOUND = 302


########################################################

class HttpHeader(UserDict):
    """Implements workflow with Http header"""

    def __init__(self, headers_list: list) -> None:
        super().__init__()
        if headers_list:
            # headers_list is not empty so it contains full header
            self['main'] = headers_list.pop(0).strip()
        for header in headers_list:
            key, value = header.split(':', maxsplit=1)
            self[key] = value.strip()

    def __bytes__(self) -> bytes:
        lines = []
        for key, value in self.items():
            if key == 'main':
                lines.append(value)
            else:
                lines.append(f'{key}: {value}')
        lines.append('\r\n')
        return '\r\n'.join(lines).encode('utf8')

    @classmethod
    def read_from_buffer(cls, buffer: BinaryIO) -> 'HttpHeader':
        """
        Read Http header from BufferedRead.
        And create HttpHeader instance
        """
        headers_list = []
        while True:
            data = buffer.readline()
            if not data or data == b'\r\n':
                break
            headers_list.append(data.decode('utf8'))

        return cls(headers_list)


########################################################


class BaseStream:
    _header: HttpHeader

    def __init__(self, header: HttpHeader) -> None:
        self._header = copy(header)

    @property
    def header(self) -> 'HttpHeader':
        return self._header

    @property
    def path(self) -> str:
        """Return path from header"""
        return self._header['main']
