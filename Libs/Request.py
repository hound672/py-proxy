import socket
import ssl
from copy import copy
from io import BufferedReader
from contextlib import AbstractContextManager
from typing import Optional

from Libs.HttpParser import HttpHeader


class SocketContextManager(AbstractContextManager):
    """Context manager for reaf from socket"""

    def __init__(self) -> None:
        self._socket: Optional[socket.socket] = None
        self._file: Optional[BufferedReader] = None

    def __enter__(self) -> BufferedReader:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket = ssl.wrap_socket(self._socket, ssl_version=ssl.PROTOCOL_TLSv1)
        self._socket.connect(('habrahabr.ru', 443))
        self._file = self._socket.makefile('rwb')
        return self._file

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._file.close()
        self._socket.close()


########################################################

class Request:
    """Implement Http request"""

    def __init__(self, header: HttpHeader) -> None:
        self._header = copy(header)
        self._header['Host'] = 'habrahabr.ru' # TODO from settings
        self._header['Accept-Encoding'] = 'gzip'

    @property
    def header(self):
        return self._header

    def send_request(self):
        """
        Send Http request to server
        """
        with SocketContextManager() as file:
            file.write(bytes(self.header))
            file.flush()
            data = file.read(100)
            print(data)
