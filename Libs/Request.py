import socket
import ssl
from copy import copy
from io import BufferedReader
from contextlib import AbstractContextManager

from Libs.HttpParser import HttpHeader


class SocketContextManager(AbstractContextManager):
    """Context manager for read from socket"""

    def __enter__(self) -> BufferedReader:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket = ssl.wrap_socket(self._socket, ssl_version=ssl.PROTOCOL_TLSv1)
        self._socket.connect(('habr.com', 443))
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
        self._header['Host'] = 'habr.com' # TODO from settings
        self._header['Accept-Encoding'] = 'gzip'

    @property
    def header(self) -> 'HttpHeader':
        return self._header

    def send_request(self) -> bytes:
        """
        Send Http request to server
        """
        with SocketContextManager() as file:
            file.write(bytes(self.header))
            file.flush()
            header = HttpHeader.read_from_buffer(file)

            # return bytes(header)  # TODO TEMP
