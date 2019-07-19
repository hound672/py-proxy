import logging
import ssl
import socket
from io import BufferedReader
from socketserver import StreamRequestHandler
from contextlib import AbstractContextManager

from settings import settings
from Libs.HttpParser import HttpHeader
from Libs.Request import Request
from Libs.Response import Response

logger = logging.getLogger(__name__)


class SocketContextManager(AbstractContextManager):
    """Context manager for read from socket"""

    def __enter__(self) -> BufferedReader:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket = ssl.wrap_socket(self._socket, ssl_version=ssl.PROTOCOL_TLSv1)
        self._socket.connect(('habr.com', 443))  # TODO from settings
        self._file = self._socket.makefile('rwb')
        return self._file

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._file.close()
        self._socket.close()


########################################################

class ProxyHandler(StreamRequestHandler):
    def handle(self) -> None:
        """Handler for incoming request"""
        header_request = HttpHeader.read_from_buffer(self.rfile)
        if not header_request:
            return

        request = Request(header_request)
        logger.info(f'Request: {request.path}')

        response = self.send_request(request)
        logger.info(f'Response: {response.path}')

        for chunk in response:
            self.wfile.write(chunk)

    def send_request(self, request: Request) -> Response:
        """Send request to host. And read response"""

        with SocketContextManager() as file:
            file.write(bytes(request))
            file.flush()
            response = self.read_response(file)

        return response

    def read_response(self, buffer: BufferedReader) -> Response:
        """Read response from host"""

        header_response = HttpHeader.read_from_buffer(buffer)
        data = b''
        return Response(header_response, data)
